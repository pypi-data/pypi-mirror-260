"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2023-12-27
- Purpose: The `Command` type which implements a mini-DSL for graph
    editing. Command lists can be embedded as effects in a graph to give
    ultimate flexibility in defining graphs that modify themselves in
    complex ways.

Commands represent a simplified mini-programming-language for editing a
graph and/or exploration. The language stores a single 'current value'
which many effects set or operate on (and which can be referred to as
'$_' where variable names are used) The previous 'current value' is also
stored in '$__' for convenience. It also allows the definition of
arbitrary variables, and calling graph/exploration methods works mainly
via keyword arguments pulled automatically from the set of defined
variables. This allows each command to have a fixed number of arguments.
The following definitions specify the different types of command, each
as a named tuple with a 'command' slot in the first position that names
the command.
"""

from typing import (
    Tuple, Literal, TypeAlias, Dict, Callable, Union, Any, Optional,
    List, Collection, get_args
)

import collections
import math
import copy
import logging
import re

#--------#
# Errors #
#--------#


class CommandError(Exception):
    """
    TODO: This?
    An error raised during command execution will be converted to one of
    the subtypes of this class. Stores the underlying error as `cause`,
    and also stores the `command` and `line` where the error occurred.
    """
    def __init__(
        self,
        command: 'Command',
        line: int,
        cause: Exception
    ) -> None:
        self.command = command
        self.line = line
        self.cause = cause

    def __str__(self):
        return (
            f"\n  Command block, line {self.line}, running command:"
            f"\n    {self.command!r}"
            f"\n{type(self.cause).__name__}: {self.cause}"
        )


class CommandValueError(CommandError, ValueError):
    "A `ValueError` encountered during command execution."
    pass


class CommandTypeError(CommandError, TypeError):
    "A `TypeError` encountered during command execution."
    pass


class CommandIndexError(CommandError, IndexError):
    "A `IndexError` encountered during command execution."
    pass


class CommandKeyError(CommandError, KeyError):
    "A `KeyError` encountered during command execution."
    pass


class CommandOtherError(CommandError):
    """
    Any error other than a `ValueError`, `TypeError`, `IndexError`, or
    `KeyError` that's encountered during command execution. You can use
    the `.cause` field to figure out what the type of the underlying
    error was.
    """
    pass


#----------#
# Commands #
#----------#

LiteralValue: Tuple[Literal['val'], str] = collections.namedtuple(
    'LiteralValue',
    ['command', 'value']
)
"""
A command that replaces the current value with a specific literal value.
The values allowed are `None`, `True`, `False`, integers, floating-point
numbers, and quoted strings (single or double quotes only). Note that
lists, tuples, dictionaries, sets, and other complex data structures
cannot be created this way.
"""

EstablishCollection: Tuple[
    Literal['empty'],
    Literal['list', 'tuple', 'set', 'dict']
] = collections.namedtuple(
    'EstablishCollection',
    ['command', 'collection']
)
"""
A command which replaces the current value with an empty collection. The
collection type must be one of 'list', 'tuple', 'set', or 'dict'.
"""

AppendValue: Tuple[Literal['append'], str] = collections.namedtuple(
    'AppendValue',
    ['command', 'value']
)
"""
A command which appends/adds a specific value (either a literal value
that could be used with `LiteralValue` or a variable reference starting
with '$') to the current value, which must be a list, tuple, or set.
"""

SetValue: Tuple[Literal['set'], str, str] = collections.namedtuple(
    'SetValue',
    ['command', 'location', 'value']
)
"""
A command which sets the value for a specific key in a dictionary stored
as the current value, or for at a specific index in a tuple or list.
Both the key and the value may be either a literal that could be used
with `LiteralValue` or a variable reference starting with '$'.

When used with a set, if the value is truthy the location is added to
the set, and otherwise the location is removed from the set.
"""

PopValue: Tuple[Literal['pop']] = collections.namedtuple(
    'PopValue',
    ['command']
)
"""
A command which pops the last value in the tuple or list which is stored
as the current value, setting the value it pops as the new current value.

Does not work with sets or dictionaries.
"""

GetValue: Tuple[Literal['get'], str] = collections.namedtuple(
    'GetValue',
    ['command', 'location']
)
"""
A command which reads a value at a particular index within the current
value and sets that as the new current value. For lists or tuples, the
index must be convertible to an integer (but can also be a variable
reference storing such a value). For sets, if the listed value is in the
set the result will be `True` and otherwise it will be `False`. For
dictionaries, it looks up a value under that key.

For all other kinds of values, it looks for an attribute with the same
name as the string specified and returns the value of that attribute
(it's an error to specify a non-string value in this case).
"""

RemoveValue: Tuple[Literal['remove'], str] = collections.namedtuple(
    'RemoveValue',
    ['command', 'location']
)
"""
A command which removes an item from a tuple, list, set, or dictionary
which is stored as the current value. The value should be an integer (or
a variable holding one) if the current value is a tuple or list. Unlike
python's `.remove` method, this removes a single item at a particular
index/under a particular key, not all copies of a particular value.
"""

BinaryOperator: 'TypeAlias' = Literal[
    '+', '-', '*', '/', '//', '**', '%', '^', '|', '&', 'and', 'or',
    '<', '>', '<=', '>=', '==', 'is'
]
"""
The supported binary operators for commands.
"""

UnaryOperator: 'TypeAlias' = Literal['-', '~', 'not']
"""
The supported binary operators for commands.
"""

ApplyOperator: Tuple[
    Literal['op'],
    BinaryOperator,
    str,
    str
] = collections.namedtuple(
    'ApplyOperator',
    ['command', 'op', 'left', 'right']
)
"""
A command which establishes a new current value based on the result of an
operator. See `BinaryOperator` for the list of supported operators. The
two operand may be literals as accepted by `LiteralValue` or variable
references starting with '$'.
"""

ApplyUnary: Tuple[
    Literal['unary'],
    UnaryOperator,
    str
] = collections.namedtuple(
    'ApplyUnary',
    ['command', 'op', 'value']
)
"""
The unary version of `ApplyOperator`. See `UnaryOperator` for the list
of supported operators.
"""

VariableAssignment: Tuple[
    Literal['assign'],
    str,
    str
] = collections.namedtuple(
    'VariableAssignment',
    ['command', 'varname', 'value']
)
"""
Assigns the specified value (may be a variable reference) into a named
variable. The variable name should not start with '$', which is used when
referencing variables. If it does, variable substitution will be
performed to compute the name of the variable being created.
"""

VariableDeletion: Tuple[Literal['delete'], str] = collections.namedtuple(
    'VariableDeletion',
    ['command', 'varname']
)
"""
Deletes the variable with the given name. Doesn't actually delete the
stored object if it's reference elsewhere. Useful for unspecifying
arguments for a 'call' command.
"""

LoadVariable: Tuple[Literal['load'], str] = collections.namedtuple(
    'LoadVariable',
    ['command', 'varname']
)
"""
Loads the named variable as the current value, replacing the old current
value. The variable name should normally be specified without the '$',
with '$' variable substitution will take place and the resulting string
will be used as the name of the variable to load.
"""

CallType: 'TypeAlias' = Literal[
    'builtin',
    'stored',
    'graph',
    'exploration'
]
"""
Types of function calls available via the 'call' command.
"""

FunctionCall: Tuple[
    Literal['call'],
    CallType,
    str
] = collections.namedtuple(
    'FunctionCall',
    ['command', 'target', 'function']
)
"""
A command which calls a function or method. IF the target is 'builtin',
one of the `COMMAND_BUILTINS` will be called. If the target is 'graph' or
'exploration' then a method of the current graph or exploration will be
called. If the target is 'stored', then the function part will be
treated as a variable reference and the function stored in that variable
will be called.

For builtins, the current value will be used as the only argument. There
are two special cases: for `round`, if an 'ndigits' variable is defined
its value will be used for the optional second argument, and for `range`,
if the current value is `None`, then the values of the 'start', 'stop',
and/or 'step' variables are used for its arguments, with a default start
of 0 and a default step of 1 (there is no default stop; it's an error if
you don't supply one). If the current value is not `None`, `range` just
gets called with the current value as its only argument.

For graph/exploration methods, the current value is ignored and each
listed parameter is sourced from a defined variable of that name, with
parameters for which there is no defined variable going unsupplied
(which might be okay if they're optional). For varargs parameters, the
value of the associated variable will be converted to a tuple and that
will be supplied as if using '*'; for kwargs parameters the value of the
associated variable must be a dictionary, and it will be applied as if
using '**' (except that duplicate arguments will not cause an error;
instead those coming fro the dictionary value will override any already
supplied).
"""

COMMAND_BUILTINS: Dict[str, Callable] = {
    'len': len,
    'min': min,
    'max': max,
    'round': round,  # 'ndigits' may be specified via the environment
    'ceil': math.ceil,
    'floor': math.floor,
    'int': int,
    'float': float,
    'str': str,
    'list': list,
    'tuple': tuple,
    'dict': dict,
    'set': set,
    'copy': copy.copy,
    'deepcopy': copy.deepcopy,
    'range': range,  # parameter names are 'start', 'stop', and 'step'
    'reversed': reversed,
    'sorted': sorted,  # cannot use key= or reverse=
    'print': print,  # prints just one value, ignores sep= and end=
    'warning': logging.warning,  # just one argument
}
"""
The mapping from names to built-in functions usable in commands. Each is
available for use with the 'call' command when 'builtin' is used as the
target. See `FunctionCall` for more details.
"""

SkipCommands: Tuple[
    Literal['skip'],
    str,
    str
] = collections.namedtuple(
    'SkipCommands',
    ['command', 'condition', 'amount']
)
"""
A command which skips forward or backward within the command list it's
included in, but only if a condition value is True. A skip amount of 0
just continues execution as normal. Negative amounts jump to previous
commands (so e.g., -2 will re-execute the two commands above the skip
command), while positive amounts skip over subsequent commands (so e.g.,
1 will skip over one command after this one, resuming execution with the
second command after the skip).

If the condition is False, execution continues with the subsequent
command as normal.

If the distance value is a string instead of an integer, the skip will
redirect execution to the label that uses that name. Note that the
distance value may be a variable reference, in which case the integer or
string inside the reference will determine where to skip to.
"""

Label: Tuple[Literal['label'], str] = collections.namedtuple(
    'Label',
    ['command', 'name']
)
"""
Has no effect, but establishes a label that can be skipped to using the
'skip' command. Note that instead of just a fixed label, a variable name
can be used and variable substitution will determine the label name in
that case, BUT there are two restrictions: the value must be a string,
and you cannot execute a forward-skip to a label which has not already
been evaluated, since the value isn't known when the skip occurs. If you
use a literal label name instead of a variable, you will be able to skip
down to that label from above.

When multiple labels with the same name occur, a skip command will go to
the last label with that name before the skip, only considering labels
after the skip if there are no labels with that name beforehand (and
skipping to the first available label in that case).
"""

Command: 'TypeAlias' = Union[
    LiteralValue,
    EstablishCollection,
    AppendValue,
    SetValue,
    PopValue,
    GetValue,
    RemoveValue,
    ApplyOperator,
    ApplyUnary,
    VariableAssignment,
    VariableDeletion,
    LoadVariable,
    FunctionCall,
    SkipCommands,
    Label
]
"""
The union type for any kind of command. Note that these are all tuples,
all of their members are strings in all cases, and their first member
(named 'command') is always a string that uniquely identifies the type of
the command. Use the `command` function to get some type-checking while
constructing them.
"""

Scope: 'TypeAlias' = Dict[str, Any]
"""
A scope holds variables defined during the execution of a sequence of
commands. Variable names (sans the '$' sign) are mapped to arbitrary
Python values.
"""

CommandResult: 'TypeAlias' = Tuple[
    Scope,
    Union[int, str, None],
    Optional[str]
]
"""
The main result of a command is an updated scope (usually but not
necessarily the same scope object that was used to execute the command).
Additionally, there may be a skip integer that indicates how many
commands should be skipped (if positive) or repeated (if negative) as a
result of the command just executed. This value may also be a string to
skip to a label. There may also be a label value which indicates that
the command that was executed defines that label.
"""


def isSimpleValue(valStr: str) -> bool:
    """
    Returns `True` if the given string is a valid simple value for use
    with a command. Simple values are strings that represent `None`,
    `True`, `False`, integers, floating-point numbers, and quoted
    strings (single or double quotes only). Numbers themselves are not
    simple values.

    Examples:

    >>> isSimpleValue('None')
    True
    >>> isSimpleValue('True')
    True
    >>> isSimpleValue('False')
    True
    >>> isSimpleValue('none')
    False
    >>> isSimpleValue('12')
    True
    >>> isSimpleValue('5.6')
    True
    >>> isSimpleValue('3.2e-10')
    True
    >>> isSimpleValue('2 + 3j')  # ba-dump tsss
    False
    >>> isSimpleValue('hello')
    False
    >>> isSimpleValue('"hello"')
    True
    >>> isSimpleValue('"hel"lo"')
    False
    >>> isSimpleValue('"hel\\\\"lo"')  # note we're in a docstring here
    True
    >>> isSimpleValue("'hi'")
    True
    >>> isSimpleValue("'don\\\\'t'")
    True
    >>> isSimpleValue("")
    False
    >>> isSimpleValue(3)
    False
    >>> isSimpleValue(3.5)
    False
    """
    if not isinstance(valStr, str):
        return False
    if valStr in ('None', 'True', 'False'):
        return True
    else:
        try:
            _ = int(valStr)
            return True
        except ValueError:
            pass

        try:
            _ = float(valStr)
            return True
        except ValueError:
            pass

        if (
            len(valStr) >= 2
        and valStr.startswith("'") or valStr.startswith('"')
        ):
            quote = valStr[0]
            ends = valStr.endswith(quote)
            mismatched = re.search(r'[^\\]' + quote, valStr[1:-1])
            return ends and mismatched is None
        else:
            return False


def resolveValue(valStr: str, context: Scope) -> Any:
    """
    Given a value string which could be a literal value or a variable
    reference, returns the value of that expression. Note that operators
    are not handled: only variable substitution is done.
    """
    if isVariableReference(valStr):
        varName = valStr[1:]
        if varName not in context:
            raise NameError(f"Variable '{varName}' is not defined.")
        return context[varName]
    elif not isSimpleValue(valStr):
        raise ValueError(
            f"{valStr!r} is not a valid value (perhaps you need to add"
            f" quotes to get a string, or '$' to reference a variable?)"
        )
    else:
        if valStr == "True":
            return True
        elif valStr == "False":
            return False
        elif valStr == "None":
            return None
        elif valStr.startswith('"') or valStr.startswith("'"):
            return valStr[1:-1]
        else:
            try:
                return int(valStr)
            except ValueError:
                pass

            try:
                return float(valStr)
            except ValueError:
                pass

            raise RuntimeError(
                f"Validated value {valStr!r} is not a string, a number,"
                f" or a recognized keyword type."
            )


def isVariableReference(value: str) -> bool:
    """
    Returns `True` if the given value is a variable reference. Variable
    references start with '$' and the rest of the reference must be a
    valid python identifier (i.e., a sequence of alphabetic characters,
    digits, and/or underscores which does not start with a digit).

    There is one other possibility: references that start with '$@'
    possibly followed by an identifier.

    Examples:

    >>> isVariableReference('$hi')
    True
    >>> isVariableReference('$good bye')
    False
    >>> isVariableReference('$_')
    True
    >>> isVariableReference('$123')
    False
    >>> isVariableReference('$1ab')
    False
    >>> isVariableReference('$ab1')
    True
    >>> isVariableReference('hi')
    False
    >>> isVariableReference('')
    False
    >>> isVariableReference('$@')
    True
    >>> isVariableReference('$@a')
    True
    >>> isVariableReference('$@1')
    False
    """
    if len(value) < 2:
        return False
    elif value[0] != '$':
        return False
    elif len(value) == 2:
        return value[1] == '@' or value[1].isidentifier()
    else:
        return (
            value[1:].isidentifier()
        ) or (
            value[1] == '@'
        and value[2:].isidentifier()
        )


def resolveVarName(name: str, scope: Scope) -> str:
    """
    Resolves a variable name as either a literal name, or if the name
    starts with '$', via a variable reference in the given scope whose
    value must be a string.
    """
    if name.startswith('$'):
        result = scope[name[1:]]
        if not isinstance(result, str):
            raise TypeError(
                f"Variable '{name[1:]}' cannot be referenced as a"
                f" variable name because it does not hold a string (its"
                f" value is: {result!r}"
            )
        return result
    else:
        return name


def fixArgs(command: str, requires: int, args: List[str]) -> List[str]:
    """
    Checks that the proper number of arguments has been supplied, using
    the command name as part of the message for a `ValueError` if not.
    This will fill in '$_' and '$__' for the first two missing arguments
    instead of generating an error, and returns the possibly modified
    argument list.
    """
    if not (requires - 2 <= len(args) <= requires):
        raise ValueError(
            f"Command '{command}' requires {requires} argument(s) but"
            f" you provided {len(args)}."
        )
    return (args + ['$_', '$__'])[:requires]


def requiresValue(command: str, argDesc: str, arg: str) -> str:
    """
    Checks that the given argument is a simple value, and raises a
    `ValueError` if it's not. Otherwise just returns. The given command
    name and argument description are used in the error message. The
    `argDesc` should be an adjectival phrase, like 'first'.

    Returns the argument given to it.
    """
    if not isSimpleValue(arg):
        raise ValueError(
            f"The {argDesc} argument to '{command}' must be a simple"
            f" value string (got {arg!r})."
        )
    return arg


def requiresLiteralOrVariable(
    command: str,
    argDesc: str,
    options: Collection[str],
    arg: str
) -> str:
    """
    Like `requiresValue` but only allows variable references or one of a
    collection of specific strings as the argument.
    """
    if not isVariableReference(arg) and arg not in options:
        raise ValueError(
            (
                f"The {argDesc} argument to '{command}' must be either"
                f" a variable reference or one of the following strings"
                f" (got {arg!r}):\n  "
            ) + '\n  '.join(options)
        )
    return arg


def requiresValueOrVariable(command: str, argDesc: str, arg: str) -> str:
    """
    Like `requiresValue` but allows variable references as well as
    simple values.
    """
    if not (isSimpleValue(arg) or isVariableReference(arg)):
        raise ValueError(
            f"The {argDesc} argument to '{command}' must be a simple"
            f" value or a variable reference (got {arg!r})."
        )
    return arg


def requiresVariableName(command: str, argDesc: str, arg: str) -> str:
    """
    Like `requiresValue` but allows only variable names, with or without
    the leading '$'.
    """
    if not (isVariableReference(arg) or isVariableReference('$' + arg)):
        raise ValueError(
            f"The {argDesc} argument to '{command}' must be a variable"
            f" name without the '$' or a variable reference (got"
            f" {arg!r})."
        )
    return arg


COMMAND_SETUP: Dict[
    str,
    Tuple[
        type[Command],
        int,
        List[
            Union[
                Literal[
                    "requiresValue",
                    "requiresVariableName",
                    "requiresValueOrVariable"
                ],
                Tuple[
                    Literal["requiresLiteralOrVariable"],
                    Collection[str]
                ]
            ]
        ]
    ]
] = {
    'val': (LiteralValue, 1, ["requiresValue"]),
    'empty': (
        EstablishCollection,
        1,
        [("requiresLiteralOrVariable", {'list', 'tuple', 'set', 'dict'})]
    ),
    'append': (AppendValue, 1, ["requiresValueOrVariable"]),
    'set': (
        SetValue,
        2,
        ["requiresValueOrVariable", "requiresValueOrVariable"]
    ),
    'pop': (PopValue, 0, []),
    'get': (GetValue, 1, ["requiresValueOrVariable"]),
    'remove': (RemoveValue, 1, ["requiresValueOrVariable"]),
    'op': (
        ApplyOperator,
        3,
        [
            ("requiresLiteralOrVariable", get_args(BinaryOperator)),
            "requiresValueOrVariable",
            "requiresValueOrVariable"
        ]
    ),
    'unary': (
        ApplyUnary,
        2,
        [
            ("requiresLiteralOrVariable", get_args(UnaryOperator)),
            "requiresValueOrVariable"
        ]
    ),
    'assign': (
        VariableAssignment,
        2,
        ["requiresVariableName", "requiresValueOrVariable"]
    ),
    'delete': (VariableDeletion, 1, ["requiresVariableName"]),
    'load': (LoadVariable, 1, ["requiresVariableName"]),
    'call': (
        FunctionCall,
        2,
        [
            ("requiresLiteralOrVariable", get_args(CallType)),
            "requiresVariableName"
        ]
    ),
    'skip': (
        SkipCommands,
        2,
        [
            "requiresValueOrVariable",
            "requiresValueOrVariable"
        ]
    ),
    'label': (Label, 1, ["requiresVariableName"]),
}


def command(commandType: str, *_args: str) -> Command:
    """
    A convenience function for constructing a command tuple which
    type-checks the arguments a bit. Raises a `ValueError` if invalid
    information is supplied; otherwise it returns a `Command` tuple.

    Up to two missing arguments will be replaced automatically with '$_'
    and '$__' respectively in most cases.

    Examples:

    >>> command('val', '5')
    LiteralValue(command='val', value='5')
    >>> command('val', '"5"')
    LiteralValue(command='val', value='"5"')
    >>> command('val')
    Traceback (most recent call last):
    ...
    ValueError...
    >>> command('empty')
    EstablishCollection(command='empty', collection='$_')
    >>> command('empty', 'list')
    EstablishCollection(command='empty', collection='list')
    >>> command('empty', '$ref')
    EstablishCollection(command='empty', collection='$ref')
    >>> command('empty', 'invalid')  # invalid argument
    Traceback (most recent call last):
    ...
    ValueError...
    >>> command('empty', 'list', 'dict')  # too many arguments
    Traceback (most recent call last):
    ...
    ValueError...
    >>> command('append', '5')
    AppendValue(command='append', value='5')
    """
    args = list(_args)

    spec = COMMAND_SETUP.get(commandType)
    if spec is None:
        raise ValueError(
            f"Command type '{commandType}' cannot be constructed by"
            f" assembleSimpleCommand (try the command function"
            f" instead)."
        )

    commandVariant, nArgs, checkers = spec

    args = fixArgs(commandType, nArgs, args)

    checkedArgs = []
    for i, (checker, arg) in enumerate(zip(checkers, args)):
        argDesc = str(i + 1)
        if argDesc.endswith('1') and nArgs != 11:
            argDesc += 'st'
        elif argDesc.endswith('2') and nArgs != 12:
            argDesc += 'nd'
        elif argDesc.endswith('3') and nArgs != 13:
            argDesc += 'rd'
        else:
            argDesc += 'th'

        if isinstance(checker, tuple):
            checkName, allowed = checker
            checkFn = globals()[checkName]
            checkedArgs.append(
                checkFn(commandType, argDesc, allowed, arg)
            )
        else:
            checkFn = globals()[checker]
            checkedArgs.append(checkFn(commandType, argDesc, arg))

    return commandVariant(
        commandType,
        *checkedArgs
    )


def pushCurrentValue(scope: Scope, value: Any) -> None:
    """
    Pushes the given value as the 'current value' for the given scope,
    storing it in the '_' variable. Stores the old '_' value into '__'
    if there was one.
    """
    if '_' in scope:
        scope['__'] = scope['_']
    scope['_'] = value
