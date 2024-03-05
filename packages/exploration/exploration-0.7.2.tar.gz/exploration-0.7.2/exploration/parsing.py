"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2023-12-27
- Purpose: Common code for parsing things, including conversions to
    custom string formats and JSON for some types.
"""

from typing import (
    Union, Dict, Optional, get_args, Tuple, List, cast, Set, TypeVar,
    Literal, TypeAlias, Generator, TypedDict, TextIO, Any, Callable,
    Type, Sequence
)

import enum
import collections
import copy
import warnings
import json

import networkx  # type: ignore

from . import base
from . import core
from . import utils
from . import commands


#----------------#
# Format Details #
#----------------#

Lexeme = enum.IntEnum(
    "Lexeme",
    [
        'domainSeparator',
        'zoneSeparator',
        'partSeparator',
        'stateOn',
        'stateOff',
        'tokenCount',
        'effectCharges',
        'sepOrDelay',
        'consequenceSeparator',
        'inCommon',
        'isHidden',
        'skillLevel',
        'inverseSkill',
        'withDetails',
        'reciprocalSeparator',
        'mechanismSeparator',
        'openCurly',
        'closeCurly',
        'openParen',
        'closeParen',
        'angleLeft',
        'angleRight',
        'doubleQuestionmark',
        'ampersand',
        'orBar',
        'notMarker',
    ]
)
"""
These are the different separators, grouping characters, and keywords
used as part of parsing. The characters that are actually recognized are
defined as part of a `Format`.
"""

Format = Dict[Lexeme, str]
"""
A journal format is specified using a dictionary with keys that denote
journal marker types and values which are one-to-several-character
strings indicating the markup used for that entry/info type.
"""

DEFAULT_FORMAT: Format = {
    # Separator
    Lexeme.domainSeparator: '//',
    Lexeme.zoneSeparator: '::',
    Lexeme.partSeparator: '%%',
    Lexeme.stateOn: '=on',  # TODO :Lexing issue!
    Lexeme.stateOff: '=off',
    Lexeme.tokenCount: '*',
    Lexeme.effectCharges: '=',
    Lexeme.sepOrDelay: ',',
    Lexeme.consequenceSeparator: ';',
    Lexeme.inCommon: '+c',
    Lexeme.isHidden: '+h',
    Lexeme.skillLevel: '^',
    Lexeme.inverseSkill: '~',
    Lexeme.withDetails: '%',
    Lexeme.reciprocalSeparator: '/',
    Lexeme.mechanismSeparator: ':',
    Lexeme.openCurly: '{',
    Lexeme.closeCurly: '}',
    Lexeme.openParen: '(',
    Lexeme.closeParen: ')',
    Lexeme.angleLeft: '<',
    Lexeme.angleRight: '>',
    Lexeme.doubleQuestionmark: '??',
    Lexeme.ampersand: '&',
    Lexeme.orBar: '|',
    Lexeme.notMarker: '!',
}
"""
The default parsing format.
"""

DEFAULT_EFFECT_NAMES: Dict[str, base.EffectType] = {
    x: x for x in get_args(base.EffectType)
}
"""
Default names for each effect type. Maps names to canonical effect type
strings. A different mapping could be used to allow for writing effect
names in another language, for example.
"""

DEFAULT_FOCALIZATION_NAMES: Dict[str, base.DomainFocalization] = {
    x: x for x in get_args(base.DomainFocalization)
}
"""
Default names for each domain focalization type. Maps each focalization
type string to itself.
"""

DEFAULT_SF_INDICATORS: Tuple[str, str] = ('s', 'f')
"""
Default characters used to indicate success/failure when transcribing a
`TransitionWithOutcomes`.
"""


#-------------------#
# Errors & Warnings #
#-------------------#

class ParseWarning(Warning):
    """
    Represents a warning encountered when parsing something.
    """
    pass


class ParseError(ValueError):
    """
    Represents a error encountered when parsing.
    """
    pass


class DotParseError(ParseError):
    """
    An error raised during parsing when incorrectly-formatted graphviz
    "dot" data is provided. See `parseDot`.
    """
    pass


class InvalidFeatureSpecifierError(ParseError):
    """
    An error used when a feature specifier is in the wrong format.
    Errors with part specifiers also use this.
    """


#--------#
# Lexing #
#--------#

LexedTokens: TypeAlias = List[Union[Lexeme, str]]
"""
When lexing, we pull apart a string into pieces, but when we recognize
lexemes, we use their integer IDs in the list instead of strings, so we
get a list that's a mix of ints and strings.
"""

GroupedTokens: TypeAlias = List[Union[Lexeme, str, 'GroupedTokens']]
"""
Some parsing processes group tokens into sub-lists. This type represents
`LexedTokens` which might also contain sub-lists, to arbitrary depth.
"""

GroupedRequirementParts: TypeAlias = List[
    Union[Lexeme, base.Requirement, 'GroupedRequirementParts']
]
"""
Another intermediate parsing result during requirement parsing: a list
of `base.Requirements` possibly with some sub-lists and/or `Lexeme`s
mixed in.
"""


def lex(
    characters: str,
    tokenMap: Optional[Dict[str, Lexeme]] = None
) -> LexedTokens:
    """
    Lexes a list of tokens from a characters string. Recognizes any
    special characters you provide in the token map, as well as
    collections of non-mapped characters. Recognizes double-quoted
    strings which can contain any of those (and which use
    backslash-escapes for internal double quotes) and includes quoted
    versions of those strings as tokens (any token string starting with a
    double quote will be such a string). Breaks tokens on whitespace
    outside of quotation marks, and ignores that whitespace.

    Examples:

    >>> lex('abc')
    ['abc']
    >>> lex('(abc)', {'(': 0, ')': 1})
    [0, 'abc', 1]
    >>> lex('{(abc)}', {'(': 0, ')': 1, '{': 2, '}': 3})
    [2, 0, 'abc', 1, 3]
    >>> lex('abc def')
    ['abc', 'def']
    >>> lex('abc   def')
    ['abc', 'def']
    >>> lex('abc \\n def')
    ['abc', 'def']
    >>> lex ('"quoted"')
    ['"quoted"']
    >>> lex ('"quoted  pair"')
    ['"quoted  pair"']
    >>> lex ('  oneWord | "two words"|"three  words words" ', {'|': 0})
    ['oneWord', 0, '"two words"', 0, '"three  words words"']
    >>> tokenMap = { c: i for (i, c) in enumerate("(){}~:;>,") }
    >>> tokenMap['::'] = 9
    >>> tokenMap['~~'] = 10
    >>> lex(
    ...     '{~~2:best(brains, brawn)>{set switch on}'
    ...     '{deactivate ,1; bounce}}',
    ...     tokenMap
    ... )
    [2, 10, '2', 5, 'best', 0, 'brains', 8, 'brawn', 1, 7, 2, 'set',\
 'switch', 'on', 3, 2, 'deactivate', 8, '1', 6, 'bounce', 3, 3]
    >>> lex('set where::mechanism state', tokenMap)
    ['set', 'where', 9, 'mechanism', 'state']
    >>> # Note r' doesn't take full effect 'cause we're in triple quotes
    >>> esc = r'"escape \\\\a"'
    >>> result = [ r'"escape \\\\a"' ]  # 'quoted' doubles the backslash
    >>> len(esc)
    12
    >>> len(result[0])
    12
    >>> lex(esc) == result
    True
    >>> quoteInQuote = r'before "hello \\\\ \\" goodbye"after'
    >>> # Note r' doesn't take full effect 'cause we're in triple quotes
    >>> expect = ['before', r'"hello \\\\ \\" goodbye"', 'after']
    >>> lex(quoteInQuote) == expect
    True
    >>> lex('O\\'Neill')
    ["O'Neill"]
    >>> lex('one "quote ')
    ['one', '"quote "']
    >>> lex('geo*15', {'*': 0})
    ['geo', 0, '15']
    """
    if tokenMap is None:
        tokenMap = {}
    tokenStarts: Dict[str, List[str]] = {}
    for key in sorted(tokenMap.keys(), key=lambda x: -len(x)):
        tokenStarts.setdefault(key[:1], []).append(key)
    tokens: LexedTokens = []
    sofar = ''
    inQuote = False
    escaped = False
    skip = 0
    for i in range(len(characters)):
        if skip > 0:
            skip -= 1
            continue

        char = characters[i]
        if escaped:
            # TODO: Escape sequences?
            sofar += char
            escaped = False

        elif char == '\\':
            if inQuote:
                escaped = True
            else:
                sofar += char

        elif char == '"':
            if sofar != '':
                if inQuote:
                    tokens.append(utils.quoted(sofar))
                else:
                    tokens.append(sofar)
            sofar = ''
            inQuote = not inQuote

        elif inQuote:
            sofar += char

        elif char in tokenStarts:
            options = tokenStarts[char]
            hit: Optional[str] = None
            for possibility in options:
                lp = len(possibility)
                if (
                    (lp == 1 and char == possibility)
                or characters[i:i + lp] == possibility
                ):
                    hit = possibility
                    break

            if hit is not None:
                if sofar != '':
                    tokens.append(sofar)
                tokens.append(tokenMap[possibility])
                sofar = ''
                skip = len(hit) - 1
            else:  # Not actually a recognized token
                sofar += char

        elif char.isspace():
            if sofar != '':
                tokens.append(sofar)
            sofar = ''

        else:
            sofar += char

    if sofar != '':
        if inQuote:
            tokens.append(utils.quoted(sofar))
        else:
            tokens.append(sofar)

    return tokens


def unLex(
    tokens: LexedTokens,
    tokenMap: Optional[Dict[str, Lexeme]] = None
) -> str:
    """
    Turns lexed stuff back into a string, substituting strings back into
    token spots by reversing the given token map. Adds quotation marks to
    complex tokens where necessary to prevent them from re-lexing into
    multiple tokens (but `lex` doesn't  remove those, so in some cases
    there's not a perfect round-trip unLex -> lex).

    For example:

    >>> unLex(['a', 'b'])
    'a b'
    >>> tokens = {'(': 0, ')': 1, '{': 2, '}': 3, '::': 4}
    >>> unLex([0, 'hi', 1], tokens)
    '(hi)'
    >>> unLex([0, 'visit', 'zone', 4, 'decision', 1], tokens)
    '(visit zone::decision)'
    >>> q = unLex(['a complex token', '\\'single\\' and "double" quotes'])
    >>> q  # unLex adds quotes
    '"a complex token" "\\'single\\' and \\\\"double\\\\" quotes"'
    >>> lex(q)  # Not the same as the original list
    ['"a complex token"', '"\\'single\\' and \\\\"double\\\\" quotes"']
    >>> lex(unLex(lex(q)))  # But further round-trips work
    ['"a complex token"', '"\\'single\\' and \\\\"double\\\\" quotes"']

    TODO: Fix this:
    For now, it generates incorrect results when token combinations can
    be ambiguous. These ambiguous token combinations should not ever be
    generated by `lex` at least. For example:

    >>> ambiguous = {':': 0, '::': 1}
    >>> u = unLex(['a', 0, 0, 'b'], ambiguous)
    >>> u
    'a::b'
    >>> l = lex(u, ambiguous)
    >>> l
    ['a', 1, 'b']
    >>> l == u
    False
    """
    if tokenMap is None:
        nTokens = 0
        revMap = {}
    else:
        nTokens = len(tokenMap)
        revMap = {y: x for (x, y) in tokenMap.items()}

    prevRaw = False
    # TODO: add spaces where necessary to disambiguate token sequences...
    if len(revMap) != nTokens:
        warnings.warn(
            (
                "Irreversible token map! Two or more tokens have the same"
                " integer value."
            ),
            ParseWarning
        )

    result = ""
    for item in tokens:
        if isinstance(item, int):
            try:
                result += revMap[item]
            except KeyError:
                raise ValueError(
                    f"Tokens list contains {item} but the token map"
                    f" does not have any entry which maps to {item}."
                )
            prevRaw = False
        elif isinstance(item, str):
            if prevRaw:
                result += ' '
            if len(lex(item)) > 1:
                result += utils.quoted(item)
            else:
                result += item
            prevRaw = True
        else:
            raise TypeError(
                f"Token list contained non-int non-str item:"
                f" {repr(item)}"
            )

    return result


#-------------------#
# ParseFormat class #
#-------------------#

def normalizeEnds(
    tokens: List,
    start: int,
    end: int
) -> Tuple[int, int, int]:
    """
    Given a tokens list and start & end integers, does some bounds
    checking and normalization on the integers: converts negative
    indices to positive indices, and raises an `IndexError` if they're
    out-of-bounds after conversion. Returns a tuple containing the
    normalized start & end indices, along with the number of tokens they
    cover.
    """
    totalTokens = len(tokens)
    if start < -len(tokens):
        raise IndexError(
            f"Negative start index out of bounds (got {start} for"
            f" {totalTokens} tokens)."
        )
    elif start >= totalTokens:
        raise IndexError(
            f"Start index out of bounds (got {start} for"
            f" {totalTokens} tokens)."
        )
    elif start < 0:
        start = totalTokens + start

    if end < -len(tokens):
        raise IndexError(
            f"Negative end index out of bounds (got {end} for"
            f" {totalTokens} tokens)."
        )
    elif end >= totalTokens:
        raise IndexError(
            f"Start index out of bounds (got {end} for"
            f" {totalTokens} tokens)."
        )
    elif end < 0:
        end = totalTokens + end

    if end >= len(tokens):
        end = len(tokens) - 1

    return (start, end, (end - start) + 1)


def findSeparatedParts(
    tokens: LexedTokens,
    sep: Union[str, int],
    start: int = 0,
    end: int = -1,
    groupStart: Union[str, int, None] = None,
    groupEnd: Union[str, int, None] = None
) -> Generator[Tuple[int, int], None, None]:
    """
    Finds parts separated by a separator lexeme, such as ';' or ',', but
    ignoring separators nested within groupStart/groupEnd pairs (if
    those arguments are supplied). For each token sequence found, yields
    a tuple containing the start index and end index for that part, with
    separators not included in the parts.

    If two separators appear in a row, the start/end pair will have a
    start index one after the end index.

    If there are no separators, yields one pair containing the start and
    end of the entire tokens sequence.

    Raises a `ParseError` if there are unbalanced grouping elements.

    For example:

    >>> list(findSeparatedParts(
    ...     [ 'one' ],
    ...     Lexeme.sepOrDelay,
    ...     0,
    ...     0,
    ...     Lexeme.openParen,
    ...     Lexeme.closeParen
    ... ))
    [(0, 0)]
    >>> list(findSeparatedParts(
    ...     [
    ...         'best',
    ...         Lexeme.openParen,
    ...         'chess',
    ...         Lexeme.sepOrDelay,
    ...         'checkers',
    ...         Lexeme.closeParen
    ...     ],
    ...     Lexeme.sepOrDelay,
    ...     2,
    ...     4,
    ...     Lexeme.openParen,
    ...     Lexeme.closeParen
    ... ))
    [(2, 2), (4, 4)]
    """
    start, end, n = normalizeEnds(tokens, start, end)
    level = 0
    thisStart = start
    for i in range(start, end + 1):
        token = tokens[i]
        if token == sep and level == 0:
            yield (thisStart, i - 1)
            thisStart = i + 1
        elif token == groupStart:
            level += 1
        elif token == groupEnd:
            level -= 1
            if level < 0:
                raise ParseError("Unbalanced grouping tokens.")
    if level < 0:
        raise ParseError("Unbalanced grouping tokens.")
    yield (thisStart, end)


K = TypeVar('K')
"Type variable for dictionary keys."
V = TypeVar('V')
"Type variable for dictionary values."


def checkCompleteness(
    name,
    mapping: Dict[K, V],
    keysSet: Optional[Set[K]] = None,
    valuesSet: Optional[Set[V]] = None
):
    """
    Checks that a dictionary has a certain exact set of keys (or
    values). Raises a `ValueError` if it finds an extra or missing key
    or value.
    """
    if keysSet is not None:
        for key in mapping.keys():
            if key not in keysSet:
                raise ValueError("{name} has extra key {repr(key)}.")

        for key in keysSet:
            if key not in mapping:
                raise ValueError("{name} is missing key {repr(key)}.")

    if valuesSet is not None:
        for value in mapping.values():
            if value not in valuesSet:
                raise ValueError("{name} has extra value {repr(value)}.")

        checkVals = mapping.values()
        for value in valuesSet:
            if value not in checkVals:
                raise ValueError("{name} is missing value {repr(value)}.")


class ParseFormat:
    """
    A ParseFormat manages the mapping from markers to entry types and
    vice versa.
    """
    def __init__(
        self,
        formatDict: Format = DEFAULT_FORMAT,
        effectNames: Dict[str, base.EffectType] = DEFAULT_EFFECT_NAMES,
        focalizationNames: Dict[
            str,
            base.DomainFocalization
        ] = DEFAULT_FOCALIZATION_NAMES,
        successFailureIndicators: Tuple[str, str] = DEFAULT_SF_INDICATORS
    ):
        """
        Sets up the parsing format. Requires a `Format` dictionary to
        define the specifics. Raises a `ValueError` unless the keys of
        the `Format` dictionary exactly match the `Lexeme` values.
        """
        self.formatDict = formatDict
        self.effectNames = effectNames
        self.focalizationNames = focalizationNames
        if (
            len(successFailureIndicators) != 2
        or any(len(i) != 1 for i in successFailureIndicators)
        ):
            raise ValueError(
                f"Invalid success/failure indicators: must be a pair of"
                f" length-1 strings. Got: {successFailureIndicators!r}"
            )
        self.successIndicator, self.failureIndicator = (
            successFailureIndicators
        )

        # Check completeness for each dictionary
        checkCompleteness('formatDict', self.formatDict, set(Lexeme))
        checkCompleteness(
            'effectNames',
            self.effectNames,
            valuesSet=set(get_args(base.EffectType))
        )
        checkCompleteness(
            'focalizationNames',
            self.focalizationNames,
            valuesSet=set(get_args(base.DomainFocalization))
        )

        # Build some reverse lookup dictionaries for specific
        self.reverseFormat = {y: x for (x, y) in self.formatDict.items()}

        # circumstances:
        self.effectModMap = {
            self.formatDict[x]: x
            for x in [
                Lexeme.effectCharges,
                Lexeme.sepOrDelay,
                Lexeme.inCommon,
                Lexeme.isHidden
            ]
        }

    def lex(self, content: str) -> LexedTokens:
        """
        Applies `lex` using this format's lexeme mapping.
        """
        return lex(content, self.reverseFormat)

    def onOff(self, word: str) -> Optional[bool]:
        """
        Parse an on/off indicator and returns a boolean (`True` for on
        and `False` for off). Returns `None` if the word isn't either
        the 'on' or the 'off' word. Generates a `ParseWarning`
        (and still returns `None`) if the word is a case-swapped version
        of the 'on' or 'off' word and is not equal to either of them.
        """
        onWord = self.formatDict[Lexeme.stateOn]
        offWord = self.formatDict[Lexeme.stateOff]

        # Generate warning if we suspect a case error
        if (
            word.casefold() in (onWord, offWord)
        and word not in (onWord, offWord)
        ):
            warnings.warn(
                (
                    f"Word '{word}' cannot be interpreted as an on/off"
                    f" value, although it is almost one (the correct"
                    f" values are '{onWord}' and '{offWord}'."
                ),
                ParseWarning
            )

        # return the appropriate value
        if word == onWord:
            return True
        elif word == offWord:
            return False
        else:
            return None

    def matchingBrace(
        self,
        tokens: LexedTokens,
        where: int,
        opener: int = Lexeme.openCurly,
        closer: int = Lexeme.closeCurly
    ) -> int:
        """
        Returns the index within the given tokens list of the closing
        curly brace which matches the open brace at the specified index.
        You can specify custom `opener` and/or `closer` lexemes to find
        matching pairs of other things. Raises a `ParseError` if there
        is no opening brace at the specified index, or if there isn't a
        matching closing brace. Handles nested braces of the specified
        type.

        Examples:
        >>> pf = ParseFormat()
        >>> ob = Lexeme.openCurly
        >>> cb = Lexeme.closeCurly
        >>> pf.matchingBrace([ob, cb], 0)
        1
        >>> pf.matchingBrace([ob, cb], 1)
        Traceback (most recent call last):
          ...
        exploration.parsing.ParseError: ...
        >>> pf.matchingBrace(['hi', ob, cb], 0)
        Traceback (most recent call last):
          ...
        exploration.parsing.ParseError: ...
        >>> pf.matchingBrace(['hi', ob, cb], 1)
        2
        >>> pf.matchingBrace(['hi', ob, 'lo', cb], 1)
        3
        >>> pf.matchingBrace([ob, 'hi', 'lo', cb], 1)
        Traceback (most recent call last):
          ...
        exploration.parsing.ParseError: ...
        >>> pf.matchingBrace([ob, 'hi', 'lo', cb], 0)
        3
        >>> pf.matchingBrace([ob, ob, cb, cb], 0)
        3
        >>> pf.matchingBrace([ob, ob, cb, cb], 1)
        2
        >>> pf.matchingBrace([ob, cb, ob, cb], 0)
        1
        >>> pf.matchingBrace([ob, cb, ob, cb], 2)
        3
        >>> pf.matchingBrace([ob, cb, cb, cb], 0)
        1
        >>> pf.matchingBrace([ob, ob, ob, cb], 0)
        Traceback (most recent call last):
          ...
        exploration.parsing.ParseError: ...
        >>> pf.matchingBrace([ob, ob, 'hi', ob, cb, 'lo', cb, cb], 0)
        7
        >>> pf.matchingBrace([ob, ob, 'hi', ob, cb, 'lo', cb, cb], 1)
        6
        >>> pf.matchingBrace([ob, ob, 'hi', ob, cb, 'lo', cb, cb], 2)
        Traceback (most recent call last):
          ...
        exploration.parsing.ParseError: ...
        >>> pf.matchingBrace([ob, ob, 'hi', ob, cb, 'lo', cb, cb], 3)
        4
        >>> op = Lexeme.openParen
        >>> cp = Lexeme.closeParen
        >>> pf.matchingBrace([ob, op, ob, cp], 1, op, cp)
        3
        """
        if where >= len(tokens):
            raise ParseError(
                f"Out-of-bounds brace start: index {where} with"
                f" {len(tokens)} tokens."
            )
        if tokens[where] != opener:
            raise ParseError(
                f"Can't find matching brace for token"
                f" {repr(tokens[where])} at index {where} because it's"
                f" not an open brace."
            )

        level = 1
        for i in range(where + 1, len(tokens)):
            token = tokens[i]
            if token == opener:
                level += 1
            elif token == closer:
                level -= 1
                if level == 0:
                    return i

        raise ParseError(
            f"Failed to find matching curly brace from index {where}."
        )

    def parseFocalization(self, word: str) -> base.DomainFocalization:
        """
        Parses a focalization type for a domain, recognizing
        'domainFocalizationSingular', 'domainFocalizationPlural', and
        'domainFocalizationSpreading'.
        """
        try:
            return self.focalizationNames[word]
        except KeyError:
            raise ParseError(
                f"Invalid domain focalization name {repr(word)}. Valid"
                f" name are: {repr(list(self.focalizationNames))}'."
            )

    def hasZoneParts(self, name: str) -> bool:
        """
        Returns true if the specified name contains zone parts (using
        the `zoneSeparator`).
        """
        return self.formatDict[Lexeme.zoneSeparator] in name

    def splitZone(
        self,
        name: str
    ) -> Tuple[List[base.Zone], base.DecisionName]:
        """
        Splits a decision name that includes zone information into the
        list-of-zones part and the decision part. If there is no zone
        information in the name, the list-of-zones will be an empty
        list.
        """
        sep = self.formatDict[Lexeme.zoneSeparator]
        parts = name.split(sep)
        return (list(parts[:-1]), parts[-1])

    def prefixWithZone(
        self,
        name: base.DecisionName,
        zone: base.Zone
    ) -> base.DecisionName:
        """
        Returns the given decision name, prefixed with the given zone
        name. Does NOT check whether the decision name already includes
        a prefix or not.
        """
        return zone + self.formatDict[Lexeme.zoneSeparator] + name

    def parseAnyTransitionFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0
    ) -> Tuple[base.TransitionWithOutcomes, int]:
        """
        Parses a `base.TransitionWithOutcomes` from a tokens list,
        accepting either a transition name or a transition name followed
        by a `Lexeme.withDetails` followed by a string of success and
        failure indicator characters. Returns a tuple containing a
        `base.TransitionWithOutcomes` and an integer indicating the end
        index of the parsed item within the tokens.
        """
        # Normalize start index so we can do index math
        if start < 0:
            useIndex = len(tokens) + start
        else:
            useIndex = start

        try:
            first = tokens[useIndex]
        except IndexError:
            raise ParseError(
                f"Invalid token index: {start!r} among {len(tokens)}"
                f" tokens."
            )

        if isinstance(first, Lexeme):
            raise ParseError(
                f"Expecting a transition name (possibly with a"
                f" success/failure indicator string) but first token is"
                f" {first!r}."
            )

        try:
            second = tokens[useIndex + 1]
            third = tokens[useIndex + 2]
        except IndexError:
            return ((first, []), useIndex)

        if second != Lexeme.withDetails or isinstance(third, Lexeme):
            return ((first, []), useIndex)

        outcomes = []
        for char in third:
            if char == self.successIndicator:
                outcomes.append(True)
            elif char == self.failureIndicator:
                outcomes.append(False)
            else:
                return ((first, []), useIndex)

        return ((first, outcomes), useIndex + 2)

    def parseTransitionWithOutcomes(
        self,
        content: str
    ) -> base.TransitionWithOutcomes:
        """
        Takes a transition that may have outcomes listed as a series of
        s/f strings after a colon and returns the corresponding
        `TransitionWithOutcomes` tuple. Calls `lex` and then
        `parseAnyTransitionFromTokens`.
        """
        return self.parseAnyTransitionFromTokens(self.lex(content))[0]

    def unparseTransitionWithOutocmes(
        self,
        transition: base.AnyTransition
    ) -> str:
        """
        Turns a `base.AnyTransition` back into a string that would parse
        to an equivalent `base.TransitionWithOutcomes` via
        `parseTransitionWithOutcomes`. If a bare `base.Transition` is
        given, returns a string that would result in a
        `base.TransitionWithOutcomes` that has an empty outcomes
        sequence.
        """
        if isinstance(transition, base.Transition):
            return transition
        elif (
            isinstance(transition, tuple)
        and len(transition) == 2
        and isinstance(transition[0], base.Transition)
        and isinstance(transition[1], list)
        and all(isinstance(sfi, bool) for sfi in transition[1])
        ):
            if len(transition[1]) == 0:
                return transition[0]
            else:
                result = transition[0] + self.formatDict[Lexeme.withDetails]
                for outcome in transition[1]:
                    if outcome:
                        result += self.successIndicator
                    else:
                        result += self.failureIndicator
                return result
        else:
            raise TypeError(
                f"Invalid AnyTransition: neither a string, nor a"
                f" length-2 tuple consisting of a string followed by a"
                f" list of booleans. Got: {transition!r}"
            )

    def parseSpecificTransition(
        self,
        content: str
    ) -> Tuple[base.DecisionName, base.Transition]:
        """
        Splits a decision:transition pair to the decision and transition
        part, using a custom separator if one is defined.
        """
        sep = self.formatDict[Lexeme.withDetails]
        n = content.count(sep)
        if n == 0:
            raise ParseError(
                f"Cannot split '{content}' into a decision name and a"
                f" transition name (no separator '{sep}' found)."
            )
        elif n > 1:
            raise ParseError(
                f"Cannot split '{content}' into a decision name and a"
                f" transition name (too many ({n}) '{sep}' separators"
                f" found)."
            )
        else:
            return cast(
                Tuple[base.DecisionName, base.Transition],
                tuple(content.split(sep))
            )

    def splitDirections(
        self,
        content: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Splits a piece of text using the 'Lexeme.reciprocalSeparator'
        into two pieces. If there is no separator, the second piece will
        be `None`; if either side of the separator is blank, that side
        will be `None`, and if there is more than one separator, a
        `ParseError` will be raised. Whitespace will be stripped from
        both sides of each result.

        Examples:

        >>> pf = ParseFormat()
        >>> pf.splitDirections('abc / def')
        ('abc', 'def')
        >>> pf.splitDirections('abc def ')
        ('abc def', None)
        >>> pf.splitDirections('abc def /')
        ('abc def', None)
        >>> pf.splitDirections('/abc def')
        (None, 'abc def')
        >>> pf.splitDirections('a/b/c') # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        ParseError: ...
        """
        sep = self.formatDict[Lexeme.reciprocalSeparator]
        count = content.count(sep)
        if count > 1:
            raise ParseError(
                f"Too many split points ('{sep}') in content:"
                f" '{content}' (only one is allowed)."
            )

        elif count == 1:
            before, after = content.split(sep)
            before = before.strip()
            after = after.strip()
            return (before or None, after or None)

        else: # no split points
            stripped = content.strip()
            if stripped:
                return stripped, None
            else:
                return None, None

    def parseItem(
        self,
        item: str
    ) -> Union[
        base.Capability,
        Tuple[base.Token, int],
        Tuple[base.MechanismName, base.MechanismState]
    ]:
        """
        Parses an item, which is a capability (just a string), a
        token-type*number pair (returned as a tuple with the number
        converted to an integer), or a mechanism-name:state pair
        (returned as a tuple with the state as a string). The
        'Lexeme.tokenCount' and `Lexeme.mechanismSeparator` format
        values determine the separators that this looks for.
        """
        tsep = self.formatDict[Lexeme.tokenCount]
        msep = self.formatDict[Lexeme.mechanismSeparator]
        if tsep in item:
            # It's a token w/ an associated count
            parts = item.split(tsep)
            if len(parts) != 2:
                raise ParseError(
                    f"Item '{item}' has a '{tsep}' but doesn't separate"
                    f" into a token type and a count."
                )
            typ, count = parts
            try:
                num = int(count)
            except ValueError:
                raise ParseError(
                    f"Item '{item}' has invalid token count '{count}'."
                )

            return (typ, num)
        elif msep in item:
            parts = item.split(msep)
            mechanism = msep.join(parts[:-1])
            state = parts[-1]
            if mechanism.endswith(':'):
                # Just a zone-qualified name...
                return item
            else:
                return (mechanism, state)
        else:
            # It's just a capability
            return item

    def unparseDecisionSpecifier(self, spec: base.DecisionSpecifier) -> str:
        """
        Turns a decision specifier back into a string, which would be
        parsed as a decision specifier as part of various different
        things.

        For example:

        >>> pf = ParseFormat()
        >>> pf.unparseDecisionSpecifier(
        ...     base.DecisionSpecifier(None, None, 'where')
        ... )
        'where'
        >>> pf.unparseDecisionSpecifier(
        ...     base.DecisionSpecifier(None, 'zone', 'where')
        ... )
        'zone::where'
        >>> pf.unparseDecisionSpecifier(
        ...     base.DecisionSpecifier('domain', 'zone', 'where')
        ... )
        'domain//zone::where'
        >>> pf.unparseDecisionSpecifier(
        ...     base.DecisionSpecifier('domain', None, 'where')
        ... )
        'domain//where'
        """
        result = spec.name
        if spec.zone is not None:
            result = (
                spec.zone
              + self.formatDict[Lexeme.zoneSeparator]
              + result
            )
        if spec.domain is not None:
            result = (
                spec.domain
              + self.formatDict[Lexeme.domainSeparator]
              + result
            )
        return result

    def unparseMechanismSpecifier(
        self,
        spec: base.MechanismSpecifier
    ) -> str:
        """
        Turns a mechanism specifier back into a string, which would be
        parsed as a mechanism specifier as part of various different
        things. Note that a mechanism specifier with a zone part but no
        decision part is not valid, since it would parse as a decision
        part instead.

        For example:

        >>> pf = ParseFormat()
        >>> pf.unparseMechanismSpecifier(
        ...     base.MechanismSpecifier(None, None, None, 'lever')
        ... )
        'lever'
        >>> pf.unparseMechanismSpecifier(
        ...     base.MechanismSpecifier('domain', 'zone', 'decision', 'door')
        ... )
        'domain//zone::decision::door'
        >>> pf.unparseMechanismSpecifier(
        ...     base.MechanismSpecifier('domain', None, None, 'door')
        ... )
        'domain//door'
        >>> pf.unparseMechanismSpecifier(
        ...     base.MechanismSpecifier(None, 'a', 'b', 'door')
        ... )
        'a::b::door'
        >>> pf.unparseMechanismSpecifier(
        ...     base.MechanismSpecifier(None, 'a', None, 'door')
        ... )
        Traceback (most recent call last):
        ...
        exploration.base.InvalidMechanismSpecifierError...
        >>> pf.unparseMechanismSpecifier(
        ...     base.MechanismSpecifier(None, None, 'a', 'door')
        ... )
        'a::door'
        """
        if spec.decision is None and spec.zone is not None:
            raise base.InvalidMechanismSpecifierError(
                f"Mechanism specifier has a zone part but no decision"
                f" part; it cannot be unparsed since it would parse"
                f" differently:\n{spec}"
            )
        result = spec.name
        if spec.decision is not None:
            result = (
                spec.decision
              + self.formatDict[Lexeme.zoneSeparator]
              + result
            )
        if spec.zone is not None:
            result = (
                spec.zone
              + self.formatDict[Lexeme.zoneSeparator]
              + result
            )
        if spec.domain is not None:
            result = (
                spec.domain
              + self.formatDict[Lexeme.domainSeparator]
              + result
            )
        return result

    def effectType(self, effectMarker: str) -> Optional[base.EffectType]:
        """
        Returns the `base.EffectType` string corresponding to the
        given effect marker string. Returns `None` for an unrecognized
        marker.
        """
        return self.effectNames.get(effectMarker)

    def parseCommandFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> commands.Command:
        """
        Given tokens that specify a `commands.Command`, parses that
        command and returns it. Really just turns the tokens back into
        strings and calls `commands.command`.

        For example:

        >>> pf = ParseFormat()
        >>> t = ['val', '5']
        >>> c = commands.command(*t)
        >>> pf.parseCommandFromTokens(t) == c
        True
        >>> t = ['op', Lexeme.tokenCount, '$val', '$val']
        >>> c = commands.command('op', '*', '$val', '$val')
        >>> pf.parseCommandFromTokens(t) == c
        True
        """
        start, end, nTokens = normalizeEnds(tokens, start, end)
        args: List[str] = []
        for token in tokens[start:end + 1]:
            if isinstance(token, Lexeme):
                args.append(self.formatDict[token])
            else:
                args.append(token)

        if len(args) == 0:
            raise ParseError(
                f"No arguments for command:\n{tokens[start:end + 1]}"
            )
        return commands.command(*args)

    def unparseCommand(self, command: commands.Command) -> str:
        """
        Turns a `Command` back into the string that would produce that
        command when parsed using `parseCommandList`.

        Note that the results will be more explicit in some cases than what
        `parseCommandList` would accept as input.

        For example:

        >>> pf = ParseFormat()
        >>> pf.unparseCommand(
        ...     commands.LiteralValue(command='val', value='5')
        ... )
        'val 5'
        >>> pf.unparseCommand(
        ...     commands.LiteralValue(command='val', value='"5"')
        ... )
        'val "5"'
        >>> pf.unparseCommand(
        ...     commands.EstablishCollection(
        ...         command='empty',
        ...         collection='list'
        ...     )
        ... )
        'empty list'
        >>> pf.unparseCommand(
        ...     commands.AppendValue(command='append', value='$_')
        ... )
        'append $_'
        """
        candidate = None
        for k, v in commands.COMMAND_SETUP.items():
            if v[0] == type(command):
                if candidate is None:
                    candidate = k
                else:
                    raise ValueError(
                        f"COMMAND_SETUP includes multiple keys with"
                        f" {type(command)} as their value type:"
                        f" '{candidate}' and '{k}'."
                    )

        if candidate is None:
            raise ValueError(
                f"COMMAND_SETUP has no key with {type(command)} as its"
                f" value type."
            )

        result = candidate
        for x in command[1:]:
            # TODO: Is this hack good enough?
            result += ' ' + str(x)
        return result

    def unparseCommandList(self, commands: List[commands.Command]) -> str:
        """
        Takes a list of commands and returns a string that would parse
        into them using `parseOneEffectArg`. The result contains
        newlines and indentation to make it easier to read.

        For example:

        >>> pf = ParseFormat()
        >>> pf.unparseCommandList(
        ...     [commands.command('val', '5'), commands.command('pop')]
        ... )
        '{\\n  val 5;\\n  pop;\\n}'
        """
        result = self.formatDict[Lexeme.openCurly]
        for cmd in commands:
            result += f'\n  {self.unparseCommand(cmd)};'
        if len(commands) > 0:
            result += '\n'
        return result + self.formatDict[Lexeme.closeCurly]

    def parseCommandListFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0
    ) -> Tuple[List[commands.Command], int]:
        """
        Parses a command list from a list of lexed tokens, which must
        start with `Lexeme.openCurly`. Returns the parsed command list
        as a list of `commands.Command` objects, along with the end
        index of that command list (which will be the matching curly
        brace.
        """
        end = self.matchingBrace(
            tokens,
            start,
            Lexeme.openCurly,
            Lexeme.closeCurly
        )
        parts = list(
            findSeparatedParts(
                tokens,
                Lexeme.consequenceSeparator,
                start + 1,
                end - 1,
                Lexeme.openCurly,
                Lexeme.closeCurly,
            )
        )
        return (
            [
                self.parseCommandFromTokens(tokens, fromIndex, toIndex)
                for fromIndex, toIndex in parts
                if fromIndex <= toIndex  # ignore empty parts
            ],
            end
        )

    def parseOneEffectArg(
        self,
        tokens: LexedTokens,
        start: int = 0,
        limit: Optional[int] = None
    ) -> Tuple[
        Union[
            base.Capability,  # covers 'str' possibility
            Tuple[base.Token, base.TokenCount],
            Tuple[Literal['skill'], base.Skill, base.Level],
            Tuple[base.MechanismSpecifier, base.MechanismState],
            base.DecisionSpecifier,
            base.DecisionID,
            Literal[Lexeme.inCommon, Lexeme.isHidden],
            Tuple[Literal[Lexeme.sepOrDelay, Lexeme.effectCharges], int],
            List[commands.Command]
        ],
        int
    ]:
        """
        Looks at tokens starting at the specified position and parses
        one or more of them as an effect argument (an argument that
        could be given to `base.effect`). Looks at various key `Lexeme`s
        to determine which type to use.

        Items in the tokens list beyond the specified limit will not be
        considered, even when they in theory could be grouped with items
        up to the limit into a more complex argument.

        For example:

        >>> pf = ParseFormat()
        >>> pf.parseOneEffectArg(['hi'])
        ('hi', 0)
        >>> pf.parseOneEffectArg(['hi'], 1)
        Traceback (most recent call last):
        ...
        IndexError...
        >>> pf.parseOneEffectArg(['hi', 'bye'])
        ('hi', 0)
        >>> pf.parseOneEffectArg(['hi', 'bye'], 1)
        ('bye', 1)
        >>> pf.parseOneEffectArg(
        ...     ['gate', Lexeme.mechanismSeparator, 'open'],
        ...     0
        ... )
        ((MechanismSpecifier(domain=None, zone=None, decision=None,\
 name='gate'), 'open'), 2)
        >>> pf.parseOneEffectArg(
        ...     ['set', 'gate', Lexeme.mechanismSeparator, 'open'],
        ...     1
        ... )
        ((MechanismSpecifier(domain=None, zone=None, decision=None,\
 name='gate'), 'open'), 3)
        >>> pf.parseOneEffectArg(
        ...     ['gate', Lexeme.mechanismSeparator, 'open'],
        ...     1
        ... )
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseOneEffectArg(
        ...     ['gate', Lexeme.mechanismSeparator, 'open'],
        ...     2
        ... )
        ('open', 2)
        >>> pf.parseOneEffectArg(['gold', Lexeme.tokenCount, '10'], 0)
        (('gold', 10), 2)
        >>> pf.parseOneEffectArg(['gold', Lexeme.tokenCount, 'ten'], 0)
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseOneEffectArg([Lexeme.inCommon], 0)
        (<Lexeme.inCommon: ...>, 0)
        >>> pf.parseOneEffectArg([Lexeme.isHidden], 0)
        (<Lexeme.isHidden: ...>, 0)
        >>> pf.parseOneEffectArg([Lexeme.tokenCount, '3'], 0)
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseOneEffectArg([Lexeme.effectCharges, '3'], 0)
        ((<Lexeme.effectCharges: ...>, 3), 1)
        >>> pf.parseOneEffectArg([Lexeme.tokenCount, 3], 0)  # int is a lexeme
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseOneEffectArg([Lexeme.sepOrDelay, '-2'], 0)
        ((<Lexeme.sepOrDelay: ...>, -2), 1)
        >>> pf.parseOneEffectArg(['agility', Lexeme.skillLevel, '3'], 0)
        (('skill', 'agility', 3), 2)
        >>> pf.parseOneEffectArg(
        ...     [
        ...         'main',
        ...         Lexeme.domainSeparator,
        ...         'zone',
        ...         Lexeme.zoneSeparator,
        ...         'decision',
        ...         Lexeme.zoneSeparator,
        ...         'compass',
        ...         Lexeme.mechanismSeparator,
        ...         'north',
        ...         'south',
        ...         'east',
        ...         'west'
        ...     ],
        ...     0
        ... )
        ((MechanismSpecifier(domain='main', zone='zone',\
 decision='decision', name='compass'), 'north'), 8)
        >>> pf.parseOneEffectArg(
        ...     [
        ...         'before',
        ...         'main',
        ...         Lexeme.domainSeparator,
        ...         'zone',
        ...         Lexeme.zoneSeparator,
        ...         'decision',
        ...         Lexeme.zoneSeparator,
        ...         'compass',
        ...         'north',
        ...         'south',
        ...         'east',
        ...         'west'
        ...     ],
        ...     1
        ... )  # a mechanism specifier without a state will become a
        ...    # decision specifier
        (DecisionSpecifier(domain='main', zone='zone',\
 name='decision'), 5)
        >>> tokens = [
        ...     'set',
        ...     'main',
        ...     Lexeme.domainSeparator,
        ...     'zone',
        ...     Lexeme.zoneSeparator,
        ...     'compass',
        ...     'north',
        ...     'bounce',
        ... ]
        >>> pf.parseOneEffectArg(tokens, 0)
        ('set', 0)
        >>> pf.parseDecisionSpecifierFromTokens(tokens, 1)
        (DecisionSpecifier(domain='main', zone='zone', name='compass'), 5)
        >>> pf.parseOneEffectArg(tokens, 1)
        (DecisionSpecifier(domain='main', zone='zone', name='compass'), 5)
        >>> pf.parseOneEffectArg(tokens, 6)
        ('north', 6)
        >>> pf.parseOneEffectArg(tokens, 7)
        ('bounce', 7)
        >>> pf.parseOneEffectArg(
        ...     [
        ...         "fort", Lexeme.zoneSeparator, "gate",
        ...             Lexeme.mechanismSeparator, "open",
        ...     ],
        ...     0
        ... )
        ((MechanismSpecifier(domain=None, zone=None, decision='fort',\
 name='gate'), 'open'), 4)
        >>> pf.parseOneEffectArg(
        ...     [Lexeme.openCurly, 'val', '5', Lexeme.closeCurly],
        ...     0
        ... ) == ([commands.command('val', '5')], 3)
        True
        >>> a = [
        ...     Lexeme.openCurly, 'val', '5', Lexeme.closeCurly,
        ...     Lexeme.openCurly, 'append', Lexeme.consequenceSeparator,
        ...     'pop', Lexeme.closeCurly
        ... ]
        >>> cl = [
        ...     [commands.command('val', '5')],
        ...     [commands.command('append'), commands.command('pop')]
        ... ]
        >>> pf.parseOneEffectArg(a, 0) == (cl[0], 3)
        True
        >>> pf.parseOneEffectArg(a, 4) == (cl[1], 8)
        True
        >>> pf.parseOneEffectArg(a, 1)
        ('val', 1)
        >>> pf.parseOneEffectArg(a, 2)
        ('5', 2)
        >>> pf.parseOneEffectArg(a, 3)
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        """
        start, limit, nTokens = normalizeEnds(
            tokens,
            start,
            limit if limit is not None else -1
        )
        if nTokens == 0:
            raise ParseError("No effect arguments available.")

        first = tokens[start]

        if nTokens == 1:
            if first in (Lexeme.inCommon, Lexeme.isHidden):
                return (first, start)
            elif not isinstance(first, str):
                raise ParseError(
                    f"Only one token and it's a special character"
                    f" ({first} = {repr(self.formatDict[first])})"
                )
            else:
                return (cast(base.Capability, first), start)

        assert (nTokens > 1)

        second = tokens[start + 1]

        # Command lists start with an open curly brace and effect
        # modifiers start with a Lexme, but nothing else may
        if first == Lexeme.openCurly:
            return self.parseCommandListFromTokens(tokens, start)
        elif first in (Lexeme.inCommon, Lexeme.isHidden):
            return (first, start)
        elif first in (Lexeme.sepOrDelay, Lexeme.effectCharges):
            if not isinstance(second, str):
                raise ParseError(
                    f"Token following a modifier that needs a count"
                    f" must be a string in tokens:"
                    f"\n{tokens[start:limit or len(tokens)]}"
                )
            try:
                val = int(second)
            except ValueError:
                raise ParseError(
                    f"Token following a modifier that needs a count"
                    f" must be convertible to an int:"
                    f"\n{tokens[start:limit or len(tokens)]}"
                )

            first = cast(
                Literal[Lexeme.sepOrDelay, Lexeme.effectCharges],
                first
            )
            return ((first, val), start + 1)
        elif not isinstance(first, str):
            raise ParseError(
                f"First token must be a string unless it's a modifier"
                f" lexeme or command/reversion-set opener. Got:"
                f"\n{tokens[start:limit or len(tokens)]}"
            )

        # If we have two strings in a row, then the first is our parsed
        # value alone and we'll parse the second separately.
        if isinstance(second, str):
            return (first, start)
        elif second in (Lexeme.inCommon, Lexeme.isHidden):
            return (first, start)

        # Must have at least 3 tokens at this point, or else we need to
        # have the inCommon or isHidden lexeme second.
        if nTokens < 3:
            return (first, start)

        third = tokens[start + 2]
        if not isinstance(third, str):
            return (first, start)

        second = cast(Lexeme, second)
        third = cast(str, third)

        if second in (Lexeme.tokenCount, Lexeme.skillLevel):
            try:
                num = int(third)
            except ValueError:
                raise ParseError(
                    f"Invalid effect tokens: count for Tokens or level"
                    f" for Skill must be convertible to an integer."
                    f"\n{tokens[start:limit + 1]}"
                )
            if second == Lexeme.tokenCount:
                return ((first, num), start + 2)  # token/count pair
            else:
                return (('skill', first, num), start + 2)  # token/count pair

        elif second == Lexeme.mechanismSeparator:  # bare mechanism
            return (
                (
                    base.MechanismSpecifier(
                        domain=None,
                        zone=None,
                        decision=None,
                        name=first
                    ),
                    third
                ),
                start + 2
            )

        elif second in (Lexeme.domainSeparator, Lexeme.zoneSeparator):
            try:
                mSpec, mEnd = self.parseMechanismSpecifierFromTokens(
                    tokens,
                    start
                )  # works whether it's a mechanism or decision specifier...
            except ParseError:
                return self.parseDecisionSpecifierFromTokens(tokens, start)
            if mEnd + 2 > limit:
                # No room for following mechanism separator + state
                return self.parseDecisionSpecifierFromTokens(tokens, start)
            sep = tokens[mEnd + 1]
            after = tokens[mEnd + 2]
            if sep == Lexeme.mechanismSeparator:
                if not isinstance(after, str):
                    raise ParseError(
                        f"Mechanism separator not followed by state:"
                        f"\n{tokens[start]}"
                    )
                return ((mSpec, after), mEnd + 2)
            else:
                # No mechanism separator afterwards
                return self.parseDecisionSpecifierFromTokens(tokens, start)

        else:  # unrecognized as a longer combo
            return (first, start)

    def coalesceEffectArgs(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> Tuple[
        List[  # List of effect args
            Union[
                base.Capability,  # covers 'str' possibility
                Tuple[base.Token, base.TokenCount],
                Tuple[Literal['skill'], base.Skill, base.Level],
                Tuple[base.MechanismSpecifier, base.MechanismState],
                base.DecisionSpecifier,
                List[commands.Command],
                Set[str]
            ]
        ],
        Tuple[  # Slots for modifiers: common/hidden/charges/delay
            Optional[bool],
            Optional[bool],
            Optional[int],
            Optional[int],
        ]
    ]:
        """
        Given a region of a lexed tokens list which contains one or more
        effect arguments, combines token sequences representing things
        like capabilities, mechanism states, token counts, and skill
        levels, representing these using the tuples that would be passed
        to `base.effect`. Returns a tuple with two elements:

        - First, a list that contains several different kinds of
            objects, each of which is distinguishable by its type or
            part of its value.
        - Next, a tuple with four entires for common, hidden, charges,
            and/or delay values based on the presence of modifier
            sequences. Any or all of these may be `None` if the relevant
            modifier was not present (the usual case).

        For example:

        >>> pf = ParseFormat()
        >>> pf.coalesceEffectArgs(["jump"])
        (['jump'], (None, None, None, None))
        >>> pf.coalesceEffectArgs(["coin", Lexeme.tokenCount, "3", "fly"])
        ([('coin', 3), 'fly'], (None, None, None, None))
        >>> pf.coalesceEffectArgs(
        ...     [
        ...         "fort", Lexeme.zoneSeparator, "gate",
        ...             Lexeme.mechanismSeparator, "open"
        ...     ]
        ... )
        ([(MechanismSpecifier(domain=None, zone=None, decision='fort',\
 name='gate'), 'open')], (None, None, None, None))
        >>> pf.coalesceEffectArgs(
        ...     [
        ...         "main", Lexeme.domainSeparator, "cliff"
        ...     ]
        ... )
        ([DecisionSpecifier(domain='main', zone=None, name='cliff')],\
 (None, None, None, None))
        >>> pf.coalesceEffectArgs(
        ...     [
        ...         "door", Lexeme.mechanismSeparator, "open"
        ...     ]
        ... )
        ([(MechanismSpecifier(domain=None, zone=None, decision=None,\
 name='door'), 'open')], (None, None, None, None))
        >>> pf.coalesceEffectArgs(
        ...     [
        ...         "fort", Lexeme.zoneSeparator, "gate",
        ...             Lexeme.mechanismSeparator, "open",
        ...         "canJump",
        ...         "coins", Lexeme.tokenCount, "3",
        ...         Lexeme.inCommon,
        ...         "agility", Lexeme.skillLevel, "-1",
        ...         Lexeme.sepOrDelay, "0",
        ...         "main", Lexeme.domainSeparator, "cliff"
        ...     ]
        ... )
        ([(MechanismSpecifier(domain=None, zone=None, decision='fort',\
 name='gate'), 'open'), 'canJump', ('coins', 3), ('skill', 'agility', -1),\
 DecisionSpecifier(domain='main', zone=None, name='cliff')],\
 (True, None, None, 0))
        >>> pf.coalesceEffectArgs(["bounce", Lexeme.isHidden])
        (['bounce'], (None, True, None, None))
        >>> pf.coalesceEffectArgs(
        ...     ["goto", "3", Lexeme.inCommon, Lexeme.isHidden]
        ... )
        (['goto', '3'], (True, True, None, None))
        """
        start, end, nTokens = normalizeEnds(tokens, start, end)
        where = start
        result: List[  # List of effect args
            Union[
                base.Capability,  # covers 'str' possibility
                Tuple[base.Token, base.TokenCount],
                Tuple[Literal['skill'], base.Skill, base.Level],
                Tuple[base.MechanismSpecifier, base.MechanismState],
                base.DecisionSpecifier,
                List[commands.Command],
                Set[str]
            ]
        ] = []
        inCommon: Optional[bool] = None
        isHidden: Optional[bool] = None
        charges: Optional[int] = None
        delay: Optional[int] = None
        while where <= end:
            following, thisEnd = self.parseOneEffectArg(tokens, where, end)
            if following == Lexeme.inCommon:
                if inCommon is not None:
                    raise ParseError(
                        f"In-common effect modifier specified more than"
                        f" once in effect args:"
                        f"\n{tokens[start:end + 1]}"
                    )
                inCommon = True
            elif following == Lexeme.isHidden:
                if isHidden is not None:
                    raise ParseError(
                        f"Is-hidden effect modifier specified more than"
                        f" once in effect args:"
                        f"\n{tokens[start:end + 1]}"
                    )
                isHidden = True
            elif (
                isinstance(following, tuple)
            and len(following) == 2
            and following[0] in (Lexeme.effectCharges, Lexeme.sepOrDelay)
            and isinstance(following[1], int)
            ):
                if following[0] == Lexeme.effectCharges:
                    if charges is not None:
                        raise ParseError(
                            f"Charges effect modifier specified more than"
                            f" once in effect args:"
                            f"\n{tokens[start:end + 1]}"
                        )
                    charges = following[1]
                else:
                    if delay is not None:
                        raise ParseError(
                            f"Delay effect modifier specified more than"
                            f" once in effect args:"
                            f"\n{tokens[start:end + 1]}"
                        )
                    delay = following[1]
            elif (
                    isinstance(following, base.Capability)
                 or (
                    isinstance(following, tuple)
                and len(following) == 2
                and isinstance(following[0], base.Token)
                and isinstance(following[1], base.TokenCount)
                ) or (
                    isinstance(following, tuple)
                and len(following) == 3
                and following[0] == 'skill'
                and isinstance(following[1], base.Skill)
                and isinstance(following[2], base.Level)
                ) or (
                    isinstance(following, tuple)
                and len(following) == 2
                and isinstance(following[0], base.MechanismSpecifier)
                and isinstance(following[1], base.MechanismState)
                ) or (
                    isinstance(following, base.DecisionSpecifier)
                ) or (
                    isinstance(following, list)
                and all(isinstance(item, tuple) for item in following)
                    # TODO: Stricter command list check here?
                ) or (
                    isinstance(following, set)
                and all(isinstance(item, str) for item in following)
                )
            ):
                result.append(following)
            else:
                raise ParseError(f"Invalid coalesced argument: {following}")
            where = thisEnd + 1

        return (result, (inCommon, isHidden, charges, delay))

    def parseEffectFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> base.Effect:
        """
        Given a region of a list of lexed tokens specifying an effect,
        returns the `Effect` object that those tokens specify.
        """
        start, end, nTokens = normalizeEnds(tokens, start, end)

        # Check for empty list
        if nTokens == 0:
            raise ParseError(
                "Effect must include at least a type."
            )

        firstPart = tokens[start]

        if isinstance(firstPart, Lexeme):
            raise ParseError(
                f"First part of effect must be an effect type. Got"
                f" {firstPart} ({repr(self.formatDict[firstPart])})."
            )

        firstPart = cast(str, firstPart)

        # Get the effect type
        fType = self.effectType(firstPart)

        if fType is None:
            raise ParseError(
                f"Unrecognized effect type {firstPart!r}. Check the"
                f" EffectType entries in the effect names dictionary."
            )

        if start + 1 > end:  # No tokens left: set empty args
            groupedArgs: List[
                Union[
                    base.Capability,  # covers 'str' possibility
                    Tuple[base.Token, base.TokenCount],
                    Tuple[Literal['skill'], base.Skill, base.Level],
                    Tuple[base.MechanismSpecifier, base.MechanismState],
                    base.DecisionSpecifier,
                    List[commands.Command],
                    Set[str]
                ]
            ] = []
            modifiers: Tuple[
                Optional[bool],
                Optional[bool],
                Optional[int],
                Optional[int]
            ] = (None, None, None, None)
        else:  # Coalesce remaining tokens if there are any
            groupedArgs, modifiers = self.coalesceEffectArgs(
                tokens,
                start + 1,
                end
            )

        # Set up arguments for base.effect and handle modifiers first
        args: Dict[
            str,
            Union[
                None,
                base.ContextSpecifier,
                base.Capability,
                Tuple[base.Token, base.TokenCount],
                Tuple[Literal['skill'], base.Skill, base.Level],
                Tuple[base.MechanismSpecifier, base.MechanismState],
                Tuple[base.MechanismSpecifier, List[base.MechanismState]],
                List[base.Capability],
                base.AnyDecisionSpecifier,
                Tuple[base.AnyDecisionSpecifier, base.FocalPointName],
                bool,
                int,
                base.SaveSlot,
                Tuple[base.SaveSlot, Set[str]]
            ]
        ] = {}
        if modifiers[0]:
            args['applyTo'] = 'common'
        if modifiers[1]:
            args['hidden'] = True
        else:
            args['hidden'] = False
        if modifiers[2] is not None:
            args['charges'] = modifiers[2]
        if modifiers[3] is not None:
            args['delay'] = modifiers[3]

        # Now handle the main effect-type-based argument
        if fType in ("gain", "lose"):
            if len(groupedArgs) != 1:
                raise ParseError(
                    f"'{fType}' effect must have exactly one grouped"
                    f" argument (got {len(groupedArgs)}:\n{groupedArgs}"
                )
            thing = groupedArgs[0]
            if isinstance(thing, tuple):
                if len(thing) == 2:
                    if (
                        not isinstance(thing[0], base.Token)
                     or not isinstance(thing[1], base.TokenCount)
                    ):
                        raise ParseError(
                            f"'{fType}' effect grouped arg pair must be a"
                            f" (token, amount) pair. Got:\n{thing}"
                        )
                elif len(thing) == 3:
                    if (
                        thing[0] != 'skill'
                     or not isinstance(thing[1], base.Skill)
                     or not isinstance(thing[2], base.Level)
                    ):
                        raise ParseError(
                            f"'{fType}' effect grouped arg pair must be a"
                            f" (token, amount) pair. Got:\n{thing}"
                        )
                else:
                    raise ParseError(
                        f"'{fType}' effect grouped arg tuple must have"
                        f" length 2 or 3. Got (length {len(thing)}):\n{thing}"
                    )
            elif not isinstance(thing, base.Capability):
                raise ParseError(
                    f"'{fType}' effect grouped arg must be a capability"
                    f" or a (token, amount) tuple. Got:\n{thing}"
                )
            args[fType] = thing
            return base.effect(**args)  # type:ignore

        elif fType == "set":
            if len(groupedArgs) != 1:
                raise ParseError(
                    f"'{fType}' effect must have exactly one grouped"
                    f" argument (got {len(groupedArgs)}:\n{groupedArgs}"
                )
            setVal = groupedArgs[0]
            if not isinstance(
                setVal,
                tuple
            ):
                raise ParseError(
                    f"'{fType}' effect grouped arg must be a tuple. Got:"
                    f"\n{setVal}"
                )
            if len(setVal) == 2:
                setWhat, setTo = setVal
                if (
                    isinstance(setWhat, base.Token)
                and isinstance(setTo, base.TokenCount)
                ) or (
                    isinstance(setWhat, base.MechanismSpecifier)
                and isinstance(setTo, base.MechanismState)
                ):
                    args[fType] = setVal
                    return base.effect(**args)  # type:ignore
                else:
                    raise ParseError(
                        f"Invalid '{fType}' effect grouped args:"
                        f"\n{groupedArgs}"
                    )
            elif len(setVal) == 3:
                indicator, whichSkill, setTo = setVal
                if (
                    indicator == 'skill'
                and isinstance(whichSkill, base.Skill)
                and isinstance(setTo, base.Level)
                ):
                    args[fType] = setVal
                    return base.effect(**args)  # type:ignore
                else:
                    raise ParseError(
                        f"Invalid '{fType}' effect grouped args (not a"
                        f" skill):\n{groupedArgs}"
                    )
            else:
                raise ParseError(
                    f"Invalid '{fType}' effect grouped args (wrong"
                    f" length tuple):\n{groupedArgs}"
                )

        elif fType == "toggle":
            if len(groupedArgs) == 0:
                raise ParseError(
                    f"'{fType}' effect must have at least one grouped"
                    f" argument. Got:\n{groupedArgs}"
                )
            if (
                isinstance(groupedArgs[0], tuple)
            and len(groupedArgs[0]) == 2
            and isinstance(groupedArgs[0][0], base.MechanismSpecifier)
            and isinstance(groupedArgs[0][1], base.MechanismState)
            and all(
                    isinstance(a, base.MechanismState)
                    for a in groupedArgs[1:]
                )
            ):  # a mechanism toggle
                args[fType] = (
                    groupedArgs[0][0],
                    cast(
                        List[base.MechanismState],
                        [groupedArgs[0][1]] + groupedArgs[1:]
                    )
                )
                return base.effect(**args)  # type:ignore
            elif all(isinstance(a, base.Capability) for a in groupedArgs):
                # a capability toggle
                args[fType] = cast(List[base.Capability], groupedArgs)
                return base.effect(**args)  # type:ignore
            else:
                raise ParseError(
                    f"Invalid arguments for '{fType}' effect. Got:"
                    f"\n{groupedArgs}"
                )

        elif fType in ("bounce", "deactivate"):
            if len(groupedArgs) != 0:
                raise ParseError(
                    f"'{fType}' effect may not include any"
                    f" arguments. Got {len(groupedArgs)}):"
                    f"\n{groupedArgs}"
                )
            args[fType] = True
            return base.effect(**args)  # type:ignore

        elif fType == "follow":
            if len(groupedArgs) != 1:
                raise ParseError(
                    f"'{fType}' effect must include exactly one"
                    f" argument. Got {len(groupedArgs)}):"
                    f"\n{groupedArgs}"
                )

            transition = groupedArgs[0]
            if not isinstance(transition, base.Transition):
                raise ParseError(
                    f"Invalid argument for '{fType}' effect. Needed a"
                    f" transition but got:\n{groupedArgs}"
                )
            args[fType] = transition
            return base.effect(**args)  # type:ignore

        elif fType == "edit":
            if len(groupedArgs) == 0:
                raise ParseError(
                    "An 'edit' effect requires at least one argument."
                )
            for i, arg in enumerate(groupedArgs):
                if not isinstance(arg, list):
                    raise ParseError(
                        f"'edit' effect argument {i} is not a sub-list:"
                        f"\n  {arg!r}"
                        f"\nAmong arguments:"
                        f"\n  {groupedArgs}"
                    )
                for j, cmd in enumerate(arg):
                    if not isinstance(cmd, tuple):
                        raise ParseError(
                            f"'edit' effect argument {i} contains"
                            f" non-tuple part {j}:"
                            f"\n  {cmd!r}"
                            f"\nAmong arguments:"
                            f"\n  {groupedArgs}"
                        )

            args[fType] = groupedArgs  # type:ignore
            return base.effect(**args)  # type:ignore

        elif fType == "goto":
            if len(groupedArgs) not in (1, 2):
                raise ParseError(
                    f"A 'goto' effect must include either one or two"
                    f" grouped arguments. Got {len(groupedArgs)}:"
                    f"\n{groupedArgs}"
                )

            first = groupedArgs[0]
            if not isinstance(
                first,
                (base.DecisionName, base.DecisionSpecifier)
            ):
                raise ParseError(
                    f"'{fType}' effect must first specify a destination"
                    f" decision. Got:\n{groupedArgs}"
                )

            # Check if it's really a decision ID
            dSpec: base.AnyDecisionSpecifier
            if isinstance(first, base.DecisionName):
                try:
                    dSpec = int(first)
                except ValueError:
                    dSpec = first
            else:
                dSpec = first

            if len(groupedArgs) == 2:
                second = groupedArgs[1]
                if not isinstance(second, base.FocalPointName):
                    raise ParseError(
                        f"'{fType}' effect must have a focal point name"
                        f" if it has a second part. Got:\n{groupedArgs}"
                    )
                args[fType] = (dSpec, second)
            else:
                args[fType] = dSpec

            return base.effect(**args)  # type:ignore

        elif fType == "save":
            if len(groupedArgs) not in (0, 1):
                raise ParseError(
                    f"'{fType}' effect must include exactly zero or one"
                    f" argument(s). Got {len(groupedArgs)}):"
                    f"\n{groupedArgs}"
                )

            if len(groupedArgs) == 1:
                slot = groupedArgs[0]
            else:
                slot = base.DEFAULT_SAVE_SLOT
            if not isinstance(slot, base.SaveSlot):
                raise ParseError(
                    f"Invalid argument for '{fType}' effect. Needed a"
                    f" save slot but got:\n{groupedArgs}"
                )
            args[fType] = slot
            return base.effect(**args)  # type:ignore

        else:
            raise ParseError(f"Invalid effect type: '{fType}'.")

    def parseEffect(self, effectStr: str) -> base.Effect:
        """
        Works like `parseEffectFromTokens` but starts with a raw string.
        For example:

        >>> pf = ParseFormat()
        >>> pf.parseEffect("gain jump") == base.effect(gain='jump')
        True
        >>> pf.parseEffect("set door:open") == base.effect(
        ...     set=(
        ...         base.MechanismSpecifier(None, None, None, 'door'),
        ...         'open'
        ...     )
        ... )
        True
        >>> pf.parseEffect("set coins*10") == base.effect(set=('coins', 10))
        True
        """
        return self.parseEffectFromTokens(self.lex(effectStr))

    def unparseEffect(self, effect: base.Effect) -> str:
        """
        The opposite of `parseEffect`; turns an effect back into a
        string reprensentation.

        For example:

        >>> pf = ParseFormat()
        >>> e = {
        ...     "type": "gain",
        ...     "applyTo": "active",
        ...     "value": "flight",
        ...     "delay": None,
        ...     "charges": None,
        ...     "hidden": False
        ... }
        >>> pf.unparseEffect(e)
        'gain flight'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> s = 'gain flight'
        >>> pf.unparseEffect(pf.parseEffect(s)) == s
        True
        >>> s2 = '  gain\\nflight'
        >>> pf.unparseEffect(pf.parseEffect(s2)) == s
        True
        >>> e = {
        ...     "type": "gain",
        ...     "applyTo": "active",
        ...     "value": ("gold", 5),
        ...     "delay": 1,
        ...     "charges": 2,
        ...     "hidden": False
        ... }
        >>> pf.unparseEffect(e)
        'gain gold*5 ,1 =2'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> e = {
        ...     "type": "set",
        ...     "applyTo": "active",
        ...     "value": (
        ...         base.MechanismSpecifier(None, None, None, "gears"),
        ...         "on"
        ...     ),
        ...     "delay": None,
        ...     "charges": 1,
        ...     "hidden": False
        ... }
        >>> pf.unparseEffect(e)
        'set gears:on =1'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> e = {
        ...     "type": "toggle",
        ...     "applyTo": "active",
        ...     "value": ["red", "blue"],
        ...     "delay": None,
        ...     "charges": None,
        ...     "hidden": False
        ... }
        >>> pf.unparseEffect(e)
        'toggle red blue'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> e = {
        ...     "type": "toggle",
        ...     "applyTo": "active",
        ...     "value": (
        ...         base.MechanismSpecifier(None, None, None, "switch"),
        ...         ["on", "off"]
        ...     ),
        ...     "delay": None,
        ...     "charges": None,
        ...     "hidden": False
        ... }
        >>> pf.unparseEffect(e)
        'toggle switch:on off'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> e = {
        ...     "type": "deactivate",
        ...     "applyTo": "active",
        ...     "value": None,
        ...     "delay": 2,
        ...     "charges": None,
        ...     "hidden": False
        ... }
        >>> pf.unparseEffect(e)
        'deactivate ,2'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> e = {
        ...     "type": "goto",
        ...     "applyTo": "common",
        ...     "value": 3,
        ...     "delay": None,
        ...     "charges": None,
        ...     "hidden": False
        ... }
        >>> pf.unparseEffect(e)
        'goto 3 +c'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> e = {
        ...     "type": "goto",
        ...     "applyTo": "common",
        ...     "value": 3,
        ...     "delay": None,
        ...     "charges": None,
        ...     "hidden": True
        ... }
        >>> pf.unparseEffect(e)
        'goto 3 +c +h'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> e = {
        ...     "type": "goto",
        ...     "applyTo": "active",
        ...     "value": 'home',
        ...     "delay": None,
        ...     "charges": None,
        ...     "hidden": False
        ... }
        >>> pf.unparseEffect(e)
        'goto home'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        >>> e = base.effect(edit=[
        ...     [
        ...         commands.command('val', '5'),
        ...         commands.command('empty', 'list'),
        ...         commands.command('append', '$_')
        ...     ],
        ...     [
        ...         commands.command('val', '11'),
        ...         commands.command('assign', 'var', '$_'),
        ...         commands.command('op', '+', '$var', '$var')
        ...     ],
        ... ])
        >>> pf.unparseEffect(e)
        'edit {\\n  val 5;\\n  empty list;\\n  append $_;\\n}\
 {\\n  val 11;\\n  assign var $_;\\n  op + $var $var;\\n}'
        >>> pf.parseEffect(pf.unparseEffect(e)) == e
        True
        """
        result: List[str] = []

        # Reverse the effect type into a marker
        eType = effect['type']
        for key, val in self.effectNames.items():
            if val == eType:
                if len(result) != 0:
                    raise ParseError(
                        f"Effect map contains multiple matching entries"
                        f"for effect type '{effect['type']}':"
                        f" '{result[0]}' and '{key}'"
                    )
                result.append(key)
                # Don't break 'cause we'd like to check uniqueness

        eVal = effect['value']
        if eType in ('gain', 'lose'):
            eVal = cast(Union[base.Capability, Tuple[base.Token, int]], eVal)
            if isinstance(eVal, str):  # a capability
                result.append(eVal)
            else:  # a token
                result.append(
                    eVal[0]
                  + self.formatDict[Lexeme.tokenCount]
                  + str(eVal[1])
                )
        elif eType == 'set':
            eVal = cast(
                # TODO: Add skill level setting here & elsewhere
                Union[
                    Tuple[base.Token, base.TokenCount],
                    Tuple[base.MechanismName, base.MechanismState]
                ],
                eVal
            )
            if len(eVal) != 2:
                raise ValueError(
                    f"'set' effect has non-length-2 value:"
                    f"\n  {repr(effect)}"
                )
            if isinstance(eVal[1], int):  # a token count
                result.append(eVal[0])
                result.append(self.formatDict[Lexeme.tokenCount])
                result.append(str(eVal[1]))
            else:  # a mechanism
                if isinstance(eVal[0], base.MechanismSpecifier):
                    mSpec = self.unparseMechanismSpecifier(eVal[0])
                else:
                    assert isinstance(eVal[0], base.MechanismName)
                    mSpec = eVal[0]
                result.append(
                    mSpec
                  + self.formatDict[Lexeme.mechanismSeparator]
                  + eVal[1]
                )
        elif eType == 'toggle':
            if isinstance(eVal, tuple):  # mechanism states
                tSpec, states = cast(
                    Tuple[
                        base.AnyMechanismSpecifier,
                        List[base.MechanismState]
                    ],
                    eVal
                )
                firstState = states[0]
                restStates = states[1:]
                if isinstance(tSpec, base.MechanismSpecifier):
                    mStr = self.unparseMechanismSpecifier(tSpec)
                else:
                    mStr = str(tSpec)
                result.append(
                    mStr
                  + self.formatDict[Lexeme.mechanismSeparator]
                  + firstState
                )
                result.extend(restStates)
            else:  # capabilities
                assert isinstance(eVal, list)
                eVal = cast(List[base.Capability], eVal)
                result.extend(eVal)
        elif eType in ('deactivate', 'bounce'):
            if eVal is not None:
                raise ValueError(
                    f"'{eType}' effect has non-None value:"
                    f"\n  {repr(effect)}"
                )
        elif eType == 'follow':
            eVal = cast(base.Token, eVal)
            result.append(eVal)
        elif eType == 'edit':
            eVal = cast(List[List[commands.Command]], eVal)
            if len(eVal) == 0:
                result[-1] = '{}'
            else:
                for cmdList in eVal:
                    result.append(
                        self.unparseCommandList(cmdList)
                    )
        elif eType == 'goto':
            if isinstance(eVal, base.DecisionSpecifier):
                result.append(self.unparseDecisionSpecifier(eVal))
            elif isinstance(eVal, (base.DecisionID, base.DecisionName)):
                result.append(str(eVal))
            elif (
                isinstance(eVal, tuple)
            and len(eVal) == 2
            and isinstance(eVal[1], base.FocalPointName)
            ):
                if isinstance(eVal[0], base.DecisionSpecifier):
                    result.append(self.unparseDecisionSpecifier(eVal[0]))
                else:
                    result.append(str(eVal[0]))
                result.append(eVal[1])
            else:
                raise ValueError(
                    f"'{eType}' effect has invalid value {eVal}"
                )
        else:
            raise ValueError(
                f"Unrecognized effect type '{eType}' in effect:"
                f"\n  {repr(effect)}"
            )

        # Add modifier strings
        if effect['applyTo'] == 'common':
            result.append(self.formatDict[Lexeme.inCommon])

        if effect['hidden']:
            result.append(self.formatDict[Lexeme.isHidden])

        dVal = effect['delay']
        if dVal is not None:
            result.append(
                self.formatDict[Lexeme.sepOrDelay] + str(dVal)
            )

        cVal = effect['charges']
        if cVal is not None:
            result.append(
                self.formatDict[Lexeme.effectCharges] + str(cVal)
            )

        joined = ''
        before = False
        for r in result:
            if (
                r.startswith(' ')
             or r.startswith('\n')
             or r.endswith(' ')
             or r.endswith('\n')
            ):
                joined += r
                before = False
            else:
                joined += (' ' if before else '') + r
                before = True
        return joined

    def parseDecisionSpecifierFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0
    ) -> Tuple[Union[base.DecisionSpecifier, int], int]:
        """
        Parses a decision specifier starting at the specified position
        in the given tokens list. No ending position is specified, but
        instead this function returns a tuple containing the parsed
        `base.DecisionSpecifier` along with an index in the tokens list
        where the end of the specifier was found.

        For example:

        >>> pf = ParseFormat()
        >>> pf.parseDecisionSpecifierFromTokens(['m'])
        (DecisionSpecifier(domain=None, zone=None, name='m'), 0)
        >>> pf.parseDecisionSpecifierFromTokens(['12'])  # ID specifier
        (12, 0)
        >>> pf.parseDecisionSpecifierFromTokens(['a', 'm'])
        (DecisionSpecifier(domain=None, zone=None, name='a'), 0)
        >>> pf.parseDecisionSpecifierFromTokens(['a', 'm'], 1)
        (DecisionSpecifier(domain=None, zone=None, name='m'), 1)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     ['a', Lexeme.domainSeparator, 'm']
        ... )
        (DecisionSpecifier(domain='a', zone=None, name='m'), 2)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'm']
        ... )
        (DecisionSpecifier(domain=None, zone='a', name='m'), 2)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'b', Lexeme.zoneSeparator, 'm']
        ... )
        (DecisionSpecifier(domain=None, zone='a', name='b'), 2)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     ['a', Lexeme.domainSeparator, 'b', Lexeme.zoneSeparator, 'm']
        ... )
        (DecisionSpecifier(domain='a', zone='b', name='m'), 4)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'b', Lexeme.domainSeparator, 'm']
        ... )
        (DecisionSpecifier(domain=None, zone='a', name='b'), 2)
        >>> pf.parseDecisionSpecifierFromTokens(  # ID-style name w/ zone
        ...     ['a', Lexeme.zoneSeparator, '5'],
        ... )
        Traceback (most recent call last):
        ...
        exploration.base.InvalidDecisionSpecifierError...
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     ['d', Lexeme.domainSeparator, '123']
        ... )
        Traceback (most recent call last):
        ...
        exploration.base.InvalidDecisionSpecifierError...
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'b', Lexeme.domainSeparator, 'm'],
        ...     1
        ... )
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'b', Lexeme.domainSeparator, 'm'],
        ...     2
        ... )
        (DecisionSpecifier(domain='b', zone=None, name='m'), 4)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     [
        ...         'a',
        ...         Lexeme.domainSeparator,
        ...         'b',
        ...         Lexeme.zoneSeparator,
        ...         'c',
        ...         Lexeme.zoneSeparator,
        ...         'm'
        ...     ]
        ... )
        (DecisionSpecifier(domain='a', zone='b', name='c'), 4)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     [
        ...         'a',
        ...         Lexeme.domainSeparator,
        ...         'b',
        ...         Lexeme.zoneSeparator,
        ...         'c',
        ...         Lexeme.zoneSeparator,
        ...         'm'
        ...     ],
        ...     2
        ... )
        (DecisionSpecifier(domain=None, zone='b', name='c'), 4)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     [
        ...         'a',
        ...         Lexeme.domainSeparator,
        ...         'b',
        ...         Lexeme.zoneSeparator,
        ...         'c',
        ...         Lexeme.zoneSeparator,
        ...         'm'
        ...     ],
        ...     4
        ... )
        (DecisionSpecifier(domain=None, zone='c', name='m'), 6)
        >>> pf.parseDecisionSpecifierFromTokens(
        ...     [
        ...         'set',
        ...         'main',
        ...         Lexeme.domainSeparator,
        ...         'zone',
        ...         Lexeme.zoneSeparator,
        ...         'compass',
        ...         'north',
        ...         'bounce',
        ...     ],
        ...     1
        ... )
        (DecisionSpecifier(domain='main', zone='zone', name='compass'), 5)
        """
        # Check bounds & normalize start index
        nTokens = len(tokens)
        if start < -nTokens:
            raise IndexError(
                f"Invalid start index {start} for {nTokens} tokens (too"
                f" negative)."
            )
        elif start >= nTokens:
            raise IndexError(
                f"Invalid start index {start} for {nTokens} tokens (too"
                f" big)."
            )
        elif start < 0:
            start = nTokens + start

        assert (start < nTokens)

        first = tokens[start]
        if not isinstance(first, str):
            raise ParseError(
                f"Invalid domain specifier (must start with a name or"
                f" id; got: {first} = {self.formatDict[first]})."
            )

        ds = base.DecisionSpecifier(None, None, first)
        result = (base.idOrDecisionSpecifier(ds), start)

        domain = None
        zoneOrDecision = None

        if start + 1 >= nTokens:  # at end of tokens
            return result

        firstSep = tokens[start + 1]
        if firstSep == Lexeme.domainSeparator:
            domain = first
        elif firstSep == Lexeme.zoneSeparator:
            zoneOrDecision = first
        else:
            return result

        if start + 2 >= nTokens:
            return result

        second = tokens[start + 2]
        if isinstance(second, Lexeme):
            return result

        ds = base.DecisionSpecifier(domain, zoneOrDecision, second)
        result = (base.idOrDecisionSpecifier(ds), start + 2)

        if start + 3 >= nTokens:
            return result

        secondSep = tokens[start + 3]
        if start + 4 >= nTokens:
            return result

        third = tokens[start + 4]
        if secondSep == Lexeme.zoneSeparator:
            if zoneOrDecision is not None:  # two in a row
                return result
            else:
                if not isinstance(third, base.DecisionName):
                    return result
                else:
                    zoneOrDecision = second
        else:
            return result

        if isinstance(third, Lexeme):
            return result

        ds = base.DecisionSpecifier(domain, zoneOrDecision, third)
        return (base.idOrDecisionSpecifier(ds), start + 4)

    def parseDecisionSpecifier(
        self,
        specString: str
    ) -> Union[base.DecisionID, base.DecisionSpecifier]:
        """
        Parses a full `DecisionSpecifier` from a single string. Can
        parse integer decision IDs in string form, and returns a
        `DecisionID` in that case, otherwise returns a
        `DecisionSpecifier`. Assumes that all int-convertible strings
        are decision IDs, so it cannot deal with feature names which are
        just numbers.

        For example:

        >>> pf = ParseFormat()
        >>> pf.parseDecisionSpecifier('example')
        DecisionSpecifier(domain=None, zone=None, name='example')
        >>> pf.parseDecisionSpecifier('outer::example')
        DecisionSpecifier(domain=None, zone='outer', name='example')
        >>> pf.parseDecisionSpecifier('domain//region::feature')
        DecisionSpecifier(domain='domain', zone='region', name='feature')
        >>> pf.parseDecisionSpecifier('123')
        123
        >>> pf.parseDecisionSpecifier('region::domain//feature')
        Traceback (most recent call last):
        ...
        exploration.base.InvalidDecisionSpecifierError...
        >>> pf.parseDecisionSpecifier('domain1//domain2//feature')
        Traceback (most recent call last):
        ...
        exploration.base.InvalidDecisionSpecifierError...
        >>> pf.parseDecisionSpecifier('domain//123')
        Traceback (most recent call last):
        ...
        exploration.base.InvalidDecisionSpecifierError...
        >>> pf.parseDecisionSpecifier('region::123')
        Traceback (most recent call last):
        ...
        exploration.base.InvalidDecisionSpecifierError...
        """
        try:
            return int(specString)
        except ValueError:
            tokens = self.lex(specString)
            result, end = self.parseDecisionSpecifierFromTokens(tokens)
            if end != len(tokens) - 1:
                raise base.InvalidDecisionSpecifierError(
                    f"Junk after end of decision specifier:"
                    f"\n{tokens[end + 1:]}"
                )
            return result

    def parseFeatureSpecifierFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        limit: int = -1
    ) -> Tuple[base.FeatureSpecifier, int]:
        """
        Parses a `FeatureSpecifier` starting from the specified part of
        a tokens list. Returns a tuple containing the feature specifier
        and the end position of the end of the feature specifier.

        Can parse integer feature IDs in string form, as well as nested
        feature specifiers and plain feature specifiers. Assumes that
        all int-convertible strings are feature IDs, so it cannot deal
        with feature names which are just numbers.

        For example:

        >>> pf = ParseFormat()
        >>> pf.parseFeatureSpecifierFromTokens(['example'])
        (FeatureSpecifier(domain=None, within=[], feature='example',\
 part=None), 0)
        >>> pf.parseFeatureSpecifierFromTokens(['example1', 'example2'], 1)
        (FeatureSpecifier(domain=None, within=[], feature='example2',\
 part=None), 1)
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'domain',
        ...         Lexeme.domainSeparator,
        ...         'region',
        ...         Lexeme.zoneSeparator,
        ...         'feature',
        ...         Lexeme.partSeparator,
        ...         'part'
        ...     ]
        ... )
        (FeatureSpecifier(domain='domain', within=['region'],\
 feature='feature', part='part'), 6)
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'outerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'midRegion',
        ...         Lexeme.zoneSeparator,
        ...         'innerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'feature'
        ...     ]
        ... )
        (FeatureSpecifier(domain=None, within=['outerRegion', 'midRegion',\
 'innerRegion'], feature='feature', part=None), 6)
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'outerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'midRegion',
        ...         Lexeme.zoneSeparator,
        ...         'innerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'feature'
        ...     ],
        ...     1
        ... )
        Traceback (most recent call last):
        ...
        exploration.parsing.InvalidFeatureSpecifierError...
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'outerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'midRegion',
        ...         Lexeme.zoneSeparator,
        ...         'innerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'feature'
        ...     ],
        ...     2
        ... )
        (FeatureSpecifier(domain=None, within=['midRegion', 'innerRegion'],\
 feature='feature', part=None), 6)
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'outerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'feature',
        ...         Lexeme.domainSeparator,
        ...         'after',
        ...     ]
        ... )
        (FeatureSpecifier(domain=None, within=['outerRegion'],\
 feature='feature', part=None), 2)
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'outerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'feature',
        ...         Lexeme.domainSeparator,
        ...         'after',
        ...     ],
        ...     2
        ... )
        (FeatureSpecifier(domain='feature', within=[], feature='after',\
 part=None), 4)
        >>> # Including a limit:
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'outerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'midRegion',
        ...         Lexeme.zoneSeparator,
        ...         'feature',
        ...     ],
        ...     0,
        ...     2
        ... )
        (FeatureSpecifier(domain=None, within=['outerRegion'],\
 feature='midRegion', part=None), 2)
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'outerRegion',
        ...         Lexeme.zoneSeparator,
        ...         'midRegion',
        ...         Lexeme.zoneSeparator,
        ...         'feature',
        ...     ],
        ...     0,
        ...     0
        ... )
        (FeatureSpecifier(domain=None, within=[], feature='outerRegion',\
 part=None), 0)
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'region',
        ...         Lexeme.zoneSeparator,
        ...         Lexeme.zoneSeparator,
        ...         'feature',
        ...     ]
        ... )
        (FeatureSpecifier(domain=None, within=[], feature='region',\
 part=None), 0)
        """
        start, limit, nTokens = normalizeEnds(tokens, start, limit)

        if nTokens == 0:
            raise InvalidFeatureSpecifierError(
                "Can't parse a feature specifier from 0 tokens."
            )
        first = tokens[start]
        if isinstance(first, Lexeme):
            raise InvalidFeatureSpecifierError(
                f"Feature specifier can't begin with a special token."
                f"Got:\n{tokens[start:limit + 1]}"
            )

        if nTokens in (1, 2):
            # 2 tokens isn't enough for a second part
            fs = base.FeatureSpecifier(
                domain=None,
                within=[],
                feature=first,
                part=None
            )
            return (base.normalizeFeatureSpecifier(fs), start)

        firstSep = tokens[start + 1]
        secondPart = tokens[start + 2]

        if (
            firstSep not in (
                Lexeme.domainSeparator,
                Lexeme.zoneSeparator,
                Lexeme.partSeparator
            )
         or not isinstance(secondPart, str)
        ):
            # Following tokens won't work out
            fs = base.FeatureSpecifier(
                domain=None,
                within=[],
                feature=first,
                part=None
            )
            return (base.normalizeFeatureSpecifier(fs), start)

        if firstSep == Lexeme.domainSeparator:
            if start + 2 > limit:
                return (
                    base.FeatureSpecifier(
                        domain=first,
                        within=[],
                        feature=secondPart,
                        part=None
                    ),
                    start + 2
                )
            else:
                rest, restEnd = self.parseFeatureSpecifierFromTokens(
                    tokens,
                    start + 2,
                    limit
                )
                if rest.domain is not None:  # two domainSeparators in a row
                    fs = base.FeatureSpecifier(
                        domain=first,
                        within=[],
                        feature=rest.domain,
                        part=None
                    )
                    return (base.normalizeFeatureSpecifier(fs), start + 2)
                else:
                    fs = base.FeatureSpecifier(
                        domain=first,
                        within=rest.within,
                        feature=rest.feature,
                        part=rest.part
                    )
                    return (base.normalizeFeatureSpecifier(fs), restEnd)

        elif firstSep == Lexeme.zoneSeparator:
            if start + 2 > limit:
                fs = base.FeatureSpecifier(
                    domain=None,
                    within=[first],
                    feature=secondPart,
                    part=None
                )
                return (base.normalizeFeatureSpecifier(fs), start + 2)
            else:
                rest, restEnd = self.parseFeatureSpecifierFromTokens(
                    tokens,
                    start + 2,
                    limit
                )
                if rest.domain is not None:  # domain sep after zone sep
                    fs = base.FeatureSpecifier(
                        domain=None,
                        within=[first],
                        feature=rest.domain,
                        part=None
                    )
                    return (base.normalizeFeatureSpecifier(fs), start + 2)
                else:
                    within = [first]
                    within.extend(rest.within)
                    fs = base.FeatureSpecifier(
                        domain=None,
                        within=within,
                        feature=rest.feature,
                        part=rest.part
                    )
                    return (base.normalizeFeatureSpecifier(fs), restEnd)

        else:  # must be partSeparator
            fs = base.FeatureSpecifier(
                domain=None,
                within=[],
                feature=first,
                part=secondPart
            )
            return (base.normalizeFeatureSpecifier(fs), start + 2)

    def parseFeatureSpecifier(self, specString: str) -> base.FeatureSpecifier:
        """
        Parses a full `FeatureSpecifier` from a single string. See
        `parseFeatureSpecifierFromTokens`.

        >>> pf = ParseFormat()
        >>> pf.parseFeatureSpecifier('example')
        FeatureSpecifier(domain=None, within=[], feature='example', part=None)
        >>> pf.parseFeatureSpecifier('outer::example')
        FeatureSpecifier(domain=None, within=['outer'], feature='example',\
 part=None)
        >>> pf.parseFeatureSpecifier('example%%middle')
        FeatureSpecifier(domain=None, within=[], feature='example',\
 part='middle')
        >>> pf.parseFeatureSpecifier('domain//region::feature%%part')
        FeatureSpecifier(domain='domain', within=['region'],\
 feature='feature', part='part')
        >>> pf.parseFeatureSpecifier(
        ...     'outerRegion::midRegion::innerRegion::feature'
        ... )
        FeatureSpecifier(domain=None, within=['outerRegion', 'midRegion',\
 'innerRegion'], feature='feature', part=None)
        >>> pf.parseFeatureSpecifier('region::domain//feature')
        Traceback (most recent call last):
        ...
        exploration.parsing.InvalidFeatureSpecifierError...
        >>> pf.parseFeatureSpecifier('feature%%part1%%part2')
        Traceback (most recent call last):
        ...
        exploration.parsing.InvalidFeatureSpecifierError...
        >>> pf.parseFeatureSpecifier('domain1//domain2//feature')
        Traceback (most recent call last):
        ...
        exploration.parsing.InvalidFeatureSpecifierError...
        >>> # TODO: Issue warnings for these...
        >>> pf.parseFeatureSpecifier('domain//123')  # domain discarded
        FeatureSpecifier(domain=None, within=[], feature=123, part=None)
        >>> pf.parseFeatureSpecifier('region::123')  # zone discarded
        FeatureSpecifier(domain=None, within=[], feature=123, part=None)
        >>> pf.parseFeatureSpecifier('123%%part')
        FeatureSpecifier(domain=None, within=[], feature=123, part='part')
        """
        tokens = self.lex(specString)
        result, rEnd = self.parseFeatureSpecifierFromTokens(tokens)
        if rEnd != len(tokens) - 1:
            raise InvalidFeatureSpecifierError(
                f"Feature specifier has extra stuff at end:"
                f" {tokens[rEnd + 1:]}"
            )
        else:
            return result

    def normalizeFeatureSpecifier(
        self,
        spec: base.AnyFeatureSpecifier
    ) -> base.FeatureSpecifier:
        """
        Normalizes any kind of feature specifier into an official
        `FeatureSpecifier` tuple.

        For example:

        >>> pf = ParseFormat()
        >>> pf.normalizeFeatureSpecifier('town')
        FeatureSpecifier(domain=None, within=[], feature='town', part=None)
        >>> pf.normalizeFeatureSpecifier(5)
        FeatureSpecifier(domain=None, within=[], feature=5, part=None)
        >>> pf.parseFeatureSpecifierFromTokens(
        ...     [
        ...         'domain',
        ...         Lexeme.domainSeparator,
        ...         'region',
        ...         Lexeme.zoneSeparator,
        ...         'feature',
        ...         Lexeme.partSeparator,
        ...         'part'
        ...     ]
        ... )
        (FeatureSpecifier(domain='domain', within=['region'],\
 feature='feature', part='part'), 6)
        >>> pf.normalizeFeatureSpecifier('dom//one::two::three%%middle')
        FeatureSpecifier(domain='dom', within=['one', 'two'],\
 feature='three', part='middle')
        >>> pf.normalizeFeatureSpecifier(
        ...   base.FeatureSpecifier(None, ['region'], 'place', None)
        ... )
        FeatureSpecifier(domain=None, within=['region'], feature='place',\
 part=None)
        >>> fs = base.FeatureSpecifier(None, [], 'place', None)
        >>> ns = pf.normalizeFeatureSpecifier(fs)
        >>> ns is fs  # Doesn't create unnecessary clones
        True
        """
        if isinstance(spec, base.FeatureSpecifier):
            return spec
        elif isinstance(spec, base.FeatureID):
            return base.FeatureSpecifier(None, [], spec, None)
        elif isinstance(spec, str):
            return self.parseFeatureSpecifier(spec)
        else:
            raise TypeError(f"Invalid feature specifier type: '{type(spec)}'")

    def unparseChallenge(self, challenge: base.Challenge) -> str:
        """
        Turns a `base.Challenge` into a string that can be turned back
        into an equivalent challenge by `parseChallenge`. For example:

        >>> pf = ParseFormat()
        >>> c = base.challenge(
        ...     skills=base.BestSkill('brains', 'brawn'),
        ...     level=2,
        ...     success=[base.effect(set=('switch', 'on'))],
        ...     failure=[
        ...         base.effect(deactivate=True, delay=1),
        ...         base.effect(bounce=True)
        ...     ],
        ...     outcome=True
        ... )
        >>> r = pf.unparseChallenge(c)
        >>> r
        '<2>best(brains, brawn)>{set switch:on}{deactivate ,1; bounce}'
        >>> pf.parseChallenge(r) == c
        True
        >>> c2 = base.challenge(
        ...     skills=base.CombinedSkill(
        ...         -2,
        ...         base.ConditionalSkill(
        ...             base.ReqCapability('tough'),
        ...             base.BestSkill(1),
        ...             base.BestSkill(-1)
        ...         )
        ...     ),
        ...     level=-2,
        ...     success=[base.effect(gain='orb')],
        ...     failure=[],
        ...     outcome=None
        ... )
        >>> r2 = pf.unparseChallenge(c2)
        >>> r2
        '<-2>sum(-2, if(tough, best(1), best(-1))){gain orb}{}'
        >>> # TODO: let this parse through without BestSkills...
        >>> pf.parseChallenge(r2) == c2
        True
        """
        lt = self.formatDict[Lexeme.angleLeft]
        gt = self.formatDict[Lexeme.angleRight]
        result = (
            lt + str(challenge['level']) + gt
          + challenge['skills'].unparse()
        )
        if challenge['outcome'] is True:
            result += gt
        result += self.unparseConsequence(challenge['success'])
        if challenge['outcome'] is False:
            result += gt
        result += self.unparseConsequence(challenge['failure'])
        return result

    def unparseCondition(self, condition: base.Condition) -> str:
        """
        Given a `base.Condition` returns a string that would result in
        that condition if given to `parseCondition`. For example:

        >>> pf = ParseFormat()
        >>> c = base.condition(
        ...     condition=base.ReqAny([
        ...         base.ReqCapability('brawny'),
        ...         base.ReqNot(base.ReqTokens('weights', 3))
        ...     ]),
        ...     consequence=[base.effect(gain='power')]
        ... )
        >>> r = pf.unparseCondition(c)
        >>> r
        '??((brawny|!(weights*3))){gain power}{}'
        >>> pf.parseCondition(r) == c
        True
        """
        return (
            self.formatDict[Lexeme.doubleQuestionmark]
          + self.formatDict[Lexeme.openParen]
          + condition['condition'].unparse()
          + self.formatDict[Lexeme.closeParen]
          + self.unparseConsequence(condition['consequence'])
          + self.unparseConsequence(condition['alternative'])
        )

    def unparseConsequence(self, consequence: base.Consequence) -> str:
        """
        Given a `base.Consequence`, returns a string encoding of it,
        using the same format that `parseConsequence` will parse. Uses
        function-call-like syntax and curly braces to denote different
        sub-consequences. See also `SkillCombination.unparse` and
        `Requirement.unparse` For example:

        >>> pf = ParseFormat()
        >>> c = [base.effect(gain='one'), base.effect(lose='one')]
        >>> pf.unparseConsequence(c)
        '{gain one; lose one}'
        >>> c = [
        ...     base.challenge(
        ...         skills=base.BestSkill('brains', 'brawn'),
        ...         level=2,
        ...         success=[base.effect(set=('switch', 'on'))],
        ...         failure=[
        ...             base.effect(deactivate=True, delay=1),
        ...             base.effect(bounce=True)
        ...         ],
        ...         outcome=True
        ...     )
        ... ]
        >>> pf.unparseConsequence(c)
        '{<2>best(brains, brawn)>{set switch:on}{deactivate ,1; bounce}}'
        >>> c[0]['outcome'] = False
        >>> pf.unparseConsequence(c)
        '{<2>best(brains, brawn){set switch:on}>{deactivate ,1; bounce}}'
        >>> c[0]['outcome'] = None
        >>> pf.unparseConsequence(c)
        '{<2>best(brains, brawn){set switch:on}{deactivate ,1; bounce}}'
        >>> c = [
        ...     base.condition(
        ...         condition=base.ReqAny([
        ...             base.ReqCapability('brawny'),
        ...             base.ReqNot(base.ReqTokens('weights', 3))
        ...         ]),
        ...         consequence=[
        ...             base.challenge(
        ...                 skills=base.CombinedSkill('brains', 'brawn'),
        ...                 level=3,
        ...                 success=[base.effect(goto='home')],
        ...                 failure=[base.effect(bounce=True)],
        ...                 outcome=None
        ...             )
        ...         ]  # no alternative -> empty list
        ...     )
        ... ]
        >>> pf.unparseConsequence(c)
        '{??((brawny|!(weights*3))){\
<3>sum(brains, brawn){goto home}{bounce}}{}}'
        >>> c = [base.effect(gain='if(power){gain "mimic"}')]
        >>> # TODO: Make this work!
        >>> # pf.unparseConsequence(c)

        '{gain "if(power){gain \\\\"mimic\\\\"}"}'
        """
        result = self.formatDict[Lexeme.openCurly]
        for item in consequence:
            if 'skills' in item:  # a Challenge
                item = cast(base.Challenge, item)
                result += self.unparseChallenge(item)

            elif 'value' in item:  # an Effect
                item = cast(base.Effect, item)
                result += self.unparseEffect(item)

            elif 'condition' in item:  # a Condition
                item = cast(base.Condition, item)
                result += self.unparseCondition(item)

            else:  # bad dict
                raise TypeError(
                    f"Invalid consequence: items in the list must be"
                    f" Effects, Challenges, or Conditions (got a dictionary"
                    f" without 'skills', 'value', or 'condition' keys)."
                    f"\nGot item: {repr(item)}"
                )
            result += '; '

        if result.endswith('; '):
            result = result[:-2]

        return result + self.formatDict[Lexeme.closeCurly]

    def parseMechanismSpecifierFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0
    ) -> Tuple[base.MechanismSpecifier, int]:
        """
        Parses a mechanism specifier starting at the specified position
        in the given tokens list. No ending position is specified, but
        instead this function returns a tuple containing the parsed
        `base.MechanismSpecifier` along with an index in the tokens list
        where the end of the specifier was found.

        For example:

        >>> pf = ParseFormat()
        >>> pf.parseMechanismSpecifierFromTokens(['m'])
        (MechanismSpecifier(domain=None, zone=None, decision=None,\
 name='m'), 0)
        >>> pf.parseMechanismSpecifierFromTokens(['a', 'm'])
        (MechanismSpecifier(domain=None, zone=None, decision=None,\
 name='a'), 0)
        >>> pf.parseMechanismSpecifierFromTokens(['a', 'm'], 1)
        (MechanismSpecifier(domain=None, zone=None, decision=None,\
 name='m'), 1)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     ['a', Lexeme.domainSeparator, 'm']
        ... )
        (MechanismSpecifier(domain='a', zone=None, decision=None,\
 name='m'), 2)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'm']
        ... )
        (MechanismSpecifier(domain=None, zone=None, decision='a',\
 name='m'), 2)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'b', Lexeme.zoneSeparator, 'm']
        ... )
        (MechanismSpecifier(domain=None, zone='a', decision='b',\
 name='m'), 4)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     ['a', Lexeme.domainSeparator, 'b', Lexeme.zoneSeparator, 'm']
        ... )
        (MechanismSpecifier(domain='a', zone=None, decision='b',\
 name='m'), 4)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'b', Lexeme.domainSeparator, 'm']
        ... )
        (MechanismSpecifier(domain=None, zone=None, decision='a',\
 name='b'), 2)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'b', Lexeme.domainSeparator, 'm'],
        ...     1
        ... )
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     ['a', Lexeme.zoneSeparator, 'b', Lexeme.domainSeparator, 'm'],
        ...     2
        ... )
        (MechanismSpecifier(domain='b', zone=None, decision=None,\
 name='m'), 4)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     [
        ...         'a',
        ...         Lexeme.domainSeparator,
        ...         'b',
        ...         Lexeme.zoneSeparator,
        ...         'c',
        ...         Lexeme.zoneSeparator,
        ...         'm'
        ...     ]
        ... )
        (MechanismSpecifier(domain='a', zone='b', decision='c', name='m'), 6)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     [
        ...         'a',
        ...         Lexeme.domainSeparator,
        ...         'b',
        ...         Lexeme.zoneSeparator,
        ...         'c',
        ...         Lexeme.zoneSeparator,
        ...         'm'
        ...     ],
        ...     2
        ... )
        (MechanismSpecifier(domain=None, zone='b', decision='c',\
 name='m'), 6)
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     [
        ...         'a',
        ...         Lexeme.domainSeparator,
        ...         'b',
        ...         Lexeme.zoneSeparator,
        ...         'c',
        ...         Lexeme.zoneSeparator,
        ...         'm'
        ...     ],
        ...     4
        ... )
        (MechanismSpecifier(domain=None, zone=None, decision='c',\
 name='m'), 6)
        """
        start, tEnd, nLeft = normalizeEnds(tokens, start, -1)

        try:
            dSpec, dEnd = self.parseDecisionSpecifierFromTokens(
                tokens,
                start
            )
        except ParseError:
            raise ParseError(
                "Failed to parse mechanism specifier couldn't parse"
                " initial mechanism name."
            )

        if isinstance(dSpec, int):
            raise ParseError(
                f"Invalid mechanism specifier: cannot use a decision ID"
                f" as the decision part. Got: {tokens[start:]}"
            )
            # TODO: Allow that?

        mDomain = dSpec.domain
        if dEnd == tEnd or dEnd == tEnd - 1:
            return (
                base.MechanismSpecifier(
                    domain=mDomain,
                    zone=None,
                    decision=dSpec.zone,
                    name=dSpec.name
                ),
                dEnd
            )

        sep = tokens[dEnd + 1]
        after = tokens[dEnd + 2]

        if sep == Lexeme.zoneSeparator:
            if isinstance(after, Lexeme):
                return (
                    base.MechanismSpecifier(
                        domain=mDomain,
                        zone=None,
                        decision=dSpec.zone,
                        name=dSpec.name
                    ),
                    dEnd
                )
            else:
                return (
                    base.MechanismSpecifier(
                        domain=mDomain,
                        zone=dSpec.zone,
                        decision=dSpec.name,
                        name=after
                    ),
                    dEnd + 2
                )
        else:
            return (
                base.MechanismSpecifier(
                    domain=mDomain,
                    zone=None,
                    decision=dSpec.zone,
                    name=dSpec.name
                ),
                dEnd
            )

    def groupReqTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> GroupedTokens:
        """
        Groups tokens for a requirement, stripping out all parentheses
        but replacing parenthesized expressions with sub-lists of tokens.

        For example:

        >>> pf = ParseFormat()
        >>> pf.groupReqTokens(['jump'])
        ['jump']
        >>> pf.groupReqTokens([Lexeme.openParen, 'jump'])
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.groupReqTokens([Lexeme.closeParen, 'jump'])
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.groupReqTokens(['jump', Lexeme.closeParen])
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.groupReqTokens([Lexeme.openParen, 'jump', Lexeme.closeParen])
        [['jump']]
        >>> pf.groupReqTokens(
        ...     [
        ...         Lexeme.openParen,
        ...         'jump',
        ...         Lexeme.orBar,
        ...         'climb',
        ...         Lexeme.closeParen,
        ...         Lexeme.ampersand,
        ...         'crawl',
        ...     ]
        ... )
        [['jump', <Lexeme.orBar: ...>, 'climb'], <Lexeme.ampersand: ...>,\
 'crawl']
        """
        start, end, nTokens = normalizeEnds(tokens, start, end)
        if nTokens == 0:
            raise ParseError("Ran out of tokens.")

        resultsStack: List[GroupedTokens] = [[]]
        here = start
        while here <= end:
            token = tokens[here]
            here += 1
            if token == Lexeme.closeParen:
                if len(resultsStack) == 1:
                    raise ParseError(
                        f"Too many closing parens at index {here - 1}"
                        f" in:\n{tokens[start:end + 1]}"
                    )
                else:
                    closed = resultsStack.pop()
                    resultsStack[-1].append(closed)
            elif token == Lexeme.openParen:
                resultsStack.append([])
            else:
                resultsStack[-1].append(token)
        if len(resultsStack) != 1:
            raise ParseError(
                f"Mismatched parentheses in tokens:"
                f"\n{tokens[start:end + 1]}"
            )
        return resultsStack[0]

    def groupReqTokensByPrecedence(
        self,
        tokenGroups: GroupedTokens
    ) -> GroupedRequirementParts:
        """
        Re-groups requirement tokens that have been grouped using
        `groupReqTokens` according to operator precedence, effectively
        creating an equivalent result which would have been obtained by
        `groupReqTokens` if all possible non-redundant explicit
        parentheses had been included.

        Also turns each leaf part into a `Requirement`.

        TODO: Make this actually reasonably efficient T_T

        Examples:

        >>> pf = ParseFormat()
        >>> pf.parseMechanismSpecifierFromTokens(
        ...     [
        ...         'roomB',
        ...         Lexeme.zoneSeparator,
        ...         'switch',
        ...         Lexeme.mechanismSeparator,
        ...         'on'
        ...     ]
        ... )
        (MechanismSpecifier(domain=None, zone=None, decision='roomB',\
 name='switch'), 2)
        >>> r = pf.parseRequirement('capability&roomB::switch:on')
        >>> pf.groupReqTokensByPrecedence(
        ...     [
        ...         ['jump', Lexeme.orBar, 'climb'],
        ...         Lexeme.ampersand,
        ...         Lexeme.notMarker,
        ...         'coin',
        ...         Lexeme.tokenCount,
        ...         '3'
        ...     ]
        ... )
        [\
[\
[[ReqCapability('jump'), <Lexeme.orBar: ...>, ReqCapability('climb')]],\
 <Lexeme.ampersand: ...>,\
 [<Lexeme.notMarker: ...>, ReqTokens('coin', 3)]\
]\
]
        """
        subgrouped: List[Union[Lexeme, str, GroupedRequirementParts]] = []
        # First recursively group all parenthesized expressions
        for i, item in enumerate(tokenGroups):
            if isinstance(item, list):
                subgrouped.append(self.groupReqTokensByPrecedence(item))
            else:
                subgrouped.append(item)

        # Now process all leaf requirements
        leavesConverted: GroupedRequirementParts = []
        i = 0
        while i < len(subgrouped):
            gItem = subgrouped[i]

            if isinstance(gItem, list):
                leavesConverted.append(gItem)
            elif isinstance(gItem, Lexeme):
                leavesConverted.append(gItem)
            elif i == len(subgrouped) - 1:
                if isinstance(gItem, Lexeme):
                    raise ParseError(
                        f"Lexeme at end of requirement. Grouped tokens:"
                        f"\n{tokenGroups}"
                    )
                else:
                    assert isinstance(gItem, str)
                    if gItem == 'X':
                        leavesConverted.append(base.ReqImpossible())
                    elif gItem == 'O':
                        leavesConverted.append(base.ReqNothing())
                    else:
                        leavesConverted.append(base.ReqCapability(gItem))
            else:
                assert isinstance(gItem, str)
                try:
                    # TODO: Avoid list copy here...
                    couldBeMechanismSpecifier: LexedTokens = []
                    for ii in range(i, len(subgrouped)):
                        lexemeOrStr = subgrouped[ii]
                        if isinstance(lexemeOrStr, (Lexeme, str)):
                            couldBeMechanismSpecifier.append(lexemeOrStr)
                        else:
                            break
                    mSpec, mEnd = self.parseMechanismSpecifierFromTokens(
                        couldBeMechanismSpecifier
                    )
                    mEnd += i
                    if (
                        mEnd >= len(subgrouped) - 2
                     or subgrouped[mEnd + 1] != Lexeme.mechanismSeparator
                    ):
                        raise ParseError("Not a mechanism requirement.")

                    mState = subgrouped[mEnd + 2]
                    if not isinstance(mState, base.MechanismState):
                        raise ParseError("Not a mechanism requirement.")
                    leavesConverted.append(base.ReqMechanism(mSpec, mState))
                    i = mEnd + 2  # + 1 will happen automatically below
                except ParseError:
                    following = subgrouped[i + 1]
                    if following in (
                        Lexeme.tokenCount,
                        Lexeme.mechanismSeparator
                    ):
                        if i == len(subgrouped) - 2:
                            raise ParseError(
                                f"Lexeme at end of requirement. Grouped"
                                f" tokens:\n{tokenGroups}"
                            )
                        afterwards = subgrouped[i + 2]
                        if not isinstance(afterwards, str):
                            raise ParseError(
                                f"Lexeme after token or mechanism"
                                f" separator at index {i}."
                                f" Grouped tokens:\n{tokenGroups}"
                            )
                        i += 2  # another +1 automatic below
                        if following == Lexeme.tokenCount:
                            try:
                                tCount = int(afterwards)
                            except ValueError:
                                raise ParseError(
                                    f"Token count could not be parsed as an"
                                    f" integer: {afterwards!r}."
                                    f" Grouped tokens:\n{tokenGroups}"
                                )
                            leavesConverted.append(
                                base.ReqTokens(gItem, tCount)
                            )
                        else:
                            assert following == Lexeme.mechanismSeparator
                            leavesConverted.append(
                                base.ReqMechanism(gItem, afterwards)
                            )
                    else:
                        if gItem == 'X':
                            leavesConverted.append(base.ReqImpossible())
                        elif gItem == 'O':
                            leavesConverted.append(base.ReqNothing())
                        else:
                            leavesConverted.append(base.ReqCapability(gItem))

            # Finally, increment our index:
            i += 1

        # Now group all NOT operators
        i = 0
        notsGrouped: GroupedRequirementParts = []
        while i < len(leavesConverted):
            leafItem = leavesConverted[i]
            group = []
            while leafItem == Lexeme.notMarker:
                group.append(leafItem)
                i += 1
                if i >= len(leavesConverted):
                    raise ParseError(
                        f"NOT at end of tokens:\n{leavesConverted}"
                    )
                leafItem = leavesConverted[i]
            if group == []:
                notsGrouped.append(leafItem)
                i += 1
            else:
                group.append(leafItem)
                i += 1
                notsGrouped.append(group)

        # Next group all AND operators
        i = 0
        andsGrouped: GroupedRequirementParts = []
        while i < len(notsGrouped):
            notGroupItem = notsGrouped[i]
            if notGroupItem == Lexeme.ampersand:
                if i == len(notsGrouped) - 1:
                    raise ParseError(
                        f"AND at end of group in tokens:"
                        f"\n{tokenGroups}"
                        f"Which had been grouped into:"
                        f"\n{notsGrouped}"
                    )
                itemAfter = notsGrouped[i + 1]
                if isinstance(itemAfter, Lexeme):
                    raise ParseError(
                        f"Lexeme after AND in of group in tokens:"
                        f"\n{tokenGroups}"
                        f"Which had been grouped into:"
                        f"\n{notsGrouped}"
                    )
                assert isinstance(itemAfter, (base.Requirement, list))
                prev = andsGrouped[-1]
                if (
                    isinstance(prev, list)
                and len(prev) > 2
                and prev[1] == Lexeme.ampersand
                ):
                    prev.extend(notsGrouped[i:i + 2])
                    i += 1  # with an extra +1 below
                else:
                    andsGrouped.append(
                        [andsGrouped.pop()] + notsGrouped[i:i + 2]
                    )
                    i += 1 # extra +1 below
            else:
                andsGrouped.append(notGroupItem)
            i += 1

        # Finally check that we only have OR operators left over
        i = 0
        finalResult: GroupedRequirementParts = []
        while i < len(andsGrouped):
            andGroupItem = andsGrouped[i]
            if andGroupItem == Lexeme.orBar:
                if i == len(andsGrouped) - 1:
                    raise ParseError(
                        f"OR at end of group in tokens:"
                        f"\n{tokenGroups}"
                        f"Which had been grouped into:"
                        f"\n{andsGrouped}"
                    )
                itemAfter = andsGrouped[i + 1]
                if isinstance(itemAfter, Lexeme):
                    raise ParseError(
                        f"Lexeme after OR in of group in tokens:"
                        f"\n{tokenGroups}"
                        f"Which had been grouped into:"
                        f"\n{andsGrouped}"
                    )
                assert isinstance(itemAfter, (base.Requirement, list))
                prev = finalResult[-1]
                if (
                    isinstance(prev, list)
                and len(prev) > 2
                and prev[1] == Lexeme.orBar
                ):
                    prev.extend(andsGrouped[i:i + 2])
                    i += 1  # with an extra +1 below
                else:
                    finalResult.append(
                        [finalResult.pop()] + andsGrouped[i:i + 2]
                    )
                    i += 1 # extra +1 below
            elif isinstance(andGroupItem, Lexeme):
                raise ParseError(
                    f"Leftover lexeme when grouping ORs at index {i}"
                    f" in grouped tokens:\n{andsGrouped}"
                    f"\nOriginal tokens were:\n{tokenGroups}"
                )
            else:
                finalResult.append(andGroupItem)
            i += 1

        return finalResult

    def parseRequirementFromRegroupedTokens(
        self,
        reqGroups: GroupedRequirementParts
    ) -> base.Requirement:
        """
        Recursive parser that works once tokens have been turned into
        requirements at the leaves and grouped by operator precedence
        otherwise (see `groupReqTokensByPrecedence`).

        TODO: Simply by just doing this while grouping... ?
        """
        if len(reqGroups) == 0:
            raise ParseError("Ran out of tokens.")

        elif len(reqGroups) == 1:
            only = reqGroups[0]
            if isinstance(only, list):
                return self.parseRequirementFromRegroupedTokens(only)
            elif isinstance(only, base.Requirement):
                return only
            else:
                raise ParseError(f"Invalid singleton group:\n{only}")
        elif reqGroups[0] == Lexeme.notMarker:
            if (
                not all(x == Lexeme.notMarker for x in reqGroups[:-1])
             or not isinstance(reqGroups[-1], (list, base.Requirement))
            ):
                raise ParseError(f"Invalid negation group:\n{reqGroups}")
            result = reqGroups[-1]
            if isinstance(result, list):
                result = self.parseRequirementFromRegroupedTokens(result)
            assert isinstance(result, base.Requirement)
            for i in range(len(reqGroups) - 1):
                result = base.ReqNot(result)
            return result
        elif len(reqGroups) % 2 == 0:
            raise ParseError(f"Even-length non-negation group:\n{reqGroups}")
        else:
            if (
                reqGroups[1] not in (Lexeme.ampersand, Lexeme.orBar)
             or not all(
                    reqGroups[i] == reqGroups[1]
                    for i in range(1, len(reqGroups), 2)
                )
            ):
                raise ParseError(
                    f"Inconsistent operator(s) in group:\n{reqGroups}"
                )
            op = reqGroups[1]
            operands = [
                (
                    self.parseRequirementFromRegroupedTokens(x)
                    if isinstance(x, list)
                    else x
                )
                for x in reqGroups[::2]
            ]
            if not all(isinstance(x, base.Requirement) for x in operands):
                raise ParseError(
                    f"Item not reducible to Requirement in AND group:"
                    f"\n{reqGroups}"
                )
            reqSequence = cast(Sequence[base.Requirement], operands)
            if op == Lexeme.ampersand:
                return base.ReqAll(reqSequence).flatten()
            else:
                assert op == Lexeme.orBar
                return base.ReqAny(reqSequence).flatten()

    def parseRequirementFromGroupedTokens(
        self,
        tokenGroups: GroupedTokens
    ) -> base.Requirement:
        """
        Parses a `base.Requirement` from a pre-grouped tokens list (see
        `groupReqTokens`). Uses the 'orBar', 'ampersand', 'notMarker',
        'tokenCount', and 'mechanismSeparator' `Lexeme`s to provide
        'or', 'and', and 'not' operators along with distinguishing
        between capabilities, tokens, and mechanisms.

        Precedence ordering is not, then and, then or, but you are
        encouraged to use parentheses for explicit grouping (the
        'openParen' and 'closeParen' `Lexeme`s, although these must be
        handled by `groupReqTokens` so this function won't see them
        directly).

        You can also use 'X' (without quotes) for a never-satisfied
        requirement, and 'O' (without quotes) for an always-satisfied
        requirement.

        Note that when '!' is applied to a token requirement it flips
        the sense of the integer from 'must have at least this many' to
        'must have strictly less than this many'.

        Raises a `ParseError` if the grouped tokens it is given cannot
        be parsed as a `Requirement`.

        Examples:

        >>> pf = ParseFormat()
        >>> pf.parseRequirementFromGroupedTokens(['capability'])
        ReqCapability('capability')
        >>> pf.parseRequirementFromGroupedTokens(
        ...     ['token', Lexeme.tokenCount, '3']
        ... )
        ReqTokens('token', 3)
        >>> pf.parseRequirementFromGroupedTokens(
        ...     ['mechanism', Lexeme.mechanismSeparator, 'state']
        ... )
        ReqMechanism('mechanism', 'state')
        >>> pf.parseRequirementFromGroupedTokens(
        ...     ['capability', Lexeme.orBar, 'token',
        ...      Lexeme.tokenCount, '3']
        ... )
        ReqAny([ReqCapability('capability'), ReqTokens('token', 3)])
        >>> pf.parseRequirementFromGroupedTokens(
        ...     ['one', Lexeme.ampersand, 'two', Lexeme.orBar, 'three']
        ... )
        ReqAny([ReqAll([ReqCapability('one'), ReqCapability('two')]),\
 ReqCapability('three')])
        >>> pf.parseRequirementFromGroupedTokens(
        ...     [
        ...         'one',
        ...         Lexeme.ampersand,
        ...         [
        ...              'two',
        ...              Lexeme.orBar,
        ...              'three'
        ...         ]
        ...     ]
        ... )
        ReqAll([ReqCapability('one'), ReqAny([ReqCapability('two'),\
 ReqCapability('three')])])
        >>> pf.parseRequirementFromTokens(['X'])
        ReqImpossible()
        >>> pf.parseRequirementFromTokens(['O'])
        ReqNothing()
        >>> pf.parseRequirementFromTokens(
        ...     [Lexeme.openParen, 'O', Lexeme.closeParen]
        ... )
        ReqNothing()
        """
        if len(tokenGroups) == 0:
            raise ParseError("Ran out of tokens.")

        reGrouped = self.groupReqTokensByPrecedence(tokenGroups)

        return self.parseRequirementFromRegroupedTokens(reGrouped)

    def parseRequirementFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> base.Requirement:
        """
        Parses a requirement from `LexedTokens` by grouping them first
        and then using `parseRequirementFromGroupedTokens`.

        For example:

        >>> pf = ParseFormat()
        >>> pf.parseRequirementFromTokens(
        ...     [
        ...         'one',
        ...         Lexeme.ampersand,
        ...         Lexeme.openParen,
        ...         'two',
        ...         Lexeme.orBar,
        ...         'three',
        ...         Lexeme.closeParen
        ...     ]
        ... )
        ReqAll([ReqCapability('one'), ReqAny([ReqCapability('two'),\
 ReqCapability('three')])])
        """
        grouped = self.groupReqTokens(tokens, start, end)
        return self.parseRequirementFromGroupedTokens(grouped)

    def parseRequirement(self, encoded: str) -> base.Requirement:
        """
        Parses a `base.Requirement` from a string by calling `lex` and
        then feeding it into `ParseFormat.parseRequirementFromTokens`.
        As stated in `parseRequirementFromTokens`, the precedence
        binding order is NOT, then AND, then OR.

        For example:

        >>> pf = ParseFormat()
        >>> pf.parseRequirement('! coin * 3')
        ReqNot(ReqTokens('coin', 3))
        >>> pf.parseRequirement(
        ...     '  oneWord | "two words"|"three  words words" '
        ... )
        ReqAny([ReqCapability('oneWord'), ReqCapability('"two words"'),\
 ReqCapability('"three  words words"')])
        >>> pf.parseRequirement('words-with-dashes')
        ReqCapability('words-with-dashes')
        >>> r = pf.parseRequirement('capability&roomB::switch:on')
        >>> r
        ReqAll([ReqCapability('capability'),\
 ReqMechanism(MechanismSpecifier(domain=None, zone=None, decision='roomB',\
 name='switch'), 'on')])
        >>> r.unparse()
        '(capability&roomB::switch:on)'
        >>> pf.parseRequirement('!!!one')
        ReqNot(ReqNot(ReqNot(ReqCapability('one'))))
        >>> pf.parseRequirement('domain//zone::where::mechanism:state')
        ReqMechanism(MechanismSpecifier(domain='domain', zone='zone',\
 decision='where', name='mechanism'), 'state')
        >>> pf.parseRequirement('domain//mechanism:state')
        ReqMechanism(MechanismSpecifier(domain='domain', zone=None,\
 decision=None, name='mechanism'), 'state')
        >>> pf.parseRequirement('where::mechanism:state')
        ReqMechanism(MechanismSpecifier(domain=None, zone=None,\
 decision='where', name='mechanism'), 'state')
        >>> pf.parseRequirement('zone::where::mechanism:state')
        ReqMechanism(MechanismSpecifier(domain=None, zone='zone',\
 decision='where', name='mechanism'), 'state')

        Precedence examples:

        >>> pf.parseRequirement('A|B&C')
        ReqAny([ReqCapability('A'), ReqAll([ReqCapability('B'),\
 ReqCapability('C')])])
        >>> pf.parseRequirement('A&B|C')
        ReqAny([ReqAll([ReqCapability('A'), ReqCapability('B')]),\
 ReqCapability('C')])
        >>> pf.parseRequirement('(A&B)|C')
        ReqAny([ReqAll([ReqCapability('A'), ReqCapability('B')]),\
 ReqCapability('C')])
        >>> pf.parseRequirement('(A&B|C)&D')
        ReqAll([ReqAny([ReqAll([ReqCapability('A'), ReqCapability('B')]),\
 ReqCapability('C')]), ReqCapability('D')])

        Error examples:

        >>> pf.parseRequirement('one ! Word')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('a|')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('b!')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('*emph*')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('one&&two')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('one!|two')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('one*two')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('one*')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('()')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('(one)*3')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('a:')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('a:b:c')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        >>> pf.parseRequirement('where::capability')
        Traceback (most recent call last):
        ...
        exploration.parsing.ParseError...
        """
        return self.parseRequirementFromTokens(
            lex(encoded, self.reverseFormat)
        )

    def parseSkillCombinationFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> Union[base.Skill, base.SkillCombination]:
        """
        Parses a skill combination from the specified range within the
        given tokens list. If just a single string token is selected, it
        will be returned as a `base.BestSkill` with just that skill
        inside.

        For example:

        >>> pf = ParseFormat()
        >>> pf.parseSkillCombinationFromTokens(['climbing'])
        BestSkill('climbing')
        >>> tokens = [
        ...     'best',
        ...     Lexeme.openParen,
        ...     'brains',
        ...     Lexeme.sepOrDelay,
        ...     'brawn',
        ...     Lexeme.closeParen,
        ... ]
        >>> pf.parseSkillCombinationFromTokens(tokens)
        BestSkill('brains', 'brawn')
        >>> tokens[2] = '3'  # not a lexeme so it's a string
        >>> pf.parseSkillCombinationFromTokens(tokens)
        BestSkill(3, 'brawn')
        >>> tokens = [
        ...     Lexeme.inverseSkill,
        ...     Lexeme.inverseSkill,
        ...     'yes',
        ... ]
        >>> pf.parseSkillCombinationFromTokens(tokens)
        InverseSkill(InverseSkill('yes'))
        """
        start, end, nTokens = normalizeEnds(tokens, start, end)

        first = tokens[start]
        if nTokens == 1:
            if isinstance(first, base.Skill):
                try:
                    level = int(first)
                    return base.BestSkill(level)
                except ValueError:
                    return base.BestSkill(first)
            else:
                raise ParseError(
                    "Invalid SkillCombination:\n{tokens[start:end + 1]"
                )

        if first == Lexeme.inverseSkill:
            inv = self.parseSkillCombinationFromTokens(
                tokens,
                start + 1,
                end
            )
            if isinstance(inv, base.BestSkill) and len(inv.skills) == 1:
                return base.InverseSkill(inv.skills[0])
            else:
                return base.InverseSkill(inv)

        second = tokens[start + 1]
        if second != Lexeme.openParen:
            raise ParseError(
                f"Invalid SkillCombination (missing paren):"
                f"\n{tokens[start:end + 1]}"
            )

        parenEnd = self.matchingBrace(
            tokens,
            start + 1,
            Lexeme.openParen,
            Lexeme.closeParen
        )
        if parenEnd != end:
            raise ParseError(
                f"Extra junk after SkillCombination:"
                f"\n{tokens[parenEnd + 1:end + 1]}"
            )

        if first == 'if':
            parts = list(
                findSeparatedParts(
                    tokens,
                    Lexeme.sepOrDelay,
                    start + 2,
                    end - 1,
                    Lexeme.openParen,
                    Lexeme.closeParen
                )
            )
            if len(parts) != 3:
                raise ParseError(
                    f"Wrong number of parts for ConditionalSkill (needs"
                    f" 3, got {len(parts)}:"
                    f"\n{tokens[start + 2:end]}"
                )
            reqStart, reqEnd = parts[0]
            ifStart, ifEnd = parts[1]
            elseStart, elseEnd = parts[2]
            return base.ConditionalSkill(
                self.parseRequirementFromTokens(tokens, reqStart, reqEnd),
                self.parseSkillCombinationFromTokens(tokens, ifStart, ifEnd),
                self.parseSkillCombinationFromTokens(
                    tokens,
                    elseStart,
                    elseEnd
                ),
            )
        elif first in ('sum', 'best', 'worst'):
            make: type[base.SkillCombination]
            if first == 'sum':
                make = base.CombinedSkill
            elif first == 'best':
                make = base.BestSkill
            else:
                make = base.WorstSkill

            subs = []
            for partStart, partEnd in findSeparatedParts(
                tokens,
                Lexeme.sepOrDelay,
                start + 2,
                end - 1,
                Lexeme.openParen,
                Lexeme.closeParen
            ):
                sub = self.parseSkillCombinationFromTokens(
                    tokens,
                    partStart,
                    partEnd
                )
                if (
                    isinstance(sub, base.BestSkill)
                and len(sub.skills) == 1
                ):
                    subs.append(sub.skills[0])
                else:
                    subs.append(sub)

            return make(*subs)
        else:
            raise ParseError(
                "Invalid SkillCombination:\n{tokens[start:end + 1]"
            )

    def parseSkillCombination(
        self,
        encoded: str
    ) -> base.SkillCombination:
        """
        Parses a `SkillCombination` from a string. Calls `lex` and then
        `parseSkillCombinationFromTokens`.
        """
        result = self.parseSkillCombinationFromTokens(
            lex(encoded, self.reverseFormat)
        )
        if not isinstance(result, base.SkillCombination):
            return base.BestSkill(result)
        else:
            return result

    def parseConditionFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> base.Condition:
        """
        Parses a `base.Condition` from a lexed tokens list. For example:

        >>> pf = ParseFormat()
        >>> tokens = [
        ...     Lexeme.doubleQuestionmark,
        ...     Lexeme.openParen,
        ...     "fire",
        ...     Lexeme.ampersand,
        ...     "water",
        ...     Lexeme.closeParen,
        ...     Lexeme.openCurly,
        ...     "gain",
        ...     "wind",
        ...     Lexeme.closeCurly,
        ...     Lexeme.openCurly,
        ...     Lexeme.closeCurly,
        ... ]
        >>> pf.parseConditionFromTokens(tokens) == base.condition(
        ...     condition=base.ReqAll([
        ...         base.ReqCapability('fire'),
        ...         base.ReqCapability('water')
        ...     ]),
        ...     consequence=[base.effect(gain='wind')]
        ... )
        True
        """
        start, end, nTokens = normalizeEnds(tokens, start, end)
        if nTokens < 8:
            raise ParseError(
                f"A Condition requires at least 8 tokens (got {nTokens})."
            )
        if tokens[start] != Lexeme.doubleQuestionmark:
            raise ParseError(
                f"A Condition must start with"
                f" {repr(self.formatDict[Lexeme.doubleQuestionmark])}"
            )
        try:
            consequenceStart = tokens.index(Lexeme.openCurly, start)
        except ValueError:
            raise ParseError("A condition must include a consequence block.")
        consequenceEnd = self.matchingBrace(tokens, consequenceStart)
        altStart = consequenceEnd + 1
        altEnd = self.matchingBrace(tokens, altStart)

        if altEnd != end:
            raise ParseError(
                f"Junk after condition:\n{tokens[altEnd + 1: end + 1]}"
            )

        return base.condition(
            condition=self.parseRequirementFromTokens(
                tokens,
                start + 1,
                consequenceStart - 1
            ),
            consequence=self.parseConsequenceFromTokens(
                tokens,
                consequenceStart,
                consequenceEnd
            ),
            alternative=self.parseConsequenceFromTokens(
                tokens,
                altStart,
                altEnd
            )
        )

    def parseCondition(
        self,
        encoded: str
    ) -> base.Condition:
        """
        Lexes the given string and then calls `parseConditionFromTokens`
        to return a `base.Condition`.
        """
        return self.parseConditionFromTokens(
            lex(encoded, self.reverseFormat)
        )

    def parseChallengeFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> base.Challenge:
        """
        Parses a `base.Challenge` from a lexed tokens list.

        For example:

        >>> pf = ParseFormat()
        >>> tokens = [
        ...     Lexeme.angleLeft,
        ...     '2',
        ...     Lexeme.angleRight,
        ...     'best',
        ...     Lexeme.openParen,
        ...     "chess",
        ...     Lexeme.sepOrDelay,
        ...     "checkers",
        ...     Lexeme.closeParen,
        ...     Lexeme.openCurly,
        ...     "gain",
        ...     "coin",
        ...     Lexeme.tokenCount,
        ...     "5",
        ...     Lexeme.closeCurly,
        ...     Lexeme.angleRight,
        ...     Lexeme.openCurly,
        ...     "lose",
        ...     "coin",
        ...     Lexeme.tokenCount,
        ...     "5",
        ...     Lexeme.closeCurly,
        ... ]
        >>> c = pf.parseChallengeFromTokens(tokens)
        >>> c['skills'] == base.BestSkill('chess', 'checkers')
        True
        >>> c['level']
        2
        >>> c['success'] == [base.effect(gain=('coin', 5))]
        True
        >>> c['failure'] == [base.effect(lose=('coin', 5))]
        True
        >>> c['outcome']
        False
        >>> c == base.challenge(
        ...     skills=base.BestSkill('chess', 'checkers'),
        ...     level=2,
        ...     success=[base.effect(gain=('coin', 5))],
        ...     failure=[base.effect(lose=('coin', 5))],
        ...     outcome=False
        ... )
        True
        >>> t2 = ['hi'] + tokens + ['bye']  # parsing only part of the list
        >>> c == pf.parseChallengeFromTokens(t2, 1, -2)
        True
        """
        start, end, nTokens = normalizeEnds(tokens, start, end)
        if nTokens < 8:
            raise ParseError(
                f"Not enough tokens for a challenge: {nTokens}"
            )
        if tokens[start] != Lexeme.angleLeft:
            raise ParseError(
                f"Challenge must start with"
                f" {repr(self.formatDict[Lexeme.angleLeft])}"
            )
        levelStr = tokens[start + 1]
        if isinstance(levelStr, Lexeme):
            raise ParseError(
                f"Challenge must start with a level in angle brackets"
                f" (got {repr(self.formatDict[levelStr])})."
            )
        if tokens[start + 2] != Lexeme.angleRight:
            raise ParseError(
                f"Challenge must include"
                f" {repr(self.formatDict[Lexeme.angleRight])} after"
                f" the level."
            )
        try:
            level = int(levelStr)
        except ValueError:
            raise ParseError(
                f"Challenge level must be an integer (got"
                f" {repr(tokens[start + 1])}."
            )
        try:
            successStart = tokens.index(Lexeme.openCurly, start)
            skillsEnd = successStart - 1
        except ValueError:
            raise ParseError("A challenge must include a consequence block.")

        outcome: Optional[bool] = None
        if tokens[skillsEnd] == Lexeme.angleRight:
            skillsEnd -= 1
            outcome = True
        successEnd = self.matchingBrace(tokens, successStart)
        failStart = successEnd + 1
        if tokens[failStart] == Lexeme.angleRight:
            failStart += 1
            if outcome is not None:
                raise ParseError(
                    "Cannot indicate both success and failure as"
                    " outcomes in a challenge."
                )
            outcome = False
        failEnd = self.matchingBrace(tokens, failStart)

        if failEnd != end:
            raise ParseError(
                f"Junk after condition:\n{tokens[failEnd + 1:end + 1]}"
            )

        skills = self.parseSkillCombinationFromTokens(
            tokens,
            start + 3,
            skillsEnd
        )
        if isinstance(skills, base.Skill):
            skills = base.BestSkill(skills)

        return base.challenge(
            level=level,
            outcome=outcome,
            skills=skills,
            success=self.parseConsequenceFromTokens(
                tokens[successStart:successEnd + 1]
            ),
            failure=self.parseConsequenceFromTokens(
                tokens[failStart:failEnd + 1]
            )
        )

    def parseChallenge(
        self,
        encoded: str
    ) -> base.Challenge:
        """
        Lexes the given string and then calls `parseChallengeFromTokens`
        to return a `base.Challenge`.
        """
        return self.parseChallengeFromTokens(
            lex(encoded, self.reverseFormat)
        )

    def parseConsequenceFromTokens(
        self,
        tokens: LexedTokens,
        start: int = 0,
        end: int = -1
    ) -> base.Consequence:
        """
        Parses a consequence from a lexed token list. If start and/or end
        are specified, only processes the part of the list between those
        two indices (inclusive). Use `lex` to turn a string into a
        `LexedTokens` list (or use `ParseFormat.parseConsequence` which
        does that for you).

        An example:

        >>> pf = ParseFormat()
        >>> tokens = [
        ...     Lexeme.openCurly,
        ...     'gain',
        ...     'power',
        ...     Lexeme.closeCurly
        ... ]
        >>> c = pf.parseConsequenceFromTokens(tokens)
        >>> c == [base.effect(gain='power')]
        True
        >>> tokens.append('hi')
        >>> c == pf.parseConsequenceFromTokens(tokens, end=-2)
        True
        >>> c == pf.parseConsequenceFromTokens(tokens, end=3)
        True
        """
        start, end, nTokens = normalizeEnds(tokens, start, end)

        if nTokens < 2:
            raise ParseError("Consequence must have at least two tokens.")

        if tokens[start] != Lexeme.openCurly:
            raise ParseError(
                f"Consequence must start with an open curly brace:"
                f" {repr(self.formatDict[Lexeme.openCurly])}."
            )

        if tokens[end] != Lexeme.closeCurly:
            raise ParseError(
                f"Consequence must end with a closing curly brace:"
                f" {repr(self.formatDict[Lexeme.closeCurly])}."
            )

        if nTokens == 2:
            return []

        result: base.Consequence = []
        for partStart, partEnd in findSeparatedParts(
            tokens,
            Lexeme.consequenceSeparator,
            start + 1,
            end - 1,
            Lexeme.openCurly,
            Lexeme.closeCurly
        ):
            if partEnd - partStart < 0:
                raise ParseError("Empty consequence part.")
            if tokens[partStart] == Lexeme.angleLeft:  # a challenge
                result.append(
                    self.parseChallengeFromTokens(
                        tokens,
                        partStart,
                        partEnd
                    )
                )
            elif tokens[partStart] == Lexeme.doubleQuestionmark:  # condition
                result.append(
                    self.parseConditionFromTokens(
                        tokens,
                        partStart,
                        partEnd
                    )
                )
            else:  # Must be an effect
                result.append(
                    self.parseEffectFromTokens(
                        tokens,
                        partStart,
                        partEnd
                    )
                )

        return result

    def parseConsequence(self, encoded: str) -> base.Consequence:
        """
        Parses a consequence from a string. Uses `lex` and
        `ParseFormat.parseConsequenceFromTokens`. For example:

        >>> pf = ParseFormat()
        >>> c = pf.parseConsequence(
        ...   '{gain power}'
        ... )
        >>> c == [base.effect(gain='power')]
        True
        >>> pf.unparseConsequence(c)
        '{gain power}'
        >>> c = pf.parseConsequence(
        ...     '{\\n'
        ...     '    ??(brawny|!weights*3){\\n'
        ...     '        <3>sum(brains, brawn){goto home}>{bounce}\\n'
        ...     '    }{};\\n'
        ...     '    lose coin*1\\n'
        ...     '}'
        ... )
        >>> len(c)
        2
        >>> c[0]['condition'] == base.ReqAny([
        ...     base.ReqCapability('brawny'),
        ...     base.ReqNot(base.ReqTokens('weights', 3))
        ... ])
        True
        >>> len(c[0]['consequence'])
        1
        >>> len(c[0]['alternative'])
        0
        >>> cons = c[0]['consequence'][0]
        >>> cons['skills'] == base.CombinedSkill('brains', 'brawn')
        True
        >>> cons['level']
        3
        >>> len(cons['success'])
        1
        >>> len(cons['failure'])
        1
        >>> cons['success'][0] == base.effect(goto='home')
        True
        >>> cons['failure'][0] == base.effect(bounce=True)
        True
        >>> cons['outcome'] = False
        >>> c[0] == base.condition(
        ...     condition=base.ReqAny([
        ...         base.ReqCapability('brawny'),
        ...         base.ReqNot(base.ReqTokens('weights', 3))
        ...     ]),
        ...     consequence=[
        ...         base.challenge(
        ...             skills=base.CombinedSkill('brains', 'brawn'),
        ...             level=3,
        ...             success=[base.effect(goto='home')],
        ...             failure=[base.effect(bounce=True)],
        ...             outcome=False
        ...         )
        ...     ]
        ... )
        True
        >>> c[1] == base.effect(lose=('coin', 1))
        True
        """
        return self.parseConsequenceFromTokens(
            lex(encoded, self.reverseFormat)
        )


#---------------------#
# Graphviz dot format #
#---------------------#

class ParsedDotGraph(TypedDict):
    """
    Represents a parsed `graphviz` dot-format graph consisting of nodes,
    edges, and subgraphs, with attributes attached to nodes and/or
    edges. An intermediate format during conversion to a full
    `DecisionGraph`. Includes the following slots:

    - `'nodes'`: A list of tuples each holding a node ID followed by a
        list of name/value attribute pairs.
    - `'edges'`: A list of tuples each holding a from-ID, a to-ID,
        and then a list of name/value attribute pairs.
    - `'attrs'`: A list of tuples each holding a name/value attribute
        pair for graph-level attributes.
    - `'subgraphs'`: A list of subgraphs (each a tuple with a subgraph
        name and then another dictionary in the same format as this
        one).
    """
    nodes: List[Tuple[int, List[Tuple[str, str]]]]
    edges: List[Tuple[int, int, List[Tuple[str, str]]]]
    attrs: List[Tuple[str, str]]
    subgraphs: List[Tuple[str, 'ParsedDotGraph']]


def parseSimpleDotAttrs(fragment: str) -> List[Tuple[str, str]]:
    """
    Given a string fragment that starts with '[' and ends with ']',
    parses a simple attribute list in `graphviz` dot format from that
    fragment, returning a list of name/value attribute tuples. Raises a
    `DotParseError` if the fragment doesn't have the right format.

    Examples:

    >>> parseSimpleDotAttrs('[ name=value ]')
    [('name', 'value')]
    >>> parseSimpleDotAttrs('[ a=b c=d e=f ]')
    [('a', 'b'), ('c', 'd'), ('e', 'f')]
    >>> parseSimpleDotAttrs('[ a=b "c d"="e f" ]')
    [('a', 'b'), ('c d', 'e f')]
    >>> parseSimpleDotAttrs('[a=b "c d"="e f"]')
    [('a', 'b'), ('c d', 'e f')]
    >>> parseSimpleDotAttrs('[ a=b "c d"="e f"')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseSimpleDotAttrs('a=b "c d"="e f" ]')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseSimpleDotAttrs('[ a b=c ]')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseSimpleDotAttrs('[ a=b c ]')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseSimpleDotAttrs('[ name="value" ]')
    [('name', 'value')]
    >>> parseSimpleDotAttrs('[ name="\\\\"value\\\\"" ]')
    [('name', '"value"')]
    """
    if not fragment.startswith('[') or not fragment.endswith(']'):
        raise DotParseError(
            f"Simple attrs fragment missing delimiters:"
            f"\n  {repr(fragment)}"
        )
    result = []
    rest = fragment[1:-1].strip()
    while rest:
        # Get possibly-quoted attribute name:
        if rest.startswith('"'):
            try:
                aName, rest = utils.unquoted(rest)
            except ValueError:
                raise DotParseError(
                    f"Malformed quoted attribute name in"
                    f" fragment:\n  {repr(fragment)}"
                )
            rest = rest.lstrip()
            if not rest.startswith('='):
                raise DotParseError(
                    f"Missing '=' in attribute block in"
                    f" fragment:\n  {repr(fragment)}"
                )
            rest = rest[1:].lstrip()
        else:
            try:
                eqInd = rest.index('=')
            except ValueError:
                raise DotParseError(
                    f"Missing '=' in attribute block in"
                    f" fragment:\n  {repr(fragment)}"
                )
            aName = rest[:eqInd]
            if ' ' in aName:
                raise DotParseError(
                    f"Malformed unquoted attribute name"
                    f" {repr(aName)} in fragment:"
                    f"\n  {repr(fragment)}"
                )
            rest = rest[eqInd + 1:].lstrip()

        # Get possibly-quoted attribute value:
        if rest.startswith('"'):
            try:
                aVal, rest = utils.unquoted(rest)
            except ValueError:
                raise DotParseError(
                    f"Malformed quoted attribute value in"
                    f" fragment:\n  {repr(fragment)}"
                )
            rest = rest.lstrip()
        else:
            try:
                spInd = rest.index(' ')
            except ValueError:
                spInd = len(rest)
            aVal = rest[:spInd]
            rest = rest[spInd:].lstrip()

        # Append this attribute pair and continue parsing
        result.append((aName, aVal))

    return result


def parseDotNode(
    nodeLine: str
) -> Tuple[int, Union[bool, List[Tuple[str, str]]]]:
    """
    Given a line of text from a `graphviz` dot-format graph
    (possibly ending in an '[' to indicate attributes to follow, or
    possible including a '[ ... ]' block with attributes in-line),
    parses it as a node declaration, returning the ID of the node,
    along with a boolean indicating whether attributes follow or
    not. If an inline attribute block is present, the second member
    of the tuple will be a list of attribute name/value pairs. In
    that case, all attribute names and values must either be quoted
    or not include spaces.
    Examples:

    >>> parseDotNode('1')
    (1, False)
    >>> parseDotNode(' 1 [ ')
    (1, True)
    >>> parseDotNode(' 1 [ a=b "c d"="e f" ] ')
    (1, [('a', 'b'), ('c d', 'e f')])
    >>> parseDotNode(' 3 [ name="A = \\\\"grate:open\\\\"" ]')
    (3, [('name', 'A = "grate:open"')])
    >>> parseDotNode('  "1"[')
    (1, True)
    >>> parseDotNode('  100[')
    (100, True)
    >>> parseDotNode('  1 2')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotNode('  1 [ 2')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotNode('  1 2')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotNode('  1 [ junk not=attrs ]')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotNode('  \\n')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    """
    stripped = nodeLine.strip()
    if len(stripped) == 0:
        raise DotParseError(
            "Empty node in dot graph on line:\n  {repr(nodeLine)}"
        )
    hasAttrs: Union[bool, List[Tuple[str, str]]] = False
    if stripped.startswith('"'):
        nodeName, rest = utils.unquoted(stripped)
        rest = rest.strip()
        if rest == '[':
            hasAttrs = True
        elif rest.startswith('[') and rest.endswith(']'):
            hasAttrs = parseSimpleDotAttrs(rest)
        elif rest:
            raise DotParseError(
                f"Extra junk {repr(rest)} after node on line:"
                f"\n {repr(nodeLine)}"
            )

    else:
        if stripped.endswith('['):
            hasAttrs = True
            stripped = stripped[:-1].rstrip()
        elif stripped.endswith(']'):
            try:
                # TODO: Why did this used to be rindex? Was that
                # important in some case? (That doesn't work since the
                # value may contain a quoted open bracket).
                attrStart = stripped.index('[')
            except ValueError:
                raise DotParseError(
                    f"Unmatched ']' on line:\n  {repr(nodeLine)}"
                )
            hasAttrs = parseSimpleDotAttrs(
                stripped[attrStart:]
            )
            stripped = stripped[:attrStart].rstrip()

        if ' ' in stripped:
            raise DotParseError(
                f"Unquoted multi-word node on line:\n  {repr(nodeLine)}"
            )
        else:
            nodeName = stripped

    try:
        nodeID = int(nodeName)
    except ValueError:
        raise DotParseError(
            f"Node name f{repr(nodeName)} is not an integer on"
            f" line:\n {repr(nodeLine)}"
        )

    return (nodeID, hasAttrs)


def parseDotAttr(attrLine: str) -> Tuple[str, str]:
    """
    Given a line of text from a `graphviz` dot-format graph, parses
    it as an attribute (maybe-quoted-attr-name =
    maybe-quoted-attr-value). Returns the (maybe-unquoted) attr-name
    and the (maybe-unquoted) attr-value as a pair of strings. Raises
    a `DotParseError` if the line cannot be parsed as an attribute.
    Examples:

    >>> parseDotAttr("a=b")
    ('a', 'b')
    >>> parseDotAttr("  a = b ")
    ('a', 'b')
    >>> parseDotAttr('"a" = "b"')
    ('a', 'b')
    >>> parseDotAttr('"a" -> "b"')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotAttr('"a" = "b" c')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotAttr('a')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotAttr('')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotAttr('0 [ name="A" ]')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    """
    stripped = attrLine.lstrip()
    if len(stripped) == 0:
        raise DotParseError(
            "Empty attribute in dot graph on line:\n  {repr(attrLine)}"
        )
    if stripped.endswith(']') or stripped.endswith('['):
        raise DotParseError(
            f"Node attribute ends in '[' or ']' on line:"
            f"\n  {repr(attrLine)}"
        )
    if stripped.startswith('"'):
        try:
            attrName, rest = utils.unquoted(stripped)
        except ValueError:
            raise DotParseError(
                f"Unmatched quotes in line:\n  {repr(attrLine)}"
            )
        rest = rest.lstrip()
        if len(rest) == 0 or rest[0] != '=':
            raise DotParseError(
                f"No equals sign following attribute name on"
                f" line:\n  {repr(attrLine)}"
            )
        rest = rest[1:].lstrip()
    else:
        try:
            eqInd = stripped.index('=')
        except ValueError:
            raise DotParseError(
                f"No equals sign in attribute line:"
                f"\n  {repr(attrLine)}"
            )
        attrName = stripped[:eqInd].rstrip()
        rest = stripped[eqInd + 1:].lstrip()

    if rest[0] == '"':
        try:
            attrVal, rest = utils.unquoted(rest)
        except ValueError:
            raise DotParseError(
                f"Unmatched quotes in line:\n  {repr(attrLine)}"
            )
        if rest.strip():
            raise DotParseError(
                f"Junk after attribute on line:"
                f"\n  {repr(attrLine)}"
            )
    else:
        attrVal = rest.rstrip()

    return attrName, attrVal


def parseDotEdge(edgeLine: str) -> Tuple[int, int, bool]:
    """
    Given a line of text from a `graphviz` dot-format graph, parses
    it as an edge (fromID -> toID). Returns a tuple containing the
    from ID, the to ID, and a boolean indicating whether attributes
    follow the edge on subsequent lines (true if the line ends with
    '['). Raises a `DotParseError` if the line cannot be parsed as
    an edge pair. Examples:

    >>> parseDotEdge("1 -> 2")
    (1, 2, False)
    >>> parseDotEdge("  1 -> 2 ")
    (1, 2, False)
    >>> parseDotEdge('"1" -> "2"')
    (1, 2, False)
    >>> parseDotEdge('"1" -> "2" [')
    (1, 2, True)
    >>> parseDotEdge("a -> b")
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotEdge('"1" = "1"')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotEdge('"1" -> "2" c')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotEdge('1')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotEdge('')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    """
    stripped = edgeLine.lstrip()
    if len(stripped) == 0:
        raise DotParseError(
            "Empty edge in dot graph on line:\n  {repr(edgeLine)}"
        )
    if stripped.startswith('"'):
        try:
            fromStr, rest = utils.unquoted(stripped)
        except ValueError:
            raise DotParseError(
                f"Unmatched quotes in line:\n  {repr(edgeLine)}"
            )
        rest = rest.lstrip()
        if rest[:2] != '->':
            raise DotParseError(
                f"No arrow sign following source name on"
                f" line:\n  {repr(edgeLine)}"
            )
        rest = rest[2:].lstrip()
    else:
        try:
            arrowInd = stripped.index('->')
        except ValueError:
            raise DotParseError(
                f"No arrow in edge line:"
                f"\n  {repr(edgeLine)}"
            )
        fromStr = stripped[:arrowInd].rstrip()
        rest = stripped[arrowInd + 2:].lstrip()
        if ' ' in fromStr:
            raise DotParseError(
                f"Unquoted multi-word edge source on line:"
                f"\n  {repr(edgeLine)}"
            )

    hasAttrs = False
    if rest[0] == '"':
        try:
            toStr, rest = utils.unquoted(rest)
        except ValueError:
            raise DotParseError(
                f"Unmatched quotes in line:\n  {repr(edgeLine)}"
            )
        stripped = rest.strip()
        if stripped == '[':
            hasAttrs = True
        elif stripped:
            raise DotParseError(
                f"Junk after edge on line:"
                f"\n  {repr(edgeLine)}"
            )
    else:
        toStr = rest.rstrip()
        if toStr.endswith('['):
            toStr = toStr[:-1].rstrip()
            hasAttrs = True
        if ' ' in toStr:
            raise DotParseError(
                f"Unquoted multi-word edge destination on line:"
                f"\n  {repr(edgeLine)}"
            )

    try:
        fromID = int(fromStr)
    except ValueError:
        raise DotParseError(
            f"Invalid 'from' ID: {repr(fromStr)} on line:"
            f"\n  {repr(edgeLine)}"
        )

    try:
        toID = int(toStr)
    except ValueError:
        raise DotParseError(
            f"Invalid 'to' ID: {repr(toStr)} on line:"
            f"\n  {repr(edgeLine)}"
        )

    return (fromID, toID, hasAttrs)


def parseDotAttrList(
    lines: List[str]
) -> Tuple[List[Tuple[str, str]], List[str]]:
    """
    Given a list of lines of text from a `graphviz` dot-format
    graph which starts with an attribute line, parses multiple
    attribute lines until a line containing just ']' is found.
    Returns a list of the parsed name/value attribute pair tuples,
    along with a list of remaining unparsed strings (not counting
    the closing ']' line). Raises a `DotParseError` if it finds a
    non-attribute line or if it fails to find a closing ']' line.
    Examples:

    >>> parseDotAttrList([
    ...     'a=b\\n',
    ...     'c=d\\n',
    ...     ']\\n',
    ... ])
    ([('a', 'b'), ('c', 'd')], [])
    >>> parseDotAttrList([
    ...     'a=b',
    ...     'c=d',
    ...     '  ]',
    ...     'more',
    ...     'lines',
    ... ])
    ([('a', 'b'), ('c', 'd')], ['more', 'lines'])
    >>> parseDotAttrList([
    ...     'a=b',
    ...     'c=d',
    ... ])
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    """
    index = 0
    found = []
    while index < len(lines):
        thisLine = lines[index]
        try:
            found.append(parseDotAttr(thisLine))
        except DotParseError:
            if thisLine.strip() == ']':
                return (found, lines[index + 1:])
            else:
                raise DotParseError(
                    f"Could not parse attribute from line:"
                    f"\n  {repr(thisLine)}"
                    f"\nAttributes block starts on line:"
                    f"\n  {repr(lines[0])}"
                )
        index += 1

    raise DotParseError(
        f"No list terminator (']') for attributes starting on line:"
        f"\n  {repr(lines[0])}"
    )


def parseDotSubgraphStart(line: str) -> str:
    """
    Parses the start of a subgraph from a line of a graph file. The
    line must start with the word 'subgraph' and then have a name,
    followed by a '{' at the end of the line. Raises a
    `DotParseError` if this format doesn't match. Examples:

    >>> parseDotSubgraphStart('subgraph A {')
    'A'
    >>> parseDotSubgraphStart('subgraph A B {')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    >>> parseDotSubgraphStart('subgraph "A B" {')
    'A B'
    >>> parseDotSubgraphStart('subgraph A')
    Traceback (most recent call last):
    ...
    exploration.parsing.DotParseError...
    """
    stripped = line.strip()
    if len(stripped) == 0:
        raise DotParseError(
            f"Empty line where subgraph was expected:"
            f"\n  {repr(line)}"
        )

    if not stripped.startswith('subgraph '):
        raise DotParseError(
            f"Subgraph doesn't start with 'subgraph' on line:"
            f"\n  {repr(line)}"
        )

    stripped = stripped[9:]
    if stripped.startswith('"'):
        try:
            name, rest = utils.unquoted(stripped)
        except ValueError:
            raise DotParseError(
                f"Malformed quotes on subgraph line:\n {repr(line)}"
            )
        if rest.strip() != '{':
            raise DotParseError(
                f"Junk or missing '{{' on subgraph line:\n {repr(line)}"
            )
    else:
        parts = stripped.split()
        if len(parts) != 2 or parts[1] != '{':
            raise DotParseError(
                f"Junk or missing '{{' on subgraph line:\n {repr(line)}"
            )
        name, _ = parts

    return name


def parseDotGraphContents(
    lines: List[str]
) -> Tuple[ParsedDotGraph, List[str]]:
    """
    Given a list of lines from a `graphviz` dot-format string,
    parses the list as the contents of a graph (or subgraph),
    stopping when it reaches a line that just contains '}'. Raises a
    `DotParseError` if it cannot do so or if the terminator is
    missing. Returns a tuple containing the parsed graph data (see
    `ParsedDotGraph` and the list of remaining lines after the
    terminator. Recursively parses subgraphs. Example:

    >>> bits = parseDotGraphContents([
    ...     '"graph attr"=1',
    ...     '1 [',
    ...     '  attr=value',
    ...     ']',
    ...     '1 -> 2 [',
    ...     '  fullLabel="to_B"',
    ...     '  quality=number',
    ...     ']',
    ...     'subgraph name {',
    ...     '  300',
    ...     '  400',
    ...     '  300 -> 400 [',
    ...     '    fullLabel=forward',
    ...     '  ]',
    ...     '}',
    ...     '}',
    ... ])
    >>> len(bits)
    2
    >>> g = bits[0]
    >>> bits[1]
    []
    >>> sorted(g.keys())
    ['attrs', 'edges', 'nodes', 'subgraphs']
    >>> g['nodes']
    [(1, [('attr', 'value')])]
    >>> g['edges']
    [(1, 2, [('fullLabel', 'to_B'), ('quality', 'number')])]
    >>> g['attrs']
    [('graph attr', '1')]
    >>> sgs = g['subgraphs']
    >>> len(sgs)
    1
    >>> len(sgs[0])
    2
    >>> sgs[0][0]
    'name'
    >>> sg = sgs[0][1]
    >>> sorted(sg.keys())
    ['attrs', 'edges', 'nodes', 'subgraphs']
    >>> sg["nodes"]
    [(300, []), (400, [])]
    >>> sg["edges"]
    [(300, 400, [('fullLabel', 'forward')])]
    >>> sg["attrs"]
    []
    >>> sg["subgraphs"]
    []
    """
    result: ParsedDotGraph = {
        'nodes': [],
        'edges': [],
        'attrs': [],
        'subgraphs': [],
    }
    index = 0
    remainder = None
    # Consider each line:
    while index < len(lines):
        # Grab line and pre-increment index
        thisLine = lines[index]
        index += 1

        # Check for } first because it could be parsed as a node
        stripped = thisLine.strip()
        if stripped == '}':
            remainder = lines[index:]
            break
        elif stripped == '':  # ignore blank lines
            continue

        # Cascading parsing attempts, since the possibilities are
        # mostly mutually exclusive.
        # TODO: Node/attr confusion with = in a node name?
        try:
            attrName, attrVal = parseDotAttr(thisLine)
            result['attrs'].append((attrName, attrVal))
        except DotParseError:
            try:
                fromNode, toNode, hasEAttrs = parseDotEdge(
                    thisLine
                )
                if hasEAttrs:
                    attrs, rest = parseDotAttrList(
                        lines[index:]
                    )
                    # Restart to process rest
                    lines = rest
                    index = 0
                else:
                    attrs = []
                result['edges'].append((fromNode, toNode, attrs))
            except DotParseError:
                try:
                    nodeName, hasNAttrs = parseDotNode(
                        thisLine
                    )
                    if hasNAttrs is True:
                        attrs, rest = parseDotAttrList(
                            lines[index:]
                        )
                        # Restart to process rest
                        lines = rest
                        index = 0
                    elif hasNAttrs:
                        attrs = hasNAttrs
                    else:
                        attrs = []
                    result['nodes'].append((nodeName, attrs))
                except DotParseError:
                    try:
                        subName = parseDotSubgraphStart(
                            thisLine
                        )
                        subStuff, rest = \
                            parseDotGraphContents(
                                lines[index:]
                            )
                        result['subgraphs'].append((subName, subStuff))
                        # Restart to process rest
                        lines = rest
                        index = 0
                    except DotParseError:
                        raise DotParseError(
                            f"Unrecognizable graph line (possibly"
                            f" beginning of unfinished structure):"
                            f"\n  {repr(thisLine)}"
                        )
    if remainder is None:
        raise DotParseError(
            f"Graph (or subgraph) is missing closing '}}'. Starts"
            f" on line:\n  {repr(lines[0])}"
        )
    else:
        return (result, remainder)


def parseDot(
    dotStr: str,
    parseFormat: ParseFormat = ParseFormat()
) -> core.DecisionGraph:
    """
    Converts a `graphviz` dot-format string into a `core.DecisionGraph`.
    A custom `ParseFormat` may be specified if desired; the default
    `ParseFormat` is used if not. Note that this relies on specific
    indentation schemes used by `toDot` so a hand-edited dot-format
    graph will probably not work. A `DotParseError` is raised if the
    provided string can't be parsed. Example

    >>> parseDotNode(' 3 [ name="A = \\\\"grate:open\\\\"" ]')
    (3, [('name', 'A = "grate:open"')])
    >>> sg = '''\
    ... subgraph __requirements__ {
    ...   3 [ name="A = \\\\"grate:open\\\\"" ]
    ...   4 [ name="B = \\\\"!(helmet)\\\\"" ]
    ...   5 [ name="C = \\\\"helmet\\\\"" ]
    ... }'''
    >>> parseDotGraphContents(sg.splitlines()[1:])
    ({'nodes': [(3, [('name', 'A = "grate:open"')]),\
 (4, [('name', 'B = "!(helmet)"')]), (5, [('name', 'C = "helmet"')])],\
 'edges': [], 'attrs': [], 'subgraphs': []}, [])
    >>> from . import core
    >>> dg = core.DecisionGraph.example('simple')
    >>> encoded = toDot(dg)
    >>> reconstructed = parseDot(encoded)
    >>> for diff in dg.listDifferences(reconstructed):
    ...     print(diff)
    >>> reconstructed == dg
    True
    >>> dg = core.DecisionGraph.example('abc')
    >>> encoded = toDot(dg)
    >>> reconstructed = parseDot(encoded)
    >>> for diff in dg.listDifferences(reconstructed):
    ...     print(diff)
    >>> reconstructed == dg
    True
    >>> tg = core.DecisionGraph()
    >>> tg.addDecision('A')
    0
    >>> tg.addDecision('B')
    1
    >>> tg.addTransition('A', 'up', 'B', 'down')
    >>> same = parseDot('''
    ... digraph {
    ...     0 [ name=A ]
    ...       0 -> 1 [
    ...         label=up
    ...         fullLabel=up
    ...         reciprocal=down
    ...       ]
    ...     1 [ name=B ]
    ...       1 -> 0 [
    ...         label=down
    ...         fullLabel=down
    ...         reciprocal=up
    ...       ]
    ... }''')
    >>> for diff in tg.listDifferences(same):
    ...     print(diff)
    >>> same == tg
    True
    >>> pf = ParseFormat()
    >>> tg.setTransitionRequirement('A', 'up', pf.parseRequirement('one|two'))
    >>> tg.setConsequence(
    ...     'B',
    ...     'down',
    ...     [base.effect(gain="one")]
    ... )
    >>> test = parseDot('''
    ...   digraph {
    ...     0 [ name="A = \\\\"one|two\\\\"" ]
    ...   }
    ... ''')
    >>> list(test.nodes)
    [0]
    >>> test.nodes[0]['name']
    'A = "one|two"'
    >>> eff = (
    ...   r'"A = \\"[{\\\\\\"type\\\\\\": \\\\\\"gain\\\\\\",'
    ...   r' \\\\\\"applyTo\\\\\\": \\\\\\"active\\\\\\",'
    ...   r' \\\\\\"value\\\\\\": \\\\\\"one\\\\\\",'
    ...   r' \\\\\\"charges\\\\\\": null, \\\\\\"hidden\\\\\\": false,'
    ...   r' \\\\\\"delay\\\\\\": null}]\\""'
    ... )
    >>> utils.unquoted(eff)[1]
    ''
    >>> test2 = parseDot(
    ...     'digraph {\\n 0 [ name=' + eff + ' ]\\n}'
    ... )
    >>> s = test2.nodes[0]['name']
    >>> s[:25]
    'A = "[{\\\\"type\\\\": \\\\"gain\\\\"'
    >>> s[25:50]
    ', \\\\"applyTo\\\\": \\\\"active\\\\"'
    >>> s[50:70]
    ', \\\\"value\\\\": \\\\"one\\\\"'
    >>> s[70:89]
    ', \\\\"charges\\\\": null'
    >>> s[89:108]
    ', \\\\"hidden\\\\": false'
    >>> s[108:]
    ', \\\\"delay\\\\": null}]"'
    >>> ae = s[s.index('=') + 1:].strip()
    >>> uq, after = utils.unquoted(ae)
    >>> after
    ''
    >>> fromJSON(uq) == [base.effect(gain="one")]
    True
    >>> same = parseDot('''
    ... digraph {
    ...   0 [ name=A ]
    ...     0 -> 1 [
    ...       label=up
    ...       fullLabel=up
    ...       reciprocal=down
    ...       req=A
    ...     ]
    ...   1 [ name=B ]
    ...     1 -> 0 [
    ...       label=down
    ...       fullLabel=down
    ...       reciprocal=up
    ...       consequence=A
    ...     ]
    ...   subgraph __requirements__ {
    ...     2 [ name="A = \\\\"one|two\\\\"" ]
    ...   }
    ...   subgraph __consequences__ {
    ...     3 [ name=''' + eff + ''' ]
    ...   }
    ... }''')
    >>> c = {'tags': {}, 'annotations': [], 'reciprocal': 'up', 'consequence': [{'type': 'gain', 'applyTo': 'active', 'value': 'one', 'delay': None, 'charges': None}]}['consequence']  # noqa

    >>> for diff in tg.listDifferences(same):
    ...     print(diff)
    >>> same == tg
    True
    """
    lines = dotStr.splitlines()
    while lines[0].strip() == '':
        lines.pop(0)
    if lines.pop(0).strip() != "digraph {":
        raise DotParseError("Input doesn't begin with 'digraph {'.")

    # Create our result
    result = core.DecisionGraph()

    # Parse to intermediate graph data structure
    graphStuff, remaining = parseDotGraphContents(lines)
    if remaining:
        if len(remaining) <= 4:
            junk = '\n  '.join(repr(line) for line in remaining)
        else:
            junk = '\n  '.join(repr(line) for line in remaining[:4])
            junk += '\n  ...'
        raise DotParseError("Extra junk after graph:\n  {junk}")

    # Sort out subgraphs to find legends
    zoneSubs = []
    reqLegend = None
    consequenceLegend = None
    mechanismLegend = None
    for sub in graphStuff['subgraphs']:
        if sub[0] == '__requirements__':
            reqLegend = sub[1]
        elif sub[0] == '__consequences__':
            consequenceLegend = sub[1]
        elif sub[0] == '__mechanisms__':
            mechanismLegend = sub[1]
        else:
            zoneSubs.append(sub)

    # Build out our mapping from requirement abbreviations to actual
    # requirement objects
    reqMap: Dict[str, base.Requirement] = {}
    if reqLegend is not None:
        if reqLegend['edges']:
            raise DotParseError(
                f"Requirements legend subgraph has edges:"
                f"\n  {repr(reqLegend['edges'])}"
                f"\n(It should only have nodes.)"
            )
        if reqLegend['attrs']:
            raise DotParseError(
                f"Requirements legend subgraph has attributes:"
                f"\n  {repr(reqLegend['attrs'])}"
                f"\n(It should only have nodes.)"
            )
        if reqLegend['subgraphs']:
            raise DotParseError(
                f"Requirements legend subgraph has subgraphs:"
                f"\n  {repr(reqLegend['subgraphs'])}"
                f"\n(It should only have nodes.)"
            )
        for node, attrs in reqLegend['nodes']:
            if not attrs:
                raise DotParseError(
                    f"Node in requirements legend missing attributes:"
                    f"\n  {repr(attrs)}"
                )
            if len(attrs) != 1:
                raise DotParseError(
                    f"Node in requirements legend has multiple"
                    f" attributes:\n  {repr(attrs)}"
                )
            reqStr = attrs[0][1]
            try:
                eqInd = reqStr.index('=')
            except ValueError:
                raise DotParseError(
                    f"Missing '=' in requirement specifier:"
                    f"\n  {repr(reqStr)}"
                )
            ab = reqStr[:eqInd].rstrip()
            encoded = reqStr[eqInd + 1:].lstrip()
            try:
                encVal, empty = utils.unquoted(encoded)
            except ValueError:
                raise DotParseError(
                    f"Invalid quoted requirement value:"
                    f"\n  {repr(encoded)}"
                )
            if empty.strip():
                raise DotParseError(
                    f"Extra junk after requirement value:"
                    f"\n  {repr(empty)}"
                )
            try:
                req = parseFormat.parseRequirement(encVal)
            except ValueError:
                raise DotParseError(
                    f"Invalid encoded requirement in requirements"
                    f" legend:\n  {repr(encVal)}"
                )
            if ab in reqMap:
                raise DotParseError(
                    f"Abbreviation '{ab}' was defined multiple"
                    f" times in requirements legend."
                )
            reqMap[ab] = req

    # Build out our mapping from consequence abbreviations to actual
    # consequence lists
    consequenceMap: Dict[str, base.Consequence] = {}
    if consequenceLegend is not None:
        if consequenceLegend['edges']:
            raise DotParseError(
                f"Consequences legend subgraph has edges:"
                f"\n  {repr(consequenceLegend['edges'])}"
                f"\n(It should only have nodes.)"
            )
        if consequenceLegend['attrs']:
            raise DotParseError(
                f"Consequences legend subgraph has attributes:"
                f"\n  {repr(consequenceLegend['attrs'])}"
                f"\n(It should only have nodes.)"
            )
        if consequenceLegend['subgraphs']:
            raise DotParseError(
                f"Consequences legend subgraph has subgraphs:"
                f"\n  {repr(consequenceLegend['subgraphs'])}"
                f"\n(It should only have nodes.)"
            )
        for node, attrs in consequenceLegend['nodes']:
            if not attrs:
                raise DotParseError(
                    f"Node in consequence legend missing attributes:"
                    f"\n  {repr(attrs)}"
                )
            if len(attrs) != 1:
                raise DotParseError(
                    f"Node in consequences legend has multiple"
                    f" attributes:\n  {repr(attrs)}"
                )
            consStr = attrs[0][1]
            try:
                eqInd = consStr.index('=')
            except ValueError:
                raise DotParseError(
                    f"Missing '=' in consequence string:"
                    f"\n  {repr(consStr)}"
                )
            ab = consStr[:eqInd].rstrip()
            encoded = consStr[eqInd + 1:].lstrip()
            try:
                encVal, empty = utils.unquoted(encoded)
            except ValueError:
                raise DotParseError(
                    f"Invalid quoted consequence value:"
                    f"\n  {repr(encoded)}"
                )
            if empty.strip():
                raise DotParseError(
                    f"Extra junk after consequence value:"
                    f"\n  {repr(empty)}"
                )
            try:
                consequences = fromJSON(encVal)
            except json.decoder.JSONDecodeError:
                raise DotParseError(
                    f"Invalid encoded consequence in requirements"
                    f" legend:\n  {repr(encVal)}"
                )
            if ab in consequenceMap:
                raise DotParseError(
                    f"Abbreviation '{ab}' was defined multiple"
                    f" times in effects legend."
                )
            consequenceMap[ab] = consequences

    # Reconstruct mechanisms
    if mechanismLegend is not None:
        if mechanismLegend['edges']:
            raise DotParseError(
                f"Mechanisms legend subgraph has edges:"
                f"\n  {repr(mechanismLegend['edges'])}"
                f"\n(It should only have nodes.)"
            )
        if mechanismLegend['attrs']:
            raise DotParseError(
                f"Mechanisms legend subgraph has attributes:"
                f"\n  {repr(mechanismLegend['attrs'])}"
                f"\n(It should only have nodes.)"
            )
        if mechanismLegend['subgraphs']:
            raise DotParseError(
                f"Mechanisms legend subgraph has subgraphs:"
                f"\n  {repr(mechanismLegend['subgraphs'])}"
                f"\n(It should only have nodes.)"
            )
        for node, attrs in mechanismLegend['nodes']:
            if not attrs:
                raise DotParseError(
                    f"Node in mechanisms legend missing attributes:"
                    f"\n  {repr(attrs)}"
                )
            if len(attrs) != 1:
                raise DotParseError(
                    f"Node in mechanisms legend has multiple"
                    f" attributes:\n  {repr(attrs)}"
                )
            mechStr = attrs[0][1]
            try:
                atInd = mechStr.index('@')
                colonInd = mechStr.index(':')
            except ValueError:
                raise DotParseError(
                    f"Missing '@' or ':' in mechanism string:"
                    f"\n  {repr(mechStr)}"
                )
            if atInd > colonInd:
                raise DotParseError(
                    f"':' after '@' in mechanism string:"
                    f"\n  {repr(mechStr)}"
                )
            mID: base.MechanismID
            where: Optional[base.DecisionID]
            mName: base.MechanismName
            try:
                mID = int(mechStr[:atInd].rstrip())
            except ValueError:
                raise DotParseError(
                    f"Invalid mechanism ID in mechanism string:"
                    f"\n  {repr(mechStr)}"
                )
            try:
                whereStr = mechStr[atInd + 1:colonInd].strip()
                if whereStr == "None":
                    where = None
                else:
                    where = int(whereStr)
            except ValueError:
                raise DotParseError(
                    f"Invalid mechanism location in mechanism string:"
                    f"\n  {repr(mechStr)}"
                )
            mName, rest = utils.unquoted(mechStr[colonInd + 1:].lstrip())
            if rest.strip():
                raise DotParseError(
                    f"Junk after mechanism name in mechanism string:"
                    f"\n  {repr(mechStr)}"
                )
            result.mechanisms[mID] = (where, mName)
            if where is None:
                result.globalMechanisms[mName] = mID

    # Add zones to the graph based on parent info
    # Map from zones to children we should add to them once all
    # zones are created:
    zoneChildMap: Dict[str, List[str]] = {}
    for prefixedName, graphData in zoneSubs:
        # Chop off cluster_ or _ prefix:
        zoneName = prefixedName[prefixedName.index('_') + 1:]
        if graphData['edges']:
            raise DotParseError(
                f"Zone subgraph for zone {repr(zoneName)} has edges:"
                f"\n  {repr(graphData['edges'])}"
                f"\n(It should only have nodes and attributes.)"
            )
        if graphData['subgraphs']:
            raise DotParseError(
                f"Zone subgraph for zone {repr(zoneName)} has"
                f" subgraphs:"
                f"\n  {repr(graphData['subgraphs'])}"
                f"\n(It should only have nodes and attributes.)"
            )
        # Note: we ignore nodes as that info is used for
        # visualization but is redundant with the zone parent info
        # stored in nodes, and it would be tricky to tease apart
        # direct vs. indirect relationships from merged info.
        parents = None
        level = None
        for attr, aVal in graphData['attrs']:
            if attr == 'parents':
                try:
                    parents = set(fromJSON(aVal))
                except json.decoder.JSONDecodeError:
                    raise DotParseError(
                        f"Invalid parents JSON in zone subgraph for"
                        f" zone '{zoneName}':\n  {repr(aVal)}"
                    )
            elif attr == 'level':
                try:
                    level = int(aVal)
                except ValueError:
                    raise DotParseError(
                        f"Invalid level in zone subgraph for"
                        f" zone '{zoneName}':\n  {repr(aVal)}"
                    )
            elif attr == 'label':
                pass  # name already extracted from the subgraph name

            else:
                raise DotParseError(
                    f"Unexpected attribute '{attr}' in zone"
                    f" subgraph for zone '{zoneName}'"
                )
        if parents is None:
            raise DotParseError(
                f"No parents attribute for zone '{zoneName}'."
                f" Graph is:\n  {repr(graphData)}"
            )
        if level is None:
            raise DotParseError(
                f"No level attribute for zone '{zoneName}'."
                f" Graph is:\n  {repr(graphData)}"
            )

        # Add ourself to our parents in the child map
        for parent in parents:
            zoneChildMap.setdefault(parent, []).append(zoneName)

        # Create this zone
        result.createZone(zoneName, level)

    # Add zone parent/child relationships
    for parent, children in zoneChildMap.items():
        for child in children:
            result.addZoneToZone(child, parent)

    # Add nodes to the graph
    for (node, attrs) in graphStuff['nodes']:
        name: Optional[str] = None
        annotations = []
        tags: Dict[base.Tag, base.TagValue] = {}
        zones = []
        for attr, aVal in attrs:
            if attr == 'name':  # it's the name
                name = aVal
            elif attr.startswith('t_'):  # it's a tag
                tagName = attr[2:]
                try:
                    tagAny = fromJSON(aVal)
                except json.decoder.JSONDecodeError:
                    raise DotParseError(
                        f"Error in JSON for tag attr '{attr}' of node"
                        f" '{node}'"
                    )
                if isinstance(tagAny, base.TagValueTypes):
                    tagVal: base.TagValue = cast(base.TagValue, tagAny)
                else:
                    raise DotParseError(
                        f"JSON for tag value encodes disallowed tag"
                        f" value of type {type(tagAny)}. Value is:"
                        f"\n  {repr(tagAny)}"
                    )
                tags[tagName] = tagVal
            elif attr.startswith('z_'):  # it's a zone
                zones.append(attr[2:])
            elif attr == 'annotations':  # It's the annotations
                try:
                    annotations = fromJSON(aVal)
                except json.decoder.JSONDecodeError:
                    raise DotParseError(
                        f"Bad JSON in attribute '{attr}' of node"
                        f" '{node}'"
                    )
            else:
                raise DotParseError(
                    f"Unrecognized node attribute '{attr}' for node"
                    f" '{node}'"
                )

        # TODO: Domains here?
        if name is None:
            raise DotParseError(f"Node '{node}' does not have a name.")

        result.addIdentifiedDecision(
            node,
            name,
            tags=tags,
            annotations=annotations
        )
        for zone in zones:
            try:
                result.addDecisionToZone(node, zone)
            except core.MissingZoneError:
                raise DotParseError(
                    f"Zone '{zone}' for node {node} does not"
                    f" exist."
                )

    # Add mechanisms to each node:
    for (mID, (where, mName)) in result.mechanisms.items():
        mPool = result.nodes[where].setdefault('mechanisms', {})
        if mName in mPool:
            raise DotParseError(
                f"Multiple mechanisms named {mName!r} at"
                f" decision {where}."
            )
        mPool[mName] = mID

    # Reciprocals to double-check once all edges are added
    recipChecks: Dict[
        Tuple[base.DecisionID, base.Transition],
        base.Transition
    ] = {}

    # Add each edge
    for (source, dest, attrs) in graphStuff['edges']:
        annotations = []
        tags = {}
        label = None
        requirements = None
        consequence = None
        reciprocal = None
        for attr, aVal in attrs:
            if attr.startswith('t_'):
                try:
                    tags[attr[2:]] = fromJSON(aVal)
                except json.decoder.JSONDecodeError:
                    raise DotParseError(
                        f"Invalid JSON in edge tag '{attr}' for edge"
                        f"from '{source}' to '{dest}':"
                        f"\n  {repr(aVal)}"
                    )
            elif attr == "label":  # We ignore the short-label
                pass
            elif attr == "fullLabel":  # This is our transition name
                label = aVal
            elif attr == "reciprocal":
                reciprocal = aVal
            elif attr == "req":
                reqAbbr = aVal
                if reqAbbr not in reqMap:
                    raise DotParseError(
                        f"Edge from '{source}' to '{dest}' has"
                        f" requirement abbreviation '{reqAbbr}'"
                        f" but that abbreviation was not listed"
                        f" in the '__requirements__' subgraph."
                    )
                requirements = reqMap[reqAbbr]
            elif attr == "consequence":
                consequenceAbbr = aVal
                if consequenceAbbr not in reqMap:
                    raise DotParseError(
                        f"Edge from '{source}' to '{dest}' has"
                        f" consequence abbreviation"
                        f" '{consequenceAbbr}' but that"
                        f" abbreviation was not listed in the"
                        f" '__consequences__' subgraph."
                    )
                consequence = consequenceMap[consequenceAbbr]
            elif attr == "annotations":
                try:
                    annotations = fromJSON(aVal)
                except json.decoder.JSONDecodeError:
                    raise DotParseError(
                        f"Invalid JSON in edge annotations for"
                        f" edge from '{source}' to '{dest}':"
                        f"\n  {repr(aVal)}"
                    )
            else:
                raise DotParseError(
                    f"Unrecognized edge attribute '{attr}' for edge"
                    f" from '{source}' to '{dest}'"
                )

        if label is None:
            raise DotParseError(
                f"Edge from '{source}' to '{dest}' is missing"
                f" a 'fullLabel' attribute."
            )

        # Add the requested transition
        result.addTransition(
            source,
            label,
            dest,
            tags=tags,
            annotations=annotations,
            requires=requirements,  # None works here
            consequence=consequence  # None works here
        )
        # Either we're first or our reciprocal is, so this will only
        # trigger for one of the pair
        if reciprocal is not None:
            recipDest = result.getDestination(dest, reciprocal)
            if recipDest is None:
                recipChecks[(source, label)] = reciprocal
                # we'll get set as a reciprocal when that edge is
                # instantiated, we hope, but let's check that later
            elif recipDest != source:
                raise DotParseError(
                    f"Transition '{label}' from '{source}' to"
                    f" '{dest}' lists reciprocal '{reciprocal}'"
                    f" but that transition from '{dest}' goes to"
                    f" '{recipDest}', not '{source}'."
                )
            else:
                # At this point we know the reciprocal edge exists
                # and has the appropriate destination (our source).
                # No need to check for a pre-existing reciprocal as
                # this edge is newly created and cannot already have
                # a reciprocal assigned.
                result.setReciprocal(source, label, reciprocal)

    # Double-check skipped reciprocals
    for ((source, transition), reciprocal) in recipChecks.items():
        actual = result.getReciprocal(source, transition)
        if actual != reciprocal:
            raise DotParseError(
                f"Transition '{transition}' from '{source}' was"
                f" expecting to have reciprocal '{reciprocal}' but"
                f" all edges have been processed and its reciprocal"
                f" is {repr(actual)}."
            )

    # Finally get graph-level attribute values
    for (name, value) in graphStuff['attrs']:
        if name == "unknownCount":
            try:
                result.unknownCount = int(value)
            except ValueError:
                raise DotParseError(
                    f"Invalid 'unknownCount' value {repr(value)}."
                )
        elif name == "nextID":
            try:
                result.nextID = int(value)
            except ValueError:
                raise DotParseError(
                    f"Invalid 'nextID' value:"
                    f"\n  {repr(value)}"
                )
            collisionCourse = [x for x in result if x >= result.nextID]
            if len(collisionCourse) > 0:
                raise DotParseError(
                    f"Next ID {value} is wrong because the graph"
                    f" already contains one or more node(s) with"
                    f" ID(s) that is/are at least that large:"
                    f" {collisionCourse}"
                )
        elif name == "nextMechanismID":
            try:
                result.nextMechanismID = int(value)
            except ValueError:
                raise DotParseError(
                    f"Invalid 'nextMechanismID' value:"
                    f"\n  {repr(value)}"
                )
        elif name in (
            "zoneTagDicts",
            "equivalences",
            "reversionTypes",
            "mechanisms",
            "globalMechanisms",
            "nameLookup"
        ):
            try:
                setattr(result, name, fromJSON(value))
            except json.decoder.JSONDecodeError:
                raise DotParseError(
                    f"Invalid JSON in '{name}' attribute:"
                    f"\n  {repr(value)}"
                )
        else:
            raise DotParseError(
                f"Graph has unexpected attribute '{name}'."
            )

    # Final check for mechanism ID value after both mechanism ID and
    # mechanisms dictionary have been parsed:
    leftBehind = [
        x
        for x in result.mechanisms
        if x >= result.nextMechanismID
    ]
    if len(leftBehind) > 0:
        raise DotParseError(
            f"Next mechanism ID {value} is wrong because"
            f" the graph already contains one or more"
            f" node(s) with ID(s) that is/are at least that"
            f" large: {leftBehind}"
        )

    # And we're done!
    return result


def toDot(
    graph: core.DecisionGraph,
    clusterLevels: Union[str, List[int]] = [0]
) -> str:
    """
    Converts the decision graph into a "dot"-format string suitable
    for processing by `graphviz`.

    See [the dot language
    specification](https://graphviz.org/doc/info/lang.html) for more
    detail on the syntax we convert to.

    If `clusterLevels` is given, it should be either the string '*',
    or a list of integers. '*' means that all zone levels should be
    cluster-style subgraphs, while a list of integers specifies that
    zones at those levels should be cluster-style subgraphs. This
    will prefix the subgraph names with 'cluster_' instead of just
    '_'.

    TODO: Check edge cases for quotes in capability names, tag names,
    transition names, annotations, etc.

    TODO: Spaces in decision/transition names? Other special
    characters in those names?
    """
    # Set up result including unknownCount and nextID
    result = (
        f"digraph {{"
        f"\n  unknownCount={graph.unknownCount}"
        f"\n  nextID={graph.nextID}"
        f"\n  nextMechanismID={graph.nextMechanismID}"
        f"\n"
    )

    # Dictionaries for using letters to substitute for unique
    # requirements/consequences found throughout the graph. Keys are
    # quoted requirement or consequence reprs, and values are
    # abbreviation strings for them.
    currentReqKey = utils.nextAbbrKey(None)
    currentEffectKey = utils.nextAbbrKey(None)
    reqKeys: Dict[str, str] = {}
    consequenceKeys: Dict[str, str] = {}

    # Add all decision and transition info
    decision: base.DecisionID  # TODO: Fix Multidigraph type stubs
    for decision in graph.nodes:
        nodeInfo = graph.nodes[decision]
        tags = nodeInfo.get('tags', {})
        annotations = toJSON(nodeInfo.get('annotations', []))
        zones = nodeInfo.get('zones', set())
        nodeAttrs = f"\n    name={utils.quoted(nodeInfo['name'])}"
        for tag, value in tags.items():
            rep = utils.quoted(toJSON(value))
            nodeAttrs += f"\n    t_{tag}={rep}"
        for z in sorted(zones):
            nodeAttrs += f"\n    z_{z}=1"
        if annotations:
            nodeAttrs += '\n    annotations=' + utils.quoted(annotations)

        result += f'\n  {decision} [{nodeAttrs}\n  ]'

        for (transition, destination) in graph._byEdge[decision].items():
            edgeAttrs = (
                '\n      label='
              + utils.quoted(utils.abbr(transition))
            )
            edgeAttrs += (
                '\n      fullLabel='
              + utils.quoted(transition)
            )
            reciprocal = graph.getReciprocal(decision, transition)
            if reciprocal is not None:
                edgeAttrs += (
                    '\n      reciprocal='
                  + utils.quoted(reciprocal)
                )
            info = graph.edges[
                decision,  # type:ignore
                destination,
                transition
            ]
            if 'requirement' in info:
                # Get string rep for requirement
                rep = utils.quoted(info['requirement'].unparse())
                # Get assigned abbreviation or assign one
                if rep in reqKeys:
                    ab = reqKeys[rep]
                else:
                    ab = currentReqKey
                    reqKeys[rep] = ab
                    currentReqKey = utils.nextAbbrKey(currentReqKey)
                # Add abbreviation as edge attribute
                edgeAttrs += f'\n      req={ab}'
            if 'consequence' in info:
                # Get string representation of consequences
                rep = utils.quoted(
                    toJSON(info['consequence'])
                )
                # Get abbreviation for that or assign one:
                if rep in consequenceKeys:
                    ab = consequenceKeys[rep]
                else:
                    ab = currentEffectKey
                    consequenceKeys[rep] = ab
                    currentEffectKey = utils.nextAbbrKey(
                        currentEffectKey
                    )
                # Add abbreviation as an edge attribute
                edgeAttrs += f'\n      consequence={ab}'
            for (tag, value) in info["tags"].items():
                # Get string representation of tag value
                rep = utils.quoted(toJSON(value))
                # Add edge attribute for tag
                edgeAttrs += f'\n      t_{tag}={rep}'
            if 'annotations' in info:
                edgeAttrs += (
                    '\n      annotations='
                  + utils.quoted(toJSON(info['annotations']))
                )
            result += f'\n    {decision} -> {destination}'
            result += f' [{edgeAttrs}\n    ]'

    # Add zone info as subgraph structure
    for z, zinfo in graph.zones.items():
        parents = utils.quoted(toJSON(sorted(zinfo.parents)))
        if clusterLevels == '*' or zinfo.level in clusterLevels:
            zName = "cluster_" + z
        else:
            zName = '_' + z
        zoneSubgraph = f'\n  subgraph {utils.quoted(zName)} {{'
        zoneSubgraph += f'\n    label={z}'
        zoneSubgraph += f'\n    level={zinfo.level}'
        zoneSubgraph += f'\n    parents={parents}'
        for decision in sorted(graph.allDecisionsInZone(z)):
            zoneSubgraph += f'\n    {decision}'
        zoneSubgraph += '\n  }'
        result += zoneSubgraph

    # Add equivalences, mechanisms, etc.
    for attr in [
        "zoneTagDicts",
        "equivalences",
        "reversionTypes",
        "mechanisms",
        "globalMechanisms",
        "nameLookup"
    ]:
        aRep = utils.quoted(toJSON(getattr(graph, attr)))
        result += f'\n  {attr}={aRep}'

    # Add legend subgraphs to represent abbreviations
    useID = graph.nextID
    if reqKeys:
        result += '\n  subgraph __requirements__ {'
        for rrepr, ab in reqKeys.items():
            nStr = utils.quoted(ab + ' = ' + rrepr)
            result += (
                f"\n    {useID} [ name={nStr} ]"
            )
            useID += 1
        result += '\n  }'

    if consequenceKeys:
        result += '\n  subgraph __consequences__ {'
        for erepr, ab in consequenceKeys.items():
            nStr = utils.quoted(ab + ' = ' + erepr)
            result += (
                f"\n    {useID} [ name={nStr} ]"
            )
            useID += 1
        result += '\n  }'

    if graph.mechanisms:
        result += '\n  subgraph __mechanisms__ {'
        mID: base.MechanismID
        mWhere: Optional[base.DecisionID]
        mName: base.MechanismName
        for (mID, (mWhere, mName)) in graph.mechanisms.items():
            qName = utils.quoted(mName)
            nStr = utils.quoted(f"{mID}@{mWhere}:{qName}")
            result += (
                f"\n    {useID} [ name={nStr} ]"
            )
            useID += 1
        result += '\n  }'

    result += "\n}\n"
    return result


#------#
# JSON #
#------#

T = TypeVar("T")
"Type var for `loadCustom`."


def loadCustom(stream: TextIO, loadAs: Type[T]) -> T:
    """
    Loads a new JSON-encodable object from the JSON data in the
    given text stream (e.g., a file open in read mode). See
    `CustomJSONDecoder` for details on the format and which object types
    are supported.

    This casts the result to the specified type, but errors out with a
    `TypeError` if it doesn't match.
    """
    result = json.load(stream, cls=CustomJSONDecoder)
    if isinstance(result, loadAs):
        return result
    else:
        raise TypeError(
            f"Expected to load a {loadAs} but got a {type(result)}."
        )


def saveCustom(
    toSave: Union[  # TODO: More in this union?
        base.MetricSpace,
        core.DecisionGraph,
        core.DiscreteExploration,
    ],
    stream: TextIO
) -> None:
    """
    Saves a JSON-encodable object as JSON into the given text stream
    (e.g., a file open in writing mode). See `CustomJSONEncoder` for
    details on the format and which types are supported..
    """
    json.dump(toSave, stream, cls=CustomJSONEncoder)


def toJSON(obj: Any) -> str:
    """
    Defines the standard object -> JSON operation using the
    `CustomJSONEncoder` as well as not using `sort_keys`.
    """
    return CustomJSONEncoder(sort_keys=False).encode(obj)


def fromJSON(encoded: str) -> Any:
    """
    Defines the standard JSON -> object operation using
    `CustomJSONDecoder`.
    """
    return json.loads(encoded, cls=CustomJSONDecoder)


class CustomJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder that has special protocols for handling the
    smae objects that `CustomJSONDecoder` decodes. It handles these
    objects specially so that they can be decoded back to their original
    form.

    Examples:

    >>> from . import core
    >>> tupList = [(1, 1), (2, 2)]
    >>> encTup = toJSON(tupList)
    >>> encTup
    '[{"^^d": "tuple", "values": [1, 1]}, {"^^d": "tuple", "values": [2, 2]}]'
    >>> fromJSON(encTup) == tupList
    True
    >>> dg = core.DecisionGraph.example('simple')
    >>> fromJSON(toJSON(dg)) == dg
    True
    >>> dg = core.DecisionGraph.example('abc')
    >>> zi = dg.getZoneInfo('upZone')
    >>> zi
    ZoneInfo(level=1, parents=set(), contents={'zoneA'})
    >>> zj = toJSON(zi)
    >>> zj
    '{"^^d": "namedtuple", "name": "ZoneInfo", "values":\
 {"level": 1, "parents": {"^^d": "set", "values": []},\
 "contents": {"^^d": "set", "values": ["zoneA"]}}}'
    >>> fromJSON(toJSON(zi))
    ZoneInfo(level=1, parents=set(), contents={'zoneA'})
    >>> fromJSON(toJSON(zi)) == zi
    True
    >>> toJSON({'a': 'b', 1: 2})
    '{"^^d": "dict", "items": [["a", "b"], [1, 2]]}'
    >>> toJSON(((1, 2), (3, 4)))
    '{"^^d": "tuple", "values": [{"^^d": "tuple", "values": [1, 2]},\
 {"^^d": "tuple", "values": [3, 4]}]}'
    >>> toJSON(base.effect(set=('grate', 'open')))
    '{"type": "set", "applyTo": "active",\
 "value": {"^^d": "tuple",\
 "values": [{"^^d": "namedtuple", "name": "MechanismSpecifier",\
 "values": {"domain": null, "zone": null, "decision": null, "name": "grate"}},\
 "open"]}, "delay": null, "charges": null, "hidden": false}'
    >>> j = toJSON(dg)
    >>> expected = (
    ... '{"^^d": "DecisionGraph",'
    ... ' "props": {},'
    ... ' "node_links": {"directed": true,'
    ... ' "multigraph": true,'
    ... ' "graph": {},'
    ... ' "nodes": ['
    ... '{"name": "A", "domain": "main", "tags": {},'
    ... ' "annotations": ["This is a multi-word \\\\"annotation.\\\\""],'
    ... ' "zones": {"^^d": "set", "values": ["zoneA"]},'
    ... ' "mechanisms": {"grate": 0},'
    ... ' "id": 0'
    ... '},'
    ... ' {'
    ... '"name": "B",'
    ... ' "domain": "main",'
    ... ' "tags": {"b": 1, "tag2": "\\\\"value\\\\""},'
    ... ' "annotations": [],'
    ... ' "zones": {"^^d": "set", "values": ["zoneB"]},'
    ... ' "id": 1'
    ... '},'
    ... ' {'
    ... '"name": "C",'
    ... ' "domain": "main",'
    ... ' "tags": {"aw\\\\"ful": "ha\\'ha"},'
    ... ' "annotations": [],'
    ... ' "zones": {"^^d": "set", "values": ["zoneA"]},'
    ... ' "id": 2'
    ... '}'
    ... '],'
    ... ' "links": ['
    ... '{'
    ... '"tags": {},'
    ... ' "annotations": [],'
    ... ' "reciprocal": "right",'
    ... ' "source": 0,'
    ... ' "target": 1,'
    ... ' "key": "left"'
    ... '},'
    ... ' {'
    ... '"tags": {},'
    ... ' "annotations": [],'
    ... ' "reciprocal": "up_right",'
    ... ' "requirement": {"^^d": "Requirement", "value": "grate:open"},'
    ... ' "source": 0,'
    ... ' "target": 1,'
    ... ' "key": "up_left"'
    ... '},'
    ... ' {'
    ... '"tags": {},'
    ... ' "annotations": ["Transition \\'annotation.\\'"],'
    ... ' "reciprocal": "up",'
    ... ' "source": 0,'
    ... ' "target": 2,'
    ... ' "key": "down"'
    ... '},'
    ... ' {'
    ... '"tags": {},'
    ... ' "annotations": [],'
    ... ' "reciprocal": "left",'
    ... ' "source": 1,'
    ... ' "target": 0,'
    ... ' "key": "right"'
    ... '},'
    ... ' {'
    ... '"tags": {},'
    ... ' "annotations": [],'
    ... ' "reciprocal": "up_left",'
    ... ' "requirement": {"^^d": "Requirement", "value": "grate:open"},'
    ... ' "source": 1,'
    ... ' "target": 0,'
    ... ' "key": "up_right"'
    ... '},'
    ... ' {'
    ... '"tags": {"fast": 1},'
    ... ' "annotations": [],'
    ... ' "reciprocal": "down",'
    ... ' "source": 2,'
    ... ' "target": 0,'
    ... ' "key": "up"'
    ... '},'
    ... ' {'
    ... '"tags": {},'
    ... ' "annotations": [],'
    ... ' "requirement": {"^^d": "Requirement", "value": "!(helmet)"},'
    ... ' "consequence": ['
    ... '{'
    ... '"type": "gain", "applyTo": "active", "value": "helmet",'
    ... ' "delay": null, "charges": null, "hidden": false'
    ... '},'
    ... ' {'
    ... '"type": "deactivate",'
    ... ' "applyTo": "active", "value": null,'
    ... ' "delay": 3, "charges": null, "hidden": false'
    ... '}'
    ... '],'
    ... ' "source": 2,'
    ... ' "target": 2,'
    ... ' "key": "grab_helmet"'
    ... '},'
    ... ' {'
    ... '"tags": {},'
    ... ' "annotations": [],'
    ... ' "requirement": {"^^d": "Requirement", "value": "helmet"},'
    ... ' "consequence": ['
    ... '{"type": "lose", "applyTo": "active", "value": "helmet",'
    ... ' "delay": null, "charges": null, "hidden": false},'
    ... ' {"type": "gain", "applyTo": "active",'
    ... ' "value": {"^^d": "tuple", "values": ["token", 1]},'
    ... ' "delay": null, "charges": null, "hidden": false'
    ... '},'
    ... ' {"condition":'
    ... ' {"^^d": "Requirement", "value": "token*2"},'
    ... ' "consequence": ['
    ... '{"type": "set", "applyTo": "active",'
    ... ' "value": {"^^d": "tuple", "values": ['
    ... '{"^^d": "namedtuple", "name": "MechanismSpecifier",'
    ... ' "values": {"domain": null, "zone": null, "decision": null,'
    ... ' "name": "grate"}}, "open"]},'
    ... ' "delay": null, "charges": null, "hidden": false'
    ... '},'
    ... ' {"type": "deactivate", "applyTo": "active", "value": null,'
    ... ' "delay": null, "charges": null, "hidden": false'
    ... '}'
    ... '],'
    ... ' "alternative": []'
    ... '}'
    ... '],'
    ... ' "source": 2,'
    ... ' "target": 2,'
    ... ' "key": "pull_lever"'
    ... '}'
    ... ']'
    ... '},'
    ... ' "_byEdge": {"^^d": "dict", "items":'
    ... ' [[0, {"left": 1, "up_left": 1, "down": 2}],'
    ... ' [1, {"right": 0, "up_right": 0}],'
    ... ' [2, {"up": 0, "grab_helmet": 2, "pull_lever": 2}]]},'
    ... ' "zones": {"zoneA":'
    ... ' {"^^d": "namedtuple", "name": "ZoneInfo",'
    ... ' "values": {'
    ... '"level": 0,'
    ... ' "parents": {"^^d": "set", "values": ["upZone"]},'
    ... ' "contents": {"^^d": "set", "values": [0, 2]}'
    ... '}'
    ... '},'
    ... ' "zoneB":'
    ... ' {"^^d": "namedtuple", "name": "ZoneInfo",'
    ... ' "values": {'
    ... '"level": 0,'
    ... ' "parents": {"^^d": "set", "values": []},'
    ... ' "contents": {"^^d": "set", "values": [1]}'
    ... '}'
    ... '},'
    ... ' "upZone":'
    ... ' {"^^d": "namedtuple", "name": "ZoneInfo",'
    ... ' "values": {'
    ... '"level": 1,'
    ... ' "parents": {"^^d": "set", "values": []},'
    ... ' "contents": {"^^d": "set", "values": ["zoneA"]}'
    ... '}'
    ... '}'
    ... '},'
    ... ' "unknownCount": 0,'
    ... ' "zoneTagDicts": {},'
    ... ' "equivalences": {"^^d": "dict", "items": ['
    ... '[{"^^d": "tuple", "values": [0, "open"]},'
    ... ' {"^^d": "set", "values": ['
    ... '{"^^d": "Requirement", "value": "helmet"}]}]'
    ... ']},'
    ... ' "reversionTypes": {},'
    ... ' "nextMechanismID": 1,'
    ... ' "mechanisms": {"^^d": "dict", "items": ['
    ... '[0, {"^^d": "tuple", "values": [0, "grate"]}]]},'
    ... ' "globalMechanisms": {},'
    ... ' "nameLookup": {"A": [0], "B": [1], "C": [2]}'
    ... '}'
    ... )
    >>> for i in range(len(j)):
    ...     if j[i] != expected[i:i+1]:
    ...         print(
    ...             'exp: ' + expected[i-10:i+50] + '\\ngot: ' + j[i-10:i+50]
    ...         )
    ...         break
    >>> j == expected
    True
    >>> rec = fromJSON(j)
    >>> rec.nodes == dg.nodes
    True
    >>> rec.edges == dg.edges
    True
    >>> rec.unknownCount == dg.unknownCount
    True
    >>> rec.zoneTagDicts == dg.zoneTagDicts
    True
    >>> rec.equivalences == dg.equivalences
    True
    >>> rec.reversionTypes == dg.reversionTypes
    True
    >>> rec._byEdge == dg._byEdge
    True
    >>> rec.zones == dg.zones
    True
    >>> for diff in dg.listDifferences(rec):
    ...     print(diff)
    >>> rec == dg
    True

    `base.MetricSpace` example:

    >>> ms = base.MetricSpace("test")
    >>> ms.addPoint([2, 3])
    0
    >>> ms.addPoint([2, 7, 0])
    1
    >>> ms.addPoint([2, 7])
    2
    >>> toJSON(ms) # TODO: ^^d entries here
    '{"^^d": "MetricSpace", "name": "test",\
 "points": {"^^d": "dict", "items": [[0, [2, 3]], [1, [2, 7,\
 0]], [2, [2, 7]]]}, "lastID": 2}'
    >>> ms.removePoint(0)
    >>> ms.removePoint(1)
    >>> ms.removePoint(2)
    >>> toJSON(ms)
    '{"^^d": "MetricSpace", "name": "test", "points": {}, "lastID": 2}'
    >>> ms.addPoint([5, 6])
    3
    >>> ms.addPoint([7, 8])
    4
    >>> toJSON(ms)
    '{"^^d": "MetricSpace", "name": "test",\
 "points": {"^^d": "dict", "items": [[3, [5, 6]], [4, [7, 8]]]}, "lastID": 4}'

    # TODO: more examples, including one for a DiscreteExploration
    """

    def default(self, o: Any) -> Any:
        """
        Re-writes objects for encoding. We re-write the following
        objects:

        - `set`
        - `dict` (if the keys aren't all strings)
        - `tuple`/`namedtuple`
        - `ZoneInfo`
        - `Requirement`
        - `SkillCombination`
        - `DecisionGraph`
        - `DiscreteExploration`
        - `MetricSpace`

        TODO: FeatureGraph...
        """
        if isinstance(o, list):
            return [self.default(x) for x in o]

        elif isinstance(o, set):
            return {
                '^^d': 'set',
                'values': sorted(
                    [self.default(e) for e in o],
                    key=lambda x: str(x)
                )
            }

        elif isinstance(o, dict):
            if all(isinstance(k, str) for k in o):
                return {
                    k: self.default(v)
                    for k, v in o.items()
                }
            else:
                return {
                    '^^d': 'dict',
                    'items': [
                        [self.default(k), self.default(v)]
                        for (k, v) in o.items()
                    ]
                }

        elif isinstance(o, tuple):
            if hasattr(o, '_fields') and hasattr(o, '_asdict'):
                # Named tuple
                return {
                    '^^d': 'namedtuple',
                    'name': o.__class__.__name__,
                    'values': {
                        k: self.default(v)
                        for k, v in o._asdict().items()
                    }
                }
            else:
                # Normal tuple
                return {
                    "^^d": "tuple",
                    "values": [self.default(e) for e in o]
                }

        elif isinstance(o, base.Requirement):
            return {
                '^^d': 'Requirement',
                'value': o.unparse()
            }

        elif isinstance(o, base.SkillCombination):
            return {
                '^^d': 'SkillCombination',
                'value': o.unparse()
            }

        elif isinstance(o, core.DecisionGraph):
            return {
                '^^d': 'DecisionGraph',
                'props': self.default(o.graph),  # type:ignore [attr-defined]
                'node_links': self.default(networkx.node_link_data(o)),
                '_byEdge': self.default(o._byEdge),
                'zones': self.default(o.zones),
                'unknownCount': o.unknownCount,
                'zoneTagDicts': self.default(o.zoneTagDicts),
                'equivalences': self.default(o.equivalences),
                'reversionTypes': self.default(o.reversionTypes),
                'nextMechanismID': o.nextMechanismID,
                'mechanisms': self.default(o.mechanisms),
                'globalMechanisms': self.default(o.globalMechanisms),
                'nameLookup': self.default(o.nameLookup)
            }

        elif isinstance(o, core.DiscreteExploration):
            return {
                '^^d': 'DiscreteExploration',
                'situations': self.default(o.situations)
            }

        elif isinstance(o, base.MetricSpace):
            return {
                '^^d': 'MetricSpace',
                'name': o.name,
                'points': self.default(o.points),
                'lastID': o.lastID()
            }

        else:
            return o

    def encode(self, o: Any) -> str:
        """
        Custom encode function since we need to override behavior for
        tuples and dicts.
        """
        if isinstance(o, (tuple, dict, set)):
            o = self.default(o)
        elif isinstance(o, list):
            o = [self.default(x) for x in o]

        try:
            return super().encode(o)
        except TypeError:
            return super().encode(self.default(o))

    def iterencode(
        self,
        o: Any,
        _one_shot: bool = False
    ) -> Generator[str, None, None]:
        """
        Custom iterencode function since we need to override behavior for
        tuples and dicts.
        """
        if isinstance(o, (tuple, dict)):
            o = self.default(o)

        yield from super().iterencode(o, _one_shot=_one_shot)


class CustomJSONDecoder(json.JSONDecoder):
    """
    A custom JSON decoder that has special protocols for handling
    several types, including:

    - `set`
    - `tuple` & `namedtuple`
    - `dict` (where keys aren't all strings)
    - `Requirement`
    - `SkillCombination`
    - `DecisionGraph`
    - `DiscreteExploration`
    - `MetricSpace`

    Used by `toJSON`

    When initializing it, you can st a custom parse format by supplying
    a 'parseFormat' keyword argument; by default a standard
    `ParseFormat` will be used.

    Examples:

    >>> r = base.ReqAny([
    ...     base.ReqCapability('power'),
    ...     base.ReqTokens('money', 5)
    ... ])
    >>> s = toJSON(r)
    >>> s
    '{"^^d": "Requirement", "value": "(power|money*5)"}'
    >>> l = fromJSON(s)
    >>> r == l
    True
    >>> o = {1, 2, 'hi'}
    >>> s = toJSON(o)
    >>> s
    '{"^^d": "set", "values": [1, 2, "hi"]}'
    >>> l = fromJSON(s)
    >>> o == l
    True
    >>> zi = base.ZoneInfo(1, set(), set())
    >>> s = toJSON(zi)
    >>> c = (
    ... '{"^^d": "namedtuple", "name": "ZoneInfo", "values": {'
    ... '"level": 1,'
    ... ' "parents": {"^^d": "set", "values": []},'
    ... ' "contents": {"^^d": "set", "values": []}}}'
    ... )
    >>> s == c
    True

    TODO: SkillCombination example
    """
    def __init__(self, *args, **kwargs):
        if 'object_hook' in kwargs:
            outerHook = kwargs['object_hook']
            kwargs['object_hook'] = (
                lambda o: outerHook(self.unpack(o))
            )
            # TODO: What if it's a positional argument? :(
        else:
            kwargs['object_hook'] = lambda o: self.unpack(o)

        if 'parseFormat' in kwargs:
            self.parseFormat = kwargs['parseFormat']
            del kwargs['parseFormat']
        else:
            self.parseFormat = ParseFormat()

        super().__init__(*args, **kwargs)

    def unpack(self, obj: Any) -> Any:
        """
        Unpacks an object; used as the `object_hook` for decoding.
        """
        if '^^d' in obj:
            asType = obj['^^d']
            if asType == 'tuple':
                return tuple(obj['values'])

            elif asType == 'namedtuple':
                g = globals()
                name = obj['name']
                values = obj['values']
                # Use an existing global namedtuple class if there is
                # one that goes by the specified name, so that we don't
                # create too many spurious equivalent namedtuple
                # classes. But fall back on creating a new namedtuple
                # class if we need to:
                ntClass = g.get(name)
                if (
                    ntClass is None
                 or not issubclass(ntClass, tuple)
                 or not hasattr(ntClass, '_asdict')
                ):
                    ntClass = collections.namedtuple(  # type: ignore
                        name,
                        values.keys()
                    )
                ntClass = cast(Callable, ntClass)
                return ntClass(**values)

            elif asType == 'set':
                return set(obj['values'])

            elif asType == 'dict':
                return dict(obj['items'])

            elif asType == 'Requirement':
                return self.parseFormat.parseRequirement(obj['value'])

            elif asType == 'SkillCombination':
                return self.parseFormat.parseSkillCombination(obj['value'])

            elif asType == 'Effect':
                return self.parseFormat.parseEffect(obj['value'])

            elif asType == 'Challenge':
                return self.parseFormat.parseChallenge(obj['value'])

            elif asType == 'Condition':
                return self.parseFormat.parseCondition(obj['value'])

            elif asType == 'Consequence':
                return self.parseFormat.parseConsequence(obj['value'])

            # TODO: Consequences here!

            elif asType == 'DecisionGraph':
                baseGraph: networkx.MultiDiGraph = networkx.node_link_graph(
                    obj['node_links']
                )
                graphResult = core.DecisionGraph()
                # Copy over non-internal attributes
                for attr in dir(baseGraph):
                    if attr == "name":
                        continue
                    if not attr.startswith('__') or not attr.endswith('__'):
                        val = getattr(baseGraph, attr)
                        setattr(
                            graphResult,
                            attr,
                            copy.deepcopy(val)
                        )

                if baseGraph.name != '':
                    graphResult.name = baseGraph.name
                graphResult.graph.update(obj['props'])  # type:ignore [attr-defined]  # noqa
                storedByEdge = obj['_byEdge']
                graphResult._byEdge = {
                    int(k): storedByEdge[k]
                    for k in storedByEdge
                }
                graphResult.zones = obj['zones']
                graphResult.unknownCount = obj['unknownCount']
                graphResult.zoneTagDicts = obj['zoneTagDicts']
                graphResult.equivalences = obj['equivalences']
                graphResult.reversionTypes = obj['reversionTypes']
                graphResult.nextMechanismID = obj['nextMechanismID']
                graphResult.mechanisms = {
                    int(k): v
                    for k, v in
                    obj['mechanisms'].items()
                }
                graphResult.globalMechanisms = obj['globalMechanisms']
                graphResult.nameLookup = obj['nameLookup']
                return graphResult

            elif asType == 'DiscreteExploration':
                exResult = core.DiscreteExploration()
                exResult.situations = obj['situations']
                return exResult

            elif asType == 'MetricSpace':
                msResult = base.MetricSpace(obj['name'])
                msResult.points = obj['points']
                msResult.nextID = obj['lastID'] + 1
                return msResult

            else:
                raise NotImplementedError(
                    f"No special handling has been defined for"
                    f" decoding type '{asType}'."
                )

        else:
            return obj
