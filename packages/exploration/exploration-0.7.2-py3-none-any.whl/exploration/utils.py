"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2023-12-29
- Purpose: Utility functions with no specific relevance to particular
    sub-systems.

"""

from typing import Collection, Optional, Tuple

import random

#-------------------#
# Utility functions #
#-------------------#

RANDOM_NAME_SUFFIXES = False
"""
Causes `uniqueName` to use random suffixes instead of sequential ones,
which is more efficient when many name collisions are expected but which
makes things harder to test and debug. False by default.
"""


def uniqueName(base: str, existing: Collection) -> str:
    """
    Finds a unique name relative to a collection of existing names,
    using the given base name, plus a unique suffix if that base name is
    among the existing names. If the base name isn't among the existing
    names, just returns the base name. The suffix consists of a period
    followed by a number, and the lowest unused number is used every
    time. This does lead to poor performance in cases where many
    collisions are expected; you can set `RANDOM_NAME_SUFFIXES` to True
    to use a random suffix instead.

    Note that if the base name already has a numerical suffix, that
    suffix will be changed instead of adding another one.
    """
    # Short-circuit if we're already unique
    if base not in existing:
        return base

    # Ensure a digit suffix
    if (
        '.' not in base
     or not base.split('.')[-1].isdigit()
    ):
        base += '.1'

    # Find the split point for the suffix
    # This will be the index after the '.'
    splitPoint = len(base) - list(reversed(base)).index('.')
    if not RANDOM_NAME_SUFFIXES:
        suffix = int(base[splitPoint:])

    while base in existing:
        if RANDOM_NAME_SUFFIXES:
            base = base[:splitPoint] + str(random.randint(0, 1000000))
        else:
            suffix += 1
            base = base[:splitPoint] + str(suffix)

    return base


ABBR_SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"""
The list of symbols to use, in order, for abbreviations, adding
secondary symbols when the initial list runs out. It's stored as a
string, since each item is just one letter.
"""


def nextAbbrKey(currentKey: Optional[str]) -> str:
    """
    Given an abbreviation keys, returns the next abbreviation key after
    that. Abbreviation keys are constructed using the `ABBR_SYMBOLS` as
    a base. If the argument is `None`, the first of the `ABBR_SYMBOLS`
    will be returned. For example:

    >>> nextAbbrKey(None)
    'A'
    >>> nextAbbrKey('A')
    'B'
    >>> nextAbbrKey('P')
    'Q'
    >>> nextAbbrKey('Z')
    'AA'
    >>> nextAbbrKey('AZ')
    'BA'
    >>> nextAbbrKey('BM')
    'BN'
    >>> nextAbbrKey('ZZ')
    'AAA'
    >>> nextAbbrKey('ZZZZ')
    'AAAAA'
    """
    if currentKey is None:
        return ABBR_SYMBOLS[0]
    else:
        digits = [ABBR_SYMBOLS.index(c) for c in currentKey]
        limit = len(ABBR_SYMBOLS)
        digits[-1] += 1
        i = -1
        while digits[i] >= limit:
            digits[i] = 0
            try:
                digits[i - 1] += 1
                i -= 1
            except IndexError:  # Overflow into a non-existent digit
                digits.insert(0, 0)
                break
        return ''.join(ABBR_SYMBOLS[d] for d in digits)


def abbr(string: str, length: int = 4) -> str:
    """
    Returns an abbreviated version of the given string, using at most
    the given number of characters. Creates two alternatives: a
    version without non-alphanumerics, and a version without
    non-alphanumerics or vowels (except an initial vowel). If the entire
    string fits in the given length, it just returns that. If not, and
    the version with just alphanumerics fits in the given length, or
    the version without vowels is shorter than necessary, returns the
    version with just alphanumerics, up to the given length. Otherwise,
    returns the alphanumeric version without non-initial vowels.
    Examples:

    >>> abbr('abc')
    'abc'
    >>> abbr('abcdefgh')
    'abcd'
    >>> abbr('aeiou')
    'aeio'
    >>> abbr('axyzeiou')
    'axyz'
    >>> abbr('aeiouxyz')
    'axyz'
    >>> abbr('AEIOUXYZ')
    'AXYZ'
    >>> abbr('-hi-')  # fits
    '-hi-'
    >>> abbr('--hi--')  # doesn't fit
    'hi'
    >>> abbr('A to wa')
    'Atow'
    >>> abbr('A to wor')
    'Atwr'
    """
    # Three results: all characters, all alphanumerics, and all
    # non-vowel alphanumerics (up to the given length + initial vowel)
    result1 = ''
    result2 = ''
    index = 0
    while index < len(string) and len(result1) < length:
        c = string[index]
        if not c.isalnum():
            pass
        elif c.lower() in 'aeiou' and index > 0:
            result2 += c
        else:
            result1 += c
            result2 += c
        index += 1

    # Use ~ least restricted result that's short enough
    if len(string) <= length:
        return string
    elif len(result2) <= length or len(result1) < length:
        return result2[:length]
    else:
        return result1


def quoted(string: str) -> str:
    """
    Returns a string that starts and ends with double quotes, which will
    evaluate to the given string using `eval`. Adds a layer of
    backslashes before any backslashes and/or double quotes in the
    original string. Different from `repr` because it always uses double
    quotes. Raises a `ValueError` if given a multi-line string because
    multi-line strings cannot be properly quoted using just a single
    pair of double quotes.

    >>> quoted('1\\n2')
    Traceback (most recent call last):
    ...
    ValueError...
    >>> quoted('12')
    '"12"'
    >>> quoted('back\\\\slash')
    '"back\\\\\\\\slash"'
    >>> quoted('"Yes!" she said, "it\\'s finished."')
    '"\\\\"Yes!\\\\" she said, \\\\"it\\'s finished.\\\\""'
    """
    if '\n' in string:
        raise ValueError("Cannot quote a multi-line string.")

    return '"' + string.translate({ord('"'): '\\"', ord('\\'): '\\\\'}) + '"'


def unquoted(startsQuoted: str) -> Tuple[str, str]:
    """
    Inverse of `quoted`: takes a string starting with a double quote,
    and returns the string which got quoted to become that (plus the
    leftovers after the quoted region). Parses out where the quotes end
    automatically and accumulates as leftovers any extra part of the
    string beyond that. Removes one layer of backslashes from
    everything. Raises a `ValueError` if the string does not start with
    a double quote or if it does not contain a matching double quote
    eventually.

    For example:

    >>> unquoted('abc')
    Traceback (most recent call last):
    ...
    ValueError...
    >>> unquoted('"abc')
    Traceback (most recent call last):
    ...
    ValueError...
    >>> unquoted('"abc"')
    ('abc', '')
    >>> unquoted('"a" = "b"')
    ('a', ' = "b"')
    >>> unquoted('"abc" extra')
    ('abc', ' extra')
    >>> unquoted('"abc" "extra"')
    ('abc', ' "extra"')
    >>> unquoted('"\\\\"abc\\\\""')
    ('"abc"', '')
    >>> unquoted('"back\\\\\\\\slash"')
    ('back\\\\slash', '')
    >>> unquoted('"O\\'Toole"')
    ("O'Toole", '')
    >>> unquoted('"\\\\"Yes!\\\\" she said, \\\\"it\\'s finished!\\\\""')
    ('"Yes!" she said, "it\\'s finished!"', '')
    >>> quoted(unquoted('"\\'"')[0]) == '"\\'"'
    True
    >>> unquoted(quoted('"\\'"')) == ('"\\'"', '')
    True
    """
    if not startsQuoted.startswith('"'):
        raise ValueError(
            f"No double-quote at start of string: '{startsQuoted}'"
        )
    result = ''
    leftovers = ''
    finished = False
    escaped = False
    if not startsQuoted.startswith('"'):
        raise ValueError(
            f"No starting double quote in string: {repr(startsQuoted)}"
        )
    for c in startsQuoted[1:]:
        if finished:
            leftovers += c
        elif escaped:
            escaped = False
            result += c
        elif c == '\\':
            escaped = True
        elif c == '"':
            finished = True
        else:
            result += c
    if not finished:
        raise ValueError(
            f"No matching double-quote to end string: {repr(startsQuoted)}"
        )
    else:
        return result, leftovers
