"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2023-12-27
- Purpose: Basic types that structure information used for parts of the
    core types (see `core.py`).

Besides very basic utility functions, code for dealing with these types
is defined in other files, notably `core.py` and `parsing.py`.

Defines the following base types:

- `Domain`
- `Zone`
- `DecisionID`
- `DecisionName`
- `DecisionSpecifier`
- `AnyDecisionSpecifier`
- `ZoneInfo`
- `DefaultZone`
- `Transition`
- `TransitionWithOutcomes`
- `Capability`
- `Token`
- `TokenCount`
- `Skill`
- `Level`
- `MechanismID`
- `MechanismName`
- `MechanismState`
- `CapabilitySet`
- `DomainFocalization`
- `FocalPointName`
- `ContextSpecifier`
- `FocalPointSpecifier`
- `FocalContext`
- `FocalContextName`
- `State`
- `RequirementContext`
- `Effect`
- `SkillCombination`
    - `BestSkill`
    - `WorstSkill`
    - `CombinedSkill`
    - `InverseSkill`
    - `ConditionalSkill`
- `Challenge`
- `Condition`
- `Consequence`
- `Equivalences`
- `Requirement`
    - `ReqAny`
    - `ReqAll`
    - `ReqNot`
    - `ReqCapability`
    - `ReqTokens`
    - `ReqMechanism`
    - `ReqNothing`
    - `ReqImpossible`
- `Tag`
- `TagValueTypes`
- `TagValue`
- `NoTagValue`
- `TagUpdateFunction`
- `Annotations`
- `ExplorationActionType`
- `ExplorationAction`
- `DecisionType`
- `Situation`
- `PointID`
- `Coords`
- `AnyPoint`
- `Feature`
- `FeatureID`
- `Part`
- `FeatureSpecifier`
- `AnyFeatureSpecifier`
- `MetricSpace`
- `FeatureType`
- `FeatureRelationshipType`
- `FeatureDecision`
- `FeatureAffordance`
- `FeatureEffect`
- `FeatureAction`
"""

from typing import (
    Any, Optional, List, Set, Union, Iterable, Tuple, Dict, TypedDict,
    Literal, TypeAlias, TYPE_CHECKING, cast, Callable, get_args,
    Sequence, NamedTuple, Generator
)

import copy
import random
import re
import warnings
import math

from . import commands

# `DecisionGraph` is defined in core.py, but `RequirementContext` needs to
# be defined here for a couple of reasons. Thankfully, the details of
# `DecisionGraph` don't matter here for type-checking purposes, so we
# can provide this fake definition for the type checker:
if TYPE_CHECKING:
    from .core import DecisionGraph


#---------#
# Globals #
#---------#

DEFAULT_DOMAIN: 'Domain' = 'main'
"""
Default domain value for use when a domain is needed but not specified.
"""

DEFAULT_FOCAL_CONTEXT_NAME: 'FocalContextName' = 'main'
"""
Default focal context name for use when a focal context name is needed
but not specified.
"""

DEFAULT_MECHANISM_STATE: 'MechanismState' = 'off'
"""
Default state we assume in situations where a mechanism hasn't been
assigned a state.
"""

DEFAULT_EXPLORATION_STATUS: 'ExplorationStatus' = 'noticed'
"""
Default exploration status we assume when no exploration status has been
set.
"""

DEFAULT_SAVE_SLOT: 'SaveSlot' = "slot0"
"""
Default save slot to use when saving or reverting and the slot isn't
specified.
"""


#------------#
# Base Types #
#------------#

Domain: TypeAlias = str
"""
A type alias: Domains are identified by their names.

A domain represents a separable sphere of action in a game, such as
movement in the in-game virtual space vs. movement in a menu (which is
really just another kind of virtual space). Progress along a quest or tech
tree can also be modeled as a separate domain.

Conceptually, domains may be either currently-active or
currently-inactive (e.g., when a menu is open vs. closed, or when
real-world movement is paused (or not) during menuing; see `State`). Also,
the game state stores a set of 'active' decision points for each domain.
At each particular game step, the set of options available to the player
is the union of all outgoing transitions from active nodes in each active
domain.

Each decision belongs to a single domain.
"""

Zone: 'TypeAlias' = str
"""
A type alias: A zone as part of a `DecisionGraph` is identified using
its name.

Zones contain decisions and/or other zones; one zone may be contained by
multiple other zones, but a zone may not contain itself or otherwise
form a containment loop.

Note that zone names must be globally unique within a `DecisionGraph`,
and by extension, two zones with the same name at different steps of a
`DiscreteExploration` are assumed to represent the same space.
"""

DecisionID: 'TypeAlias' = int
"""
A type alias: decision points are defined by arbitrarily assigned
unique-per-`Exploration` ID numbers.

A decision represents a location within a decision graph where a decision
can be made about where to go, or a dead-end reached by a previous
decision. Typically, one room can have multiple decision points in it,
even though many rooms have only one. Concepts like 'room' and 'area'
that group multiple decisions together (at various scales) are handled
by the idea of a `Zone`.
"""

DecisionName: 'TypeAlias' = str
"""
A type alias: decisions have names which are strings.

Two decisions might share the same name, but they can be disambiguated
because they may be in different `Zone`s, and ultimately, they will have
different `DecisionID`s.
"""


class DecisionSpecifier(NamedTuple):
    """
    A decision specifier attempts to uniquely identify a decision by
    name, rather than by ID. See `AnyDecisionSpecifier` for a type which
    can also be an ID.

    Ambiguity is possible if two decisions share the same name; the
    decision specifier provides two means of disambiguation: a domain
    may be specified, and a zone may be specified; if either is
    specified only decisions within that domain and/or zone will match,
    but of course there could still be multiple decisions that match
    those criteria that still share names, in which case many operations
    will end up raising an `AmbiguousDecisionSpecifierError`.
    """
    domain: Optional[Domain]
    zone: Optional[Zone]
    name: DecisionName


AnyDecisionSpecifier: 'TypeAlias' = Union[DecisionID, DecisionSpecifier, str]
"""
A type alias: Collects three different ways of specifying a decision: by
ID, by `DecisionSpecifier`, or by a string which will be treated as
either a `DecisionName`, or as a `DecisionID` if it can be converted to
an integer.
"""


class InvalidDecisionSpecifierError(ValueError):
    """
    An error used when a decision specifier is in the wrong format.
    """


class InvalidMechanismSpecifierError(ValueError):
    """
    An error used when a mechanism specifier is invalid.
    """


class ZoneInfo(NamedTuple):
    """
    Zone info holds a level integer (starting from 0 as the level directly
    above decisions), a set of parent zones, and a set of child decisions
    and/or zones. Zones at a particular level may only contain zones in lower
    levels, although zones at any level may also contain decisions directly.
    The norm is for zones at level 0 to contain decisions, while zones at
    higher levels contain zones from the level directly below them.

    Note that zones may have multiple parents, because one sub-zone may be
    contained within multiple super-zones.
    """
    level: int
    parents: Set[Zone]
    contents: Set[Union[DecisionID, Zone]]


class DefaultZone:
    """
    Default argument for a `Zone` when `None` is used to mean "Do not add
    to the zone you normally would."
    """
    pass


Transition: 'TypeAlias' = str
"""
A type alias: transitions are defined by their names.

A transition represents a means of travel from one decision to another.
Outgoing transition names have to be unique at each decision, but not
globally.
"""


TransitionWithOutcomes: 'TypeAlias' = Tuple[Transition, List[bool]]
"""
A type alias: a transition with an outcome attached is a tuple that has
a `Transition` and then a sequence of booleans indicating
success/failure of successive challenges attached to that transition.
Challenges encountered during application of transition effects will each
have their outcomes dictated by successive booleans in the sequence. If
the sequence is shorter than the number of challenges encountered,
additional challenges are resolved according to a `ChallengePolicy`
specified when applying effects.
TODO: Implement this, including parsing.
"""


AnyTransition: 'TypeAlias' = Union[Transition, TransitionWithOutcomes]
"""
Either a `Transition` or a `TransitionWithOutcomes`.
"""


def nameAndOutcomes(transition: AnyTransition) -> TransitionWithOutcomes:
    """
    Returns a `TransitionWithOutcomes` when given either one of those
    already or a base `Transition`. Outcomes will be an empty list when
    given a transition alone. Checks that the type actually matches.
    """
    if isinstance(transition, Transition):
        return (transition, [])
    else:
        if not isinstance(transition, tuple) or len(transition) != 2:
            raise TypeError(
                f"Transition with outcomes must be a length-2 tuple."
                f" Got: {transition!r}"
            )
        name, outcomes = transition
        if not isinstance(name, Transition):
            raise TypeError(
                f"Transition name must be a string."
                f" Got: {name!r}"
            )
        if (
            not isinstance(outcomes, list)
         or not all(isinstance(x, bool) for x in outcomes)
        ):
            raise TypeError(
                f"Transition outcomes must be a list of booleans."
                f" Got: {outcomes!r}"
            )
        return transition


Capability: 'TypeAlias' = str
"""
A type alias: capabilities are defined by their names.

A capability represents the power to traverse certain transitions. These
transitions should have a `Requirement` specified to indicate which
capability/ies and/or token(s) can be used to traverse them. Capabilities
are usually permanent, but may in some cases be temporary or be
temporarily disabled. Capabilities might also combine (e.g., speed booster
can't be used underwater until gravity suit is acquired but this is
modeled through either `Requirement` expressions or equivalences (see
`DecisionGraph.addEquivalence`).

By convention, a capability whose name starts with '?' indicates a
capability that the player considers unknown, to be filled in later via
equivalence. Similarly, by convention capabilities local to a particular
zone and/or decision will be prefixed with the name of that zone/decision
and '::' (subject to the restriction that capability names may NOT contain
the symbols '&', '|', '!', '*', '(', and ')'). Note that in most cases
zone-local capabilities can instead be `Mechanism`s, which are zone-local
by default.
"""

Token: 'TypeAlias' = str
"""
A type alias: tokens are defined by their type names.

A token represents an expendable item that can be used to traverse certain
transitions a limited number of times (normally once after which the
token is used up), or to permanently open certain transitions (perhaps
when a certain amount have been acquired).

When a key permanently opens only one specific door, or is re-usable to
open many doors, that should be represented as a `Capability`, not a
token. Only when there is a choice of which door to unlock (and the key is
then used up) should keys be represented as tokens.

Like capabilities, tokens can be unknown (names starting with '?') or may
be zone- or decision-specific (prefixed with a zone/decision name and
'::'). Also like capabilities, token names may not contain any of the
symbols '&', '|', '!', '*', '(', or ')'.
"""

TokenCount: 'TypeAlias' = int
"""
A token count is just an integer.
"""

Skill: 'TypeAlias' = str
"""
Names a skill to be used for a challenge. The agent's skill level along
with the challenge level determines the probability of success (see
`Challenge`). When an agent doesn't list a skill at all, the level is
assumed to be 0.
"""


Level: 'TypeAlias' = int
"""
A challenge or skill level is just an integer.
"""

MechanismID: 'TypeAlias' = int
"""
A type alias: mechanism IDs are integers. See `MechanismName` and
`MechanismState`.
"""

MechanismName: 'TypeAlias' = str
"""
A type alias: mechanism names are strings. See also `MechanismState`.

A mechanism represents something in the world that can be toggled or can
otherwise change state, and which may alter the requirements for
transitions and/or actions. For example, a switch that opens and closes
one or more gates. Mechanisms can be used in `Requirement`s by writing
"mechanism:state", for example, "switch:on". Each mechanism can only be
in one of its possible states at a time, so an effect that puts a
mechanism in one state removes it from all other states. Mechanism states
can be the subject of equivalences (see `DecisionGraph.addEquivalence`).

Mechanisms have `MechanismID`s and are each associated with a specific
decision (unless they are global), and when a mechanism name is
mentioned, we look for the first mechanism with that name at the current
decision, then in the lowest zone(s) containing that decision, etc. It's
an error if we find two mechanisms with the same name at the same level
of search. `DecisionGraph.addMechanism` will create a named mechanism
and assign it an ID.

By convention, a capability whose name starts with '?' indicates a
mechanism that the player considers unknown, to be filled in later via
equivalence. Mechanism names are resolved by searching incrementally
through higher and higher-level zones, then a global mechanism set and
finally in all decisions. This means that the same mechanism name can
potentially be re-used in different zones, especially when all
transitions which depend on that mechanism's state are within the same
zone.
TODO: G: for global scope?

Mechanism states are not tracked as part of `FocalContext`s but are
instead tracked as part of the `DecisionGraph` itself. If there are
mechanism-like things which operate on a per-character basis or otherwise
need to be tracked as part of focal contexts, use decision-local
`Capability` names to track them instead.
"""


class MechanismSpecifier(NamedTuple):
    """
    Specifies a mechanism either just by name, or with domain and/or
    zone and/or decision name hints.
    """
    domain: Optional[Domain]
    zone: Optional[Zone]
    decision: Optional[DecisionName]
    name: MechanismName


def mechanismAt(
    name: MechanismName,
    domain: Optional[Domain] = None,
    zone: Optional[Zone] = None,
    decision: Optional[DecisionName] = None
) -> MechanismSpecifier:
    """
    Builds a `MechanismSpecifier` using `None` default hints but
    accepting `domain`, `zone`, and/or `decision` hints.
    """
    return MechanismSpecifier(domain, zone, decision, name)


AnyMechanismSpecifier: 'TypeAlias' = Union[
    MechanismID,
    MechanismName,
    MechanismSpecifier
]
"""
Can be a mechanism ID, mechanism name, or a mechanism specifier.
"""

MechanismState: 'TypeAlias' = str
"""
A type alias: the state of a mechanism is a string. See `Mechanism`.

Each mechanism may have any number of states, but may only be in one of
them at once. Mechanism states may NOT be strings which can be
converted to integers using `int` because otherwise the 'set' effect
would have trouble figuring out whether a mechanism or item count was
being set.
"""

EffectSpecifier: 'TypeAlias' = Tuple[DecisionID, Transition, int]
"""
Identifies a particular effect that's part of a consequence attached to
a certain transition in a `DecisionGraph`. Identifies the effect based
on the transition's source `DecisionID` and `Transition` name, plus an
integer. The integer specifies the index of the effect in depth-first
traversal order of the consequence of the specified transition.

TODO: Ensure these are updated when merging/deleting/renaming stuff.
"""


class CapabilitySet(TypedDict):
    """
    Represents a set of capabilities, including boolean on/off
    `Capability` names, countable `Token`s accumulated, and
    integer-leveled skills. It has three slots:

    - 'capabilities': A set representing which `Capability`s this
        `CapabilitySet` includes.
    - 'tokens': A dictionary mapping `Token` types to integers
        representing how many of that token type this `CapabilitySet` has
        accumulated.
    - 'skills': A dictionary mapping `Skill` types to `Level` integers,
        representing what skill levels this `CapabilitySet` has.
    """
    capabilities: Set[Capability]
    tokens: Dict[Token, TokenCount]
    skills: Dict[Skill, Level]


DomainFocalization: 'TypeAlias' = Literal[
    'singular',
    'plural',
    'spreading'
]
"""
How the player experiences decisions in a domain is controlled by
focalization, which is specific to a `FocalContext` and a `Domain`:

- Typically, focalization is 'singular' and there's a particular avatar
    (or co-located group of avatars) that the player follows around, at
    each point making a decision based on the position of that avatar
    (that avatar is effectively "at" one decision in the graph). Position
    in a singular domain is represented as a single `DecisionID`. When the
    player picks a transition, this decision ID is updated to the decision
    on the other side of that transition.
- Less commonly, there can be multiple points of focalization which the
    player can freely switch between, meaning the player can at any given
    moment decide both which focal point to actually attend to, and what
    transition to take at that decision. This is called 'plural'
    focalization, and is common in tactics or strategy games where the
    player commands multiple units, although those games are often a poor
    match for decision mapping approaches. Position in a plural domain is
    represented by a dictionary mapping one or more focal-point name
    strings to single `DecisionID`s. When the player makes a decision,
    they need to specify the name of the focal point for which the
    decision is made along with the transition name at that focal point,
    and that focal point is updated to the decision on the other side of
    the chosen transition.
- Focalization can also be 'spreading' meaning that not only can the
    player pick options from one of multiple decisions, they also
    effectively expand the set of available decisions without having to
    give up access to old ones. This happens for example in a tech tree,
    where the player can invest some resource to unlock new nodes.
    Position in a spreading domain is represented by a set of
    `DecisionID`s, and when a transition is chosen, the decision on the
    other side is added to the set if it wasn't already present.
"""


FocalPointName: 'TypeAlias' = str
"""
The name of a particular focal point in 'plural' `DomainFocalization`.
"""


ContextSpecifier: 'TypeAlias' = Literal["common", "active"]
"""
Used when it's necessary to specify whether the common or the active
`FocalContext` is being referenced and/or updated.
"""


FocalPointSpecifier: 'TypeAlias' = Tuple[
    ContextSpecifier,
    Domain,
    FocalPointName
]
"""
Specifies a particular focal point by picking out whether it's in the
common or active context, which domain it's in, and the focal point name
within that domain. Only needed for domains with 'plural' focalization
(see `DomainFocalization`).
"""


class FocalContext(TypedDict):
    """
    Focal contexts identify an avatar or similar situation where the player
    has certain capabilities available (a `CapabilitySet`) and may also have
    position information in one or more `Domain`s (see `State` and
    `DomainFocalization`). Normally, only a single `FocalContext` is needed,
    but situations where the player swaps between capability sets and/or
    positions sometimes call for more.

    At each decision step, only a single `FocalContext` is active, and the
    capabilities of that context (plus capabilities of the 'common'
    context) determine what transitions are traversable. At the same time,
    the set of reachable transitions is determined by the focal context's
    per-domain position information, including its per-domain
    `DomainFocalization` type.

    The slots are:

    - 'capabilities': A `CapabilitySet` representing what capabilities,
        tokens, and skills this context has. Note that capabilities from
        the common `FocalContext` are added to these to determine what
        transition requirements are met in a given step.
    - 'focalization': A mapping from `Domain`s to `DomainFocalization`
        specifying how this context is focalized in each domain.
    - 'activeDomains': A set of `Domain`s indicating which `Domain`(s) are
        active for this focal context right now.
    - 'activeDecisions': A mapping from `Domain`s to either single
        `DecisionID`s, dictionaries mapping `FocalPointName`s to
        optional `DecisionID`s, or sets of `DecisionID`s. Which one is
        used depends on the `DomainFocalization` of this context for
        that domain. May also be `None` for domains in which no
        decisions are active (and in 'plural'-focalization lists,
       individual entries may be `None`). Active decisions from the
        common `FocalContext` are also considered active at each step.
    """
    capabilities: CapabilitySet
    focalization: Dict[Domain, DomainFocalization]
    activeDomains: Set[Domain]
    activeDecisions: Dict[
        Domain,
        Union[
            None,
            DecisionID,
            Dict[FocalPointName, Optional[DecisionID]],
            Set[DecisionID]
        ]
    ]


FocalContextName: 'TypeAlias' = str
"""
`FocalContext`s are assigned names are are indexed under those names
within `State` objects (they don't contain their own name). Note that
the 'common' focal context does not have a name.
"""


def getDomainFocalization(
    context: FocalContext,
    domain: Domain,
    defaultFocalization: DomainFocalization = 'singular'
) -> DomainFocalization:
    """
    Fetches the focalization value for the given domain in the given
    focal context, setting it to the provided default first if that
    focal context didn't have an entry for that domain yet.
    """
    return context['focalization'].setdefault(domain, defaultFocalization)


class State(TypedDict):
    """
    Represents a game state, including certain exploration-relevant
    information, plus possibly extra custom information. Has the
    following slots:

    - 'common': A single `FocalContext` containing capability and position
        information which is always active in addition to the current
        `FocalContext`'s information.
    - 'contexts': A dictionary mapping strings to `FocalContext`s, which
        store capability and position information.
    - 'activeContext': A string naming the currently-active
        `FocalContext` (a key of the 'contexts' slot).
    - 'primaryDecision': A `DecisionID` (or `None`) indicating the
        primary decision that is being considered in this state. Whereas
        the focalization structures can and often will indicate multiple
        active decisions, whichever decision the player just arrived at
        via the transition selected in a previous state will be the most
        relevant, and we track that here. Of course, for some states
        (like a pre-starting initial state) there is no primary
        decision.
    - 'mechanisms': A dictionary mapping `Mechanism` names to
        `MechanismState` strings.
    - 'exploration': A dictionary mapping decision IDs to exploration
        statuses, which tracks how much knowledge the player has of
        different decisions.
    - 'effectCounts': A dictionary mapping `EffectSpecifier`s to
        integers specifying how many times that effect has been
        triggered since the beginning of the exploration (including
        times that the actual effect was not applied due to delays
        and/or charges. This is used to figure out when effects with
        charges and/or delays should be applied.
    - 'deactivated':  A set of (`DecisionID`, `Transition`) tuples
        specifying which transitions have been deactivated. This is used
        in addition to transition requirements to figure out which
        transitions are traversable.
    - 'custom': An arbitrary sub-dictionary representing any kind of
        custom game state. In most cases, things can be reasonably
        approximated via capabilities and tokens and custom game state is
        not needed.
    """
    common: FocalContext
    contexts: Dict[FocalContextName, FocalContext]
    activeContext: FocalContextName
    primaryDecision: Optional[DecisionID]
    mechanisms: Dict[MechanismID, MechanismState]
    exploration: Dict[DecisionID, 'ExplorationStatus']
    effectCounts: Dict[EffectSpecifier, int]
    deactivated: Set[Tuple[DecisionID, Transition]]
    custom: dict


#-------------------#
# Utility Functions #
#-------------------#

def idOrDecisionSpecifier(
    ds: DecisionSpecifier
) -> Union[DecisionSpecifier, int]:
    """
    Given a decision specifier which might use a name that's convertible
    to an integer ID, returns the appropriate ID if so, and the original
    decision specifier if not, raising an
    `InvalidDecisionSpecifierError` if given a specifier with a
    convertible name that also has other parts.
    """
    try:
        dID = int(ds.name)
    except ValueError:
        return ds

    if ds.domain is None and ds.zone is None:
        return dID
    else:
        raise InvalidDecisionSpecifierError(
            f"Specifier {ds} has an ID name but also includes"
            f" domain and/or zone information."
        )


def spliceDecisionSpecifiers(
    base: DecisionSpecifier,
    default: DecisionSpecifier
) -> DecisionSpecifier:
    """
    Copies domain and/or zone info from the `default` specifier into the
    `base` specifier, returning a new `DecisionSpecifier` without
    modifying either argument. Info is only copied where the `base`
    specifier has a missing value, although if the base specifier has a
    domain but no zone and the domain is different from that of the
    default specifier, no zone info is copied.

    For example:

    >>> d1 = DecisionSpecifier('main', 'zone', 'name')
    >>> d2 = DecisionSpecifier('niam', 'enoz', 'eman')
    >>> spliceDecisionSpecifiers(d1, d2)
    DecisionSpecifier(domain='main', zone='zone', name='name')
    >>> spliceDecisionSpecifiers(d2, d1)
    DecisionSpecifier(domain='niam', zone='enoz', name='eman')
    >>> d3 = DecisionSpecifier(None, None, 'three')
    >>> spliceDecisionSpecifiers(d3, d1)
    DecisionSpecifier(domain='main', zone='zone', name='three')
    >>> spliceDecisionSpecifiers(d3, d2)
    DecisionSpecifier(domain='niam', zone='enoz', name='three')
    >>> d4 = DecisionSpecifier('niam', None, 'four')
    >>> spliceDecisionSpecifiers(d4, d1)  # diff domain -> no zone
    DecisionSpecifier(domain='niam', zone=None, name='four')
    >>> spliceDecisionSpecifiers(d4, d2)  # same domian -> copy zone
    DecisionSpecifier(domain='niam', zone='enoz', name='four')
    >>> d5 = DecisionSpecifier(None, 'cone', 'five')
    >>> spliceDecisionSpecifiers(d4, d5)  # None domain -> copy zone
    DecisionSpecifier(domain='niam', zone='cone', name='four')
    """
    newDomain = base.domain
    if newDomain is None:
        newDomain = default.domain
    newZone = base.zone
    if (
        newZone is None
    and (newDomain == default.domain or default.domain is None)
    ):
        newZone = default.zone

    return DecisionSpecifier(domain=newDomain, zone=newZone, name=base.name)


def mergeCapabilitySets(A: CapabilitySet, B: CapabilitySet) -> CapabilitySet:
    """
    Merges two capability sets into a new one, where all capabilities in
    either original set are active, and token counts and skill levels are
    summed.

    Example:

    >>> cs1 = {
    ...    'capabilities': {'fly', 'whistle'},
    ...    'tokens': {'subway': 3},
    ...    'skills': {'agility': 1, 'puzzling': 3},
    ... }
    >>> cs2 = {
    ...    'capabilities': {'dig', 'fly'},
    ...    'tokens': {'subway': 1, 'goat': 2},
    ...    'skills': {'agility': -1},
    ... }
    >>> ms = mergeCapabilitySets(cs1, cs2)
    >>> ms['capabilities'] == {'fly', 'whistle', 'dig'}
    True
    >>> ms['tokens'] == {'subway': 4, 'goat': 2}
    True
    >>> ms['skills'] == {'agility': 0, 'puzzling': 3}
    True
    """
    # Set up our result
    result: CapabilitySet = {
        'capabilities': set(),
        'tokens': {},
        'skills': {}
    }

    # Merge capabilities
    result['capabilities'].update(A['capabilities'])
    result['capabilities'].update(B['capabilities'])

    # Merge tokens
    tokensA = A['tokens']
    tokensB = B['tokens']
    resultTokens = result['tokens']
    for tType, val in tokensA.items():
        if tType not in resultTokens:
            resultTokens[tType] = val
        else:
            resultTokens[tType] += val
    for tType, val in tokensB.items():
        if tType not in resultTokens:
            resultTokens[tType] = val
        else:
            resultTokens[tType] += val

    # Merge skills
    skillsA = A['skills']
    skillsB = B['skills']
    resultSkills = result['skills']
    for skill, level in skillsA.items():
        if skill not in resultSkills:
            resultSkills[skill] = level
        else:
            resultSkills[skill] += level
    for skill, level in skillsB.items():
        if skill not in resultSkills:
            resultSkills[skill] = level
        else:
            resultSkills[skill] += level

    return result


def emptyFocalContext() -> FocalContext:
    """
    Returns a completely empty focal context, which has no capabilities
    and which has no associated domains.
    """
    return {
        'capabilities': {
            'capabilities': set(),
            'tokens': {},
            'skills': {}
        },
        'focalization': {},
        'activeDomains': set(),
        'activeDecisions': {}
    }


def basicFocalContext(
    domain: Optional[Domain] = None,
    focalization: DomainFocalization = 'singular'
):
    """
    Returns a basic focal context, which has no capabilities and which
    uses the given focalization (default 'singular') for a single
    domain with the given name (default `DEFAULT_DOMAIN`) which is
    active but which has no position specified.
    """
    if domain is None:
        domain = DEFAULT_DOMAIN
    return {
        'capabilities': {
            'capabilities': set(),
            'tokens': {},
            'skills': {}
        },
        'focalization': {domain: focalization},
        'activeDomains': {domain},
        'activeDecisions': {domain: None}
    }


def emptyState() -> State:
    """
    Returns an empty `State` dictionary. The empty dictionary uses
    `DEFAULT_FOCAL_CONTEXT_NAME` as the name of the active
    `FocalContext`.
    """
    return {
        'common': emptyFocalContext(),
        'contexts': {DEFAULT_FOCAL_CONTEXT_NAME: basicFocalContext()},
        'activeContext': DEFAULT_FOCAL_CONTEXT_NAME,
        'primaryDecision': None,
        'mechanisms': {},
        'exploration': {},
        'effectCounts': {},
        'deactivated': set(),
        'custom': {}
    }


def basicState(
    context: Optional[FocalContextName] = None,
    domain: Optional[Domain] = None,
    focalization: DomainFocalization = 'singular'
) -> State:
    """
    Returns a `State` dictionary with a newly created single active
    focal context that uses the given name (default
    `DEFAULT_FOCAL_CONTEXT_NAME`). This context is created using
    `basicFocalContext` with the given domain and focalization as
    arguments (defaults `DEFAULT_DOMAIN` and 'singular').
    """
    if context is None:
        context = DEFAULT_FOCAL_CONTEXT_NAME
    return {
        'common': emptyFocalContext(),
        'contexts': {context: basicFocalContext(domain, focalization)},
        'activeContext': context,
        'primaryDecision': None,
        'mechanisms': {},
        'exploration': {},
        'effectCounts': {},
        'deactivated': set(),
        'custom': {}
    }


def effectiveCapabilitySet(state: State) -> CapabilitySet:
    """
    Given a `baseTypes.State` object, computes the effective capability
    set for that state, which merges capabilities and tokens from the
    common `baseTypes.FocalContext` with those of the active one.

    Returns a `CapabilitySet`.
    """
    # Grab relevant contexts
    commonContext = state['common']
    activeContext = state['contexts'][state['activeContext']]

    # Extract capability dictionaries
    commonCapabilities = commonContext['capabilities']
    activeCapabilities = activeContext['capabilities']

    return mergeCapabilitySets(
        commonCapabilities,
        activeCapabilities
    )


def combinedDecisionSet(state: State) -> Set[DecisionID]:
    """
    Given a `State` object, computes the active decision set for that
    state, which is the set of decisions at which the player can make an
    immediate decision. This depends on the 'common' `FocalContext` as
    well as the active focal context, and of course each `FocalContext`
    may specify separate active decisions for different domains, separate
    sets of active domains, etc. See `FocalContext` and
    `DomainFocalization` for more details, as well as `activeDecisionSet`.

    Returns a set of `DecisionID`s.
    """
    commonContext = state['common']
    activeContext = state['contexts'][state['activeContext']]
    result = set()
    for ctx in (commonContext, activeContext):
        result |= activeDecisionSet(ctx)

    return result


def activeDecisionSet(context: FocalContext) -> Set[DecisionID]:
    """
    Given a `FocalContext`, returns the set of all `DecisionID`s which
    are active in that focal context. This includes only decisions which
    are in active domains.

    For example:

    >>> fc = emptyFocalContext()
    >>> activeDecisionSet(fc)
    set()
    >>> fc['focalization'] = {
    ...     'Si': 'singular',
    ...     'Pl': 'plural',
    ...     'Sp': 'spreading'
    ... }
    >>> fc['activeDomains'] = {'Si'}
    >>> fc['activeDecisions'] = {
    ...     'Si': 0,
    ...     'Pl': {'one': 1, 'two': 2},
    ...     'Sp': {3, 4}
    ... }
    >>> activeDecisionSet(fc)
    {0}
    >>> fc['activeDomains'] = {'Si', 'Pl'}
    >>> sorted(activeDecisionSet(fc))
    [0, 1, 2]
    >>> fc['activeDomains'] = {'Pl'}
    >>> sorted(activeDecisionSet(fc))
    [1, 2]
    >>> fc['activeDomains'] = {'Sp'}
    >>> sorted(activeDecisionSet(fc))
    [3, 4]
    >>> fc['activeDomains'] = {'Si', 'Pl', 'Sp'}
    >>> sorted(activeDecisionSet(fc))
    [0, 1, 2, 3, 4]
    """
    result = set()
    decisionsMap = context['activeDecisions']
    for domain in context['activeDomains']:
        activeGroup = decisionsMap[domain]
        if activeGroup is None:
            pass
        elif isinstance(activeGroup, DecisionID):
            result.add(activeGroup)
        elif isinstance(activeGroup, dict):
            for x in activeGroup.values():
                if x is not None:
                    result.add(x)
        elif isinstance(activeGroup, set):
            result.update(activeGroup)
        else:
            raise TypeError(
                f"The FocalContext {repr(context)} has an invalid"
                f" active group for domain {repr(domain)}."
                f"\nGroup is: {repr(activeGroup)}"
            )

    return result


ExplorationStatus: 'TypeAlias' = Literal[
    'unknown',
    'hypothesized',
    'noticed',
    'exploring',
    'explored',
]
"""
Exploration statuses track what kind of knowledge the player has about a
decision. Note that this is independent of whether or not they've
visited it. They are one of the following strings:

    - 'unknown': Indicates a decision that the player has absolutely no
        knowledge of, not even by implication. Normally such decisions
        are not part of a decision map, since the player can only write
        down what they've at least seen implied. But in cases where you
        want to track exploration of a pre-specified decision map,
        decisions that are pre-specified but which the player hasn't had
        any hint of yet would have this status.
    - 'hypothesized': Indicates a decision that the player can
        reasonably expect might be there, but which they haven't yet
        confirmed. This comes up when, for example, there's a flashback
        during which the player explores an older version of an area,
        which they then return to in the "present day." In this case,
        the player can hypothesize that the area layout will be the
        same, although in the end, it could in fact be different. The
        entire flashback area can be cloned and the cloned decisions
        marked as hypothesized to represent this. Note that this does
        NOT apply to decisions which are definitely implied, such as the
        decision on the other side of something the player recognizes as
        a door. Those kind of decisions should be marked as 'noticed'.
    - 'noticed': Indicates a decision that the player assumes will
        exist, and/or which the player has been able to observe some
        aspects of indirectly, such as in a cutscene. A decision on the
        other side of a closed door is in this category, since even
        though the player hasn't seen anything about it, they can pretty
        reliably assume there will be some decision there.
    - 'exploring': Indicates that a player has started to gain some
        knowledge of the transitions available at a decision (beyond the
        obvious reciprocals for connections to a 'noticed' decision,
        usually but not always by having now visited that decision. Even
        the most cursory visit should elevate a decision's exploration
        level to 'exploring', except perhaps if the visit is in a
        cutscene (although that can also count in some cases).
    - 'explored': Indicates that the player believes they have
        discovered all of the relevant transitions at this decision, and
        there is no need for them to explore it further. This notation
        should be based on the player's immediate belief, so even if
        it's known that the player will later discover another hidden
        option at this transition (or even if the options will later
        change), unless the player is cognizant of that, it should be
        marked as 'explored' as soon as the player believes they've
        exhausted observation of transitions. The player does not have
        to have explored all of those transitions yet, including
        actions, as long as they're satisfied for now that they've found
        all of the options available.
"""


def moreExplored(
    a: ExplorationStatus,
    b: ExplorationStatus
) -> ExplorationStatus:
    """
    Returns whichever of the two exploration statuses counts as 'more
    explored'.
    """
    eArgs = get_args(ExplorationStatus)
    try:
        aIndex = eArgs.index(a)
    except ValueError:
        raise ValueError(
            f"Status {a!r} is not a valid exploration status. Must be"
            f" one of: {eArgs!r}"
        )
    try:
        bIndex = eArgs.index(b)
    except ValueError:
        raise ValueError(
            f"Status {b!r} is not a valid exploration status. Must be"
            f" one of: {eArgs!r}"
        )
    if aIndex > bIndex:
        return a
    else:
        return b


def statusVisited(status: ExplorationStatus) -> bool:
    """
    Returns true or false depending on whether the provided status
    indicates a decision has been visited or not. The 'exploring' and
    'explored' statuses imply a decision has been visisted, but other
    statuses do not.
    """
    return status in ('exploring', 'explored')


RestoreFCPart: 'TypeAlias' = Literal[
    "capabilities",
    "tokens",
    "skills",
    "positions"
]
"""
Parts of a `FocalContext` that can be restored. Used in `revertedState`.
"""

RestoreCapabilityPart = Literal["capabilities", "tokens", "skills"]
"""
Parts of a focal context `CapabilitySet` that can be restored. Used in
`revertedState`.
"""

RestoreFCKey = Literal["focalization", "activeDomains", "activeDecisions"]
"""
Parts of a `FocalContext` besides the capability set that we can restore.
"""

RestoreStatePart = Literal["mechanisms", "exploration", "custom"]
"""
Parts of a State that we can restore besides the `FocalContext` stuff.
Doesn't include the stuff covered by the 'effects' restore aspect. See
`revertedState` for more.
"""


def revertedState(
    currentStuff: Tuple['DecisionGraph', State],
    savedStuff: Tuple['DecisionGraph', State],
    revisionAspects: Set[str]
) -> Tuple['DecisionGraph', State]:
    """
    Given two (graph, state) pairs, as well as a set of reversion aspect
    strings, returns a (graph, state) pair representing the reverted
    graph and state. The provided graphs and states will not be
    modified, and the return value will not include references to them,
    so modifying the returned state will not modify the original or
    saved states or graphs.

    If the `revisionAspects` set is empty, then all aspects except
    skills, exploration statuses, and the graph will be reverted.

    Note that the reversion process can lead to impossible states if the
    wrong combination of reversion aspects is used (e.g., reverting the
    graph but not focal context position information might lead to
    positions that refer to decisions which do not exist).

    Valid reversion aspect strings are:
    - "common-capabilities", "common-tokens", "common-skills,"
        "common-positions" or just "common" for all four. These
        control the parts of the common context's `CapabilitySet`
        that get reverted, as well as whether the focalization,
        active domains, and active decisions get reverted (those
        three as "positions").
    - "c-*NAME*-capabilities" as well as -tokens, -skills,
        -positions, and without a suffix, where *NAME* is the name of
        a specific focal context.
    - "all-capabilities" as well as -tokens, -skills, -positions,
        and -contexts, reverting the relevant part of all focal
        contexts except the common one, with "all-contexts" reverting
        every part of all non-common focal contexts.
    - "current-capabilities" as well as -tokens, -skills, -positions,
        and without a suffix, for the currently-active focal context.
    - "primary" which reverts the primary decision (some positions should
        also be reverted in this case).
    - "mechanisms" which reverts mechanism states.
    - "exploration" which reverts the exploration state of decisions
        (note that the `DecisionGraph` also stores "unconfirmed" tags
        which are NOT affected by a revert unless "graph" is specified).
    - "effects" which reverts the record of how many times transition
        effects have been triggered, plus whether transitions have
        been disabled or not.
    - "custom" which reverts custom state.
    - "graph" reverts the graph itself (but this is usually not
        desired). This will still preserve the next-ID value for
        assigning new nodes, so that nodes created in a reverted graph
        will not re-use IDs from nodes created before the reversion.
    - "-*NAME*" where *NAME* is a custom reversion specification
        defined using `core.DecisionGraph.reversionType` and available
        in the "current" decision graph (note the colon is required
        before the custom name). This allows complex reversion systems
        to be set up once and referenced repeatedly. Any strings
        specified along with a custom reversion type will revert the
        specified state in addition to what the custom reversion type
        specifies.

    For example:

    >>> from . import core
    >>> g = core.DecisionGraph.example("simple")  # A - B - C triangle
    >>> g.setTransitionRequirement('B', 'next', ReqCapability('helmet'))
    >>> g.addAction(
    ...     'A',
    ...     'getHelmet',
    ...     consequence=[effect(gain='helmet'), effect(deactivate=True)]
    ... )
    >>> s0 = basicState()
    >>> fc0 = s0['contexts']['main']
    >>> fc0['activeDecisions']['main'] = 0  # A
    >>> s1 = basicState()
    >>> fc1 = s1['contexts']['main']
    >>> fc1['capabilities']['capabilities'].add('helmet')
    >>> fc1['activeDecisions']['main'] = 1  # B
    >>> s1['exploration'] = {0: 'explored', 1: 'exploring', 2: 'unknown'}
    >>> s1['effectCounts'] = {(0, 'getHelmet', 1): 1}
    >>> s1['deactivated'] = {(0, "getHelmet")}
    >>> # Basic reversion of everything except graph & exploration
    >>> rg, rs = revertedState((g, s1), (g, s0), set())
    >>> rg == g
    True
    >>> rg is g
    False
    >>> rs == s0
    False
    >>> rs is s0
    False
    >>> rs['contexts'] == s0['contexts']
    True
    >>> rs['exploration'] == s1['exploration']
    True
    >>> rs['effectCounts'] = s0['effectCounts']
    >>> rs['deactivated'] = s0['deactivated']
    >>> # Reverting capabilities but not position, exploration, or effects
    >>> rg, rs = revertedState((g, s1), (g, s0), {"current-capabilities"})
    >>> rg == g
    True
    >>> rs == s0 or rs == s1
    False
    >>> s1['contexts']['main']['capabilities']['capabilities']
    {'helmet'}
    >>> s0['contexts']['main']['capabilities']['capabilities']
    set()
    >>> rs['contexts']['main']['capabilities']['capabilities']
    set()
    >>> s1['contexts']['main']['activeDecisions']['main']
    1
    >>> s0['contexts']['main']['activeDecisions']['main']
    0
    >>> rs['contexts']['main']['activeDecisions']['main']
    1
    >>> # Restore position and effects; that's all that wasn't reverted
    >>> rs['contexts']['main']['activeDecisions']['main'] = 0
    >>> rs['exploration'] = {}
    >>> rs['effectCounts'] = {}
    >>> rs['deactivated'] = set()
    >>> rs == s0
    True
    >>> # Reverting position but not state
    >>> rg, rs = revertedState((g, s1), (g, s0), {"current-positions"})
    >>> rg == g
    True
    >>> s1['contexts']['main']['capabilities']['capabilities']
    {'helmet'}
    >>> s0['contexts']['main']['capabilities']['capabilities']
    set()
    >>> rs['contexts']['main']['capabilities']['capabilities']
    {'helmet'}
    >>> s1['contexts']['main']['activeDecisions']['main']
    1
    >>> s0['contexts']['main']['activeDecisions']['main']
    0
    >>> rs['contexts']['main']['activeDecisions']['main']
    0
    >>> # Reverting based on specific focal context name
    >>> rg2, rs2 = revertedState((g, s1), (g, s0), {"c-main-positions"})
    >>> rg2 == rg
    True
    >>> rs2 == rs
    True
    >>> # Test of graph reversion
    >>> import copy
    >>> g2 = copy.deepcopy(g)
    >>> g2.addDecision('D')
    3
    >>> g2.addTransition(2, 'alt', 'D', 'return')
    >>> rg, rs = revertedState((g2, s1), (g, s0), {'graph'})
    >>> rg == g
    True
    >>> rg is g
    False

    TODO: More tests for various other reversion aspects
    """
    # Expand custom references
    expandedAspects = set()
    queue = list(revisionAspects)
    if len(queue) == 0:
        queue = [  # don't revert skills, exploration, and graph
            "common-capabilities",
            "common-tokens",
            "common-positions",
            "all-capabilities",
            "all-tokens",
            "all-positions",
            "mechanisms",
            "primary",
            "effects",
            "custom"
        ]  # we do not include "graph" or "exploration" here...
    customLookup = currentStuff[0].reversionTypes
    while len(queue) > 0:
        aspect = queue.pop(0)
        if aspect.startswith('-'):
            customName = aspect[1:]
            if customName not in customLookup:
                raise ValueError(
                    f"Custom reversion type {aspect[1:]!r} is invalid"
                    f" because that reversion type has not been"
                    f" defined. Defined types are:"
                    f"\n{list(customLookup.keys())}"
                )
            queue.extend(customLookup[customName])
        else:
            expandedAspects.add(aspect)

    # Further expand focal-context-part collectives
    if "common" in expandedAspects:
        expandedAspects.add("common-capabilities")
        expandedAspects.add("common-tokens")
        expandedAspects.add("common-skills")
        expandedAspects.add("common-positions")

    if "all-contexts" in expandedAspects:
        expandedAspects.add("all-capabilities")
        expandedAspects.add("all-tokens")
        expandedAspects.add("all-skills")
        expandedAspects.add("all-positions")

    if "current" in expandedAspects:
        expandedAspects.add("current-capabilities")
        expandedAspects.add("current-tokens")
        expandedAspects.add("current-skills")
        expandedAspects.add("current-positions")

    # Figure out things to revert that are specific to named focal
    # contexts
    perFC: Dict[FocalContextName, Set[RestoreFCPart]] = {}
    currentFCName = currentStuff[1]['activeContext']
    for aspect in expandedAspects:
        # For current- stuff, look up current context name
        if aspect.startswith("current"):
            found = False
            part: RestoreFCPart
            for part in get_args(RestoreFCPart):
                if aspect == f"current-{part}":
                    perFC.setdefault(currentFCName, set()).add(part)
                    found = True
            if not found and aspect != "current":
                raise RuntimeError(f"Invalid reversion aspect: {aspect!r}")
        elif aspect.startswith("c-"):
            if aspect.endswith("-capabilities"):
                fcName = aspect[2:-13]
                perFC.setdefault(fcName, set()).add("capabilities")
            elif aspect.endswith("-tokens"):
                fcName = aspect[2:-7]
                perFC.setdefault(fcName, set()).add("tokens")
            elif aspect.endswith("-skills"):
                fcName = aspect[2:-7]
                perFC.setdefault(fcName, set()).add("skills")
            elif aspect.endswith("-positions"):
                fcName = aspect[2:-10]
                perFC.setdefault(fcName, set()).add("positions")
            else:
                fcName = aspect[2:]
                forThis = perFC.setdefault(fcName, set())
                forThis.add("capabilities")
                forThis.add("tokens")
                forThis.add("skills")
                forThis.add("positions")

    currentState = currentStuff[1]
    savedState = savedStuff[1]

    # Expand all-FC reversions to per-FC entries for each FC in both
    # current and prior states
    allFCs = set(currentState['contexts']) | set(savedState['contexts'])
    for part in get_args(RestoreFCPart):
        if f"all-{part}" in expandedAspects:
            for fcName in allFCs:
                perFC.setdefault(fcName, set()).add(part)

    # Revert graph or not
    if "graph" in expandedAspects:
        resultGraph = copy.deepcopy(savedStuff[0])
        # Patch nextID to avoid spurious ID matches
        resultGraph.nextID = currentStuff[0].nextID
    else:
        resultGraph = copy.deepcopy(currentStuff[0])

    # Start from non-reverted state copy
    resultState = copy.deepcopy(currentState)

    # Revert primary decision or not
    if "primary" in expandedAspects:
        resultState['primaryDecision'] = savedState['primaryDecision']

    # Revert specified aspects of the common focal context
    savedCommon = savedState['common']
    capKey: RestoreCapabilityPart
    for capKey in get_args(RestoreCapabilityPart):
        if f"common-{part}" in expandedAspects:
            resultState['common']['capabilities'][capKey] = copy.deepcopy(
                savedCommon['capabilities'][capKey]
            )
    if "common-positions" in expandedAspects:
        fcKey: RestoreFCKey
        for fcKey in get_args(RestoreFCKey):
            resultState['common'][fcKey] = copy.deepcopy(savedCommon[fcKey])

    # Update focal context parts for named focal contexts:
    savedContextMap = savedState['contexts']
    for fcName, restore in perFC.items():
        thisFC = resultState['contexts'].setdefault(
            fcName,
            emptyFocalContext()
        )  # Create FC by name if it didn't exist already
        thatFC = savedContextMap.get(fcName)
        if thatFC is None:  # what if it's a new one?
            if restore == set(get_args(RestoreFCPart)):
                # If we're restoring everything and the context didn't
                # exist in the prior state, delete it in the restored
                # state
                del resultState['contexts'][fcName]
            else:
                # Otherwise update parts of it to be blank since prior
                # state didn't have any info
                for part in restore:
                    if part == "positions":
                        thisFC['focalization'] = {}
                        thisFC['activeDomains'] = set()
                        thisFC['activeDecisions'] = {}
                    elif part == "capabilities":
                        thisFC['capabilities'][part] = set()
                    else:
                        thisFC['capabilities'][part] = {}
        else:  # same context existed in saved data; update parts
            for part in restore:
                if part == "positions":
                    for fcKey in get_args(RestoreFCKey):  # typed above
                        thisFC[fcKey] = copy.deepcopy(thatFC[fcKey])
                else:
                    thisFC['capabilities'][part] = copy.deepcopy(
                        thatFC['capabilities'][part]
                    )

    # Revert mechanisms, exploration, and/or custom state if specified
    statePart: RestoreStatePart
    for statePart in get_args(RestoreStatePart):
        if statePart in expandedAspects:
            resultState[statePart] = copy.deepcopy(savedState[statePart])

    # Revert effect tracking if specified
    if "effects" in expandedAspects:
        resultState['effectCounts'] = copy.deepcopy(
            savedState['effectCounts']
        )
        resultState['deactivated'] = copy.deepcopy(savedState['deactivated'])

    return (resultGraph, resultState)


#--------------#
# Consequences #
#--------------#

class RequirementContext(NamedTuple):
    """
    The context necessary to check whether a requirement is satisfied or
    not. Also used for computing effective skill levels for
    `SkillCombination`s. Includes a `State` that specifies `Capability`
    and `Token` states, a `DecisionGraph` (which includes equivalences),
    and a set of `DecisionID`s to use as the starting place for finding
    mechanisms by name.
    """
    state: State
    graph: 'DecisionGraph'
    searchFrom: Set[DecisionID]


def getSkillLevel(state: State, skill: Skill) -> Level:
    """
    Given a `State` and a `Skill`, looks up that skill in both the
    common and active `FocalContext`s of the state, and adds those
    numbers together to get an effective skill level for that skill.
    Note that `SkillCombination`s can be used to set up more complex
    logic for skill combinations across different skills; if adding
    levels isn't desired between `FocalContext`s, use different skill
    names.

    If the skill isn't mentioned, the level will count as 0.
    """
    commonContext = state['common']
    activeContext = state['contexts'][state['activeContext']]
    return (
        commonContext['capabilities']['skills'].get(skill, 0)
      + activeContext['capabilities']['skills'].get(skill, 0)
    )


SaveSlot: TypeAlias = str


EffectType = Literal[
    'gain',
    'lose',
    'set',
    'toggle',
    'deactivate',
    'edit',
    'goto',
    'bounce',
    'follow',
    'save'
]
"""
The types that effects can use. See `Effect` for details.
"""

AnyEffectValue: TypeAlias = Union[
    Capability,
    Tuple[Token, TokenCount],
    Tuple[AnyMechanismSpecifier, MechanismState],
    Tuple[Literal['skill'], Skill, Level],
    Tuple[AnyMechanismSpecifier, List[MechanismState]],
    List[Capability],
    None,
    List[List[commands.Command]],
    AnyDecisionSpecifier,
    Tuple[AnyDecisionSpecifier, FocalPointName],
    Transition,
    SaveSlot
]
"""
A union of all possible effect types.
"""


class Effect(TypedDict):
    """
    Represents one effect of a transition on the decision graph and/or
    game state. The `type` slot is an `EffectType` that indicates what
    type of effect it is, and determines what the `value` slot will hold.
    The `charges` slot is normally `None`, but when set to an integer,
    the effect will only trigger that many times, subtracting one charge
    each time until it reaches 0, after which the effect will remain but
    be ignored. The `delay` slot is also normally `None`, but when set to
    an integer, the effect won't trigger but will instead subtract one
    from the delay until it reaches zero, at which point it will start to
    trigger (and use up charges if there are any). The 'applyTo' slot
    should be either 'common' or 'active' (a `ContextSpecifier`) and
    determines which focal context the effect applies to.

    The `value` values for each `type` are:

    - `'gain'`: A `Capability`, (`Token`, `TokenCount`) pair, or
        ('skill', `Skill`, `Level`) triple indicating a capability
        gained, some tokens acquired, or skill levels gained.
    - `'lose'`: A `Capability`, (`Token`, `TokenCount`) pair, or
        ('skill', `Skill`, `Level`) triple indicating a capability lost,
        some tokens spent, or skill levels lost. Note that the literal
        string 'skill' is added to disambiguate skills from tokens.
    - `'set'`: A (`Token`, `TokenCount`) pair, a (`MechanismSpecifier`,
        `MechanismState`) pair, or a ('skill', `Skill`, `Level`) triple
        indicating the new number of tokens, new mechanism state, or new
        skill level to establish. Ignores the old count/level, unlike
        'gain' and 'lose.'
    - `'toggle'`: A list of capabilities which will be toggled on one
        after the other, toggling the rest off, OR, a tuple containing a
        mechanism name followed by a list of states to be set one after
        the other. Does not work for tokens or skills. If a `Capability`
        list only has one item, it will be toggled on or off depending
        on whether the player currently has that capability or not,
        otherwise, whichever capability in the toggle list is currently
        active will determine which one gets activated next (the
        subsequent one in the list, wrapping from the end to the start).
        Note that equivalences are NOT considered when determining which
        capability to turn on, and ALL capabilities in the toggle list
        except the next one to turn on are turned off. Also, if none of
        the capabilities in the list is currently activated, the first
        one will be. For mechanisms, `DEFAULT_MECHANISM_STATE` will be
        used as the default state if only one state is provided, since
        mechanisms can't be "not in a state." `Mechanism` toggles
        function based on the current mechanism state; if it's not in
        the list they set the first given state.
    - `'deactivate'`: `None`. When the effect is activated, the
        transition it applies on will be added to the deactivated set in
        the current state. This effect type ignores the 'applyTo' value
        since it does not make changes to a `FocalContext`.
    - `'edit'`: A list of lists of `Command`s, with each list to be
        applied in succession on every subsequent activation of the
        transition (like toggle). These can use extra variables '$@' to
        refer to the source decision of the transition the edit effect is
        attached to, '$@d' to refer to the destination decision, '$@t' to
        refer to the transition, and '$@r' to refer to its reciprocal.
        Commands are powerful and might edit more than just the
        specified focal context.
        TODO: How to handle list-of-lists format?
    - `'goto'`: Either an `AnyDecisionSpecifier` specifying where the
        player should end up, or an (`AnyDecisionSpecifier`,
        `FocalPointName`) specifying both where they should end up and
        which focal point in the relevant domain should be moved. If
        multiple 'goto' values are present on different effects of a
        transition, they each trigger in turn (and e.g., might activate
        multiple decision points in a spreading-focalized domain). Every
        transition has a destination, so 'goto' is not necessary: use it
        only when an attempt to take a transition is diverted (and
        normally, in conjunction with 'charges', 'delay', and/or as an
        effect that's behind a `Challenge` or `Conditional`). If a goto
        specifies a destination in a plural-focalized domain, but does
        not include a focal point name, then the focal point which was
        taking the transition will be the one to move. If that
        information is not available, the first focal point created in
        that domain will be moved by default. Note that when using
        something other than a destination ID as the
        `AnyDecisionSpecifier`, it's up to you to ensure that the
        specifier is not ambiguous, otherwise taking the transition will
        crash the program.
    - `'bounce'`: Value will be `None`. Prevents the normal position
        update associated with a transition that this effect applies to.
        Normally, a transition should be marked with an appropriate
        requirement to prevent access, even in cases where access seems
        possible until tested (just add the requirement on a step after
        the transition is observed where relevant). However, 'bounce' can
        be used in cases where there's a challenge to fail, for example.
        `bounce` is redundant with `goto`: if a `goto` effect applies on
        a certain transition, the presence or absence of `bounce` on the
        same transition is ignored, since the new position will be
        specified by the `goto` value anyways.
    - `'follow'`: Value will be a `Transition` name. A transition with
        that name must exist at the destination of the action, and when
        the follow effect triggers, the player will immediately take
        that transition (triggering any consequences it has) after
        arriving at their normal destination (so the exploration status
        of the normal destination will also be updated). This can result
        in an infinite loop if two 'follow' effects imply transitions
        which trigger each other, so don't do that.
    - `'save'`: Value will be a string indicating a save-slot name.
        Indicates a save point, which can be returned to using a
        'revertTo' `ExplorationAction`. The entire game state and current
        graph is recorded, including effects of the current consequence
        before, but not after, the 'save' effect. However, the graph
        configuration is not restored by default (see 'revert'). A revert
        effect may specify only parts of the state to revert.

    TODO:
        'focus',
        'foreground',
        'background',
    """
    type: EffectType
    applyTo: ContextSpecifier
    value: AnyEffectValue
    charges: Optional[int]
    delay: Optional[int]
    hidden: bool


def effect(
    *,
    applyTo: ContextSpecifier = 'active',
    gain: Optional[Union[
        Capability,
        Tuple[Token, TokenCount],
        Tuple[Literal['skill'], Skill, Level]
    ]] = None,
    lose: Optional[Union[
        Capability,
        Tuple[Token, TokenCount],
        Tuple[Literal['skill'], Skill, Level]
    ]] = None,
    set: Optional[Union[
        Tuple[Token, TokenCount],
        Tuple[AnyMechanismSpecifier, MechanismState],
        Tuple[Literal['skill'], Skill, Level]
    ]] = None,
    toggle: Optional[Union[
        Tuple[AnyMechanismSpecifier, List[MechanismState]],
        List[Capability]
    ]] = None,
    deactivate: Optional[bool] = None,
    edit: Optional[List[List[commands.Command]]] = None,
    goto: Optional[Union[
        AnyDecisionSpecifier,
        Tuple[AnyDecisionSpecifier, FocalPointName]
    ]] = None,
    bounce: Optional[bool] = None,
    follow: Optional[Transition] = None,
    save: Optional[SaveSlot] = None,
    delay: Optional[int] = None,
    charges: Optional[int] = None,
    hidden: bool = False
) -> Effect:
    """
    Factory for a transition effect which includes default values so you
    can just specify effect types that are relevant to a particular
    situation. You may not supply values for more than one of
    gain/lose/set/toggle/deactivate/edit/goto/bounce, since which one
    you use determines the effect type.
    """
    tCount = len([
        x
        for x in (
            gain,
            lose,
            set,
            toggle,
            deactivate,
            edit,
            goto,
            bounce,
            follow,
            save
        )
        if x is not None
    ])
    if tCount == 0:
        raise ValueError(
            "You must specify one of gain, lose, set, toggle, deactivate,"
            " edit, goto, bounce, follow, or save."
        )
    elif tCount > 1:
        raise ValueError(
            f"You may only specify one of gain, lose, set, toggle,"
            f" deactivate, edit, goto, bounce, follow, or save"
            f" (you provided values for {tCount} of those)."
        )

    result: Effect = {
        'type': 'edit',
        'applyTo': applyTo,
        'value': [],
        'delay': delay,
        'charges': charges,
        'hidden': hidden
    }

    if gain is not None:
        result['type'] = 'gain'
        result['value'] = gain
    elif lose is not None:
        result['type'] = 'lose'
        result['value'] = lose
    elif set is not None:
        result['type'] = 'set'
        if (
            isinstance(set[0], MechanismName)
        and isinstance(set[1], MechanismState)
        ):
            result['value'] = (
                MechanismSpecifier(None, None, None, set[0]),
                set[1]
            )
        else:
            result['value'] = set
    elif toggle is not None:
        result['type'] = 'toggle'
        result['value'] = toggle
    elif deactivate is not None:
        result['type'] = 'deactivate'
        result['value'] = None
    elif edit is not None:
        result['type'] = 'edit'
        result['value'] = edit
    elif goto is not None:
        result['type'] = 'goto'
        result['value'] = goto
    elif bounce is not None:
        result['type'] = 'bounce'
        result['value'] = None
    elif follow is not None:
        result['type'] = 'follow'
        result['value'] = follow
    elif save is not None:
        result['type'] = 'save'
        result['value'] = save
    else:
        raise RuntimeError(
            "No effect specified in effect function & check failed."
        )

    return result


class SkillCombination:
    """
    Represents which skill(s) are used for a `Challenge`, including under
    what circumstances different skills might apply using
    `Requirement`s. This is an abstract class, use the subclasses
    `BestSkill`, `WorstSkill`, `CombinedSkill`, `InverseSkill`, and/or
    `ConditionalSkill` to represent a specific situation. To represent a
    single required skill, use a `BestSkill` or `CombinedSkill` with
    that skill as the only skill.

    Use `SkillCombination.effectiveLevel` to figure out the effective
    level of the entire requirement in a given situation. Note that
    levels from the common and active `FocalContext`s are added together
    whenever a specific skill level is referenced.

    Some examples:

    >>> from . import core
    >>> ctx = RequirementContext(emptyState(), core.DecisionGraph(), set())
    >>> ctx.state['common']['capabilities']['skills']['brawn'] = 1
    >>> ctx.state['common']['capabilities']['skills']['brains'] = 3
    >>> ctx.state['common']['capabilities']['skills']['luck'] = -1

    1. To represent using just the 'brains' skill, you would use:

        `BestSkill('brains')`

        >>> sr = BestSkill('brains')
        >>> sr.effectiveLevel(ctx)
        3

        If a skill isn't listed, its level counts as 0:

        >>> sr = BestSkill('agility')
        >>> sr.effectiveLevel(ctx)
        0

        To represent using the higher of 'brains' or 'brawn' you'd use:

        `BestSkill('brains', 'brawn')`

        >>> sr = BestSkill('brains', 'brawn')
        >>> sr.effectiveLevel(ctx)
        3

        The zero default only applies if an unknown skill is in the mix:

        >>> sr = BestSkill('luck')
        >>> sr.effectiveLevel(ctx)
        -1
        >>> sr = BestSkill('luck', 'agility')
        >>> sr.effectiveLevel(ctx)
        0

    2. To represent using the lower of 'brains' or 'brawn' you'd use:

        `WorstSkill('brains', 'brawn')`

        >>> sr = WorstSkill('brains', 'brawn')
        >>> sr.effectiveLevel(ctx)
        1

    3. To represent using 'brawn' if the focal context has the 'brawny'
        capability, but brains if not, use:

        ```
        ConditionalSkill(
            ReqCapability('brawny'),
            'brawn',
            'brains'
        )
        ```

        >>> sr = ConditionalSkill(
        ...     ReqCapability('brawny'),
        ...     'brawn',
        ...     'brains'
        ... )
        >>> sr.effectiveLevel(ctx)
        3
        >>> brawny = copy.deepcopy(ctx)
        >>> brawny.state['common']['capabilities']['capabilities'].add(
        ...     'brawny'
        ... )
        >>> sr.effectiveLevel(brawny)
        1

        If the player can still choose to use 'brains' even when they
        have the 'brawny' capability, you would do:

        >>> sr = ConditionalSkill(
        ...     ReqCapability('brawny'),
        ...     BestSkill('brawn', 'brains'),
        ...     'brains'
        ... )
        >>> sr.effectiveLevel(ctx)
        3
        >>> sr.effectiveLevel(brawny)  # can still use brains if better
        3

    4. To represent using the combined level of the 'brains' and
        'brawn' skills, you would use:

        `CombinedSkill('brains', 'brawn')`

        >>> sr = CombinedSkill('brains', 'brawn')
        >>> sr.effectiveLevel(ctx)
        4

    5. Skill names can be replaced by entire sub-`SkillCombination`s in
        any position, so more complex forms are possible:

        >>> sr = BestSkill(CombinedSkill('brains', 'luck'), 'brawn')
        >>> sr.effectiveLevel(ctx)
        2
        >>> sr = BestSkill(
        ...     ConditionalSkill(
        ...         ReqCapability('brawny'),
        ...         'brawn',
        ...         'brains',
        ...     ),
        ...     CombinedSkill('brains', 'luck')
        ... )
        >>> sr.effectiveLevel(ctx)
        3
        >>> sr.effectiveLevel(brawny)
        2
    """
    def effectiveLevel(self, context: 'RequirementContext') -> Level:
        """
        Returns the effective `Level` of the skill combination, given
        the situation specified by the provided `RequirementContext`.
        """
        raise NotImplementedError(
            "SkillCombination is an abstract class. Use one of its"
            " subclsases instead."
        )

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError(
            "SkillCombination is an abstract class and cannot be compared."
        )

    def __hash__(self) -> int:
        raise NotImplementedError(
            "SkillCombination is an abstract class and cannot be hashed."
        )

    def walk(self) -> Generator[
        Union['SkillCombination', Skill, Level],
        None,
        None
    ]:
        """
        Yields this combination and each sub-part in depth-first
        traversal order.
        """
        raise NotImplementedError(
            "SkillCombination is an abstract class and cannot be walked."
        )

    def unparse(self) -> str:
        """
        Returns a string that `SkillCombination.parse` would turn back
        into a `SkillCombination` equivalent to this one. For example:

        >>> BestSkill('brains').unparse()
        'best(brains)'
        >>> WorstSkill('brains', 'brawn').unparse()
        'worst(brains, brawn)'
        >>> CombinedSkill(
        ...     ConditionalSkill(ReqTokens('orb', 3), 'brains', 0),
        ...     InverseSkill('luck')
        ... ).unparse()
        'sum(if(orb*3, brains, 0), ~luck)'
        """
        raise NotImplementedError(
            "SkillCombination is an abstract class and cannot be"
            " unparsed."
        )


class BestSkill(SkillCombination):
    def __init__(
        self,
        *skills: Union[SkillCombination, Skill, Level]
    ):
        """
        Given one or more `SkillCombination` sub-items and/or skill
        names or levels, represents a situation where the highest
        effective level among the sub-items is used. Skill names
        translate to the player's level for that skill (with 0 as a
        default) while level numbers translate to that number.
        """
        if len(skills) == 0:
            raise ValueError(
                "Cannot create a `BestSkill` with 0 sub-skills."
            )
        self.skills = skills

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BestSkill) and other.skills == self.skills

    def __hash__(self) -> int:
        result = 1829
        for sk in self.skills:
            result += hash(sk)
        return result

    def __repr__(self) -> str:
        subs = ', '.join(repr(sk) for sk in self.skills)
        return "BestSkill(" + subs + ")"

    def walk(self) -> Generator[
        Union[SkillCombination, Skill, Level],
        None,
        None
    ]:
        yield self
        for sub in self.skills:
            if isinstance(sub, (Skill, Level)):
                yield sub
            else:
                yield from sub.walk()

    def effectiveLevel(self, ctx: 'RequirementContext') -> Level:
        """
        Determines the effective level of each sub-skill-combo and
        returns the highest of those.
        """
        result = None
        level: Level
        if len(self.skills) == 0:
            raise RuntimeError("Invalid BestSkill: has zero sub-skills.")
        for sk in self.skills:
            if isinstance(sk, Level):
                level = sk
            elif isinstance(sk, Skill):
                level = getSkillLevel(ctx.state, sk)
            elif isinstance(sk, SkillCombination):
                level = sk.effectiveLevel(ctx)
            else:
                raise RuntimeError(
                    f"Invalid BestSkill: found sub-skill '{repr(sk)}'"
                    f" which is not a skill name string, level integer,"
                    f" or SkillCombination."
                )
            if result is None or result < level:
                result = level

        assert result is not None
        return result

    def unparse(self):
        result = "best("
        for sk in self.skills:
            if isinstance(sk, SkillCombination):
                result += sk.unparse()
            else:
                result += str(sk)
            result += ', '
        return result[:-2] + ')'


class WorstSkill(SkillCombination):
    def __init__(
        self,
        *skills: Union[SkillCombination, Skill, Level]
    ):
        """
        Given one or more `SkillCombination` sub-items and/or skill
        names or levels, represents a situation where the lowest
        effective level among the sub-items is used. Skill names
        translate to the player's level for that skill (with 0 as a
        default) while level numbers translate to that number.
        """
        if len(skills) == 0:
            raise ValueError(
                "Cannot create a `WorstSkill` with 0 sub-skills."
            )
        self.skills = skills

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, WorstSkill) and other.skills == self.skills

    def __hash__(self) -> int:
        result = 7182
        for sk in self.skills:
            result += hash(sk)
        return result

    def __repr__(self) -> str:
        subs = ', '.join(repr(sk) for sk in self.skills)
        return "WorstSkill(" + subs + ")"

    def walk(self) -> Generator[
        Union[SkillCombination, Skill, Level],
        None,
        None
    ]:
        yield self
        for sub in self.skills:
            if isinstance(sub, (Skill, Level)):
                yield sub
            else:
                yield from sub.walk()

    def effectiveLevel(self, ctx: 'RequirementContext') -> Level:
        """
        Determines the effective level of each sub-skill-combo and
        returns the lowest of those.
        """
        result = None
        level: Level
        if len(self.skills) == 0:
            raise RuntimeError("Invalid WorstSkill: has zero sub-skills.")
        for sk in self.skills:
            if isinstance(sk, Level):
                level = sk
            elif isinstance(sk, Skill):
                level = getSkillLevel(ctx.state, sk)
            elif isinstance(sk, SkillCombination):
                level = sk.effectiveLevel(ctx)
            else:
                raise RuntimeError(
                    f"Invalid WorstSkill: found sub-skill '{repr(sk)}'"
                    f" which is not a skill name string, level integer,"
                    f" or SkillCombination."
                )
            if result is None or result > level:
                result = level

        assert result is not None
        return result

    def unparse(self):
        result = "worst("
        for sk in self.skills:
            if isinstance(sk, SkillCombination):
                result += sk.unparse()
            else:
                result += str(sk)
            result += ', '
        return result[:-2] + ')'


class CombinedSkill(SkillCombination):
    def __init__(
        self,
        *skills: Union[SkillCombination, Skill, Level]
    ):
        """
        Given one or more `SkillCombination` sub-items and/or skill
        names or levels, represents a situation where the sum of the
        effective levels of each sub-item is used. Skill names
        translate to the player's level for that skill (with 0 as a
        default) while level numbers translate to that number.
        """
        if len(skills) == 0:
            raise ValueError(
                "Cannot create a `CombinedSkill` with 0 sub-skills."
            )
        self.skills = skills

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, CombinedSkill)
        and other.skills == self.skills
        )

    def __hash__(self) -> int:
        result = 2871
        for sk in self.skills:
            result += hash(sk)
        return result

    def __repr__(self) -> str:
        subs = ', '.join(repr(sk) for sk in self.skills)
        return "CombinedSkill(" + subs + ")"

    def walk(self) -> Generator[
        Union[SkillCombination, Skill, Level],
        None,
        None
    ]:
        yield self
        for sub in self.skills:
            if isinstance(sub, (Skill, Level)):
                yield sub
            else:
                yield from sub.walk()

    def effectiveLevel(self, ctx: 'RequirementContext') -> Level:
        """
        Determines the effective level of each sub-skill-combo and
        returns the sum of those, with 0 as a default.
        """
        result = 0
        level: Level
        if len(self.skills) == 0:
            raise RuntimeError(
                "Invalid CombinedSkill: has zero sub-skills."
            )
        for sk in self.skills:
            if isinstance(sk, Level):
                level = sk
            elif isinstance(sk, Skill):
                level = getSkillLevel(ctx.state, sk)
            elif isinstance(sk, SkillCombination):
                level = sk.effectiveLevel(ctx)
            else:
                raise RuntimeError(
                    f"Invalid CombinedSkill: found sub-skill '{repr(sk)}'"
                    f" which is not a skill name string, level integer,"
                    f" or SkillCombination."
                )
            result += level

        assert result is not None
        return result

    def unparse(self):
        result = "sum("
        for sk in self.skills:
            if isinstance(sk, SkillCombination):
                result += sk.unparse()
            else:
                result += str(sk)
            result += ', '
        return result[:-2] + ')'


class InverseSkill(SkillCombination):
    def __init__(
        self,
        invert: Union[SkillCombination, Skill, Level]
    ):
        """
        Represents the effective level of the given `SkillCombination`,
        the level of the given `Skill`, or just the provided specific
        `Level`, except inverted (multiplied by -1).
        """
        self.invert = invert

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, InverseSkill)
        and other.invert == self.invert
        )

    def __hash__(self) -> int:
        return 3193 + hash(self.invert)

    def __repr__(self) -> str:
        return "InverseSkill(" + repr(self.invert) + ")"

    def walk(self) -> Generator[
        Union[SkillCombination, Skill, Level],
        None,
        None
    ]:
        yield self
        if isinstance(self.invert, SkillCombination):
            yield from self.invert.walk()
        else:
            yield self.invert

    def effectiveLevel(self, ctx: 'RequirementContext') -> Level:
        """
        Determines whether the requirement is satisfied or not and then
        returns the effective level of either the `ifSatisfied` or
        `ifNot` skill combination, as appropriate.
        """
        if isinstance(self.invert, Level):
            return -self.invert
        elif isinstance(self.invert, Skill):
            return -getSkillLevel(ctx.state, self.invert)
        elif isinstance(self.invert, SkillCombination):
            return -self.invert.effectiveLevel(ctx)
        else:
            raise RuntimeError(
                f"Invalid InverseSkill: invert value {repr(self.invert)}"
                f" The invert value must be a Level (int), a Skill"
                f" (str), or a SkillCombination."
            )

    def unparse(self):
        # TODO: Move these to `parsing` to avoid hard-coded tokens here?
        if isinstance(self.invert, SkillCombination):
            return '~' + self.invert.unparse()
        else:
            return '~' + str(self.invert)


class ConditionalSkill(SkillCombination):
    def __init__(
        self,
        requirement: 'Requirement',
        ifSatisfied: Union[SkillCombination, Skill, Level],
        ifNot: Union[SkillCombination, Skill, Level] = 0
    ):
        """
        Given a `Requirement` and two different sub-`SkillCombination`s,
        which can also be `Skill` names or fixed `Level`s, represents
        situations where which skills come into play depends on what
        capabilities the player has. In situations where the given
        requirement is satisfied, the `ifSatisfied` combination's
        effective level is used, and otherwise the `ifNot` level is
        used. By default `ifNot` is just the fixed level 0.
        """
        self.requirement = requirement
        self.ifSatisfied = ifSatisfied
        self.ifNot = ifNot

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, ConditionalSkill)
        and other.requirement == self.requirement
        and other.ifSatisfied == self.ifSatisfied
        and other.ifNot == self.ifNot
        )

    def __hash__(self) -> int:
        return (
            1278
          + hash(self.requirement)
          + hash(self.ifSatisfied)
          + hash(self.ifNot)
        )

    def __repr__(self) -> str:
        return (
            "ConditionalSkill("
          + repr(self.requirement) + ", "
          + repr(self.ifSatisfied) + ", "
          + repr(self.ifNot)
          + ")"
        )

    def walk(self) -> Generator[
        Union[SkillCombination, Skill, Level],
        None,
        None
    ]:
        yield self
        for sub in (self.ifSatisfied, self.ifNot):
            if isinstance(sub, SkillCombination):
                yield from sub.walk()
            else:
                yield sub

    def effectiveLevel(self, ctx: 'RequirementContext') -> Level:
        """
        Determines whether the requirement is satisfied or not and then
        returns the effective level of either the `ifSatisfied` or
        `ifNot` skill combination, as appropriate.
        """
        if self.requirement.satisfied(ctx):
            use = self.ifSatisfied
            sat = True
        else:
            use = self.ifNot
            sat = False

        if isinstance(use, Level):
            return use
        elif isinstance(use, Skill):
            return getSkillLevel(ctx.state, use)
        elif isinstance(use, SkillCombination):
            return use.effectiveLevel(ctx)
        else:
            raise RuntimeError(
                f"Invalid ConditionalSkill: Requirement was"
                f" {'not ' if not sat else ''}satisfied, and the"
                f" corresponding skill value was not a level, skill, or"
                f" SkillCombination: {repr(use)}"
            )

    def unparse(self):
        result = f"if({self.requirement.unparse()}, "
        if isinstance(self.ifSatisfied, SkillCombination):
            result += self.ifSatisfied.unparse()
        else:
            result += str(self.ifSatisfied)
        result += ', '
        if isinstance(self.ifNot, SkillCombination):
            result += self.ifNot.unparse()
        else:
            result += str(self.ifNot)
        return result + ')'


class Challenge(TypedDict):
    """
    Represents a random binary decision between two possible outcomes,
    only one of which will actually occur. The 'outcome' can be set to
    `True` or `False` to represent that the outcome of the challenge has
    been observed, or to `None` (the default) to represent a pending
    challenge. The chance of 'success' is determined by the associated
    skill(s) and the challenge level, although one or both may be
    unknown in which case a variable is used in place of a concrete
    value. Probabilities that are of the form 1/2**n or (2**n - 1) /
    (2**n) can be represented, the specific formula for the chance of
    success is for a challenge with a single skill is:

        s = interacting entity's skill level in associated skill
        c = challenge level
        P(success) = {
          1 - 1/2**(1 + s - c)    if s > c
          1/2                     if s == c
          1/2**(1 + c - s)        if c > s
        }

    This probability formula is equivalent to the following procedure:

    1. Flip one coin, plus one additional coin for each level difference
        between the skill and challenge levels.
    2. If the skill level is equal to or higher than the challenge
        level, the outcome is success if any single coin comes up heads.
    3. If the skill level is less than the challenge level, then the
        outcome is success only if *all* coins come up heads.
    4. If the outcome is not success, it is failure.

    Multiple skills can be combined into a `SkillCombination`, which can
    use the max or min of several skills, add skill levels together,
    and/or have skills which are only relevant when a certain
    `Requirement` is satisfied. If a challenge has no skills associated
    with it, then the player's skill level counts as 0.

    The slots are:

    - 'skills': A `SkillCombination` that specifies the relevant
        skill(s).
    - 'level': An integer specifying the level of the challenge. Along
        with the appropriate skill level of the interacting entity, this
        determines the probability of success or failure.
    - 'success': A `Consequence` which will happen when the outcome is
        success. Note that since a `Consequence` can be a `Challenge`,
        multi-outcome challenges can be represented by chaining multiple
        challenges together.
    - 'failure': A `Consequence` which will happen when the outcome is
        failure.
    - 'outcome': The outcome of the challenge: `True` means success,
        `False` means failure, and `None` means "not known (yet)."
    """
    skills: SkillCombination
    level: Level
    success: 'Consequence'
    failure: 'Consequence'
    outcome: Optional[bool]


def challenge(
    skills: Optional[SkillCombination] = None,
    level: Level = 0,
    success: Optional['Consequence'] = None,
    failure: Optional['Consequence'] = None,
    outcome: Optional[bool] = None
):
    """
    Factory for `Challenge`s, defaults to empty effects for both success
    and failure outcomes, so that you can just provide one or the other
    if you need to. Skills defaults to an empty list, the level defaults
    to 0 and the outcome defaults to `None` which means "not (yet)
    known."
    """
    if skills is None:
        skills = BestSkill(0)
    if success is None:
        success = []
    if failure is None:
        failure = []
    return {
        'skills': skills,
        'level': level,
        'success': success,
        'failure': failure,
        'outcome': outcome
    }


class Condition(TypedDict):
    """
    Represents a condition over `Capability`, `Token`, and/or `Mechanism`
    states which applies to one or more `Effect`s or `Challenge`s as part
    of a `Consequence`. If the specified `Requirement` is satisfied, the
    included `Consequence` is treated as if it were part of the
    `Consequence` that the `Condition` is inside of, if the requirement
    is not satisfied, then the internal `Consequence` is skipped and the
    alternate consequence is used instead. Either sub-consequence may of
    course be an empty list.
    """
    condition: 'Requirement'
    consequence: 'Consequence'
    alternative: 'Consequence'


def condition(
    condition: 'Requirement',
    consequence: 'Consequence',
    alternative: Optional['Consequence'] = None
):
    """
    Factory for conditions that just glues the given requirement,
    consequence, and alternative together. The alternative defaults to
    an empty list if not specified.
    """
    if alternative is None:
        alternative = []
    return {
        'condition': condition,
        'consequence': consequence,
        'alternative': alternative
    }


Consequence: 'TypeAlias' = List[Union[Challenge, Effect, Condition]]
"""
Represents a theoretical space of consequences that can occur as a
result of attempting an action, or as the success or failure outcome for
a challenge. It includes multiple effects and/or challenges, and since
challenges have consequences as their outcomes, consequences form a tree
structure, with `Effect`s as their leaves. Items in a `Consequence` are
applied in-order resolving all outcomes and sub-outcomes of a challenge
before considering the next item in the top-level consequence.

The `Challenge`s in a `Consequence` may have their 'outcome' set to
`None` to represent a theoretical challenge, or it may be set to either
`True` or `False` to represent an observed outcome.
"""


ChallengePolicy: 'TypeAlias' = Literal[
    'random',
    'mostLikely',
    'fewestEffects',
    'success',
    'failure',
    'specified',
]
"""
Specifies how challenges should be resolved. See
`observeChallengeOutcomes`.
"""


#-------------------------------#
# Consequence Utility Functions #
#-------------------------------#


def resetChallengeOutcomes(consequence: Consequence) -> None:
    """
    Traverses all sub-consequences of the given consequence, setting the
    outcomes of any `Challenge`s it encounters to `None`, to prepare for
    a fresh call to `observeChallengeOutcomes`.

    Resets all outcomes in every branch, regardless of previous
    outcomes.

    For example:

    >>> from . import core
    >>> e = core.emptySituation()
    >>> c = challenge(
    ...     success=[effect(gain=('money', 12))],
    ...     failure=[effect(lose=('money', 10))]
    ... )  # skill defaults to 'luck', level to 0, and outcome to None
    >>> c['outcome'] is None  # default outcome is None
    True
    >>> r = observeChallengeOutcomes(e, [c], policy='mostLikely')
    >>> r[0]['outcome']
    True
    >>> c['outcome']  # original outcome is changed from None
    True
    >>> r[0] is c
    True
    >>> resetChallengeOutcomes([c])
    >>> c['outcome'] is None  # now has been reset
    True
    >>> r[0]['outcome'] is None  # same object...
    True
    >>> resetChallengeOutcomes(c)  # can't reset just a Challenge
    Traceback (most recent call last):
    ...
    TypeError...
    >>> r = observeChallengeOutcomes(e, [c], policy='success')
    >>> r[0]['outcome']
    True
    >>> r = observeChallengeOutcomes(e, [c], policy='failure')
    >>> r[0]['outcome']  # wasn't reset
    True
    >>> resetChallengeOutcomes([c])  # now reset it
    >>> c['outcome'] is None
    True
    >>> r = observeChallengeOutcomes(e, [c], policy='failure')
    >>> r[0]['outcome']  # was reset
    False
    """
    if not isinstance(consequence, list):
        raise TypeError(
            f"Invalid consequence: must be a list."
            f"\nGot: {repr(consequence)}"
        )

    for item in consequence:
        if not isinstance(item, dict):
            raise TypeError(
                f"Invalid consequence: items in the list must be"
                f" Effects, Challenges, or Conditions."
                f"\nGot item: {repr(item)}"
            )
        if 'skills' in item:  # must be a Challenge
            item = cast(Challenge, item)
            item['outcome'] = None
            # reset both branches
            resetChallengeOutcomes(item['success'])
            resetChallengeOutcomes(item['failure'])

        elif 'value' in item:  # an Effect
            continue  # Effects don't have sub-outcomes

        elif 'condition' in item:  # a Condition
            item = cast(Condition, item)
            resetChallengeOutcomes(item['consequence'])
            resetChallengeOutcomes(item['alternative'])

        else:  # bad dict
            raise TypeError(
                f"Invalid consequence: items in the list must be"
                f" Effects, Challenges, or Conditions (got a dictionary"
                f" without 'skills', 'value', or 'condition' keys)."
                f"\nGot item: {repr(item)}"
            )


def observeChallengeOutcomes(
    context: RequirementContext,
    consequence: Consequence,
    location: Optional[Set[DecisionID]] = None,
    policy: ChallengePolicy = 'random',
    knownOutcomes: Optional[List[bool]] = None,
    makeCopy: bool = False
) -> Consequence:
    """
    Given a `RequirementContext` (for `Capability`, `Token`, and `Skill`
    info as well as equivalences in the `DecisionGraph` and a
    search-from location for mechanism names) and a `Conseqeunce` to be
    observed, sets the 'outcome' value for each `Challenge` in it to
    either `True` or `False` by determining an outcome for each
    `Challenge` that's relevant (challenges locked behind unsatisfied
    `Condition`s or on untaken branches of other challenges are not
    given outcomes). `Challenge`s that already have assigned outcomes
    re-use those outcomes, call `resetChallengeOutcomes` beforehand if
    you want to re-decide each challenge with a new policy, and use the
    'specified' policy if you want to ensure only pre-specified outcomes
    are used.

    Normally, the return value is just the original `consequence`
    object. However, if `makeCopy` is set to `True`, a deep copy is made
    and returned, so the original is not modified. One potential problem
    with this is that effects will be copied in this process, which
    means that if they are applied, things like delays and toggles won't
    update properly. `makeCopy` should thus normally not be used.

    The 'policy' value can be one of the `ChallengePolicy` values. The
    default is 'random', in which case the `random.random` function is
    used to determine each outcome, based on the probability derived
    from the challenge level and the associated skill level. The other
    policies are:

    - 'mostLikely': the result of each challenge will be whichever
        outcome is more likely, with success always happening instead of
        failure when the probabilities are 50/50.
    - 'fewestEffects`: whichever combination of outcomes leads to the
        fewest total number of effects will be chosen (modulo satisfying
        requirements of `Condition`s). Note that there's no estimation
        of the severity of effects, just the raw number. Ties in terms
        of number of effects are broken towards successes. This policy
        involves evaluating all possible outcome combinations to figure
        out which one has the fewest effects.
    - 'success' or 'failure': all outcomes will either succeed, or
        fail, as specified. Note that success/failure may cut off some
        challenges, so it's not the case that literally every challenge
        will succeed/fail; some may be skipped because of the
        specified success/failure of a prior challenge.
    - 'specified': all outcomes have already been specified, and those
        pre-specified outcomes should be used as-is.


    In call cases, outcomes specified via `knownOutcomes` take precedence
    over the challenge policy. The `knownOutcomes` list will be emptied
    out as this function works, but extra consequences beyond what's
    needed will be ignored (and left in the list).

    Note that there are limits on the resolution of Python's random
    number generation; for challenges with extremely high or low levels
    relative to the associated skill(s) where the probability of success
    is very close to 1 or 0, there may not actually be any chance of
    success/failure at all. Typically you can ignore this, because such
    cases should not normally come up in practice, and because the odds
    of success/failure in those cases are such that to notice the
    missing possibility share you'd have to simulate outcomes a
    ridiculous number of times.

    TODO: Location examples; move some of these to a separate testing
    file.

    For example:

    >>> random.seed(17)
    >>> warnings.filterwarnings('error')
    >>> from . import core
    >>> e = core.emptySituation()
    >>> c = challenge(
    ...     success=[effect(gain=('money', 12))],
    ...     failure=[effect(lose=('money', 10))]
    ... )  # skill defaults to 'luck', level to 0, and outcome to None
    >>> c['outcome'] is None  # default outcome is None
    True
    >>> r = observeChallengeOutcomes(e, [c])
    >>> r[0]['outcome']
    False
    >>> c['outcome']  # original outcome is changed from None
    False
    >>> all(
    ...     observeChallengeOutcomes(e, [c])[0]['outcome'] is False
    ...     for i in range(20)
    ... )  # no reset -> same outcome
    True
    >>> resetChallengeOutcomes([c])
    >>> observeChallengeOutcomes(e, [c])[0]['outcome']  # Random after reset
    False
    >>> resetChallengeOutcomes([c])
    >>> observeChallengeOutcomes(e, [c])[0]['outcome']  # Random after reset
    False
    >>> resetChallengeOutcomes([c])
    >>> observeChallengeOutcomes(e, [c])[0]['outcome'] # Random after reset
    True
    >>> observeChallengeOutcomes(e, c)  # Can't resolve just a Challenge
    Traceback (most recent call last):
    ...
    TypeError...
    >>> allSame = []
    >>> for i in range(20):
    ...    resetChallengeOutcomes([c])
    ...    obs = observeChallengeOutcomes(e, [c, c])
    ...    allSame.append(obs[0]['outcome'] == obs[1]['outcome'])
    >>> allSame == [True]*20
    True
    >>> different = []
    >>> for i in range(20):
    ...    resetChallengeOutcomes([c])
    ...    obs = observeChallengeOutcomes(e, [c, copy.deepcopy(c)])
    ...    different.append(obs[0]['outcome'] == obs[1]['outcome'])
    >>> False in different
    True
    >>> all(  # Tie breaks towards success
    ...     (
    ...         resetChallengeOutcomes([c]),
    ...         observeChallengeOutcomes(e, [c], policy='mostLikely')
    ...     )[1][0]['outcome'] is True
    ...     for i in range(20)
    ... )
    True
    >>> all(  # Tie breaks towards success
    ...     (
    ...         resetChallengeOutcomes([c]),
    ...         observeChallengeOutcomes(e, [c], policy='fewestEffects')
    ...     )[1][0]['outcome'] is True
    ...     for i in range(20)
    ... )
    True
    >>> all(
    ...     (
    ...         resetChallengeOutcomes([c]),
    ...         observeChallengeOutcomes(e, [c], policy='success')
    ...     )[1][0]['outcome'] is True
    ...     for i in range(20)
    ... )
    True
    >>> all(
    ...     (
    ...         resetChallengeOutcomes([c]),
    ...         observeChallengeOutcomes(e, [c], policy='failure')
    ...     )[1][0]['outcome'] is False
    ...     for i in range(20)
    ... )
    True
    >>> c['outcome'] = False  # Fix the outcome; now policy is ignored
    >>> observeChallengeOutcomes(e, [c], policy='success')[0]['outcome']
    False
    >>> c = challenge(
    ...     skills=BestSkill('charisma'),
    ...     level=8,
    ...     success=[
    ...         challenge(
    ...             skills=BestSkill('strength'),
    ...             success=[effect(gain='winner')]
    ...         )
    ...     ],  # level defaults to 0
    ...     failure=[
    ...         challenge(
    ...             skills=BestSkill('strength'),
    ...             failure=[effect(gain='loser')]
    ...         ),
    ...         effect(gain='sad')
    ...     ]
    ... )
    >>> r = observeChallengeOutcomes(e, [c])  # random
    >>> r[0]['outcome']
    False
    >>> r[0]['failure'][0]['outcome']  # also random
    True
    >>> r[0]['success'][0]['outcome'] is None  # skipped so not assigned
    True
    >>> resetChallengeOutcomes([c])
    >>> r2 = observeChallengeOutcomes(e, [c])  # random
    >>> r[0]['outcome']
    False
    >>> r[0]['success'][0]['outcome'] is None  # untaken branch no outcome
    True
    >>> r[0]['failure'][0]['outcome']  # also random
    False
    >>> def outcomeList(consequence):
    ...     'Lists outcomes from each challenge attempted.'
    ...     result = []
    ...     for item in consequence:
    ...         if 'skills' in item:
    ...             result.append(item['outcome'])
    ...             if item['outcome'] is True:
    ...                 result.extend(outcomeList(item['success']))
    ...             elif item['outcome'] is False:
    ...                 result.extend(outcomeList(item['failure']))
    ...             else:
    ...                 pass  # end here
    ...     return result
    >>> def skilled(**skills):
    ...     'Create a clone of our Situation with specific skills.'
    ...     r = copy.deepcopy(e)
    ...     r.state['common']['capabilities']['skills'].update(skills)
    ...     return r
    >>> resetChallengeOutcomes([c])
    >>> r = observeChallengeOutcomes(  # 'mostLikely' policy
    ...     skilled(charisma=9, strength=1),
    ...     [c],
    ...     policy='mostLikely'
    ... )
    >>> outcomeList(r)
    [True, True]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(
    ...     skilled(charisma=7, strength=-1),
    ...     [c],
    ...     policy='mostLikely'
    ... ))
    [False, False]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(
    ...     skilled(charisma=8, strength=-1),
    ...     [c],
    ...     policy='mostLikely'
    ... ))
    [True, False]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(
    ...     skilled(charisma=7, strength=0),
    ...     [c],
    ...     policy='mostLikely'
    ... ))
    [False, True]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(
    ...     skilled(charisma=20, strength=10),
    ...     [c],
    ...     policy='mostLikely'
    ... ))
    [True, True]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(
    ...     skilled(charisma=-10, strength=-10),
    ...     [c],
    ...     policy='mostLikely'
    ... ))
    [False, False]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(
    ...     e,
    ...     [c],
    ...     policy='fewestEffects'
    ... ))
    [True, False]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(
    ...     skilled(charisma=-100, strength=100),
    ...     [c],
    ...     policy='fewestEffects'
    ... ))  # unaffected by stats
    [True, False]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(e, [c], policy='success'))
    [True, True]
    >>> resetChallengeOutcomes([c])
    >>> outcomeList(observeChallengeOutcomes(e, [c], policy='failure'))
    [False, False]
    >>> cc = copy.deepcopy(c)
    >>> resetChallengeOutcomes([cc])
    >>> cc['outcome'] = False
    >>> outcomeList(observeChallengeOutcomes(
    ...     skilled(charisma=10, strength=10),
    ...     [cc],
    ...     policy='mostLikely'
    ... ))  # pre-observed outcome won't be changed
    [False, True]
    >>> resetChallengeOutcomes([cc])
    >>> cc['outcome'] = False
    >>> outcomeList(observeChallengeOutcomes(
    ...     e,
    ...     [cc],
    ...     policy='fewestEffects'
    ... ))  # pre-observed outcome won't be changed
    [False, True]
    >>> cc['success'][0]['outcome'] is None  # not assigned on other branch
    True
    >>> resetChallengeOutcomes([cc])
    >>> r = observeChallengeOutcomes(e, [cc], policy='fewestEffects')
    >>> r[0] is cc  # results are aliases, not clones
    True
    >>> outcomeList(r)
    [True, False]
    >>> cc['success'][0]['outcome']  # inner outcome now assigned
    False
    >>> cc['failure'][0]['outcome'] is None  # now this is other branch
    True
    >>> resetChallengeOutcomes([cc])
    >>> r = observeChallengeOutcomes(
    ...     e,
    ...     [cc],
    ...     policy='fewestEffects',
    ...     makeCopy=True
    ... )
    >>> r[0] is cc  # now result is a clone
    False
    >>> outcomeList(r)
    [True, False]
    >>> observedEffects(genericContextForSituation(e), r)
    []
    >>> r[0]['outcome']  # outcome was assigned
    True
    >>> cc['outcome'] is None  # only to the copy, not to the original
    True
    >>> cn = [
    ...     condition(
    ...         ReqCapability('boost'),
    ...         [
    ...             challenge(success=[effect(gain=('$', 1))]),
    ...             effect(gain=('$', 2))
    ...         ]
    ...     ),
    ...     challenge(failure=[effect(gain=('$', 4))])
    ... ]
    >>> o = observeChallengeOutcomes(e, cn, policy='fewestEffects')
    >>> # Without 'boost', inner challenge does not get an outcome
    >>> o[0]['consequence'][0]['outcome'] is None
    True
    >>> o[1]['outcome']  # avoids effect
    True
    >>> hasBoost = copy.deepcopy(e)
    >>> hasBoost.state['common']['capabilities']['capabilities'].add('boost')
    >>> resetChallengeOutcomes(cn)
    >>> o = observeChallengeOutcomes(hasBoost, cn, policy='fewestEffects')
    >>> o[0]['consequence'][0]['outcome']  # now assigned an outcome
    False
    >>> o[1]['outcome']  # avoids effect
    True
    >>> from . import core
    >>> e = core.emptySituation()
    >>> c = challenge(
    ...     skills=BestSkill('skill'),
    ...     level=4,  # very unlikely at level 0
    ...     success=[],
    ...     failure=[effect(lose=('money', 10))],
    ...     outcome=True
    ... )  # pre-assigned outcome
    >>> c['outcome']  # verify
    True
    >>> r = observeChallengeOutcomes(e, [c], policy='specified')
    >>> r[0]['outcome']
    True
    >>> c['outcome']  # original outcome is unchanged
    True
    >>> c['outcome'] = False  # the more likely outcome
    >>> r = observeChallengeOutcomes(e, [c], policy='specified')
    >>> r[0]['outcome']  # re-uses the new outcome
    False
    >>> c['outcome']  # outcome is unchanged
    False
    >>> c['outcome'] = True  # change it back
    >>> r = observeChallengeOutcomes(e, [c], policy='specified')
    >>> r[0]['outcome']  # re-use the outcome again
    True
    >>> c['outcome']  # outcome is unchanged
    True
    >>> c['outcome'] = None  # set it to no info; will crash
    >>> r = observeChallengeOutcomes(e, [c], policy='specified')
    Traceback (most recent call last):
    ...
    ValueError...
    >>> warnings.filterwarnings('default')
    >>> c['outcome'] is None  # same after crash
    True
    >>> r = observeChallengeOutcomes(
    ...     e,
    ...     [c],
    ...     policy='specified',
    ...     knownOutcomes=[True]
    ... )
    >>> r[0]['outcome']  # picked up known outcome
    True
    >>> c['outcome']  # outcome is changed
    True
    >>> resetChallengeOutcomes([c])
    >>> c['outcome'] is None  # has been reset
    True
    >>> r = observeChallengeOutcomes(
    ...     e,
    ...     [c],
    ...     policy='specified',
    ...     knownOutcomes=[True]
    ... )
    >>> c['outcome']  # from known outcomes
    True
    >>> ko = [False]
    >>> r = observeChallengeOutcomes(
    ...     e,
    ...     [c],
    ...     policy='specified',
    ...     knownOutcomes=ko
    ... )
    >>> c['outcome']  # from known outcomes
    False
    >>> ko  # known outcomes list gets used up
    []
    >>> ko = [False, False]
    >>> r = observeChallengeOutcomes(
    ...     e,
    ...     [c],
    ...     policy='specified',
    ...     knownOutcomes=ko
    ... )  # too many outcomes is an error
    >>> ko
    [False]
    """
    if not isinstance(consequence, list):
        raise TypeError(
            f"Invalid consequence: must be a list."
            f"\nGot: {repr(consequence)}"
        )

    if knownOutcomes is None:
        knownOutcomes = []

    if makeCopy:
        result = copy.deepcopy(consequence)
    else:
        result = consequence

    for item in result:
        if not isinstance(item, dict):
            raise TypeError(
                f"Invalid consequence: items in the list must be"
                f" Effects, Challenges, or Conditions."
                f"\nGot item: {repr(item)}"
            )
        if 'skills' in item:  # must be a Challenge
            item = cast(Challenge, item)
            if len(knownOutcomes) > 0:
                item['outcome'] = knownOutcomes.pop(0)
            if item['outcome'] is not None:
                if item['outcome']:
                    observeChallengeOutcomes(
                        context,
                        item['success'],
                        location=location,
                        policy=policy,
                        knownOutcomes=knownOutcomes,
                        makeCopy=False
                    )
                else:
                    observeChallengeOutcomes(
                        context,
                        item['failure'],
                        location=location,
                        policy=policy,
                        knownOutcomes=knownOutcomes,
                        makeCopy=False
                    )
            else:  # need to assign an outcome
                if policy == 'specified':
                    raise ValueError(
                        f"Challenge has unspecified outcome so the"
                        f" 'specified' policy cannot be used when"
                        f" observing its outcomes:"
                        f"\n{item}"
                    )
                level = item['skills'].effectiveLevel(context)
                against = item['level']
                if level < against:
                    p = 1 / (2 ** (1 + against - level))
                else:
                    p = 1 - (1 / (2 ** (1 + level - against)))
                if policy == 'random':
                    if random.random() < p:  # success
                        item['outcome'] = True
                    else:
                        item['outcome'] = False
                elif policy == 'mostLikely':
                    if p >= 0.5:
                        item['outcome'] = True
                    else:
                        item['outcome'] = False
                elif policy == 'fewestEffects':
                    # Resolve copies so we don't affect original
                    subSuccess = observeChallengeOutcomes(
                        context,
                        item['success'],
                        location=location,
                        policy=policy,
                        knownOutcomes=knownOutcomes[:],
                        makeCopy=True
                    )
                    subFailure = observeChallengeOutcomes(
                        context,
                        item['failure'],
                        location=location,
                        policy=policy,
                        knownOutcomes=knownOutcomes[:],
                        makeCopy=True
                    )
                    if (
                        len(observedEffects(context, subSuccess))
                     <= len(observedEffects(context, subFailure))
                    ):
                        item['outcome'] = True
                    else:
                        item['outcome'] = False
                elif policy == 'success':
                    item['outcome'] = True
                elif policy == 'failure':
                    item['outcome'] = False

                # Figure out outcomes for sub-consequence if we don't
                # already have them...
                if item['outcome'] not in (True, False):
                    raise TypeError(
                        f"Challenge has invalid outcome type"
                        f" {type(item['outcome'])} after observation."
                        f"\nOutcome value: {repr(item['outcome'])}"
                    )

                if item['outcome']:
                    observeChallengeOutcomes(
                        context,
                        item['success'],
                        location=location,
                        policy=policy,
                        knownOutcomes=knownOutcomes,
                        makeCopy=False
                    )
                else:
                    observeChallengeOutcomes(
                        context,
                        item['failure'],
                        location=location,
                        policy=policy,
                        knownOutcomes=knownOutcomes,
                        makeCopy=False
                    )

        elif 'value' in item:
            continue  # Effects do not need success/failure assigned

        elif 'condition' in item:  # a Condition
            if item['condition'].satisfied(context):
                observeChallengeOutcomes(
                    context,
                    item['consequence'],
                    location=location,
                    policy=policy,
                    knownOutcomes=knownOutcomes,
                    makeCopy=False
                )
            else:
                observeChallengeOutcomes(
                    context,
                    item['alternative'],
                    location=location,
                    policy=policy,
                    knownOutcomes=knownOutcomes,
                    makeCopy=False
                )

        else:  # bad dict
            raise TypeError(
                f"Invalid consequence: items in the list must be"
                f" Effects, Challenges, or Conditions (got a dictionary"
                f" without 'skills', 'value', or 'condition' keys)."
                f"\nGot item: {repr(item)}"
            )

    # Return copy or original, now with options selected
    return result


class UnassignedOutcomeWarning(Warning):
    """
    A warning issued when asking for observed effects of a `Consequence`
    whose `Challenge` outcomes have not been fully assigned.
    """
    pass


def observedEffects(
    context: RequirementContext,
    observed: Consequence,
    skipWarning=False,
    baseIndex: int = 0
) -> List[int]:
    """
    Given a `Situation` and a `Consequence` whose challenges have
    outcomes assigned, returns a tuple containing a list of the
    depth-first-indices of each effect to apply. You can use
    `consequencePart` to extract the actual `Effect` values from the
    consequence based on their indices.

    Only effects that actually apply are included, based on the observed
    outcomes as well as which `Condition`(s) are met, although charges
    and delays for the effects are not taken into account.

    `baseIndex` can be set to something other than 0 to start indexing
    at that value. Issues an `UnassignedOutcomeWarning` if it encounters
    a challenge whose outcome has not been observed, unless
    `skipWarning` is set to `True`. In that case, no effects are listed
    for outcomes of that challenge.

    For example:

    >>> from . import core
    >>> warnings.filterwarnings('error')
    >>> e = core.emptySituation()
    >>> def skilled(**skills):
    ...     'Create a clone of our FocalContext with specific skills.'
    ...     r = copy.deepcopy(e)
    ...     r.state['common']['capabilities']['skills'].update(skills)
    ...     return r
    >>> c = challenge(  # index 1 in [c] (index 0 is the outer list)
    ...     skills=BestSkill('charisma'),
    ...     level=8,
    ...     success=[
    ...         effect(gain='happy'),  # index 3 in [c]
    ...         challenge(
    ...             skills=BestSkill('strength'),
    ...             success=[effect(gain='winner')]  # index 6 in [c]
    ...             # failure is index 7
    ...         )  # level defaults to 0
    ...     ],
    ...     failure=[
    ...         challenge(
    ...             skills=BestSkill('strength'),
    ...             # success is index 10
    ...             failure=[effect(gain='loser')]  # index 12 in [c]
    ...         ),
    ...         effect(gain='sad')  # index 13 in [c]
    ...     ]
    ... )
    >>> import pytest
    >>> with pytest.warns(UnassignedOutcomeWarning):
    ...     observedEffects(e, [c])
    []
    >>> with pytest.warns(UnassignedOutcomeWarning):
    ...     observedEffects(e, [c, c])
    []
    >>> observedEffects(e, [c, c], skipWarning=True)
    []
    >>> c['outcome'] = 'invalid value'  # must be True, False, or None
    >>> observedEffects(e, [c])
    Traceback (most recent call last):
    ...
    TypeError...
    >>> yesYes = skilled(charisma=10, strength=5)
    >>> yesNo = skilled(charisma=10, strength=-1)
    >>> noYes = skilled(charisma=4, strength=5)
    >>> noNo = skilled(charisma=4, strength=-1)
    >>> resetChallengeOutcomes([c])
    >>> observedEffects(
    ...     yesYes,
    ...     observeChallengeOutcomes(yesYes, [c], policy='mostLikely')
    ... )
    [3, 6]
    >>> resetChallengeOutcomes([c])
    >>> observedEffects(
    ...     yesNo,
    ...     observeChallengeOutcomes(yesNo, [c], policy='mostLikely')
    ... )
    [3]
    >>> resetChallengeOutcomes([c])
    >>> observedEffects(
    ...     noYes,
    ...     observeChallengeOutcomes(noYes, [c], policy='mostLikely')
    ... )
    [13]
    >>> resetChallengeOutcomes([c])
    >>> observedEffects(
    ...     noNo,
    ...     observeChallengeOutcomes(noNo, [c], policy='mostLikely')
    ... )
    [12, 13]
    >>> warnings.filterwarnings('default')
    >>> # known outcomes override policy & pre-specified outcomes
    >>> observedEffects(
    ...     noNo,
    ...     observeChallengeOutcomes(
    ...         noNo,
    ...         [c],
    ...         policy='mostLikely',
    ...         knownOutcomes=[True, True])
    ... )
    [3, 6]
    >>> observedEffects(
    ...     yesYes,
    ...     observeChallengeOutcomes(
    ...         yesYes,
    ...         [c],
    ...         policy='mostLikely',
    ...         knownOutcomes=[False, False])
    ... )
    [12, 13]
    >>> resetChallengeOutcomes([c])
    >>> observedEffects(
    ...     yesYes,
    ...     observeChallengeOutcomes(
    ...         yesYes,
    ...         [c],
    ...         policy='mostLikely',
    ...         knownOutcomes=[False, False])
    ... )
    [12, 13]
    """
    result: List[int] = []
    totalCount: int = baseIndex + 1  # +1 for the outer list
    if not isinstance(observed, list):
        raise TypeError(
            f"Invalid consequence: must be a list."
            f"\nGot: {repr(observed)}"
        )
    for item in observed:
        if not isinstance(item, dict):
            raise TypeError(
                f"Invalid consequence: items in the list must be"
                f" Effects, Challenges, or Conditions."
                f"\nGot item: {repr(item)}"
            )

        if 'skills' in item:  # must be a Challenge
            item = cast(Challenge, item)
            succeeded = item['outcome']
            useCh: Optional[Literal['success', 'failure']]
            if succeeded is True:
                useCh = 'success'
            elif succeeded is False:
                useCh = 'failure'
            else:
                useCh = None
                level = item["level"]
                if succeeded is not None:
                    raise TypeError(
                        f"Invalid outcome for level-{level} challenge:"
                        f" should be True, False, or None, but got:"
                        f" {repr(succeeded)}"
                    )
                else:
                    if not skipWarning:
                        warnings.warn(
                            (
                                f"A level-{level} challenge in the"
                                f" consequence being observed has no"
                                f" observed outcome; no effects from"
                                f" either success or failure branches"
                                f" will be included. Use"
                                f" observeChallengeOutcomes to fill in"
                                f" unobserved outcomes."
                            ),
                            UnassignedOutcomeWarning
                        )

            if useCh is not None:
                skipped = 0
                if useCh == 'failure':
                    skipped = countParts(item['success'])
                subEffects = observedEffects(
                    context,
                    item[useCh],
                    skipWarning=skipWarning,
                    baseIndex=totalCount + skipped + 1
                )
                result.extend(subEffects)

            # TODO: Go back to returning tuples but fix counts to include
            # skipped stuff; this is horribly inefficient :(
            totalCount += countParts(item)

        elif 'value' in item:  # an effect, not a challenge
            item = cast(Effect, item)
            result.append(totalCount)
            totalCount += 1

        elif 'condition' in item:  # a Condition
            item = cast(Condition, item)
            useCo: Literal['consequence', 'alternative']
            if item['condition'].satisfied(context):
                useCo = 'consequence'
                skipped = 0
            else:
                useCo = 'alternative'
                skipped = countParts(item['consequence'])
            subEffects = observedEffects(
                context,
                item[useCo],
                skipWarning=skipWarning,
                baseIndex=totalCount + skipped + 1
            )
            result.extend(subEffects)
            totalCount += countParts(item)

        else:  # bad dict
            raise TypeError(
                f"Invalid consequence: items in the list must be"
                f" Effects, Challenges, or Conditions (got a dictionary"
                f" without 'skills', 'value', or 'condition' keys)."
                f"\nGot item: {repr(item)}"
            )

    return result


#--------------#
# Requirements #
#--------------#

MECHANISM_STATE_SUFFIX_RE = re.compile('(.*)(?<!:):([^:]+)$')
"""
Regular expression for finding mechanism state suffixes. These are a
single colon followed by any amount of non-colon characters until the
end of a token.
"""


class Requirement:
    """
    Represents a precondition for traversing an edge or taking an action.
    This can be any boolean expression over `Capability`, mechanism (see
    `MechanismName`), and/or `Token` states that must obtain, with
    numerical values for the number of tokens required, and specific
    mechanism states or active capabilities necessary. For example, if
    the player needs either the wall-break capability or the wall-jump
    capability plus a balloon token, or for the switch mechanism to be
    on, you could represent that using:

        ReqAny(
            ReqCapability('wall-break'),
            ReqAll(
                ReqCapability('wall-jump'),
                ReqTokens('balloon', 1)
            ),
            ReqMechanism('switch', 'on')
        )

    The subclasses define concrete requirements.

    Note that mechanism names are searched for using `lookupMechanism`,
    starting from the `DecisionID`s of the decisions on either end of
    the transition where a requirement is being checked. You may need to
    rename mechanisms to avoid a `MechanismCollisionError`if decisions
    on either end of a transition use the same mechanism name.
    """
    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        """
        This will return `True` if the requirement is satisfied in the
        given `RequirementContext`, resolving mechanisms from the
        context's set of decisions and graph, and respecting the
        context's equivalences. It returns `False` otherwise.

        The `dontRecurse` set should be unspecified to start, and will
        be used to avoid infinite recursion in cases of circular
        equivalences (requirements are not considered satisfied by
        equivalence loops).

        TODO: Examples
        """
        raise NotImplementedError(
            "Requirement is an abstract class and cannot be"
            " used directly."
        )

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError(
            "Requirement is an abstract class and cannot be compared."
        )

    def __hash__(self) -> int:
        raise NotImplementedError(
            "Requirement is an abstract class and cannot be hashed."
        )

    def walk(self) -> Generator['Requirement', None, None]:
        """
        Yields every part of the requirement in depth-first traversal
        order.
        """
        raise NotImplementedError(
            "Requirement is an abstract class and cannot be walked."
        )

    def asEffectList(self) -> List[Effect]:
        """
        Transforms this `Requirement` into a list of `Effect`
        objects that gain the `Capability`, set the `Token` amounts, and
        set the `Mechanism` states mentioned by the requirement. The
        requirement must be either a `ReqTokens`, a `ReqCapability`, a
        `ReqMechanism`, or a `ReqAll` which includes nothing besides
        those types as sub-requirements. The token and capability
        requirements at the leaves of the tree will be collected into a
        list for the result (note that whether `ReqAny` or `ReqAll` is
        used is ignored, all of the tokens/capabilities/mechanisms
        mentioned are listed). For each `Capability` requirement a
        'gain' effect for that capability will be included. For each
        `Mechanism` or `Token` requirement, a 'set' effect for that
        mechanism state or token count will be included. Note that if
        the requirement has contradictory clauses (e.g., two different
        mechanism states) multiple effects which cancel each other out
        will be included. Also note that setting token amounts may end
        up decreasing them unnecessarily.

        Raises a `TypeError` if this requirement is not suitable for
        transformation into an effect list.
        """
        raise NotImplementedError("Requirement is an abstract class.")

    def flatten(self) -> 'Requirement':
        """
        Returns a simplified version of this requirement that merges
        multiple redundant layers of `ReqAny`/`ReqAll` into single
        `ReqAny`/`ReqAll` structures, including recursively. May return
        the original requirement if there's no simplification to be done.

        Default implementation just returns `self`.
        """
        return self

    def unparse(self) -> str:
        """
        Returns a string which would convert back into this `Requirement`
        object if you fed it to `parsing.ParseFormat.parseRequirement`.

        TODO: Move this over into `parsing`?

        Examples:

        >>> r = ReqAny([
        ...     ReqCapability('capability'),
        ...     ReqTokens('token', 3),
        ...     ReqMechanism('mechanism', 'state')
        ... ])
        >>> rep = r.unparse()
        >>> rep
        '(capability|token*3|mechanism:state)'
        >>> from . import parsing
        >>> pf = parsing.ParseFormat()
        >>> back = pf.parseRequirement(rep)
        >>> back == r
        True
        >>> ReqNot(ReqNothing()).unparse()
        '!(O)'
        >>> ReqImpossible().unparse()
        'X'
        >>> r = ReqAny([ReqCapability('A'), ReqCapability('B'),
        ...     ReqCapability('C')])
        >>> rep = r.unparse()
        >>> rep
        '(A|B|C)'
        >>> back = pf.parseRequirement(rep)
        >>> back == r
        True
        """
        raise NotImplementedError("Requirement is an abstract class.")


class ReqAny(Requirement):
    """
    A disjunction requirement satisfied when any one of its
    sub-requirements is satisfied.
    """
    def __init__(self, subs: Iterable[Requirement]) -> None:
        self.subs = list(subs)

    def __hash__(self) -> int:
        result = 179843
        for sub in self.subs:
            result = 31 * (result + hash(sub))
        return result

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqAny) and other.subs == self.subs

    def __repr__(self):
        return "ReqAny(" + repr(self.subs) + ")"

    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        """
        True as long as any one of the sub-requirements is satisfied.
        """
        return any(
            sub.satisfied(context, dontRecurse)
            for sub in self.subs
        )

    def walk(self) -> Generator[Requirement, None, None]:
        yield self
        for sub in self.subs:
            yield from sub.walk()

    def asEffectList(self) -> List[Effect]:
        """
        Raises a `TypeError` since disjunctions don't have a translation
        into a simple list of effects to satisfy them.
        """
        raise TypeError(
            "Cannot convert ReqAny into an effect list:"
            " contradictory token or mechanism requirements on"
            " different branches are not easy to synthesize."
        )

    def flatten(self) -> Requirement:
        """
        Flattens this requirement by merging any sub-requirements which
        are also `ReqAny` instances into this one.
        """
        merged = []
        for sub in self.subs:
            flat = sub.flatten()
            if isinstance(flat, ReqAny):
                merged.extend(flat.subs)
            else:
                merged.append(flat)

        return ReqAny(merged)

    def unparse(self) -> str:
        return '(' + '|'.join(sub.unparse() for sub in self.subs) + ')'


class ReqAll(Requirement):
    """
    A conjunction requirement satisfied when all of its sub-requirements
    are satisfied.
    """
    def __init__(self, subs: Iterable[Requirement]) -> None:
        self.subs = list(subs)

    def __hash__(self) -> int:
        result = 182971
        for sub in self.subs:
            result = 17 * (result + hash(sub))
        return result

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqAll) and other.subs == self.subs

    def __repr__(self):
        return "ReqAll(" + repr(self.subs) + ")"

    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        """
        True as long as all of the sub-requirements are satisfied.
        """
        return all(
            sub.satisfied(context, dontRecurse)
            for sub in self.subs
        )

    def walk(self) -> Generator[Requirement, None, None]:
        yield self
        for sub in self.subs:
            yield from sub.walk()

    def asEffectList(self) -> List[Effect]:
        """
        Returns a gain list composed by adding together the gain lists
        for each sub-requirement. Note that some types of requirement
        will raise a `TypeError` during this process if they appear as a
        sub-requirement.
        """
        result = []
        for sub in self.subs:
            result += sub.asEffectList()

        return result

    def flatten(self) -> Requirement:
        """
        Flattens this requirement by merging any sub-requirements which
        are also `ReqAll` instances into this one.
        """
        merged = []
        for sub in self.subs:
            flat = sub.flatten()
            if isinstance(flat, ReqAll):
                merged.extend(flat.subs)
            else:
                merged.append(flat)

        return ReqAll(merged)

    def unparse(self) -> str:
        return '(' + '&'.join(sub.unparse() for sub in self.subs) + ')'


class ReqNot(Requirement):
    """
    A negation requirement satisfied when its sub-requirement is NOT
    satisfied.
    """
    def __init__(self, sub: Requirement) -> None:
        self.sub = sub

    def __hash__(self) -> int:
        return 17293 + hash(self.sub)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqNot) and other.sub == self.sub

    def __repr__(self):
        return "ReqNot(" + repr(self.sub) + ")"

    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        """
        True as long as the sub-requirement is not satisfied.
        """
        return not self.sub.satisfied(context, dontRecurse)

    def walk(self) -> Generator[Requirement, None, None]:
        yield self
        yield self.sub

    def asEffectList(self) -> List[Effect]:
        """
        Raises a `TypeError` since understanding a `ReqNot` in terms of
        capabilities/tokens to be gained is not straightforward, and would
        need to be done relative to a game state in any case.
        """
        raise TypeError(
            "Cannot convert ReqNot into an effect list:"
            " capabilities or tokens would have to be lost, not gained to"
            " satisfy this requirement."
        )

    def flatten(self) -> Requirement:
        return ReqNot(self.sub.flatten())

    def unparse(self) -> str:
        return '!(' + self.sub.unparse() + ')'


class ReqCapability(Requirement):
    """
    A capability requirement is satisfied if the specified capability is
    possessed by the player according to the given state.
    """
    def __init__(self, capability: Capability) -> None:
        self.capability = capability

    def __hash__(self) -> int:
        return 47923 + hash(self.capability)

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, ReqCapability)
        and other.capability == self.capability
        )

    def __repr__(self):
        return "ReqCapability(" + repr(self.capability) + ")"

    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        return hasCapabilityOrEquivalent(
            self.capability,
            context,
            dontRecurse
        )

    def walk(self) -> Generator[Requirement, None, None]:
        yield self

    def asEffectList(self) -> List[Effect]:
        """
        Returns a list containing a single 'gain' effect which grants
        the required capability.
        """
        return [effect(gain=self.capability)]

    def unparse(self) -> str:
        return self.capability


class ReqTokens(Requirement):
    """
    A token requirement satisfied if the player possesses at least a
    certain number of a given type of token.

    Note that checking the satisfaction of individual doors in a specific
    state is not enough to guarantee they're jointly traversable, since
    if a series of doors requires the same kind of token and they use up
    those tokens, further logic is needed to understand that as the
    tokens get used up, their requirements may no longer be satisfied.

    Also note that a requirement for tokens does NOT mean that tokens
    will be subtracted when traversing the door (you can have re-usable
    tokens after all). To implement a token cost, use both a requirement
    and a 'lose' effect.
    """
    def __init__(self, tokenType: Token, cost: TokenCount) -> None:
        self.tokenType = tokenType
        self.cost = cost

    def __hash__(self) -> int:
        return (17 * hash(self.tokenType)) + (11 * self.cost)

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, ReqTokens)
        and other.tokenType == self.tokenType
        and other.cost == self.cost
        )

    def __repr__(self):
        return f"ReqTokens({repr(self.tokenType)}, {repr(self.cost)})"

    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        return combinedTokenCount(context.state, self.tokenType) >= self.cost

    def walk(self) -> Generator[Requirement, None, None]:
        yield self

    def asEffectList(self) -> List[Effect]:
        """
        Returns a list containing a single 'set' effect which sets the
        required tokens (note that this may unnecessarily subtract
        tokens if the state had more than enough tokens beforehand).
        """
        return [effect(set=(self.tokenType, self.cost))]

    def unparse(self) -> str:
        return f'{self.tokenType}*{self.cost}'


class ReqMechanism(Requirement):
    """
    A mechanism requirement satisfied if the specified mechanism is in
    the specified state. The mechanism is specified by name and a lookup
    on that name will be performed when assessing the requirement, based
    on the specific position at which the requirement applies. However,
    if a `where` value is supplied, the lookup on the mechanism name will
    always start from that decision, regardless of where the requirement
    is being evaluated.
    """
    def __init__(
        self,
        mechanism: AnyMechanismSpecifier,
        state: MechanismState,
    ) -> None:
        self.mechanism = mechanism
        self.reqState = state

        # Normalize mechanism specifiers without any position information
        if isinstance(mechanism, tuple):
            if len(mechanism) != 4:
                raise ValueError(
                    f"Mechanism specifier must have 4 parts if it's a"
                    f" tuple. (Got: {mechanism})."
                )
            elif all(x is None for x in mechanism[:3]):
                self.mechanism = mechanism[3]

    def __hash__(self) -> int:
        return (
            (11 * hash(self.mechanism))
          + (31 * hash(self.reqState))
        )

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, ReqMechanism)
        and other.mechanism == self.mechanism
        and other.reqState == self.reqState
        )

    def __repr__(self):
        mRep = repr(self.mechanism)
        sRep = repr(self.reqState)
        return f"ReqMechanism({mRep}, {sRep})"

    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        return mechanismInStateOrEquivalent(
            self.mechanism,
            self.reqState,
            context,
            dontRecurse
        )

    def walk(self) -> Generator[Requirement, None, None]:
        yield self

    def asEffectList(self) -> List[Effect]:
        """
        Returns a list containing a single 'set' effect which sets the
        required mechanism to the required state.
        """
        return [effect(set=(self.mechanism, self.reqState))]

    def unparse(self) -> str:
        if isinstance(self.mechanism, (MechanismID, MechanismName)):
            return f'{self.mechanism}:{self.reqState}'
        else:  # Must be a MechanismSpecifier
            # TODO: This elsewhere!
            domain, zone, decision, mechanism = self.mechanism
            mspec = ''
            if domain is not None:
                mspec += domain + '//'
            if zone is not None:
                mspec += zone + '::'
            if decision is not None:
                mspec += decision + '::'
            mspec += mechanism
            return f'{mspec}:{self.reqState}'


class ReqNothing(Requirement):
    """
    A requirement representing that something doesn't actually have a
    requirement. This requirement is always satisfied.
    """
    def __hash__(self) -> int:
        return 127942

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqNothing)

    def __repr__(self):
        return "ReqNothing()"

    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        return True

    def walk(self) -> Generator[Requirement, None, None]:
        yield self

    def asEffectList(self) -> List[Effect]:
        """
        Returns an empty list, since nothing is required.
        """
        return []

    def unparse(self) -> str:
        return 'O'


class ReqImpossible(Requirement):
    """
    A requirement representing that something is impossible. This
    requirement is never satisfied.
    """
    def __hash__(self) -> int:
        return 478743

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ReqImpossible)

    def __repr__(self):
        return "ReqImpossible()"

    def satisfied(
        self,
        context: RequirementContext,
        dontRecurse: Optional[
            Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
        ] = None
    ) -> bool:
        return False

    def walk(self) -> Generator[Requirement, None, None]:
        yield self

    def asEffectList(self) -> List[Effect]:
        """
        Raises a `TypeError` since a `ReqImpossible` cannot be converted
        into an effect which would allow the transition to be taken.
        """
        raise TypeError(
            "Cannot convert ReqImpossible into an effect list:"
            " there are no powers or tokens which could be gained to"
            " satisfy this requirement."
        )

    def unparse(self) -> str:
        return 'X'


Equivalences = Dict[
    Union[Capability, Tuple[MechanismID, MechanismState]],
    Set[Requirement]
]
"""
An `Equivalences` dictionary maps `Capability` names and/or
(`MechanismID`, `MechanismState`) pairs to `Requirement` objects,
indicating that that single capability or mechanism state should be
considered active if the specified requirement is met. Note that this
can lead to multiple states of the same mechanism being effectively
active at once if a state other than the current state is active via an
equivalence.

When a circular dependency is created via equivalences, the capability or
mechanism state in question is considered inactive when the circular
dependency on it comes up, but the equivalence may still succeed (if it
uses a disjunction, for example).
"""


#----------------------#
# Tags and Annotations #
#----------------------#

Tag: 'TypeAlias' = str
"""
A type alias: tags are strings.

A tag is an arbitrary string key attached to a decision or transition,
with an associated value (default 1 to just mean "present").

Meanings are left up to the map-maker, but some conventions include:

TODO: Actually use these conventions, or abandon them

- `'hard'` indicates that an edge is non-trivial to navigate. An
    annotation starting with `'fail:'` can be used to name another edge
    which would be traversed instead if the player fails to navigate the
    edge (e.g., a difficult series of platforms with a pit below that
    takes you to another decision). This is of course entirely
    subjective.
- `'false'` indicates that an edge doesn't actually exist, although it
    appears to. This tag is added in the same exploration step that
    requirements are updated (normally to `ReqImpossible`) to indicate
    that although the edge appeared to be traversable, it wasn't. This
    distinguishes that case from a case where edge requirements actually
    change.
- `'error'` indicates that an edge does not actually exist, and it's
    different than `'false'` because it indicates an error on the
    player's part rather than intentional deception by the game (another
    subjective distinction). It can also be used with a colon and another
    tag to indicate that that tag was applied in error (e.g., a ledge
    thought to be too high was not actually too high). This should be
    used sparingly, because in most cases capturing the player's
    perception of the world is what's desired. This is normally applied
    in the step before an edge is removed from the graph.
- `'hidden'` indicates that an edge is non-trivial to perceive. Again
    this is subjective. `'hinted'` can be used as well to indicate that
    despite being obfuscated, there are hints that suggest the edge's
    existence.
- `'created'` indicates that this transition is newly created and
    represents a change to the decision layout. Normally, when entering
    a decision point, all visible options will be listed. When
    revisiting a decision, several things can happen:
        1. You could notice a transition you hadn't noticed before.
        2. You could traverse part of the room that you couldn't before,
           observing new transitions that have always been there (this
           would be represented as an internal edge to another decision
           node).
        3. You could observe that the decision had changed due to some
           action or event, and discover a new transition that didn't
           exist previously.
    This tag distinguishes case 3 from case 1. The presence or absence
    of a `'hidden'` tag in case 1 represents whether the newly-observed
    (but not new) transition was overlooked because it was hidden or was
    just overlooked accidentally.
"""

TagValueTypes: Tuple = (
    bool,
    int,
    float,
    str,
    list,
    dict,
    None,
    Requirement,
    Consequence
)
TagValue: 'TypeAlias' = Union[
    bool,
    int,
    float,
    str,
    list,
    dict,
    None,
    Requirement,
    Consequence
]
"""
A type alias: tag values are any kind of JSON-serializable data (so
booleans, ints, floats, strings, lists, dicts, or Nones, plus
`Requirement` and `Consequence` which have custom serialization defined
(see `parsing.CustomJSONEncoder`) The default value for tags is the
integer 1. Note that this is not enforced recursively in some places...
"""


class NoTagValue:
    """
    Class used to indicate no tag value for things that return tag values
    since `None` is a valid tag value.
    """
    pass


TagUpdateFunction: 'TypeAlias' = Callable[
    [Dict[Tag, TagValue], Tag, TagValue],
    TagValue
]
"""
A tag update function gets three arguments: the entire tags dictionary
for the thing being updated, the tag name of the tag being updated, and
the tag value for that tag. It must return a new tag value.
"""


Annotation: 'TypeAlias' = str
"A type alias: annotations are strings."


#----------------------------------#
# Exploration actions & Situations #
#----------------------------------#

ExplorationActionType = Literal[
    'noAction',
    'start',
    'take',
    'explore',
    'warp',
    'focus',
    'swap',
    'focalize',
    'revertTo',
]
"""
The valid action types for exploration actions (see
`ExplorationAction`).
"""

ExplorationAction: 'TypeAlias' = Union[
    Tuple[Literal['noAction']],
    Tuple[
        Literal['start'],
        Union[DecisionID, Dict[FocalPointName, DecisionID], Set[DecisionID]],
        Optional[DecisionID],
        Domain,
        Optional[CapabilitySet],
        Optional[Dict[MechanismID, MechanismState]],
        Optional[dict]
    ],
    Tuple[
        Literal['explore'],
        ContextSpecifier,
        DecisionID,
        TransitionWithOutcomes,
        Union[DecisionName, DecisionID, None],  # new name OR target
        Optional[Transition],  # new reciprocal name
        Union[Zone, None, type[DefaultZone]]  # new level-0 zone
    ],
    Tuple[
        Literal['explore'],
        FocalPointSpecifier,
        TransitionWithOutcomes,
        Union[DecisionName, DecisionID, None],  # new name OR target
        Optional[Transition],  # new reciprocal name
        Union[Zone, None, type[DefaultZone]]  # new level-0 zone
    ],
    Tuple[
        Literal['take'],
        ContextSpecifier,
        DecisionID,
        TransitionWithOutcomes
    ],
    Tuple[Literal['take'], FocalPointSpecifier, TransitionWithOutcomes],
    Tuple[Literal['warp'], ContextSpecifier, DecisionID],
    Tuple[Literal['warp'], FocalPointSpecifier, DecisionID],
    Tuple[Literal['focus'], ContextSpecifier, Set[Domain], Set[Domain]],
    Tuple[Literal['swap'], FocalContextName],
    Tuple[Literal['focalize'], FocalContextName],
    Tuple[Literal['revertTo'], SaveSlot, Set[str]],
]
"""
Represents an action taken at one step of a `DiscreteExploration`. It's a
always a tuple, and the first element is a string naming the action. It
has multiple possible configurations:

- The string 'noAction' as a singlet means that no action has been
    taken, which can be used to represent waiting or an ending. In
    situations where the player is still deciding on an action, `None`
    (which is not a valid `ExplorationAction` should be used instead.
- The string 'start' followed by a `DecisionID` /
    (`FocalPointName`-to-`DecisionID` dictionary) / set-of-`DecisionID`s
    position(s) specifier, another `DecisionID` (or `None`), a `Domain`,
    and then optional `CapabilitySet`, mechanism state dictionary, and
    custom state dictionary objects (each of which could instead be
    `None` for default). This indicates setting up starting state in a
    new focal context. The first decision ID (or similar) specifies
    active decisions, the second specifies the primary decision (which
    ought to be one of the active ones). It always affects the active
    focal context, and a `BadStart` error will result if that context
    already has any active decisions in the specified domain. The
    specified domain must already exist and must have the appropriate
    focalization depending on the type of position(s) specifier given;
    use `DiscreteExploration.createDomain` to create a domain first if
    necessary. Likewise, any specified decisions to activate must
    already exist, use `DecisionGraph.addDecision` to create them before
    using a 'start' action.

    When mechanism states and/or custom state is specified, these
    replace current mechanism/custom states for the entire current
    state, since these things aren't focal-context-specific. Similarly,
    if capabilities are provided, these replace existing capabilities
    for the active focal context, since those aren't domain-specific.

- The string 'explore' followed by:
    * A `ContextSpecifier` indicating which context to use
    * A `DecisionID` indicating the starting decision
    * Alternatively, a `FocalPointSpecifier` can be used in place of the
        context specifier and decision to specify which focal point
        moves in a plural-focalized domain.
    * A `TransitionWithOutcomes` indicating the transition taken and
        outcomes observed (if any).
    * An optional `DecisionName` used to rename the destination.
    * An optional `Transition` used to rename the reciprocal transition.
    * An optional `Zone` used to place the destination into a
        (possibly-new) level-0 zone.
    This represents exploration of a previously-unexplored decision, in
    contrast to 'take' (see below) which represents moving across a
    previously-explored transition.

- The string 'take' followed by a `ContextSpecifier`, `DecisionID`, and
    `TransitionWithOutcomes` represents taking that transition at that
    decision, updating the specified context (i.e., common vs. active;
    to update a non-active context first swap to it). Normal
    `DomainFocalization`-based rules for updating active decisions
    determine what happens besides transition consequences, but for a
    'singular'-focalized domain (as determined by the active
    `FocalContext` in the `DiscreteExploration`'s current `State`), the
    current active decision becomes inactive and the decision at the
    other end of the selected transition becomes active. A warning or
    error may be issued if the `DecisionID` used is an inactive
    decision.
    * For 'plural'-focalized domains, a `FocalPointSpecifier` is needed
        to know which of the plural focal points to move, this takes the
        place of the source `ContextSpecifier` and `DecisionID` since it
        provides that information. In this case the third item is still a
        `Transition`.

- The string 'warp' followed by either a `DecisionID`, or a
    `FocalPointSpecifier` tuple followed by a `DecisionID`. This
    represents activating a new decision without following a
    transition in the decision graph, such as when a cutscene moves
    you. Things like teleporters can be represented by normal
    transitions; a warp should be used when there's a 1-time effect
    that has no reciprocal.

- The string 'focus' followed by a `ContextSpecifier` and then two sets
    of `Domain`s. The first one lists domains that become inactive, and
    the second lists domains that become active. This can be used to
    represent opening up a menu, although if the menu can easily be
    closed and re-opened anywhere, it's usually not necessary to track
    the focus swaps (think a cutscene that forces you to make a choice
    before being able to continue normal exploration). A focus swap can
    also be the consequence of taking a transition, in which case the
    exploration action just identifies the transition using one of the
    formats above.

- The string 'swap' is followed by a `FocalContextName` and represents
    a complete `FocalContext` swap. If this something the player can
    trigger at will (or under certain conditions) it's better to use a
    transition consequence and have the action be taking that transition.

- The string 'focalize' is followed by an unused `FocalContextName`
    and represents the creation of a new empty focal context (which
    will also be swapped-to).
    # TODO: domain and context focus swaps as effects!

- The  string 'revertTo' followed by a `SaveSlot` and then a set of
    reversion aspects (see `revertedState`). This will update the
    situation by restoring a previous state (or potentially only parts of
    it). An empty set of reversion aspects invokes the default revert
    behavior, which reverts all aspects of the state, except that changes
    to the `DecisionGraph` are preserved.
"""


def describeExplorationAction(
    situation: 'Situation',
    action: Optional[ExplorationAction]
) -> str:
    """
    Returns a string description of the action represented by an
    `ExplorationAction` object (or the string '(no action)' for the value
    `None`). Uses the provided situation to look up things like decision
    names, focal point positions, and destinations where relevant. Does
    not know details of which graph it is applied to or the outcomes of
    the action, so just describes what is being attempted.
    """
    if action is None:
        return '(no action)'

    if (
        not isinstance(action, tuple)
     or len(action) == 0
    ):
        raise TypeError(f"Not an exploration action: {action!r}")

    graph = situation.graph

    if action[0] not in get_args(ExplorationActionType):
        raise ValueError(f"Invalid exploration action type: {action[0]!r}")

    aType = action[0]
    if aType == 'noAction':
        return "wait"

    elif aType == 'start':
        if len(action) != 7:
            raise ValueError(
                f"Wrong number of parts for 'start' action: {action!r}"
            )
        (
            _,
            startActive,
            primary,
            domain,
            capabilities,
            mechanisms,
            custom
        ) = action
        Union[DecisionID, Dict[FocalPointName, DecisionID], Set[DecisionID]]
        at: str
        if primary is None:
            if isinstance(startActive, DecisionID):
                at = f" at {graph.identityOf(startActive)}"
            elif isinstance(startActive, dict):
                at = f" with {len(startActive)} focal point(s)"
            elif isinstance(startActive, set):
                at = f" from {len(startActive)} decisions"
            else:
                raise TypeError(
                    f"Invalid type for starting location:"
                    f" {type(startActive)}"
                )
        else:
            at = f" at {graph.identityOf(primary)}"
            if isinstance(startActive, dict):
                at += f" (among {len(startActive)} focal point(s))"
            elif isinstance(startActive, set):
                at += f" (among {len(startActive)} decisions)"

        return (
            f"start exploring domain {domain}{at}"
        )

    elif aType == 'explore':
        if len(action) == 7:
            assert isinstance(action[2], DecisionID)
            fromID = action[2]
            assert isinstance(action[3], tuple)
            transitionName, specified = action[3]
            assert isinstance(action[3][0], Transition)
            assert isinstance(action[3][1], list)
            assert all(isinstance(x, bool) for x in action[3][1])
        elif len(action) == 6:
            assert isinstance(action[1], tuple)
            assert len(action[1]) == 3
            fpPos = resolvePosition(situation, action[1])
            if fpPos is None:
                raise ValueError(
                    f"Invalid focal point specifier: no position found"
                    f" for:\n{action[1]}"
                )
            else:
                fromID = fpPos
            transitionName, specified = action[2]
        else:
            raise ValueError(
                f"Wrong number of parts for 'explore' action: {action!r}"
            )

        destID = graph.getDestination(fromID, transitionName)

        frDesc = graph.identityOf(fromID)
        deDesc = graph.identityOf(destID)

        newNameOrDest: Union[DecisionName, DecisionID, None] = action[-3]
        nowWord = "now "
        if newNameOrDest is None:
            if destID is None:
                nowWord = ""
                newName = "INVALID: an unspecified + unnamed decision"
            else:
                nowWord = ""
                newName = graph.nameFor(destID)
        elif isinstance(newNameOrDest, DecisionName):
            newName = newNameOrDest
        else:
            assert isinstance(newNameOrDest, DecisionID)
            destID = newNameOrDest
            nowWord = "now reaches "
            newName = graph.identityOf(destID)

        newZone: Union[Zone, type[DefaultZone], None] = action[-1]
        if newZone in (None, DefaultZone):
            deDesc = f"{destID} ({nowWord}{newName})"
        else:
            deDesc = f"{destID} ({nowWord}{newZone}::{newName})"
            # TODO: Don't hardcode '::' here?

        oDesc = ""
        if len(specified) > 0:
            oDesc = " with outcomes: "
            first = True
            for o in specified:
                if first:
                    first = False
                else:
                    oDesc += ", "
                if o:
                    oDesc += "success"
                else:
                    oDesc += "failure"

        return (
            f"explore {transitionName} from decision {frDesc} to"
            f" {deDesc}{oDesc}"
        )

    elif aType == 'take':
        if len(action) == 4:
            assert action[1] in get_args(ContextSpecifier)
            assert isinstance(action[2], DecisionID)
            assert isinstance(action[3], tuple)
            assert len(action[3]) == 2
            assert isinstance(action[3][0], Transition)
            assert isinstance(action[3][1], list)
            context = action[1]
            fromID = action[2]
            transitionName, specified = action[3]
            destID = graph.getDestination(fromID, transitionName)
            oDesc = ""
            if len(specified) > 0:
                oDesc = " with outcomes: "
                first = True
                for o in specified:
                    if first:
                        first = False
                    else:
                        oDesc += ", "
                    if o:
                        oDesc += "success"
                    else:
                        oDesc += "failure"
            if fromID == destID:  # an action
                return f"do action {transitionName}"
            else:  # normal transition
                frDesc = graph.identityOf(fromID)
                deDesc = graph.identityOf(destID)

                return (
                    f"take {transitionName} from decision {frDesc} to"
                    f" {deDesc}{oDesc}"
                )
        elif len(action) == 3:
            assert isinstance(action[1], tuple)
            assert len(action[1]) == 3
            assert isinstance(action[2], tuple)
            assert len(action[2]) == 2
            assert isinstance(action[2][0], Transition)
            assert isinstance(action[2][1], list)
            _, focalPoint, transition = action
            context, domain, name = focalPoint
            frID = resolvePosition(situation, focalPoint)

            transitionName, specified = action[2]
            oDesc = ""
            if len(specified) > 0:
                oDesc = " with outcomes: "
                first = True
                for o in specified:
                    if first:
                        first = False
                    else:
                        oDesc += ", "
                    if o:
                        oDesc += "success"
                    else:
                        oDesc += "failure"

            if frID is None:
                return (
                    f"invalid action (moves {focalPoint} which doesn't"
                    f" exist)"
                )
            else:
                destID = graph.getDestination(frID, transitionName)

                if frID == destID:
                    return "do action {transition}{oDesc}"
                else:
                    frDesc = graph.identityOf(frID)
                    deDesc = graph.identityOf(destID)
                    return (
                        f"{name} takes {transition} from {frDesc} to"
                        f" {deDesc}{oDesc}"
                    )
        else:
            raise ValueError(
                f"Wrong number of parts for 'take' action: {action!r}"
            )

    elif aType == 'warp':
        if len(action) != 3:
            raise ValueError(
                f"Wrong number of parts for 'warp' action: {action!r}"
            )
        if action[1] in get_args(ContextSpecifier):
            assert isinstance(action[1], str)
            assert isinstance(action[2], DecisionID)
            _, context, destination = action
            deDesc = graph.identityOf(destination)
            return f"warp to {deDesc!r}"
        elif isinstance(action[1], tuple) and len(action[1]) == 3:
            assert isinstance(action[2], DecisionID)
            _, focalPoint, destination = action
            context, domain, name = focalPoint
            deDesc = graph.identityOf(destination)
            frID = resolvePosition(situation, focalPoint)
            frDesc = graph.identityOf(frID)
            return f"{name} warps to {deDesc!r}"
        else:
            raise TypeError(
                f"Invalid second part for 'warp' action: {action!r}"
            )

    elif aType == 'focus':
        if len(action) != 4:
            raise ValueError(
                "Wrong number of parts for 'focus' action: {action!r}"
            )
        _, context, deactivate, activate = action
        assert isinstance(deactivate, set)
        assert isinstance(activate, set)
        result = "change in active domains: "
        clauses = []
        if len(deactivate) > 0:
            clauses.append("deactivate domain(s) {', '.join(deactivate)}")
        if len(activate) > 0:
            clauses.append("activate domain(s) {', '.join(activate)}")
        result += '; '.join(clauses)
        return result

    elif aType == 'swap':
        if len(action) != 2:
            raise ValueError(
                "Wrong number of parts for 'swap' action: {action!r}"
            )
        _, fcName = action
        return f"swap to focal context {fcName!r}"

    elif aType == 'focalize':
        if len(action) != 2:
            raise ValueError(
                "Wrong number of parts for 'focalize' action: {action!r}"
            )
        _, fcName = action
        return f"create new focal context {fcName!r}"

    else:
        raise RuntimeError(
            "Missing case for exploration action type: {action[0]!r}"
        )


DecisionType = Literal[
    "pending",
    "active",
    "unintended",
    "imposed",
    "consequence"
]
"""
The types for decisions are:
- 'pending': A decision that hasn't been made yet.
- 'active': A decision made actively and consciously (the default).
- 'unintended': A decision was made but the execution of that decision
    resulted in a different action than the one intended (note that we
    don't currently record the original intent). TODO: that?
- 'imposed': A course of action was changed/taken, but no conscious
    decision was made, meaning that the action was imposed by external
    circumstances.
- 'consequence': A different course of action resulted in a follow-up
    consequence that wasn't part of the original intent.
"""


class Situation(NamedTuple):
    """
    Holds all of the pieces of an exploration's state at a single
    exploration step, including:

    - 'graph': The `DecisionGraph` for that step. Continuity between
        graphs can be established because they use the same `DecisionID`
        for unchanged nodes.
    - 'state': The game `State` for that step, including common and
        active `FocalContext`s which determine both what capabilities
        are active in the step and which decision point(s) the player
        may select an option at.
    - 'type': The `DecisionType` for the decision made at this
        situation.
    - 'taken': an `ExplorationAction` specifying what action was taken,
        or `None` for situations where an action has not yet been
        decided on (distinct from `(`noAction`,)` for waiting). The
        effects of that action are represented by the following
        `Situation` in the `DiscreteExploration`. Note that the final
        situation in an exploration will also use `('noAction',)` as the
        'taken' value to indicate that either no further choices are
        possible (e.g., at an ending), or it will use `None` to indicate
        that no choice has been made yet.
    - 'saves': A dictionary mapping save-slot names to (graph, state)
        pairs for saved states.
    - 'tags': A dictionary of tag-name: tag-value information for this
        step, allowing custom tags with custom values to be added.
    - 'annotations': A list of `Annotation` strings allowing custom
        annotations to be applied to a situation.
    """
    graph: 'DecisionGraph'
    state: State
    type: DecisionType
    action: Optional[ExplorationAction]
    saves: Dict[SaveSlot, Tuple['DecisionGraph', State]]
    tags: Dict[Tag, TagValue]
    annotations: List[Annotation]


#-----------------------------#
# Situation support functions #
#-----------------------------#

def contextForTransition(
    situation: Situation,
    decision: AnyDecisionSpecifier,
    transition: Transition
) -> RequirementContext:
    """
    Given a `Situation` along with an `AnyDecisionSpecifier` and a
    `Transition` that together identify a particular transition of
    interest, returns the appropriate `RequirementContext` to use to
    evaluate requirements and resolve consequences for that transition,
    which involves the state & graph from the specified situation, along
    with the two ends of that transition as the search-from location.
    """
    return RequirementContext(
        graph=situation.graph,
        state=situation.state,
        searchFrom=situation.graph.bothEnds(decision, transition)
    )


def genericContextForSituation(
    situation: Situation,
    searchFrom: Optional[Set[DecisionID]] = None
) -> RequirementContext:
    """
    Turns a `Situation` into a `RequirementContext` without a specific
    transition as the origin (use `contextForTransition` if there's a
    relevant transition). By default, the `searchFrom` part of the
    requirement context will be the set of active decisions in the
    situation, but the search-from part can be overridden by supplying
    an explicit `searchFrom` set of decision IDs here.
    """
    if searchFrom is None:
        searchFrom = combinedDecisionSet(situation.state)

    return RequirementContext(
        state=situation.state,
        graph=situation.graph,
        searchFrom=searchFrom
    )


def hasCapabilityOrEquivalent(
    capability: Capability,
    context: RequirementContext,
    dontRecurse: Optional[
        Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
    ] = None
):
    """
    Determines whether a capability should be considered obtained for the
    purposes of requirements, given an entire game state and an
    equivalences dictionary which maps capabilities and/or
    mechanism/state pairs  to sets of requirements that when fulfilled
    should count as activating that capability or mechanism state.
    """
    if dontRecurse is None:
        dontRecurse = set()

    if (
        capability in context.state['common']['capabilities']['capabilities']
     or capability in (
            context.state['contexts']
                [context.state['activeContext']]
                ['capabilities']
                ['capabilities']
        )
    ):
        return True  # Capability is explicitly obtained
    elif capability in dontRecurse:
        return False  # Treat circular requirements as unsatisfied
    elif not context.graph.hasAnyEquivalents(capability):
        # No equivalences to check
        return False
    else:
        # Need to check for a satisfied equivalence
        subDont = set(dontRecurse)  # Where not to recurse
        subDont.add(capability)
        # equivalences for this capability
        options = context.graph.allEquivalents(capability)
        for req in options:
            if req.satisfied(context, subDont):
                return True

        return False


def stateOfMechanism(
    ctx: RequirementContext,
    mechanism: AnyMechanismSpecifier
) -> MechanismState:
    """
    Returns the current state of the specified mechanism, returning
    `DEFAULT_MECHANISM_STATE` if that mechanism doesn't yet have an
    assigned state.
    """
    mID = ctx.graph.resolveMechanism(mechanism, ctx.searchFrom)

    return ctx.state['mechanisms'].get(
        mID,
        DEFAULT_MECHANISM_STATE
    )


def mechanismInStateOrEquivalent(
    mechanism: AnyMechanismSpecifier,
    reqState: MechanismState,
    context: RequirementContext,
    dontRecurse: Optional[
        Set[Union[Capability, Tuple[MechanismID, MechanismState]]]
    ] = None
):
    """
    Determines whether a mechanism should be considered as being in the
    given state for the purposes of requirements, given an entire game
    state and an equivalences dictionary which maps capabilities and/or
    mechanism/state pairs to sets of requirements that when fulfilled
    should count as activating that capability or mechanism state.

    The `dontRecurse` set of capabilities and/or mechanisms indicates
    requirements which should not be considered for alternate
    fulfillment during recursion.

    Mechanisms with unspecified state are considered to be in the
    `DEFAULT_MECHANISM_STATE`, but mechanisms which don't exist are not
    considered to be in any state (i.e., this will always return False).
    """
    if dontRecurse is None:
        dontRecurse = set()

    mID = context.graph.resolveMechanism(mechanism, context.searchFrom)

    currentState = stateOfMechanism(context, mID)
    if currentState == reqState:
        return True  # Mechanism is explicitly in the target state
    elif (mID, reqState) in dontRecurse:
        return False  # Treat circular requirements as unsatisfied
    elif not context.graph.hasAnyEquivalents((mID, reqState)):
        return False  # If there are no equivalences, nothing to check
    else:
        # Need to check for a satisfied equivalence
        subDont = set(dontRecurse)  # Where not to recurse
        subDont.add((mID, reqState))
        # equivalences for this capability
        options = context.graph.allEquivalents((mID, reqState))
        for req in options:
            if req.satisfied(context, subDont):
                return True

        return False


def combinedTokenCount(state: State, tokenType: Token) -> TokenCount:
    """
    Returns the token count for a particular token type for a state,
    combining tokens from the common and active `FocalContext`s.
    """
    return (
        state['common']['capabilities']['tokens'].get(tokenType, 0)
      + state[
          'contexts'
        ][state['activeContext']]['capabilities']['tokens'].get(tokenType, 0)
    )


def explorationStatusOf(
    situation: Situation,
    decision: AnyDecisionSpecifier
) -> ExplorationStatus:
    """
    Returns the exploration status of the specified decision in the
    given situation, or the `DEFAULT_EXPLORATION_STATUS` if no status
    has been set for that decision.
    """
    dID = situation.graph.resolveDecision(decision)
    return situation.state['exploration'].get(
        dID,
        DEFAULT_EXPLORATION_STATUS
    )


def setExplorationStatus(
    situation: Situation,
    decision: AnyDecisionSpecifier,
    status: ExplorationStatus,
    upgradeOnly: bool = False
) -> None:
    """
    Sets the exploration status of the specified decision in the
    given situation. If `upgradeOnly` is set to True (default is False)
    then the exploration status will be changed only if the new status
    counts as more-explored than the old one (see `moreExplored`).
    """
    dID = situation.graph.resolveDecision(decision)
    eMap = situation.state['exploration']
    if upgradeOnly:
        status = moreExplored(
            status,
            eMap.get(dID, 'unknown')
        )
    eMap[dID] = status


def hasBeenVisited(
    situation: Situation,
    decision: AnyDecisionSpecifier
) -> bool:
    """
    Returns `True` if the specified decision has an exploration status
    which counts as having been visited (see `base.statusVisited`). Note
    that this works differently from `DecisionGraph.isConfirmed` which
    just checks for the 'unconfirmed' tag.
    """
    return statusVisited(explorationStatusOf(situation, decision))


class IndexTooFarError(IndexError):
    """
    An index error that also holds a number specifying how far beyond
    the end of the valid indices the given index was. If you are '0'
    beyond the end that means you're at the next element after the end.
    """
    def __init__(self, msg, beyond=0):
        """
        You need a message and can also include a 'beyond' value
        (default is 0).
        """
        self.msg = msg
        self.beyond = beyond

    def __str__(self):
        return self.msg + f" ({self.beyond} beyond sequence)"

    def __repr(self):
        return f"IndexTooFarError({repr(self.msg)}, {repr(self.beyond)})"


def countParts(
    consequence: Union[Consequence, Challenge, Condition, Effect]
) -> int:
    """
    Returns the number of parts the given consequence has for
    depth-first indexing purposes. The consequence itself counts as a
    part, plus each `Challenge`, `Condition`, and `Effect` within it,
    along with the part counts of any sub-`Consequence`s in challenges
    or conditions.

    For example:

    >>> countParts([])
    1
    >>> countParts([effect(gain='jump'), effect(lose='jump')])
    3
    >>> c = [  # 1
    ...     challenge(  # 2
    ...         skills=BestSkill('skill'),
    ...         level=4,
    ...         success=[],  # 3
    ...         failure=[effect(lose=('money', 10))],  # 4, 5
    ...         outcome=True
    ...    ),
    ...    condition(  # 6
    ...        ReqCapability('jump'),
    ...        [],  # 7
    ...        [effect(gain='jump')]  # 8, 9
    ...    ),
    ...    effect(set=('door', 'open'))  # 10
    ... ]
    >>> countParts(c)
    10
    >>> countParts(c[0])
    4
    >>> countParts(c[1])
    4
    >>> countParts(c[2])
    1
    >>> # (last part of the 10 is the outer list itself)
    >>> c = [  # index 0
    ...     effect(gain='happy'),  # index 1
    ...     challenge(  # index 2
    ...         skills=BestSkill('strength'),
    ...         success=[effect(gain='winner')]  # indices 3 & 4
    ...         # failure is implicit; gets index 5
    ...     )  # level defaults to 0
    ... ]
    >>> countParts(c)
    6
    >>> countParts(c[0])
    1
    >>> countParts(c[1])
    4
    >>> countParts(c[1]['success'])
    2
    >>> countParts(c[1]['failure'])
    1
    """
    total = 1
    if isinstance(consequence, list):
        for part in consequence:
            total += countParts(part)
    elif isinstance(consequence, dict):
        if 'skills' in consequence:  # it's a Challenge
            consequence = cast(Challenge, consequence)
            total += (
                countParts(consequence['success'])
              + countParts(consequence['failure'])
            )
        elif 'condition' in consequence:  # it's a Condition
            consequence = cast(Condition, consequence)
            total += (
                countParts(consequence['consequence'])
              + countParts(consequence['alternative'])
            )
        elif 'value' in consequence:  # it's an Effect
            pass  # counted already
        else:  # bad dict
            raise TypeError(
                f"Invalid consequence: items must be Effects,"
                f" Challenges, or Conditions (got a dictionary without"
                f" 'skills', 'value', or 'condition' keys)."
                f"\nGot consequence: {repr(consequence)}"
            )
    else:
        raise TypeError(
            f"Invalid consequence: must be an Effect, Challenge, or"
            f" Condition, or a list of those."
            f"\nGot part: {repr(consequence)}"
        )

    return total


def walkParts(
    consequence: Union[Consequence, Challenge, Condition, Effect],
    startIndex: int = 0
) -> Generator[
    Tuple[int, Union[Consequence, Challenge, Condition, Effect]],
    None,
    None
]:
    """
    Yields tuples containing all indices and the associated
    `Consequence`s in the given consequence tree, in depth-first
    traversal order.

    A `startIndex` other than 0 may be supplied and the indices yielded
    will start there.

    For example:

    >>> list(walkParts([]))
    [(0, [])]
    >>> e = []
    >>> list(walkParts(e))[0][1] is e
    True
    >>> c = [effect(gain='jump'), effect(lose='jump')]
    >>> list(walkParts(c)) == [
    ...     (0, c),
    ...     (1, c[0]),
    ...     (2, c[1]),
    ... ]
    True
    >>> c = [  # 1
    ...     challenge(  # 2
    ...         skills=BestSkill('skill'),
    ...         level=4,
    ...         success=[],  # 3
    ...         failure=[effect(lose=('money', 10))],  # 4, 5
    ...         outcome=True
    ...    ),
    ...    condition(  # 6
    ...        ReqCapability('jump'),
    ...        [],  # 7
    ...        [effect(gain='jump')]  # 8, 9
    ...    ),
    ...    effect(set=('door', 'open'))  # 10
    ... ]
    >>> list(walkParts(c)) == [
    ...     (0, c),
    ...     (1, c[0]),
    ...     (2, c[0]['success']),
    ...     (3, c[0]['failure']),
    ...     (4, c[0]['failure'][0]),
    ...     (5, c[1]),
    ...     (6, c[1]['consequence']),
    ...     (7, c[1]['alternative']),
    ...     (8, c[1]['alternative'][0]),
    ...     (9, c[2]),
    ... ]
    True
    """
    index = startIndex
    yield (index, consequence)
    index += 1
    if isinstance(consequence, list):
        for part in consequence:
            for (subIndex, subItem) in walkParts(part, index):
                yield (subIndex, subItem)
            index = subIndex + 1
    elif isinstance(consequence, dict) and 'skills' in consequence:
        # a Challenge
        challenge = cast(Challenge, consequence)
        for (subIndex, subItem) in walkParts(challenge['success'], index):
            yield (subIndex, subItem)
        index = subIndex + 1
        for (subIndex, subItem) in walkParts(challenge['failure'], index):
            yield (subIndex, subItem)
    elif isinstance(consequence, dict) and 'condition' in consequence:
        # a Condition
        condition = cast(Condition, consequence)
        for (subIndex, subItem) in walkParts(
            condition['consequence'],
            index
        ):
            yield (subIndex, subItem)
        index = subIndex + 1
        for (subIndex, subItem) in walkParts(
            condition['alternative'],
            index
        ):
            yield (subIndex, subItem)
    elif isinstance(consequence, dict) and 'value' in consequence:
        # an Effect; we already yielded it above
        pass
    else:
        raise TypeError(
            f"Invalid consequence: items must be lists, Effects,"
            f" Challenges, or Conditions.\nGot part:"
            f" {repr(consequence)}"
        )


def consequencePart(
    consequence: Consequence,
    index: int
) -> Union[Consequence, Challenge, Condition, Effect]:
    """
    Given a `Consequence`, returns the part at the specified index, in
    depth-first traversal order, including the consequence itself at
    index 0. Raises an `IndexTooFarError` if the index is beyond the end
    of the tree; the 'beyond' value of the error will indicate how many
    indices beyond the end it was, with 0 for an index that's just
    beyond the end.

    For example:

    >>> c = []
    >>> consequencePart(c, 0) is c
    True
    >>> try:
    ...     consequencePart(c, 1)
    ... except IndexTooFarError as e:
    ...     e.beyond
    0
    >>> try:
    ...     consequencePart(c, 2)
    ... except IndexTooFarError as e:
    ...     e.beyond
    1
    >>> c = [effect(gain='jump'), effect(lose='jump')]
    >>> consequencePart(c, 0) is c
    True
    >>> consequencePart(c, 1) is c[0]
    True
    >>> consequencePart(c, 2) is c[1]
    True
    >>> try:
    ...     consequencePart(c, 3)
    ... except IndexTooFarError as e:
    ...     e.beyond
    0
    >>> try:
    ...     consequencePart(c, 4)
    ... except IndexTooFarError as e:
    ...     e.beyond
    1
    >>> c = [
    ...     challenge(
    ...         skills=BestSkill('skill'),
    ...         level=4,
    ...         success=[],
    ...         failure=[effect(lose=('money', 10))],
    ...         outcome=True
    ...    ),
    ...    condition(ReqCapability('jump'), [], [effect(gain='jump')]),
    ...    effect(set=('door', 'open'))
    ... ]
    >>> consequencePart(c, 0) is c
    True
    >>> consequencePart(c, 1) is c[0]
    True
    >>> consequencePart(c, 2) is c[0]['success']
    True
    >>> consequencePart(c, 3) is c[0]['failure']
    True
    >>> consequencePart(c, 4) is c[0]['failure'][0]
    True
    >>> consequencePart(c, 5) is c[1]
    True
    >>> consequencePart(c, 6) is c[1]['consequence']
    True
    >>> consequencePart(c, 7) is c[1]['alternative']
    True
    >>> consequencePart(c, 8) is c[1]['alternative'][0]
    True
    >>> consequencePart(c, 9) is c[2]
    True
    >>> consequencePart(c, 10)
    Traceback (most recent call last):
    ...
    exploration.base.IndexTooFarError...
    >>> try:
    ...     consequencePart(c, 10)
    ... except IndexTooFarError as e:
    ...     e.beyond
    0
    >>> try:
    ...     consequencePart(c, 11)
    ... except IndexTooFarError as e:
    ...     e.beyond
    1
    >>> try:
    ...     consequencePart(c, 14)
    ... except IndexTooFarError as e:
    ...     e.beyond
    4
    """
    if index == 0:
        return consequence
    index -= 1
    for part in consequence:
        if index == 0:
            return part
        else:
            index -= 1
        if not isinstance(part, dict):
            raise TypeError(
                f"Invalid consequence: items in the list must be"
                f" Effects, Challenges, or Conditions."
                f"\nGot part: {repr(part)}"
            )
        elif 'skills' in part:  # it's a Challenge
            part = cast(Challenge, part)
            try:
                return consequencePart(part['success'], index)
            except IndexTooFarError as e:
                index = e.beyond
            try:
                return consequencePart(part['failure'], index)
            except IndexTooFarError as e:
                index = e.beyond
        elif 'condition' in part:  # it's a Condition
            part = cast(Condition, part)
            try:
                return consequencePart(part['consequence'], index)
            except IndexTooFarError as e:
                index = e.beyond
            try:
                return consequencePart(part['alternative'], index)
            except IndexTooFarError as e:
                index = e.beyond
        elif 'value' in part:  # it's an Effect
            pass  # if index was 0, we would have returned this part already
        else:  # bad dict
            raise TypeError(
                f"Invalid consequence: items in the list must be"
                f" Effects, Challenges, or Conditions (got a dictionary"
                f" without 'skills', 'value', or 'condition' keys)."
                f"\nGot part: {repr(part)}"
            )

    raise IndexTooFarError(
        "Part index beyond end of consequence.",
        index
    )


def lookupEffect(
    situation: Situation,
    effect: EffectSpecifier
) -> Effect:
    """
    Looks up an effect within a situation.
    """
    graph = situation.graph
    root = graph.getConsequence(effect[0], effect[1])
    try:
        result = consequencePart(root, effect[2])
    except IndexTooFarError:
        raise IndexError(
            f"Invalid effect specifier (consequence has too few parts):"
            f" {effect}"
        )

    if not isinstance(result, dict) or 'value' not in result:
        raise IndexError(
            f"Invalid effect specifier (part is not an Effect):"
            f" {effect}\nGot a/an {type(result)}:"
            f"\n  {result}"
        )

    return cast(Effect, result)


def triggerCount(
    situation: Situation,
    effect: EffectSpecifier
) -> int:
    """
    Looks up the trigger count for the specified effect in the given
    situation. This includes times the effect has been triggered but
    didn't actually do anything because of its delay and/or charges
    values.
    """
    return situation.state['effectCounts'].get(effect, 0)


def incrementTriggerCount(
    situation: Situation,
    effect: EffectSpecifier,
    add: int = 1
) -> None:
    """
    Adds one (or the specified `add` value) to the trigger count for the
    specified effect in the given situation.
    """
    counts = situation.state['effectCounts']
    if effect in counts:
        counts[effect] += add
    else:
        counts[effect] = add


def doTriggerEffect(
    situation: Situation,
    effect: EffectSpecifier
) -> Tuple[Effect, Optional[int]]:
    """
    Looks up the trigger count for the given effect, adds one, and then
    returns a tuple with the effect, plus the effective trigger count or
    `None`, returning `None` if the effect's charges or delay values
    indicate that based on its new trigger count, it should not actually
    fire, and otherwise returning a modified trigger count that takes
    delay into account.

    For example, if an effect has 2 delay and 3 charges and has been
    activated once, it will not actually trigger (since its delay value
    is still playing out). Once it hits the third attempted trigger, it
    will activate with an effective activation count of 1, since that's
    the first time it actually applies. Of course, on the 6th and
    subsequent activation attempts, it will once more cease to trigger
    because it will be out of charges.
    """
    counts = situation.state['effectCounts']
    thisCount = counts.get(effect, 0)
    counts[effect] = thisCount + 1  # increment the total count

    # Get charges and delay values
    effectDetails = lookupEffect(situation, effect)
    delay = effectDetails['delay'] or 0
    charges = effectDetails['charges']

    delayRemaining = delay - thisCount
    if delayRemaining > 0:
        return (effectDetails, None)
    else:
        thisCount -= delay

    if charges is None:
        return (effectDetails, thisCount)
    else:
        chargesRemaining = charges - thisCount
        if chargesRemaining >= 0:
            return (effectDetails, thisCount)
        else:
            return (effectDetails, None)


#------------------#
# Position support #
#------------------#

def resolvePosition(
    situation: Situation,
    posSpec: Union[Tuple[ContextSpecifier, Domain], FocalPointSpecifier]
) -> Optional[DecisionID]:
    """
    Given a tuple containing either a specific context plus a specific
    domain (which must be singular-focalized) or a full
    `FocalPointSpecifier`, this function returns the decision ID implied
    by the given specifier within the given situation, or `None` if the
    specifier is valid but the position for that specifier is `None`
    (including when the domain is not-yet-encountered). For
    singular-focalized domains, this is just the position value for that
    domain. For plural-focalized domains, you need to provide a
    `FocalPointSpecifier` and it's the position of that focal point.
    """
    fpName: Optional[FocalPointName] = None
    if len(posSpec) == 2:
        posSpec = cast(Tuple[ContextSpecifier, Domain], posSpec)
        whichContext, domain = posSpec
    elif len(posSpec) == 3:
        posSpec = cast(FocalPointSpecifier, posSpec)
        whichContext, domain, fpName = posSpec
    else:
        raise ValueError(
            f"Invalid position specifier {repr(posSpec)}. Must be a"
            f" length-2 or length-3 tuple."
        )

    state = situation.state
    if whichContext == 'common':
        targetContext = state['common']
    else:
        targetContext = state['contexts'][state['activeContext']]
    focalization = getDomainFocalization(targetContext, domain)

    if fpName is None:
        if focalization != 'singular':
            raise ValueError(
                f"Cannot resolve position {repr(posSpec)} because the"
                f" domain {repr(domain)} is not singular-focalized."
            )
        result = targetContext['activeDecisions'].get(domain)
        assert isinstance(result, DecisionID)
        return result
    else:
        if focalization != 'plural':
            raise ValueError(
                f"Cannot resolve position {repr(posSpec)} because a"
                f" focal point name was specified but the domain"
                f" {repr(domain)} is not plural-focalized."
            )
        fpMap = targetContext['activeDecisions'].get(domain, {})
        #  Double-check types for map itself and at least one entry
        assert isinstance(fpMap, dict)
        if len(fpMap) > 0:
            exKey = next(iter(fpMap))
            exVal = fpMap[exKey]
            assert isinstance(exKey, FocalPointName)
            assert exVal is None or isinstance(exVal, DecisionID)
        if fpName not in fpMap:
            raise ValueError(
                f"Cannot resolve position {repr(posSpec)} because no"
                f" focal point with name {repr(fpName)} exists in"
                f" domain {repr(domain)} for the {whichContext}"
                f" context."
            )
        return fpMap[fpName]


def updatePosition(
    situation: Situation,
    newPosition: DecisionID,
    inCommon: ContextSpecifier = "active",
    moveWhich: Optional[FocalPointName] = None
) -> None:
    """
    Given a Situation, updates the position information in that
    situation to represent updated player focalization. This can be as
    simple as a move from one virtual decision to an adjacent one, or as
    complicated as a cross-domain move where the previous decision point
    remains active and a specific focal point among a plural-focalized
    domain gets updated.

    The exploration status of the destination will be set to 'exploring'
    if it had been an unexplored status, and the 'visiting' tag in the
    `DecisionGraph` will be added (set to 1).

    TODO: Examples
    """
    graph = situation.graph
    state = situation.state
    destDomain = graph.domainFor(newPosition)

    # Set the primary decision of the state
    state['primaryDecision'] = newPosition

    if inCommon == 'common':
        targetContext = state['common']
    else:
        targetContext = state['contexts'][state['activeContext']]

    # Figure out focalization type and active decision(s)
    fType = getDomainFocalization(targetContext, destDomain)
    domainActiveMap = targetContext['activeDecisions']
    if destDomain in domainActiveMap:
        active = domainActiveMap[destDomain]
    else:
        if fType == 'singular':
            active = domainActiveMap.setdefault(destDomain, None)
        elif fType == 'plural':
            active = domainActiveMap.setdefault(destDomain, {})
        else:
            assert fType == 'spreading'
            active = domainActiveMap.setdefault(destDomain, set())

    if fType == 'plural':
        assert isinstance(active, dict)
        if len(active) > 0:
            exKey = next(iter(active))
            exVal = active[exKey]
            assert isinstance(exKey, FocalPointName)
            assert exVal is None or isinstance(exVal, DecisionID)
        if moveWhich is None and len(active) > 1:
            raise ValueError(
                f"Invalid position update: move is going to decision"
                f" {graph.identityOf(newPosition)} in domain"
                f" {repr(destDomain)}, but it did not specify which"
                f" focal point to move, and that domain has plural"
                f" focalization with more than one focal point."
            )
        elif moveWhich is None:
            moveWhich = list(active)[0]

        # Actually move the specified focal point
        active[moveWhich] = newPosition

    elif moveWhich is not None:
        raise ValueError(
            f"Invalid position update: move going to decision"
            f" {graph.identityOf(newPosition)} in domain"
            f" {repr(destDomain)}, specified that focal point"
            f" {repr(moveWhich)} should be moved, but that domain does"
            f" not have plural focalization, so it does not have"
            f" multiple focal points to move."
        )

    elif fType == 'singular':
        # Update the single position:
        domainActiveMap[destDomain] = newPosition

    elif fType == 'spreading':
        # Add the new position:
        assert isinstance(active, set)
        active.add(newPosition)

    else:
        raise ValueError(f"Invalid focalization value: {repr(fType)}")

    graph.untagDecision(newPosition, 'unconfirmed')
    if not hasBeenVisited(situation, newPosition):
        setExplorationStatus(
            situation,
            newPosition,
            'exploring',
            upgradeOnly=True
        )


#--------------------------------#
# Geographic exploration support #
#--------------------------------#

PointID: 'TypeAlias' = int

Coords: 'TypeAlias' = Sequence[float]

AnyPoint: 'TypeAlias' = Union[PointID, Coords]

Feature: 'TypeAlias' = str
"""
Each feature in a `FeatureGraph` gets a globally unique id, but also has
an explorer-assigned name. These names may repeat themselves (especially
in different regions) so a region-based address, possibly with a
creation-order numeral, can be used to specify a feature exactly even
without using its ID. Any string can be used, but for ease of parsing
and conversion between formats, sticking to alphanumerics plus
underscores is usually desirable.
"""

FeatureID: 'TypeAlias' = int
"""
Features in a feature graph have unique integer identifiers that are
assigned automatically in order of creation.
"""

Part: 'TypeAlias' = str
"""
Parts of a feature are identified using strings. Standard part names
include 'middle', compass directions, and top/bottom. To include both a
compass direction and a vertical position, put the vertical position
first and separate with a dash, like 'top-north'. Temporal positions
like start/end may also apply in some cases.
"""


class FeatureSpecifier(NamedTuple):
    """
    There are several ways to specify a feature within a `FeatureGraph`:
    Simplest is to just include the `FeatureID` directly (in that case
    the domain must be `None` and the 'within' sequence must be empty).
    A specific domain and/or a sequence of containing features (starting
    from most-external to most-internal) may also be specified when a
    string is used as the feature itself, to help disambiguate (when an
    ambiguous `FeatureSpecifier` is used,
    `AmbiguousFeatureSpecifierError` may arise in some cases). For any
    feature, a part may also be specified indicating which part of the
    feature is being referred to; this can be `None` when not referring
    to any specific sub-part.
    """
    domain: Optional[Domain]
    within: Sequence[Feature]
    feature: Union[Feature, FeatureID]
    part: Optional[Part]


def feature(
    name: Feature,
    part: Optional[Part] = None,
    domain: Optional[Domain] = None,
    within: Optional[Sequence[Feature]] = None
) -> FeatureSpecifier:
    """
    Builds a `FeatureSpecifier` with some defaults. The default domain
    is `None`, and by default the feature has an empty 'within' field and
    its part field is `None`.
    """
    if within is None:
        within = []
    return FeatureSpecifier(
        domain=domain,
        within=within,
        feature=name,
        part=part
    )


AnyFeatureSpecifier: 'TypeAlias' = Union[
    FeatureID,
    Feature,
    FeatureSpecifier
]
"""
A type for locations where a feature may be specified multiple different
ways: directly by ID, by full feature specifier, or by a string
identifying a feature name. You can use `normalizeFeatureSpecifier` to
convert one of these to a `FeatureSpecifier`.
"""


def normalizeFeatureSpecifier(spec: AnyFeatureSpecifier) -> FeatureSpecifier:
    """
    Turns an `AnyFeatureSpecifier` into a `FeatureSpecifier`. Note that
    it does not do parsing from a complex string. Use
    `parsing.ParseFormat.parseFeatureSpecifier` for that.

    It will turn a feature specifier with an int-convertible feature name
    into a feature-ID-based specifier, discarding any domain and/or zone
    parts.

    TODO: Issue a warning if parts are discarded?
    """
    if isinstance(spec, (FeatureID, Feature)):
        return FeatureSpecifier(
            domain=None,
            within=[],
            feature=spec,
            part=None
        )
    elif isinstance(spec, FeatureSpecifier):
        try:
            fID = int(spec.feature)
            return FeatureSpecifier(None, [], fID, spec.part)
        except ValueError:
            return spec
    else:
        raise TypeError(
            f"Invalid feature specifier type: {type(spec)}"
        )


class MetricSpace:
    """
    TODO
    Represents a variable-dimensional coordinate system within which
    locations can be identified by coordinates. May (or may not) include
    a reference to one or more images which are visual representation(s)
    of the space.
    """
    def __init__(self, name: str):
        self.name = name

        self.points: Dict[PointID, Coords] = {}
        # Holds all IDs and their corresponding coordinates as key/value
        # pairs

        self.nextID: PointID = 0
        # ID numbers should not be repeated or reused

    def addPoint(self, coords: Coords) -> PointID:
        """
        Given a sequence (list/array/etc) of int coordinates, creates a
        point and adds it to the metric space object

        >>> ms = MetricSpace("test")
        >>> ms.addPoint([2, 3])
        0
        >>> #expected result
        >>> ms.addPoint([2, 7, 0])
        1
        """
        thisID = self.nextID

        self.nextID += 1

        self.points[thisID] = coords  # creates key value pair

        return thisID

        # How do we "add" things to the metric space? What data structure
        # is it? dictionary

    def removePoint(self, thisID: PointID) -> None:
        """
        Given the ID of a point/coord, checks the dictionary
        (points) for that key and removes the key/value pair from
        it.

        >>> ms = MetricSpace("test")
        >>> ms.addPoint([2, 3])
        0
        >>> ms.removePoint(0)
        >>> ms.removePoint(0)
        Traceback (most recent call last):
        ...
        KeyError...
        >>> #expected result should be a caught KeyNotFound exception
        """
        self.points.pop(thisID)

    def distance(self, origin: AnyPoint, dest: AnyPoint) -> float:
        """
        Given an orgin point and destination point, returns the
        distance between the two points as a float.

        >>> ms = MetricSpace("test")
        >>> ms.addPoint([4, 0])
        0
        >>> ms.addPoint([1, 0])
        1
        >>> ms.distance(0, 1)
        3.0
        >>> p1 = ms.addPoint([4, 3])
        >>> p2 = ms.addPoint([4, 9])
        >>> ms.distance(p1, p2)
        6.0
        >>> ms.distance([8, 6], [4, 6])
        4.0
        >>> ms.distance([1, 1], [1, 1])
        0.0
        >>> ms.distance([-2, -3], [-5, -7])
        5.0
        >>> ms.distance([2.5, 3.7], [4.9, 6.1])
        3.394112549695428
        """
        if isinstance(origin, PointID):
            coord1 = self.points[origin]
        else:
            coord1 = origin

        if isinstance(dest, PointID):
            coord2 = self.points[dest]
        else:
            coord2 = dest

        inside = 0.0

        for dim in range(max(len(coord1), len(coord2))):
            if dim < len(coord1):
                val1 = coord1[dim]
            else:
                val1 = 0
            if dim < len(coord2):
                val2 = coord2[dim]
            else:
                val2 = 0

            inside += (val2 - val1)**2

        result = math.sqrt(inside)
        return result

    def NDCoords(
        self,
        point: AnyPoint,
        numDimension: int
    ) -> Coords:
        """
        Given a 2D set of coordinates (x, y), converts them to the desired
        dimension

        >>> ms = MetricSpace("test")
        >>> ms.NDCoords([5, 9], 3)
        [5, 9, 0]
        >>> ms.NDCoords([3, 1], 1)
        [3]
        """
        if isinstance(point, PointID):
            coords = self.points[point]
        else:
            coords = point

        seqLength = len(coords)

        if seqLength != numDimension:

            newCoords: Coords

            if seqLength < numDimension:

                newCoords = [item for item in coords]

                for i in range(numDimension - seqLength):
                    newCoords.append(0)

            else:
                newCoords = coords[:numDimension]

        return newCoords

    def lastID(self) -> PointID:
        """
        Returns the most updated ID of the metricSpace instance. The nextID
        field is always 1 more than the last assigned ID. Assumes that there
        has at least been one ID assigned to a point as a key value pair
        in the dictionary. Returns 0 if that is not the case. Does not
        consider possible counting errors if a point has been removed from
        the dictionary. The last ID does not neccessarily equal the number
        of points in the metricSpace (or in the dictionary).

        >>> ms = MetricSpace("test")
        >>> ms.lastID()
        0
        >>> ms.addPoint([2, 3])
        0
        >>> ms.addPoint([2, 7, 0])
        1
        >>> ms.addPoint([2, 7])
        2
        >>> ms.lastID()
        2
        >>> ms.removePoint(2)
        >>> ms.lastID()
        2
        """
        if self.nextID < 1:
            return self.nextID
        return self.nextID - 1


def featurePart(spec: AnyFeatureSpecifier, part: Part) -> FeatureSpecifier:
    """
    Returns a new feature specifier (and/or normalizes to one) that
    contains the specified part in the 'part' slot. If the provided
    feature specifier already contains a 'part', that will be replaced.

    For example:

    >>> featurePart('town', 'north')
    FeatureSpecifier(domain=None, within=[], feature='town', part='north')
    >>> featurePart(5, 'top')
    FeatureSpecifier(domain=None, within=[], feature=5, part='top')
    >>> featurePart(
    ...     FeatureSpecifier('dom', ['one', 'two'], 'three', 'middle'),
    ...     'top'
    ... )
    FeatureSpecifier(domain='dom', within=['one', 'two'], feature='three',\
 part='top')
    >>> featurePart(FeatureSpecifier(None, ['region'], 'place', None), 'top')
    FeatureSpecifier(domain=None, within=['region'], feature='place',\
 part='top')
    """
    spec = normalizeFeatureSpecifier(spec)
    return FeatureSpecifier(spec.domain, spec.within, spec.feature, part)


FeatureType = Literal[
    'node',
    'path',
    'edge',
    'region',
    'landmark',
    'affordance',
    'entity'
]
"""
The different types of features that a `FeatureGraph` can have:

1. Nodes, representing destinations, and/or intersections. A node is
    something that one can be "at" and possibly "in."
2. Paths, connecting nodes and/or other elements. Also used to represent
    access points (like doorways between regions) even when they don't
    have length.
3. Edges, separating regions and/or impeding movement (but a door is also
    a kind of edge).
4. Regions, enclosing other elements and/or regions. Besides via
    containment, region-region connections are mediated by nodes, paths,
    and/or edges.
5. Landmarks, which are recognizable and possibly visible from afar.
6. Affordances, which are exploration-relevant location-specific actions
    that can be taken, such as a lever that can be pulled. Affordances
    may require positioning within multiple domains, but should only be
    marked in the most-relevant domain, with cross-domain linkages for
    things like observability. Note that the other spatial object types
    have their own natural affordances; this is used to mark affordances
    beyond those. Each affordance can have a list of `Consequence`s to
    indicate what happens when it is activated.
7. Entities, which can be interacted with, such as an NPC which can be
    talked to. Can also be used to represent the player's avatar in a
    particular domain. Can have adjacent (touching) affordances to
    represent specific interaction options, and may have nodes which
    represent options for deeper interaction, but has a generic
    'interact' affordance as well. In general, adjacent affordances
    should be used to represent options for interaction that are
    triggerable directly within the explorable space, such as the fact
    that an NPC can be pushed or picked up or the like. In contrast,
    interaction options accessible via opening an interaction menu
    should be represented by a 'hasOptions' link to a node (typically in
    a separate domain) which has some combination of affordances and/or
    further interior nodes representing sub-menus. Sub-menus gated on
    some kind of requirement can list those requirements for entry.
"""

FeatureRelationshipType = Literal[
    'contains',
    'within',
    'touches',
    'observable',
    'positioned',
    'entranceFor',
    'enterTo',
    'optionsFor',
    'hasOptions',
    'interacting',
    'triggeredBy',
    'triggers',
]
"""
The possible relationships between features in a `FeatureGraph`:

- 'contains', specifies that one element contains another. Regions can
    contain other elements, including other regions, and nodes can
    contain regions (but only indirectly other elements). A region
    contained by a node represents some kind of interior space for that
    node, and this can be used for fractal detail levels (e.g., a town is
    a node on the overworld but when you enter it it's a full region
    inside, to contrast with a town as a sub-region of the overworld with
    no special enter/exit mechanics). The opposite relation is 'within'.
- 'touches' specifies that two elements touch each other. Not used for
    regions directly (an edge, path, or node should intercede). The
    relationship is reciprocal, but not transitive.
- 'observable' specifies that the target element is observable (visible
    or otherwise perceivable) from the source element. Can be tagged to
    indicate things like partial observability and/or
    difficult-to-observe elements. By default, things that touch each
    other are considered mutually observable, even without an
    'observable' relation being added.
- 'positioned' to indicate a specific relative position of two objects,
    with tags on the edge used to indicate what the relationship is.
    E.g., "the table is 10 feet northwest of the chair" has multiple
    possible representations, one of which is a 'positioned' relation
    from the table to the chair, with the 'direction' tag set to
    'southeast' and the 'distance' tag set to '10 feet'. Note that a
    `MetricSpace` may also be used to track coordinate positions of
    things; annotating every possible position relationship is not
    expected.
- 'entranceFor' to indicate which feature contained inside of a node is
    enterable from outside the node (possibly from a specific part of
    the outside of the node). 'enterTo' is the reciprocal relationship.
    'entranceFor' applies from the interior region to the exterior node,
    while 'enterTo' goes the other way. Note that you cannot use two
    different part specifiers to mark the *same* region as enter-able
    from two parts of the same node: each pair of nodes can only have
    one 'enteranceFor'/'enterTo' connection between them.
- 'optionsFor' to indicate which node associated with an entity holds
    the set of options for interaction with that entity. Such nodes are
    typically placed within a separate domain from the main exploration
    space. The same node could be the options for multiple entities. The
    reciprocal is 'hasOptions'. In both cases, a part specifier may be
    used to indicate more specifically how the interaction is initiated,
    but note that a given pair of entities cannot have multiple
    'optionsFor'/'hasOption' links between them. You could have multiple
    separate nodes that are 'optionsFor' the same entity with different
    parts (or even with no part specified for either, although that
    would create ambiguity in terms of action outcomes).
- 'interacting' to indicate when one feature is taking action relative
    to another. This relationship will have an 'action' tag which will
    contain a `FeatureAction` dictionary that specifies the relationship
    target as its 'subject'. This does not have a reciprocal, and is
    normal ephemeral.
- 'triggeredBy' to indicate when some kind of action with a feature
    triggers an affordance. The reciprocal is 'triggers'. The link tag
    'triggerInfo' will specify:
    * 'action': the action whose use trips the trigger (one of the
        `FeatureAffordance`s)
    * 'directions' (optional): A set of directions, one of which must
        match the specified direction of a `FeatureAction` for the
        trigger to trip. When this key is not present, no direction
        filtering is applied.
    * 'parts' (optional): A set of part specifiers, one of which must
        match the specified action part for the trigger to trip. When
        this key is not present, no part filtering is applied.
    * 'entityTags' (optional): A set of entity tags, any of which must
        match a tag on an interacting entity for the trigger to trip.
        Items in the set may also be tuples of multiple tags, in which
        case all items in the tuple must match for the entity to
        qualify.

Note that any of these relationships can be tagged as 'temporary' to
imply malleability. For example, a bus node could be temporarily 'at' a
bus stop node and 'within' a corresponding region, but then those
relationships could change when it moves on.
"""

FREL_RECIPROCALS: Dict[
    FeatureRelationshipType,
    FeatureRelationshipType
] = {
    "contains": "within",
    "within": "contains",
    "touches": "touches",
    "entranceFor": "enterTo",
    "enterTo": "entranceFor",
    "optionsFor": "hasOptions",
    "hasOptions": "optionsFor",
    "triggeredBy": "triggers",
    "triggers": "triggeredBy",
}
"""
The reciprocal feature relation types for each `FeatureRelationshipType`
which has a required reciprocal.
"""


class FeatureDecision(TypedDict):
    """
    Represents a decision made during exploration, including the
    position(s) at which the explorer made the decision, which
    feature(s) were most relevant to the decision and what course of
    action was decided upon (see `FeatureAction`). Has the following
    slots:

    - 'type': The type of decision (see `exploration.core.DecisionType`).
    - 'domains': A set of domains which are active during the decision,
        as opposed to domains which may be unfocused or otherwise
        inactive.
    - 'focus': An optional single `FeatureSpecifier` which represents the
        focal character or object for a decision. May be `None` e.g. in
        cases where a menu is in focus. Note that the 'positions' slot
        determines which positions are relevant to the decision,
        potentially separately from the focus but usually overlapping it.
    - 'positions': A dictionary mapping `core.Domain`s to sets of
        `FeatureSpecifier`s representing the player's position(s) in
        each domain. Some domains may function like tech trees, where
        the set of positions only expands over time. Others may function
        like a single avatar in a virtual world, where there is only one
        position. Still others might function like a group of virtual
        avatars, with multiple positions that can be updated
        independently.
    - 'intention': A `FeatureAction` indicating the action taken or
        attempted next as a result of the decision.
    """
    # TODO: HERE
    pass


FeatureAffordance = Literal[
    'approach',
    'recede',
    'follow',
    'cross',
    'enter',
    'exit',
    'explore',
    'scrutinize',
    'do',
    'interact',
    'focus',
]
"""
The list of verbs that can be used to express actions taken in relation
to features in a feature graph:

- 'approach' and 'recede' apply to nodes, paths, edges, regions, and
    landmarks, and indicate movement towards or away from the feature.
- 'follow' applies to paths and edges, and indicates travelling along.
    May be bundled with a direction indicator, although this can
    sometimes be inferred (e.g., if you're starting at a node that's
    touching one end of a path). For edges, a side-indicator may also be
    included. A destination-indicator can be used to indicate where
    along the item you end up (according to which other feature touching
    it you arrive at).
- 'cross' applies to nodes, paths, edges, and regions, and may include a
    destination indicator when there are multiple possible destinations
    on the other side of the target from the current position.
- 'enter' and 'exit' apply to regions and nodes, and indicate going
    inside of or coming out of the feature. The 'entranceFor' and
    'enterTo' relations are used to indicate where you'll end up when
    entering a node, note that there can be multiple of these attached
    to different parts of the node. A destination indicator can also be
    specified on the action.
- 'explore' applies to regions, nodes, and paths, and edges, and
    indicates a general lower-fractal-level series of actions taken to
    gain more complete knowledge about the target.
- 'scrutinize' applies to any feature and indicates carefully probing
    the details of the feature to learn more about it (e.g., to look for
    a secret).
- 'do' applies to affordances, and indicates performing whatever special
    action they represent.
- 'interact' applies to entities, and indicates some kind of generic
    interaction with the entity. For more specific interactions, you can
    do one of two things:
    1. Place affordances touching or within the entity.
    2. Use an 'optionsFor' link to indicate which node (typically in a
        separate domain) represents the options made available by an
        interaction.
- 'focus' applies to any kind of node, but usually entities. It
    represents changing the focal object/character for the player.
    However, note that focus shifts often happen without this affordance
    being involved, such as when entering a menu.
"""

FEATURE_TYPE_AFFORDANCES: Dict[FeatureAffordance, Set[FeatureType]] = {
    'approach': {'node', 'path', 'edge', 'region', 'landmark', 'entity'},
    'recede': {'node', 'path', 'edge', 'region', 'landmark', 'entity'},
    'follow': {'edge', 'path', 'entity'},
    'cross': {'node', 'path', 'edge', 'region'},
    'enter': {'node', 'region'},
    'exit': {'node', 'region'},
    'explore': {'node', 'path', 'edge', 'region'},
    'scrutinize': {
        'node', 'path', 'edge', 'region', 'landmark', 'affordance',
        'entity'
    },
    'do': {'affordance'},
    'interact': {'node', 'entity'},
}
"""
The mapping from affordances to the sets of feature types those
affordances apply to.
"""


class FeatureEffect(TypedDict):
    """
    Similar to `Effect` but with more options for how to manipulate the
    game state. This represents a single concrete change to either
    internal game state, or to the feature graph. Multiple changes
    (possibly with random factors involved) can be represented by a
    `Consequence`; a `FeatureEffect` is used as a leaf in a `Consequence`
    tree.
    """
    type: Literal[
        'gain',
        'lose',
        'toggle',
        'deactivate',
        'move',
        'focus',
        'initiate'
        'foreground',
        'background',
    ]
    value: Union[
        Capability,
        Tuple[Token, int],
        List[Capability],
        None
    ]
    charges: Optional[int]
    delay: Optional[int]


def featureEffect(
    #applyTo: ContextSpecifier = 'active',
    #gain: Optional[Union[
    #    Capability,
    #    Tuple[Token, TokenCount],
    #    Tuple[Literal['skill'], Skill, Level]
    #]] = None,
    #lose: Optional[Union[
    #    Capability,
    #    Tuple[Token, TokenCount],
    #    Tuple[Literal['skill'], Skill, Level]
    #]] = None,
    #set: Optional[Union[
    #    Tuple[Token, TokenCount],
    #    Tuple[AnyMechanismSpecifier, MechanismState],
    #    Tuple[Literal['skill'], Skill, Level]
    #]] = None,
    #toggle: Optional[Union[
    #    Tuple[AnyMechanismSpecifier, List[MechanismState]],
    #    List[Capability]
    #]] = None,
    #deactivate: Optional[bool] = None,
    #edit: Optional[List[List[commands.Command]]] = None,
    #goto: Optional[Union[
    #    AnyDecisionSpecifier,
    #    Tuple[AnyDecisionSpecifier, FocalPointName]
    #]] = None,
    #bounce: Optional[bool] = None,
    #delay: Optional[int] = None,
    #charges: Optional[int] = None,
    **kwargs
):
    # TODO: HERE
    return effect(**kwargs)

# TODO: FeatureConsequences?


class FeatureAction(TypedDict):
    """
    Indicates an action decided on by a `FeatureDecision`. Has the
    following slots:

    - 'subject': the main feature (an `AnyFeatureSpecifier`) that
        performs the action (usually an 'entity').
    - 'object': the main feature (an `AnyFeatureSpecifier`) with which
        the affordance is performed.
    - 'affordance': the specific `FeatureAffordance` indicating the type
        of action.
    - 'direction': The general direction of movement (especially when
        the affordance is `follow`). This can be either a direction in
        an associated `MetricSpace`, or it can be defined towards or
        away from the destination specified. If a destination but no
        direction is provided, the direction is assumed to be towards
        that destination.
    - 'part': The part within/along a feature for movement (e.g., which
        side of an edge are you on, or which part of a region are you
        traveling through).
    - 'destination': The destination of the action (when known ahead of
        time). For example, moving along a path towards a particular
        feature touching that path, or entering a node into a particular
        feature within that node. Note that entering of regions can be
        left implicit: if you enter a region to get to a landmark within
        it, noting that as approaching the landmark is more appropriate
        than noting that as entering the region with the landmark as the
        destination. The system can infer what regions you're in by
        which feature you're at.
    - 'outcome': A `Consequence` list/tree indicating one or more
        outcomes, possibly involving challenges. Note that the actual
        outcomes of an action may be altered by triggers; the outcomes
        listed here are the default outcomes if no triggers are tripped.

    The 'direction', 'part', and/or 'destination' may each be None,
    depending on the type of affordance and/or amount of detail desired.
    """
    subject: AnyFeatureSpecifier
    object: AnyFeatureSpecifier
    affordance: FeatureAffordance
    direction: Optional[Part]
    part: Optional[Part]
    destination: Optional[AnyFeatureSpecifier]
    outcome: Consequence
