"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-3-3
- Purpose: Core types and tools for dealing with them.

This file defines the main types used for processing and storing
`DiscreteExploration` objects. Note that the types in `open.py` like
`OpenExploration` represent more generic and broadly capable types.

Key types defined here are:

- `DecisionGraph`: Represents a graph of decisions, including observed
    connections to unknown destinations. This works well for games that
    focus on rooms with discrete exits where there are few open spaces to
    explore, and where pretending that each decision has a discrete set
    of options is not too much of a distortion.
- `DiscreteExploration`: A list of `DecisionGraph`s with position and
    transition information representing exploration over time.
"""

# TODO: Some way to specify the visibility conditions of a transition,
# separately from its traversal conditions? Or at least a way to specify
# that a transition is only visible when traversable (like successive
# upgrades or warp zone connections).

from typing import (
    Any, Optional, List, Set, Union, cast, Tuple, Dict, TypedDict,
    Sequence, Collection, Literal, get_args, Callable, TypeVar,
    Iterator, Generator
)

import copy
import warnings
import inspect

from . import graphs
from . import base
from . import utils
from . import commands


#---------#
# Globals #
#---------#

ENDINGS_DOMAIN = 'endings'
"""
Domain value for endings.
"""

TRIGGERS_DOMAIN = 'triggers'
"""
Domain value for triggers.
"""


#------------------#
# Supporting types #
#------------------#


LookupResult = TypeVar('LookupResult')
"""
A type variable for lookup results from the generic
`DecisionGraph.localLookup` function.
"""

LookupLayersList = List[Union[None, int, str]]
"""
A list of layers to look things up in, consisting of `None` for the
starting provided decision set, integers for zone heights, and some
custom strings like "fallback" and "all" for fallback sets.
"""


class DecisionInfo(TypedDict):
    """
    The information stored per-decision in a `DecisionGraph` includes
    the decision name (since the key is a decision ID), the domain, a
    tags dictionary, and an annotations list.
    """
    name: base.DecisionName
    domain: base.Domain
    tags: Dict[base.Tag, base.TagValue]
    annotations: List[base.Annotation]


#-----------------------#
# Transition properties #
#-----------------------#

class TransitionProperties(TypedDict, total=False):
    """
    Represents bundled properties of a transition, including a
    requirement, effects, tags, and/or annotations. Does not include the
    reciprocal. Has the following slots:

    - `'requirement'`: The requirement for the transition. This is
        always a `Requirement`, although it might be `ReqNothing` if
        nothing special is required.
    - `'consequence'`: The `Consequence` of the transition.
    - `'tags'`: Any tags applied to the transition (as a dictionary).
    - `'annotations'`: A list of annotations applied to the transition.
    """
    requirement: base.Requirement
    consequence: base.Consequence
    tags: Dict[base.Tag, base.TagValue]
    annotations: List[base.Annotation]


def mergeProperties(
    a: Optional[TransitionProperties],
    b: Optional[TransitionProperties]
) -> TransitionProperties:
    """
    Merges two sets of transition properties, following these rules:

    1. Tags and annotations are combined. Annotations from the
        second property set are ordered after those from the first.
    2. If one of the transitions has a `ReqNothing` instance as its
        requirement, we use the other requirement. If both have
        complex requirements, we create a new `ReqAll` which
        combines them as the requirement.
    3. The consequences are merged by placing all of the consequences of
        the first transition before those of the second one. This may in
        some cases change the net outcome of those consequences,
        because not all transition properties are compatible. (Imagine
        merging two transitions one of which causes a capability to be
        gained and the other of which causes a capability to be lost.
        What should happen?).
    4. The result will not list a reciprocal.

    If either transition is `None`, then a deep copy of the other is
    returned. If both are `None`, then an empty transition properties
    dictionary is returned, with `ReqNothing` as the requirement, no
    effects, no tags, and no annotations.

    Deep copies of consequences are always made, so that any `Effects`
    applications which edit effects won't end up with entangled effects.
    """
    if a is None:
        if b is None:
            return {
                "requirement": base.ReqNothing(),
                "consequence": [],
                "tags": {},
                "annotations": []
            }
        else:
            return copy.deepcopy(b)
    elif b is None:
        return copy.deepcopy(a)
    # implicitly neither a or b is None below

    result: TransitionProperties = {
        "requirement": base.ReqNothing(),
        "consequence": copy.deepcopy(a["consequence"] + b["consequence"]),
        "tags": a["tags"] | b["tags"],
        "annotations": a["annotations"] + b["annotations"]
    }

    if a["requirement"] == base.ReqNothing():
        result["requirement"] = b["requirement"]
    elif b["requirement"] == base.ReqNothing():
        result["requirement"] = a["requirement"]
    else:
        result["requirement"] = base.ReqAll(
            [a["requirement"], b["requirement"]]
        )

    return result


#---------------------#
# Errors and warnings #
#---------------------#

class TransitionBlockedWarning(Warning):
    """
    An warning type for indicating that a transition which has been
    requested does not have its requirements satisfied by the current
    game state.
    """
    pass


class BadStart(ValueError):
    """
    An error raised when the start method is used improperly.
    """
    pass


class MissingDecisionError(KeyError):
    """
    An error raised when attempting to use a decision that does not
    exist.
    """
    pass


class AmbiguousDecisionSpecifierError(KeyError):
    """
    An error raised when an ambiguous decision specifier is provided.
    Note that if a decision specifier simply doesn't match anything, you
    will get a `MissingDecisionError` instead.
    """
    pass


class AmbiguousTransitionError(KeyError):
    """
    An error raised when an ambiguous transition is specified.
    If a transition specifier simply doesn't match anything, you
    will get a `MissingTransitionError` instead.
    """
    pass


class MissingTransitionError(KeyError):
    """
    An error raised when attempting to use a transition that does not
    exist.
    """
    pass


class MissingMechanismError(KeyError):
    """
    An error raised when attempting to use a mechanism that does not
    exist.
    """
    pass


class MissingZoneError(KeyError):
    """
    An error raised when attempting to use a zone that does not exist.
    """
    pass


class InvalidLevelError(ValueError):
    """
    An error raised when an operation fails because of an invalid zone
    level.
    """
    pass


class InvalidDestinationError(ValueError):
    """
    An error raised when attempting to perform an operation with a
    transition but that transition does not lead to a destination that's
    compatible with the operation.
    """
    pass


class ExplorationStatusError(ValueError):
    """
    An error raised when attempting to perform an operation that
    requires a previously-visited destination with a decision that
    represents a not-yet-visited decision, or vice versa. For
    `Situation`s, Exploration states 'unknown', 'hypothesized', and
    'noticed' count as "not-yet-visited" while 'exploring' and 'explored'
    count as "visited" (see `base.hasBeenVisited`) Meanwhile, in a
    `DecisionGraph` where exploration statuses are not present, the
    presence or absence of the 'unconfirmed' tag is used to determine
    whether something has been confirmed or not.
    """
    pass


WARN_OF_NAME_COLLISIONS = False
"""
Whether or not to issue warnings when two decision names are the same.
"""


class DecisionCollisionWarning(Warning):
    """
    A warning raised when attempting to create a new decision using the
    name of a decision that already exists.
    """
    pass


class TransitionCollisionError(ValueError):
    """
    An error raised when attempting to re-use a transition name for a
    new transition, or otherwise when a transition name conflicts with
    an already-established transition.
    """
    pass


class MechanismCollisionError(ValueError):
    """
    An error raised when attempting to re-use a mechanism name at the
    same decision where a mechanism with that name already exists.
    """
    pass


class DomainCollisionError(KeyError):
    """
    An error raised when attempting to create a domain with the same
    name as an existing domain.
    """
    pass


class MissingFocalContextError(KeyError):
    """
    An error raised when attempting to pick out a focal context with a
    name that doesn't exist.
    """
    pass


class FocalContextCollisionError(KeyError):
    """
    An error raised when attempting to create a focal context with the
    same name as an existing focal context.
    """
    pass


class InvalidActionError(TypeError):
    """
    An error raised when attempting to take an exploration action which
    is not correctly formed.
    """
    pass


class ImpossibleActionError(ValueError):
    """
    An error raised when attempting to take an exploration action which
    is correctly formed but which specifies an action that doesn't match
    up with the graph state.
    """
    pass


class DoubleActionError(ValueError):
    """
    An error raised when attempting to set up an `ExplorationAction`
    when the current situation already has an action specified.
    """
    pass


class InactiveDomainWarning(Warning):
    """
    A warning used when an inactive domain is referenced but the
    operation in progress can still succeed (for example when
    deactivating an already-inactive domain).
    """


class ZoneCollisionError(ValueError):
    """
    An error raised when attempting to re-use a zone name for a new zone,
    or otherwise when a zone name conflicts with an already-established
    zone.
    """
    pass


#---------------------#
# DecisionGraph class #
#---------------------#

class DecisionGraph(
    graphs.UniqueExitsGraph[base.DecisionID, base.Transition]
):
    """
    Represents a view of the world as a topological graph at a moment in
    time. It derives from `networkx.MultiDiGraph`.

    Each node (a `Decision`) represents a place in the world where there
    are multiple opportunities for travel/action, or a dead end where
    you must turn around and go back; typically this is a single room in
    a game, but sometimes one room has multiple decision points. Edges
    (`Transition`s) represent choices that can be made to travel to
    other decision points (e.g., taking the left door), or when they are
    self-edges, they represent actions that can be taken within a
    location that affect the world or the game state.

    Each `Transition` includes a `Effects` dictionary
    indicating the effects that it has. Other effects of the transition
    that are not simple enough to be included in this format may be
    represented in an `DiscreteExploration` by changing the graph in the
    next step to reflect further effects of a transition.

    In addition to normal transitions between decisions, a
    `DecisionGraph` can represent potential transitions which lead to
    unknown destinations. These are represented by adding decisions with
    the `'unconfirmed'` tag (whose names where not specified begin with
    `'_u.'`) with a separate unconfirmed decision for each transition
    (although where it's known that two transitions lead to the same
    unconfirmed decision, this can be represented as well).

    Both nodes and edges can have `Annotation`s associated with them that
    include extra details about the explorer's perception of the
    situation. They can also have `Tag`s, which represent specific
    categories a transition or decision falls into.

    Nodes can also be part of one or more `Zones`, and zones can also be
    part of other zones, allowing for a hierarchical description of the
    underlying space.

    Equivalences can be specified to mark that some combination of
    capabilities can stand in for another capability.
    """
    def __init__(self) -> None:
        super().__init__()

        self.zones: Dict[base.Zone, base.ZoneInfo] = {}
        """
        Mapping from zone names to zone info
        """

        self.unknownCount: int = 0
        """
        Number of unknown decisions that have been created (not number
        of current unknown decisions, which is likely lower)
        """

        self.zoneTagDicts: Dict[base.Zone, Dict[base.Tag, base.TagValue]] = {}
        """
        Tags applied to zones, rather than decisions or edges.
        """

        self.equivalences: base.Equivalences = {}
        """
        See `base.Equivalences`. Determines what capabilities and/or
        mechanism states can count as active based on alternate
        requirements.
        """

        self.reversionTypes: Dict[str, Set[str]] = {}
        """
        This tracks shorthand reversion types. See `base.revertedState`
        for how these are applied. Keys are custom names and values are
        reversion type strings that `base.revertedState` could access.
        """

        self.nextID: base.DecisionID = 0
        """
        The ID to use for the next new decision we create.
        """

        self.nextMechanismID: base.MechanismID = 0
        """
        ID for the next mechanism.
        """

        self.mechanisms: Dict[
            base.MechanismID,
            Tuple[Optional[base.DecisionID], base.MechanismName]
        ] = {}
        """
        Mapping from `MechanismID`s to (`DecisionID`, `MechanismName`)
        pairs. For global mechanisms, the `DecisionID` is None.
        """

        self.globalMechanisms: Dict[
            base.MechanismName,
            base.MechanismID
        ] = {}
        """
        Global mechanisms
        """

        self.nameLookup: Dict[base.DecisionName, List[base.DecisionID]] = {}
        """
        A cache for name -> ID lookups
        """

    # Note: not hashable

    def __eq__(self, other):
        """
        Equality checker. `DecisionGraph`s can only be equal to other
        `DecisionGraph`s, not to other kinds of things.
        """
        if not isinstance(other, DecisionGraph):
            return False
        else:
            # Checks nodes, edges, and all attached data
            if not super().__eq__(other):
                return False

            # Check unknown count
            if self.unknownCount != other.unknownCount:
                return False

            # Check zones
            if self.zones != other.zones:
                return False

            # Check zone tags
            if self.zoneTagDicts != other.zoneTagDicts:
                return False

            # Check equivalences
            if self.equivalences != other.equivalences:
                return False

            # Check reversion types
            if self.reversionTypes != other.reversionTypes:
                return False

            # Check mechanisms
            if self.nextMechanismID != other.nextMechanismID:
                return False

            if self.mechanisms != other.mechanisms:
                return False

            if self.globalMechanisms != other.globalMechanisms:
                return False

            # Check names:
            if self.nameLookup != other.nameLookup:
                return False

            return True

    def listDifferences(
        self,
        other: 'DecisionGraph'
    ) -> Generator[str, None, None]:
        """
        Generates strings describing differences between this graph and
        another graph. This does NOT perform graph matching, so it will
        consider graphs different even if they have identical structures
        but use different IDs for the nodes in those structures.
        """
        if not isinstance(other, DecisionGraph):
            yield "other is not a graph"
        else:
            suppress = False
            myNodes = set(self.nodes)
            theirNodes = set(other.nodes)
            for n in myNodes:
                if n not in theirNodes:
                    suppress = True
                    yield (
                        f"other graph missing node {n}"
                    )
                else:
                    if self.nodes[n] != other.nodes[n]:
                        suppress = True
                        yield (
                            f"other graph has differences at node {n}:"
                            f"\n  Ours:  {self.nodes[n]}"
                            f"\nTheirs:  {other.nodes[n]}"
                        )
                    myDests = self.destinationsFrom(n)
                    theirDests = other.destinationsFrom(n)
                    for tr in myDests:
                        myTo = myDests[tr]
                        if tr not in theirDests:
                            suppress = True
                            yield (
                                f"at {self.identityOf(n)}: other graph"
                                f" missing transition {tr!r}"
                            )
                        else:
                            theirTo = theirDests[tr]
                            if myTo != theirTo:
                                suppress = True
                                yield (
                                    f"at {self.identityOf(n)}: other"
                                    f" graph transition {tr!r} leads to"
                                    f" {theirTo} instead of {myTo}"
                                )
                            else:
                                myProps = self.edges[n, myTo, tr]  # type:ignore [index] # noqa
                                theirProps = other.edges[n, myTo, tr]  # type:ignore [index] # noqa
                                if myProps != theirProps:
                                    suppress = True
                                    yield (
                                        f"at {self.identityOf(n)}: other"
                                        f" graph transition {tr!r} has"
                                        f" different properties:"
                                        f"\n  Ours:  {myProps}"
                                        f"\nTheirs:  {theirProps}"
                                    )
            for extra in theirNodes - myNodes:
                suppress = True
                yield (
                    f"other graph has extra node {extra}"
                )

            # TODO: Fix networkx stubs!
            if self.graph != other.graph:  # type:ignore [attr-defined]
                suppress = True
                yield (
                    " different graph attributes:"  # type:ignore [attr-defined]  # noqa
                    f"\n  Ours:  {self.graph}"
                    f"\nTheirs:  {other.graph}"
                )

            # Checks any other graph data we might have missed
            if not super().__eq__(other) and not suppress:
                for attr in dir(self):
                    if attr.startswith('__') and attr.endswith('__'):
                        continue
                    if not hasattr(other, attr):
                        yield f"other graph missing attribute: {attr!r}"
                    else:
                        myVal = getattr(self, attr)
                        theirVal = getattr(other, attr)
                        if (
                            myVal != theirVal
                        and not ((callable(myVal) and callable(theirVal)))
                        ):
                            yield (
                                f"other has different val for {attr!r}:"
                                f"\n  Ours:  {myVal}"
                                f"\nTheirs:  {theirVal}"
                            )
                for attr in sorted(set(dir(other)) - set(dir(self))):
                    yield f"other has extra attribute: {attr!r}"
                yield "graph data is different"
                # TODO: More detail here!

            # Check unknown count
            if self.unknownCount != other.unknownCount:
                yield "unknown count is different"

            # Check zones
            if self.zones != other.zones:
                yield "zones are different"

            # Check zoneTagDicts
            if self.zoneTagDicts != other.zoneTagDicts:
                yield "zoneTagDicts are different"

            # Check equivalences
            if self.equivalences != other.equivalences:
                yield "equivalences are different"

            # Check reversion types
            if self.reversionTypes != other.reversionTypes:
                yield "reversionTypes are different"

            # Check mechanisms
            if self.nextMechanismID != other.nextMechanismID:
                yield "nextMechanismID is different"

            if self.mechanisms != other.mechanisms:
                yield "mechanisms are different"

            if self.globalMechanisms != other.globalMechanisms:
                yield "global mechanisms are different"

            # Check names:
            if self.nameLookup != other.nameLookup:
                for name in self.nameLookup:
                    if name not in other.nameLookup:
                        yield (
                            f"other graph is missing name lookup entry"
                            f" for {name!r}"
                        )
                    else:
                        mine = self.nameLookup[name]
                        theirs = other.nameLookup[name]
                        if theirs != mine:
                            yield (
                                f"name lookup for {name!r} is {theirs}"
                                f" instead of {mine}"
                            )
                extras = set(other.nameLookup) - set(self.nameLookup)
                if extras:
                    yield (
                        f"other graph has extra name lookup entries:"
                        f" {extras}"
                    )

    def _assignID(self) -> base.DecisionID:
        """
        Returns the next `base.DecisionID` to use and increments the
        next ID counter.
        """
        result = self.nextID
        self.nextID += 1
        return result

    def _assignMechanismID(self) -> base.MechanismID:
        """
        Returns the next `base.MechanismID` to use and increments the
        next ID counter.
        """
        result = self.nextMechanismID
        self.nextMechanismID += 1
        return result

    def decisionInfo(self, dID: base.DecisionID) -> DecisionInfo:
        """
        Retrieves the decision info for the specified decision, as a
        live editable dictionary.

        For example:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.annotateDecision('A', 'note')
        >>> g.decisionInfo(0)
        {'name': 'A', 'domain': 'main', 'tags': {}, 'annotations': ['note']}
        """
        return cast(DecisionInfo, self.nodes[dID])

    def resolveDecision(
        self,
        spec: base.AnyDecisionSpecifier,
        zoneHint: Optional[base.Zone] = None,
        domainHint: Optional[base.Domain] = None
    ) -> base.DecisionID:
        """
        Given a decision specifier returns the ID associated with that
        decision, or raises an `AmbiguousDecisionSpecifierError` or a
        `MissingDecisionError` if the specified decision is either
        missing or ambiguous. Cannot handle strings that contain domain
        and/or zone parts; use
        `parsing.ParseFormat.parseDecisionSpecifier` to turn such
        strings into `DecisionSpecifier`s if you need to first.

        Examples:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.addDecision('C')
        2
        >>> g.addDecision('A')
        3
        >>> g.addDecision('B', 'menu')
        4
        >>> g.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('Z2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('Zup', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> g.addDecisionToZone(0, 'Z')
        >>> g.addDecisionToZone(1, 'Z')
        >>> g.addDecisionToZone(2, 'Z')
        >>> g.addDecisionToZone(3, 'Z2')
        >>> g.addZoneToZone('Z', 'Zup')
        >>> g.addZoneToZone('Z2', 'Zup')
        >>> g.resolveDecision(1)
        1
        >>> g.resolveDecision('A')
        Traceback (most recent call last):
        ...
        exploration.core.AmbiguousDecisionSpecifierError...
        >>> g.resolveDecision('B')
        Traceback (most recent call last):
        ...
        exploration.core.AmbiguousDecisionSpecifierError...
        >>> g.resolveDecision('C')
        2
        >>> g.resolveDecision('A', 'Z')
        0
        >>> g.resolveDecision('A', zoneHint='Z2')
        3
        >>> g.resolveDecision('B', domainHint='main')
        1
        >>> g.resolveDecision('B', None, 'menu')
        4
        >>> g.resolveDecision('B', zoneHint='Z2')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        >>> g.resolveDecision('A', domainHint='menu')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        >>> g.resolveDecision('A', domainHint='madeup')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        >>> g.resolveDecision('A', zoneHint='madeup')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        """
        # Parse it to either an ID or specifier if it's a string:
        if isinstance(spec, str):
            try:
                spec = int(spec)
            except ValueError:
                pass

        # If it's an ID, check for existence:
        if isinstance(spec, base.DecisionID):
            if spec in self:
                return spec
            else:
                raise MissingDecisionError(
                    f"There is no decision with ID {spec!r}."
                )
        else:
            if isinstance(spec, base.DecisionName):
                spec = base.DecisionSpecifier(
                    domain=None,
                    zone=None,
                    name=spec
                )
            elif not isinstance(spec, base.DecisionSpecifier):
                raise TypeError(
                    f"Specification is not provided as a"
                    f" DecisionSpecifier or other valid type. (got type"
                    f" {type(spec)})."
                )

            # Merge domain hints from spec/args
            if (
                spec.domain is not None
            and domainHint is not None
            and spec.domain != domainHint
            ):
                raise ValueError(
                    f"Specifier {repr(spec)} includes domain hint"
                    f" {repr(spec.domain)} which is incompatible with"
                    f" explicit domain hint {repr(domainHint)}."
                )
            else:
                domainHint = spec.domain or domainHint

            # Merge zone hints from spec/args
            if (
                spec.zone is not None
            and zoneHint is not None
            and spec.zone != zoneHint
            ):
                raise ValueError(
                    f"Specifier {repr(spec)} includes zone hint"
                    f" {repr(spec.zone)} which is incompatible with"
                    f" explicit zone hint {repr(zoneHint)}."
                )
            else:
                zoneHint = spec.zone or zoneHint

            if spec.name not in self.nameLookup:
                raise MissingDecisionError(
                    f"No decision named {repr(spec.name)}."
                )
            else:
                options = self.nameLookup[spec.name]
                if len(options) == 0:
                    raise MissingDecisionError(
                        f"No decision named {repr(spec.name)}."
                    )
                filtered = [
                    opt
                    for opt in options
                    if (
                        domainHint is None
                     or self.domainFor(opt) == domainHint
                    ) and (
                        zoneHint is None
                     or zoneHint in self.zoneAncestors(opt)
                    )
                ]
                if len(filtered) == 1:
                    return filtered[0]
                else:
                    filterDesc = ""
                    if domainHint is not None:
                        filterDesc += f" in domain {repr(domainHint)}"
                    if zoneHint is not None:
                        filterDesc += f" in zone {repr(zoneHint)}"
                    if len(filtered) == 0:
                        raise MissingDecisionError(
                            f"No decisions named"
                            f" {repr(spec.name)}{filterDesc}."
                        )
                    else:
                        raise AmbiguousDecisionSpecifierError(
                            f"There are {len(filtered)} decisions"
                            f" named {repr(spec.name)}{filterDesc}."
                        )

    def getDecision(
        self,
        decision: base.AnyDecisionSpecifier,
        zoneHint: Optional[base.Zone] = None,
        domainHint: Optional[base.Domain] = None
    ) -> Optional[base.DecisionID]:
        """
        Works like `resolveDecision` but returns None instead of raising
        a `MissingDecisionError` if the specified decision isn't listed.
        May still raise an `AmbiguousDecisionSpecifierError`.
        """
        try:
            return self.resolveDecision(
                decision,
                zoneHint,
                domainHint
            )
        except MissingDecisionError:
            return None

    def nameFor(
        self,
        decision: base.AnyDecisionSpecifier
    ) -> base.DecisionName:
        """
        Returns the name of the specified decision. Note that names are
        not necessarily unique.

        Example:

        >>> d = DecisionGraph()
        >>> d.addDecision('A')
        0
        >>> d.addDecision('B')
        1
        >>> d.addDecision('B')
        2
        >>> d.nameFor(0)
        'A'
        >>> d.nameFor(1)
        'B'
        >>> d.nameFor(2)
        'B'
        >>> d.nameFor(3)
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        """
        dID = self.resolveDecision(decision)
        return self.nodes[dID]['name']

    def identityOf(
        self,
        decision: Optional[base.AnyDecisionSpecifier],
        includeZones: bool = True,
        alwaysDomain: Optional[bool] = None
    ) -> str:
        """
        Returns a string containing the given decision ID and the name
        for that decision in parentheses afterwards. If the value
        provided is `None`, it returns the string "(nowhere)".

        If `includeZones` is true (the default) then zone information
        is included before the decision name.

        If `alwaysDomain` is true or false, then the domain information
        will always (or never) be included. If it's `None` (the default)
        then domain info will only be included for decisions which are
        not in the default domain.
        """
        if decision is None:
            return "(nowhere)"
        else:
            dID = self.resolveDecision(decision)
            thisDomain = self.domainFor(dID)
            dSpec = ''
            zSpec = ''
            if (
                alwaysDomain is True
             or (
                    alwaysDomain is None
                and thisDomain != base.DEFAULT_DOMAIN
                )
            ):
                dSpec = thisDomain + '//'  # TODO: Don't hardcode this?
            if includeZones:
                zones = [
                    z
                    for z in self.zoneParents(dID)
                    if self.zones[z].level == 0
                ]
                if len(zones) == 1:
                    zSpec = zones[0] + '::'  # TODO: Don't hardcode this?
                elif len(zones) > 1:
                    zSpec = '[' + ', '.join(sorted(zones)) + ']::'
                # else leave zSpec empty

            return f"{dID} ({dSpec}{zSpec}{self.nameFor(dID)})"

    def namesListing(
        self,
        decisions: Collection[base.DecisionID],
        includeZones: bool = True,
        indent: int = 2
    ) -> str:
        """
        Returns a multi-line string containing an indented listing of
        the provided decision IDs with their names in parentheses after
        each. Useful for debugging & error messages.

        Includes level-0 zones where applicable, with a zone separator
        before the decision, unless `includeZones` is set to False. Where
        there are multiple level-0 zones, they're listed together in
        brackets.

        Uses the string '(none)' when there are no decisions are in the
        list.

        Set `indent` to something other than 2 to control how much
        indentation is added.

        For example:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.addDecision('C')
        2
        >>> g.namesListing(['A', 'C', 'B'])
        '  0 (A)\\n  2 (C)\\n  1 (B)\\n'
        >>> g.namesListing([])
        '  (none)\\n'
        >>> g.createZone('zone', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('zone2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('zoneUp', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> g.addDecisionToZone(0, 'zone')
        >>> g.addDecisionToZone(1, 'zone')
        >>> g.addDecisionToZone(1, 'zone2')
        >>> g.addDecisionToZone(2, 'zoneUp')  # won't be listed: it's level-1
        >>> g.namesListing(['A', 'C', 'B'])
        '  0 (zone::A)\\n  2 (C)\\n  1 ([zone, zone2]::B)\\n'
        """
        ind = ' ' * indent
        if len(decisions) == 0:
            return ind + '(none)\n'
        else:
            result = ''
            for dID in decisions:
                result += ind + self.identityOf(dID, includeZones) + '\n'
            return result

    def destinationsListing(
        self,
        destinations: Dict[base.Transition, base.DecisionID],
        includeZones: bool = True,
        indent: int = 2
    ) -> str:
        """
        Returns a multi-line string containing an indented listing of
        the provided transitions along with their destinations and the
        names of those destinations in parentheses. Useful for debugging
        & error messages. (Use e.g., `destinationsFrom` to get a
        transitions -> destinations dictionary in the required format.)

        Uses the string '(no transitions)' when there are no transitions
        in the dictionary.

        Set `indent` to something other than 2 to control how much
        indentation is added.

        For example:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.addDecision('C')
        2
        >>> g.addTransition('A', 'north', 'B', 'south')
        >>> g.addTransition('B', 'east', 'C', 'west')
        >>> g.addTransition('C', 'southwest', 'A', 'northeast')
        >>> g.destinationsListing(g.destinationsFrom('A'))
        '  north to 1 (B)\\n  northeast to 2 (C)\\n'
        >>> g.destinationsListing(g.destinationsFrom('B'))
        '  south to 0 (A)\\n  east to 2 (C)\\n'
        >>> g.destinationsListing({})
        '  (none)\\n'
        >>> g.createZone('zone', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.addDecisionToZone(0, 'zone')
        >>> g.destinationsListing(g.destinationsFrom('B'))
        '  south to 0 (zone::A)\\n  east to 2 (C)\\n'
        """
        ind = ' ' * indent
        if len(destinations) == 0:
            return ind + '(none)\n'
        else:
            result = ''
            for transition, dID in destinations.items():
                line = f"{transition} to {self.identityOf(dID, includeZones)}"
                result += ind + line + '\n'
            return result

    def domainFor(self, decision: base.AnyDecisionSpecifier) -> base.Domain:
        """
        Returns the domain that a decision belongs to.
        """
        dID = self.resolveDecision(decision)
        return self.nodes[dID]['domain']

    def allDecisionsInDomain(
        self,
        domain: base.Domain
    ) -> Set[base.DecisionID]:
        """
        Returns the set of all `DecisionID`s for decisions in the
        specified domain.
        """
        return set(dID for dID in self if self.nodes[dID]['domain'] == domain)

    def destination(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> base.DecisionID:
        """
        Overrides base `UniqueExitsGraph.destination` to raise
        `MissingDecisionError` or `MissingTransitionError` as
        appropriate, and to work with an `AnyDecisionSpecifier`.
        """
        dID = self.resolveDecision(decision)
        try:
            return super().destination(dID, transition)
        except KeyError:
            raise MissingTransitionError(
                f"Transition {transition!r} does not exist at decision"
                f" {self.identityOf(dID)}."
            )

    def getDestination(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        default: Any = None
    ) -> Optional[base.DecisionID]:
        """
        Overrides base `UniqueExitsGraph.getDestination` with different
        argument names, since those matter for the edit DSL.
        """
        dID = self.resolveDecision(decision)
        return super().getDestination(dID, transition)

    def destinationsFrom(
        self,
        decision: base.AnyDecisionSpecifier
    ) -> Dict[base.Transition, base.DecisionID]:
        """
        Override that just changes the type of the exception from a
        `KeyError` to a `MissingDecisionError` when the source does not
        exist.
        """
        dID = self.resolveDecision(decision)
        return super().destinationsFrom(dID)

    def bothEnds(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> Set[base.DecisionID]:
        """
        Returns a set containing the `DecisionID`(s) for both the start
        and end of the specified transition. Raises a
        `MissingDecisionError` or `MissingTransitionError`if the
        specified decision and/or transition do not exist.

        Note that for actions since the source and destination are the
        same, the set will have only one element.
        """
        dID = self.resolveDecision(decision)
        result = {dID}
        dest = self.destination(dID, transition)
        if dest is not None:
            result.add(dest)
        return result

    def decisionActions(
        self,
        decision: base.AnyDecisionSpecifier
    ) -> Set[base.Transition]:
        """
        Retrieves the set of self-edges at a decision. Editing the set
        will not affect the graph.

        Example:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.addDecision('C')
        2
        >>> g.addAction('A', 'action1')
        >>> g.addAction('A', 'action2')
        >>> g.addAction('B', 'action3')
        >>> sorted(g.decisionActions('A'))
        ['action1', 'action2']
        >>> g.decisionActions('B')
        {'action3'}
        >>> g.decisionActions('C')
        set()
        """
        result = set()
        dID = self.resolveDecision(decision)
        for transition, dest in self.destinationsFrom(dID).items():
            if dest == dID:
                result.add(transition)
        return result

    def getTransitionProperties(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> TransitionProperties:
        """
        Returns a dictionary containing transition properties for the
        specified transition from the specified decision. The properties
        included are:

        - 'requirement': The requirement for the transition.
        - 'consequence': Any consequence of the transition.
        - 'tags': Any tags applied to the transition.
        - 'annotations': Any annotations on the transition.

        The reciprocal of the transition is not included.

        The result is a clone of the stored properties; edits to the
        dictionary will NOT modify the graph.
        """
        dID = self.resolveDecision(decision)
        dest = self.destination(dID, transition)

        info: TransitionProperties = copy.deepcopy(
            self.edges[dID, dest, transition]  # type:ignore
        )
        return {
            'requirement': info.get('requirement', base.ReqNothing()),
            'consequence': info.get('consequence', []),
            'tags': info.get('tags', {}),
            'annotations': info.get('annotations', [])
        }

    def setTransitionProperties(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        requirement: Optional[base.Requirement] = None,
        consequence: Optional[base.Consequence] = None,
        tags: Optional[Dict[base.Tag, base.TagValue]] = None,
        annotations: Optional[List[base.Annotation]] = None
    ) -> None:
        """
        Sets one or more transition properties all at once. Can be used
        to set the requirement, consequence, tags, and/or annotations.
        Old values are overwritten, although if `None`s are provided (or
        arguments are omitted), corresponding properties are not
        updated.

        To add tags or annotations to existing tags/annotations instead
        of replacing them, use `tagTransition` or `annotateTransition`
        instead.
        """
        dID = self.resolveDecision(decision)
        if requirement is not None:
            self.setTransitionRequirement(dID, transition, requirement)
        if consequence is not None:
            self.setConsequence(dID, transition, consequence)
        if tags is not None:
            dest = self.destination(dID, transition)
            # TODO: Submit pull request to update MultiDiGraph stubs in
            # types-networkx to include OutMultiEdgeView that accepts
            # from/to/key tuples as indices.
            info = cast(
                TransitionProperties,
                self.edges[dID, dest, transition]  # type:ignore
            )
            info['tags'] = tags
        if annotations is not None:
            dest = self.destination(dID, transition)
            info = cast(
                TransitionProperties,
                self.edges[dID, dest, transition]  # type:ignore
            )
            info['annotations'] = annotations

    def getTransitionRequirement(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> base.Requirement:
        """
        Returns the `Requirement` for accessing a specific transition at
        a specific decision. For transitions which don't have
        requirements, returns a `ReqNothing` instance.
        """
        dID = self.resolveDecision(decision)
        dest = self.destination(dID, transition)

        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )

        return info.get('requirement', base.ReqNothing())

    def setTransitionRequirement(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        requirement: Optional[base.Requirement]
    ) -> None:
        """
        Sets the `Requirement` for accessing a specific transition at
        a specific decision. Raises a `KeyError` if the decision or
        transition does not exist.

        Deletes the requirement if `None` is given as the requirement.

        Use `parsing.ParseFormat.parseRequirement` first if you have a
        requirement in string format.

        Does not raise an error if deletion is requested for a
        non-existent requirement, and silently overwrites any previous
        requirement.
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)

        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )

        if requirement is None:
            try:
                del info['requirement']
            except KeyError:
                pass
        else:
            if not isinstance(requirement, base.Requirement):
                raise TypeError(
                    f"Invalid requirement type: {type(requirement)}"
                )

            info['requirement'] = requirement

    def getConsequence(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> base.Consequence:
        """
        Retrieves the consequence of a transition.

        A `KeyError` is raised if the specified decision/transition
        combination doesn't exist.
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)

        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )

        return info.get('consequence', [])

    def addConsequence(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        consequence: base.Consequence
    ) -> Tuple[int, int]:
        """
        Adds the given `Consequence` to the consequence list for the
        specified transition, extending that list at the end. Note that
        this does NOT make a copy of the consequence, so it should not
        be used to copy consequences from one transition to another
        without making a deep copy first.

        A `MissingDecisionError` or a `MissingTransitionError` is raised
        if the specified decision/transition combination doesn't exist.

        Returns a pair of integers indicating the minimum and maximum
        depth-first-traversal-indices of the added consequence part(s).
        The outer consequence list itself (index 0) is not counted.

        >>> d = DecisionGraph()
        >>> d.addDecision('A')
        0
        >>> d.addDecision('B')
        1
        >>> d.addTransition('A', 'fwd', 'B', 'rev')
        >>> d.addConsequence('A', 'fwd', [base.effect(gain='sword')])
        (1, 1)
        >>> d.addConsequence('B', 'rev', [base.effect(lose='sword')])
        (1, 1)
        >>> ef = d.getConsequence('A', 'fwd')
        >>> er = d.getConsequence('B', 'rev')
        >>> ef == [base.effect(gain='sword')]
        True
        >>> er == [base.effect(lose='sword')]
        True
        >>> d.addConsequence('A', 'fwd', [base.effect(deactivate=True)])
        (2, 2)
        >>> ef = d.getConsequence('A', 'fwd')
        >>> ef == [base.effect(gain='sword'), base.effect(deactivate=True)]
        True
        >>> d.addConsequence(
        ...     'A',
        ...     'fwd',  # adding to consequence with 3 parts already
        ...     [  # outer list not counted because it merges
        ...         base.challenge(  # 1 part
        ...             None,
        ...             0,
        ...             [base.effect(gain=('flowers', 3))],  # 2 parts
        ...             [base.effect(gain=('flowers', 1))]  # 2 parts
        ...         )
        ...     ]
        ... )  # note indices below are inclusive; indices are 3, 4, 5, 6, 7
        (3, 7)
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)

        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )

        existing = info.setdefault('consequence', [])
        startIndex = base.countParts(existing)
        existing.extend(consequence)
        endIndex = base.countParts(existing) - 1
        return (startIndex, endIndex)

    def setConsequence(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        consequence: base.Consequence
    ) -> None:
        """
        Replaces the transition consequence for the given transition at
        the given decision. Any previous consequence is discarded. See
        `Consequence` for the structure of these. Note that this does
        NOT make a copy of the consequence, do that first to avoid
        effect-entanglement if you're copying a consequence.

        A `MissingDecisionError` or a `MissingTransitionError` is raised
        if the specified decision/transition combination doesn't exist.
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)

        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )

        info['consequence'] = consequence

    def addEquivalence(
        self,
        requirement: base.Requirement,
        capabilityOrMechanismState: Union[
            base.Capability,
            Tuple[base.MechanismID, base.MechanismState]
        ]
    ) -> None:
        """
        Adds the given requirement as an equivalence for the given
        capability or the given mechanism state. Note that having a
        capability via an equivalence does not count as actually having
        that capability; it only counts for the purpose of satisfying
        `Requirement`s.

        Note also that because a mechanism-based requirement looks up
        the specific mechanism locally based on a name, an equivalence
        defined in one location may affect mechanism requirements in
        other locations unless the mechanism name in the requirement is
        zone-qualified to be specific. But in such situations the base
        mechanism would have caused issues in any case.
        """
        self.equivalences.setdefault(
            capabilityOrMechanismState,
            set()
        ).add(requirement)

    def removeEquivalence(
        self,
        requirement: base.Requirement,
        capabilityOrMechanismState: Union[
            base.Capability,
            Tuple[base.MechanismID, base.MechanismState]
        ]
    ) -> None:
        """
        Removes an equivalence. Raises a `KeyError` if no such
        equivalence existed.
        """
        self.equivalences[capabilityOrMechanismState].remove(requirement)

    def hasAnyEquivalents(
        self,
        capabilityOrMechanismState: Union[
            base.Capability,
            Tuple[base.MechanismID, base.MechanismState]
        ]
    ) -> bool:
        """
        Returns `True` if the given capability or mechanism state has at
        least one equivalence.
        """
        return capabilityOrMechanismState in self.equivalences

    def allEquivalents(
        self,
        capabilityOrMechanismState: Union[
            base.Capability,
            Tuple[base.MechanismID, base.MechanismState]
        ]
    ) -> Set[base.Requirement]:
        """
        Returns the set of equivalences for the given capability. This is
        a live set which may be modified (it's probably better to use
        `addEquivalence` and `removeEquivalence` instead...).
        """
        return self.equivalences.setdefault(
            capabilityOrMechanismState,
            set()
        )

    def reversionType(self, name: str, equivalentTo: Set[str]) -> None:
        """
        Specifies a new reversion type, so that when used in a reversion
        aspects set with a colon before the name, all items in the
        `equivalentTo` value will be added to that set. These may
        include other custom reversion type names (with the colon) but
        take care not to create an equivalence loop which would result
        in a crash.

        If you re-use the same name, it will override the old equivalence
        for that name.
        """
        self.reversionTypes[name] = equivalentTo

    def addAction(
        self,
        decision: base.AnyDecisionSpecifier,
        action: base.Transition,
        requires: Optional[base.Requirement] = None,
        consequence: Optional[base.Consequence] = None,
        tags: Optional[Dict[base.Tag, base.TagValue]] = None,
        annotations: Optional[List[base.Annotation]] = None,
    ) -> None:
        """
        Adds the given action as a possibility at the given decision. An
        action is just a self-edge, which can have requirements like any
        edge, and which can have consequences like any edge.
        The optional arguments are given to `setTransitionRequirement`
        and `setConsequence`; see those functions for descriptions
        of what they mean.

        Raises a `KeyError` if a transition with the given name already
        exists at the given decision.
        """
        if tags is None:
            tags = {}
        if annotations is None:
            annotations = []

        dID = self.resolveDecision(decision)

        self.add_edge(
            dID,
            dID,
            key=action,
            tags=tags,
            annotations=annotations
        )
        self.setTransitionRequirement(dID, action, requires)
        if consequence is not None:
            self.setConsequence(dID, action, consequence)

    def tagDecision(
        self,
        decision: base.AnyDecisionSpecifier,
        tagOrTags: Union[base.Tag, Dict[base.Tag, base.TagValue]],
        tagValue: Union[
            base.TagValue,
            type[base.NoTagValue]
        ] = base.NoTagValue
    ) -> None:
        """
        Adds a tag (or many tags from a dictionary of tags) to a
        decision, using `1` as the value if no value is provided. It's
        a `ValueError` to provide a value when a dictionary of tags is
        provided to set multiple tags at once.

        Note that certain tags have special meanings:

        - 'unconfirmed' is used for decisions that represent unconfirmed
            parts of the graph (this is separate from the 'unknown'
            and/or 'hypothesized' exploration statuses, which are only
            tracked in a `DiscreteExploration`, not in a `DecisionGraph`).
            Various methods require this tag and many also add or remove
            it.
        """
        if isinstance(tagOrTags, base.Tag):
            if tagValue is base.NoTagValue:
                tagValue = 1

            # Not sure why this cast is necessary given the `if` above...
            tagValue = cast(base.TagValue, tagValue)

            tagOrTags = {tagOrTags: tagValue}

        elif tagValue is not base.NoTagValue:
            raise ValueError(
                "Provided a dictionary to update multiple tags, but"
                " also a tag value."
            )

        dID = self.resolveDecision(decision)

        tagsAlready = self.nodes[dID].setdefault('tags', {})
        tagsAlready.update(tagOrTags)

    def untagDecision(
        self,
        decision: base.AnyDecisionSpecifier,
        tag: base.Tag
    ) -> Union[base.TagValue, type[base.NoTagValue]]:
        """
        Removes a tag from a decision. Returns the tag's old value if
        the tag was present and got removed, or `NoTagValue` if the tag
        wasn't present.
        """
        dID = self.resolveDecision(decision)

        target = self.nodes[dID]['tags']
        try:
            return target.pop(tag)
        except KeyError:
            return base.NoTagValue

    def decisionTags(
        self,
        decision: base.AnyDecisionSpecifier
    ) -> Dict[base.Tag, base.TagValue]:
        """
        Returns the dictionary of tags for a decision. Edits to the
        returned value will be applied to the graph.
        """
        dID = self.resolveDecision(decision)

        return self.nodes[dID]['tags']

    def annotateDecision(
        self,
        decision: base.AnyDecisionSpecifier,
        annotationOrAnnotations: Union[
            base.Annotation,
            Sequence[base.Annotation]
        ]
    ) -> None:
        """
        Adds an annotation to a decision's annotations list.
        """
        dID = self.resolveDecision(decision)

        if isinstance(annotationOrAnnotations, base.Annotation):
            annotationOrAnnotations = [annotationOrAnnotations]
        self.nodes[dID]['annotations'].extend(annotationOrAnnotations)

    def decisionAnnotations(
        self,
        decision: base.AnyDecisionSpecifier
    ) -> List[base.Annotation]:
        """
        Returns the list of annotations for the specified decision.
        Modifying the list affects the graph.
        """
        dID = self.resolveDecision(decision)

        return self.nodes[dID]['annotations']

    def tagTransition(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        tagOrTags: Union[base.Tag, Dict[base.Tag, base.TagValue]],
        tagValue: Union[
            base.TagValue,
            type[base.NoTagValue]
        ] = base.NoTagValue
    ) -> None:
        """
        Adds a tag (or each tag from a dictionary) to a transition
        coming out of a specific decision. `1` will be used as the
        default value if a single tag is supplied; supplying a tag value
        when providing a dictionary of multiple tags to update is a
        `ValueError`.

        Note that certain transition tags have special meanings:
        - 'trigger' causes any actions (but not normal transitions) that
            it applies to to be automatically triggered when
            `advanceSituation` is called and the decision they're
            attached to is active in the new situation (as long as the
            action's requirements are met). This happens once per
            situation; use 'wait' steps to re-apply triggers.
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)
        if isinstance(tagOrTags, base.Tag):
            if tagValue is base.NoTagValue:
                tagValue = 1

            # Not sure why this is necessary given the `if` above...
            tagValue = cast(base.TagValue, tagValue)

            tagOrTags = {tagOrTags: tagValue}
        elif tagValue is not base.NoTagValue:
            raise ValueError(
                "Provided a dictionary to update multiple tags, but"
                " also a tag value."
            )

        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )

        info.setdefault('tags', {}).update(tagOrTags)

    def untagTransition(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        tagOrTags: Union[base.Tag, Set[base.Tag]]
    ) -> None:
        """
        Removes a tag (or each tag in a set) from a transition coming out
        of a specific decision. Raises a `KeyError` if (one of) the
        specified tag(s) is not currently applied to the specified
        transition.
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)
        if isinstance(tagOrTags, base.Tag):
            tagOrTags = {tagOrTags}

        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )
        tagsAlready = info.setdefault('tags', {})

        for tag in tagOrTags:
            tagsAlready.pop(tag)

    def transitionTags(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> Dict[base.Tag, base.TagValue]:
        """
        Returns the dictionary of tags for a transition. Edits to the
        returned dictionary will be applied to the graph.
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)
        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )
        return info.setdefault('tags', {})

    def annotateTransition(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        annotations: Union[base.Annotation, Sequence[base.Annotation]]
    ) -> None:
        """
        Adds an annotation (or a sequence of annotations) to a
        transition's annotations list.
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)
        if isinstance(annotations, base.Annotation):
            annotations = [annotations]
        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )
        info['annotations'].extend(annotations)

    def transitionAnnotations(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> List[base.Annotation]:
        """
        Returns the annotation list for a specific transition at a
        specific decision. Editing the list affects the graph.
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition)
        info = cast(
            TransitionProperties,
            self.edges[dID, dest, transition]  # type:ignore
        )
        return info['annotations']

    def tagZone(
        self,
        zone: base.Zone,
        tagOrTags: Union[base.Tag, Dict[base.Tag, base.TagValue]],
        tagValue: Union[
            base.TagValue,
            type[base.NoTagValue]
        ] = base.NoTagValue
    ) -> None:
        """
        Adds a tag (or many tags from a dictionary of tags) to a
        zone, using `1` as the value if no value is provided. It's
        a `ValueError` to provide a value when a dictionary of tags is
        provided to set multiple tags at once.

        Raises a `MissingZoneError` if the specified zone does not exist.
        """
        if zone not in self.zones:
            raise MissingZoneError(
                f"Can't add tag(s) to zone {zone!r} because that zone"
                f" doesn't exist yet."
            )

        if isinstance(tagOrTags, base.Tag):
            if tagValue is base.NoTagValue:
                tagValue = 1

            # Not sure why this cast is necessary given the `if` above...
            tagValue = cast(base.TagValue, tagValue)

            tagOrTags = {tagOrTags: tagValue}

        elif tagValue is not base.NoTagValue:
            raise ValueError(
                "Provided a dictionary to update multiple tags, but"
                " also a tag value."
            )

        tagsAlready = self.zoneTagDicts.setdefault(zone, {})
        tagsAlready.update(tagOrTags)

    def untagZone(
        self,
        zone: base.Zone,
        tag: base.Tag
    ) -> Union[base.TagValue, type[base.NoTagValue]]:
        """
        Removes a tag from a zone. Returns the tag's old value if the
        tag was present and got removed, or `NoTagValue` if the tag
        wasn't present.

        Raises a `MissingZoneError` if the specified zone does not exist.
        """
        if zone not in self.zones:
            raise MissingZoneError(
                f"Can't remove tag {tag!r} from zone {zone!r} because"
                f" that zone doesn't exist yet."
            )
        target = self.zoneTagDicts.setdefault(zone, {})
        try:
            return target.pop(tag)
        except KeyError:
            return base.NoTagValue

    def zoneTags(
        self,
        zone: base.Zone
    ) -> Dict[base.Tag, base.TagValue]:
        """
        Returns the dictionary of tags for a zone. Edits to the returned
        value will be applied to the graph. Creates and returns an empty
        tags dictionary if called on a zone that didn't have any tags
        previously, but raises a `MissingZoneError` if attempting to tag
        a zone which does not exist.

        For example:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.createZone('Zone')
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.tagZone('Zone', 'color', 'blue')
        >>> g.tagZone(
        ...     'Zone',
        ...     {'shape': 'square', 'color': 'red', 'sound': 'loud'}
        ... )
        >>> g.untagZone('Zone', 'sound')
        'loud'
        >>> g.zoneTags('Zone')
        {'color': 'red', 'shape': 'square'}
        """
        # TODO: Merge this in with ZoneInfo? That would be cleaner
        if zone in self.zoneTagDicts:
            return self.zoneTagDicts.setdefault(zone, {})
        else:
            if zone not in self.zones:
                raise MissingZoneError(
                    f"Tags for zone {zone!r} don't exist because that"
                    f" zone has not been created yet."
                )
            else:
                return self.zoneTagDicts.setdefault(zone, {})

    def createZone(self, zone: base.Zone, level: int = 0) -> base.ZoneInfo:
        """
        Creates an empty zone with the given name at the given level
        (default 0). Raises a `ZoneCollisionError` if that zone name is
        already in use (at any level), including if it's in use by a
        decision.

        Raises an `InvalidLevelError` if the level value is less than 0.

        Returns the `ZoneInfo` for the new blank zone.

        For example:

        >>> d = DecisionGraph()
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.createZone('Z2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.createZone('Z3', -1)  # level -1 is not valid (must be >= 0)
        Traceback (most recent call last):
        ...
        exploration.core.InvalidLevelError...
        >>> d.createZone('Z2')  # Name Z2 is already in use
        Traceback (most recent call last):
        ...
        exploration.core.ZoneCollisionError...
        """
        if level < 0:
            raise InvalidLevelError(
                "Cannot create a zone with a negative level."
            )
        if zone in self.zones:
            raise ZoneCollisionError(f"Zone {zone!r} already exists.")
        if zone in self:
            raise ZoneCollisionError(
                f"A decision named {zone!r} already exists, so a zone"
                f" with that name cannot be created."
            )
        info: base.ZoneInfo = base.ZoneInfo(
            level=level,
            parents=set(),
            contents=set()
        )
        self.zones[zone] = info
        return info

    def getZoneInfo(self, zone: base.Zone) -> Optional[base.ZoneInfo]:
        """
        Returns the `ZoneInfo` (level, parents, and contents) for the
        specified zone, or `None` if that zone does not exist.

        For example:

        >>> d = DecisionGraph()
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.createZone('Z2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.getZoneInfo('Z2')
        ZoneInfo(level=0, parents=set(), contents=set())
        """
        return self.zones.get(zone)

    def deleteZone(self, zone: base.Zone) -> base.ZoneInfo:
        """
        Deletes the specified zone, returning a `ZoneInfo` object with
        the information on the level, parents, and contents of that zone.

        Raises a `MissingZoneError` if the zone in question does not
        exist.

        For example:

        >>> d = DecisionGraph()
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.deleteZone('Z')
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.getZoneInfo('Z') is None  # no info any more
        True
        >>> d.deleteZone('Z')  # can't re-delete
        Traceback (most recent call last):
        ...
        exploration.core.MissingZoneError...
        """
        info = self.getZoneInfo(zone)
        if info is None:
            raise MissingZoneError(
                f"Cannot delete zone {zone!r}: it does not exist."
            )
        for sub in info.contents:
            if 'zones' in self.nodes[sub]:
                try:
                    self.nodes[sub]['zones'].remove(zone)
                except KeyError:
                    pass
        del self.zones[zone]
        return info

    def addDecisionToZone(
        self,
        decision: base.AnyDecisionSpecifier,
        zone: base.Zone
    ) -> None:
        """
        Adds a decision directly to a zone. Should normally only be used
        with level-0 zones. Raises a `MissingZoneError` if the specified
        zone did not already exist.

        For example:

        >>> d = DecisionGraph()
        >>> d.addDecision('A')
        0
        >>> d.addDecision('B')
        1
        >>> d.addDecision('C')
        2
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.addDecisionToZone('A', 'Z')
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents={0})
        >>> d.addDecisionToZone('B', 'Z')
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents={0, 1})
        """
        dID = self.resolveDecision(decision)

        if zone not in self.zones:
            raise MissingZoneError(f"Zone {zone!r} does not exist.")

        self.zones[zone].contents.add(dID)
        self.nodes[dID].setdefault('zones', set()).add(zone)

    def removeDecisionFromZone(
        self,
        decision: base.AnyDecisionSpecifier,
        zone: base.Zone
    ) -> bool:
        """
        Removes a decision from a zone if it had been in it, returning
        True if that decision had been in that zone, and False if it was
        not in that zone, including if that zone didn't exist.

        Note that this only removes a decision from direct zone
        membership. If the decision is a member of one or more zones
        which are (directly or indirectly) sub-zones of the target zone,
        the decision will remain in those zones, and will still be
        indirectly part of the target zone afterwards.

        Examples:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.createZone('level0', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('level1', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> g.createZone('level2', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> g.createZone('level3', 3)
        ZoneInfo(level=3, parents=set(), contents=set())
        >>> g.addDecisionToZone('A', 'level0')
        >>> g.addDecisionToZone('B', 'level0')
        >>> g.addZoneToZone('level0', 'level1')
        >>> g.addZoneToZone('level1', 'level2')
        >>> g.addZoneToZone('level2', 'level3')
        >>> g.addDecisionToZone('B', 'level2')  # Direct w/ skips
        >>> g.removeDecisionFromZone('A', 'level1')
        False
        >>> g.zoneParents(0)
        {'level0'}
        >>> g.removeDecisionFromZone('A', 'level0')
        True
        >>> g.zoneParents(0)
        set()
        >>> g.removeDecisionFromZone('A', 'level0')
        False
        >>> g.removeDecisionFromZone('B', 'level0')
        True
        >>> g.zoneParents(1)
        {'level2'}
        >>> g.removeDecisionFromZone('B', 'level0')
        False
        >>> g.removeDecisionFromZone('B', 'level2')
        True
        >>> g.zoneParents(1)
        set()
        """
        dID = self.resolveDecision(decision)

        if zone not in self.zones:
            return False

        info = self.zones[zone]
        if dID not in info.contents:
            return False
        else:
            info.contents.remove(dID)
            try:
                self.nodes[dID]['zones'].remove(zone)
            except KeyError:
                pass
            return True

    def addZoneToZone(
        self,
        addIt: base.Zone,
        addTo: base.Zone
    ) -> None:
        """
        Adds a zone to another zone. The `addIt` one must be at a
        strictly lower level than the `addTo` zone, or an
        `InvalidLevelError` will be raised.

        If the zone to be added didn't already exist, it is created at
        one level below the target zone. Similarly, if the zone being
        added to didn't already exist, it is created at one level above
        the target zone. If neither existed, a `MissingZoneError` will
        be raised.

        For example:

        >>> d = DecisionGraph()
        >>> d.addDecision('A')
        0
        >>> d.addDecision('B')
        1
        >>> d.addDecision('C')
        2
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.addDecisionToZone('A', 'Z')
        >>> d.addDecisionToZone('B', 'Z')
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents={0, 1})
        >>> d.createZone('Z2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.addDecisionToZone('B', 'Z2')
        >>> d.addDecisionToZone('C', 'Z2')
        >>> d.getZoneInfo('Z2')
        ZoneInfo(level=0, parents=set(), contents={1, 2})
        >>> d.createZone('l1Z', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> d.createZone('l2Z', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> d.addZoneToZone('Z', 'l1Z')
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents={'l1Z'}, contents={0, 1})
        >>> d.getZoneInfo('l1Z')
        ZoneInfo(level=1, parents=set(), contents={'Z'})
        >>> d.addZoneToZone('l1Z', 'l2Z')
        >>> d.getZoneInfo('l1Z')
        ZoneInfo(level=1, parents={'l2Z'}, contents={'Z'})
        >>> d.getZoneInfo('l2Z')
        ZoneInfo(level=2, parents=set(), contents={'l1Z'})
        >>> d.addZoneToZone('Z2', 'l2Z')
        >>> d.getZoneInfo('Z2')
        ZoneInfo(level=0, parents={'l2Z'}, contents={1, 2})
        >>> l2i = d.getZoneInfo('l2Z')
        >>> l2i.level
        2
        >>> l2i.parents
        set()
        >>> sorted(l2i.contents)
        ['Z2', 'l1Z']
        >>> d.addZoneToZone('NZ', 'NZ2')
        Traceback (most recent call last):
        ...
        exploration.core.MissingZoneError...
        >>> d.addZoneToZone('Z', 'l1Z2')
        >>> zi = d.getZoneInfo('Z')
        >>> zi.level
        0
        >>> sorted(zi.parents)
        ['l1Z', 'l1Z2']
        >>> sorted(zi.contents)
        [0, 1]
        >>> d.getZoneInfo('l1Z2')
        ZoneInfo(level=1, parents=set(), contents={'Z'})
        >>> d.addZoneToZone('NZ', 'l1Z')
        >>> d.getZoneInfo('NZ')
        ZoneInfo(level=0, parents={'l1Z'}, contents=set())
        >>> zi = d.getZoneInfo('l1Z')
        >>> zi.level
        1
        >>> zi.parents
        {'l2Z'}
        >>> sorted(zi.contents)
        ['NZ', 'Z']
        """
        # Create one or the other (but not both) if they're missing
        addInfo = self.getZoneInfo(addIt)
        toInfo = self.getZoneInfo(addTo)
        if addInfo is None and toInfo is None:
            raise MissingZoneError(
                f"Cannot add zone {addIt!r} to zone {addTo!r}: neither"
                f" exists already."
            )

        # Create missing addIt
        elif addInfo is None:
            toInfo = cast(base.ZoneInfo, toInfo)
            newLevel = toInfo.level - 1
            if newLevel < 0:
                raise InvalidLevelError(
                    f"Zone {addTo!r} is at level {toInfo.level} and so"
                    f" a new zone cannot be added underneath it."
                )
            addInfo = self.createZone(addIt, newLevel)

        # Create missing addTo
        elif toInfo is None:
            addInfo = cast(base.ZoneInfo, addInfo)
            newLevel = addInfo.level + 1
            if newLevel < 0:
                raise InvalidLevelError(
                    f"Zone {addIt!r} is at level {addInfo.level} (!!!)"
                    f" and so a new zone cannot be added above it."
                )
            toInfo = self.createZone(addTo, newLevel)

        # Now both addInfo and toInfo are defined
        if addInfo.level >= toInfo.level:
            raise InvalidLevelError(
                f"Cannot add zone {addIt!r} at level {addInfo.level}"
                f" to zone {addTo!r} at level {toInfo.level}: zones can"
                f" only contain zones of lower levels."
            )

        # Now both addInfo and toInfo are defined
        toInfo.contents.add(addIt)
        addInfo.parents.add(addTo)

    def removeZoneFromZone(
        self,
        removeIt: base.Zone,
        removeFrom: base.Zone
    ) -> bool:
        """
        Removes a zone from a zone if it had been in it, returning True
        if that zone had been in that zone, and False if it was not in
        that zone, including if either zone did not exist.

        For example:

        >>> d = DecisionGraph()
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.createZone('Z2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.createZone('l1Z', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> d.createZone('l2Z', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> d.addZoneToZone('Z', 'l1Z')
        >>> d.addZoneToZone('l1Z', 'l2Z')
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents={'l1Z'}, contents=set())
        >>> d.getZoneInfo('l1Z')
        ZoneInfo(level=1, parents={'l2Z'}, contents={'Z'})
        >>> d.getZoneInfo('l2Z')
        ZoneInfo(level=2, parents=set(), contents={'l1Z'})
        >>> d.removeZoneFromZone('l1Z', 'l2Z')
        True
        >>> d.getZoneInfo('l1Z')
        ZoneInfo(level=1, parents=set(), contents={'Z'})
        >>> d.getZoneInfo('l2Z')
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> d.removeZoneFromZone('Z', 'l1Z')
        True
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.getZoneInfo('l1Z')
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> d.removeZoneFromZone('Z', 'l1Z')
        False
        >>> d.removeZoneFromZone('Z', 'madeup')
        False
        >>> d.removeZoneFromZone('nope', 'madeup')
        False
        >>> d.removeZoneFromZone('nope', 'l1Z')
        False
        """
        remInfo = self.getZoneInfo(removeIt)
        fromInfo = self.getZoneInfo(removeFrom)

        if remInfo is None or fromInfo is None:
            return False

        if removeIt not in fromInfo.contents:
            return False

        remInfo.parents.remove(removeFrom)
        fromInfo.contents.remove(removeIt)
        return True

    def decisionsInZone(self, zone: base.Zone) -> Set[base.DecisionID]:
        """
        Returns a set of all decisions included directly in the given
        zone, not counting decisions included via intermediate
        sub-zones (see `allDecisionsInZone` to include those).

        Raises a `MissingZoneError` if the specified zone does not
        exist.

        The returned set is a copy, not a live editable set.

        For example:

        >>> d = DecisionGraph()
        >>> d.addDecision('A')
        0
        >>> d.addDecision('B')
        1
        >>> d.addDecision('C')
        2
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.addDecisionToZone('A', 'Z')
        >>> d.addDecisionToZone('B', 'Z')
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents={0, 1})
        >>> d.decisionsInZone('Z')
        {0, 1}
        >>> d.createZone('Z2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.addDecisionToZone('B', 'Z2')
        >>> d.addDecisionToZone('C', 'Z2')
        >>> d.getZoneInfo('Z2')
        ZoneInfo(level=0, parents=set(), contents={1, 2})
        >>> d.decisionsInZone('Z')
        {0, 1}
        >>> d.decisionsInZone('Z2')
        {1, 2}
        >>> d.createZone('l1Z', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> d.addZoneToZone('Z', 'l1Z')
        >>> d.decisionsInZone('Z')
        {0, 1}
        >>> d.decisionsInZone('l1Z')
        set()
        >>> d.decisionsInZone('madeup')
        Traceback (most recent call last):
        ...
        exploration.core.MissingZoneError...
        >>> zDec = d.decisionsInZone('Z')
        >>> zDec.add(2)  # won't affect the zone
        >>> zDec
        {0, 1, 2}
        >>> d.decisionsInZone('Z')
        {0, 1}
        """
        info = self.getZoneInfo(zone)
        if info is None:
            raise MissingZoneError(f"Zone {zone!r} does not exist.")

        # Everything that's not a zone must be a decision
        return {
            item
            for item in info.contents
            if isinstance(item, base.DecisionID)
        }

    def subZones(self, zone: base.Zone) -> Set[base.Zone]:
        """
        Returns the set of all immediate sub-zones of the given zone.
        Will be an empty set if there are no sub-zones; raises a
        `MissingZoneError` if the specified zone does not exit.

        The returned set is a copy, not a live editable set.

        For example:

        >>> d = DecisionGraph()
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.subZones('Z')
        set()
        >>> d.createZone('l1Z', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> d.addZoneToZone('Z', 'l1Z')
        >>> d.subZones('Z')
        set()
        >>> d.subZones('l1Z')
        {'Z'}
        >>> s = d.subZones('l1Z')
        >>> s.add('Q')  # doesn't affect the zone
        >>> sorted(s)
        ['Q', 'Z']
        >>> d.subZones('l1Z')
        {'Z'}
        >>> d.subZones('madeup')
        Traceback (most recent call last):
        ...
        exploration.core.MissingZoneError...
        """
        info = self.getZoneInfo(zone)
        if info is None:
            raise MissingZoneError(f"Zone {zone!r} does not exist.")

        # Sub-zones will appear in self.zones
        return {
            item
            for item in info.contents
            if isinstance(item, base.Zone)
        }

    def allDecisionsInZone(self, zone: base.Zone) -> Set[base.DecisionID]:
        """
        Returns a set containing all decisions in the given zone,
        including those included via sub-zones.

        Raises a `MissingZoneError` if the specified zone does not
        exist.`

        For example:

        >>> d = DecisionGraph()
        >>> d.addDecision('A')
        0
        >>> d.addDecision('B')
        1
        >>> d.addDecision('C')
        2
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.addDecisionToZone('A', 'Z')
        >>> d.addDecisionToZone('B', 'Z')
        >>> d.getZoneInfo('Z')
        ZoneInfo(level=0, parents=set(), contents={0, 1})
        >>> d.decisionsInZone('Z')
        {0, 1}
        >>> d.allDecisionsInZone('Z')
        {0, 1}
        >>> d.createZone('Z2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.addDecisionToZone('B', 'Z2')
        >>> d.addDecisionToZone('C', 'Z2')
        >>> d.getZoneInfo('Z2')
        ZoneInfo(level=0, parents=set(), contents={1, 2})
        >>> d.decisionsInZone('Z')
        {0, 1}
        >>> d.decisionsInZone('Z2')
        {1, 2}
        >>> d.allDecisionsInZone('Z2')
        {1, 2}
        >>> d.createZone('l1Z', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> d.createZone('l2Z', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> d.addZoneToZone('Z', 'l1Z')
        >>> d.addZoneToZone('l1Z', 'l2Z')
        >>> d.addZoneToZone('Z2', 'l2Z')
        >>> d.decisionsInZone('Z')
        {0, 1}
        >>> d.decisionsInZone('Z2')
        {1, 2}
        >>> d.decisionsInZone('l1Z')
        set()
        >>> d.allDecisionsInZone('l1Z')
        {0, 1}
        >>> d.allDecisionsInZone('l2Z')
        {0, 1, 2}
        """
        result: Set[base.DecisionID] = set()
        info = self.getZoneInfo(zone)
        if info is None:
            raise MissingZoneError(f"Zone {zone!r} does not exist.")

        for item in info.contents:
            if isinstance(item, base.Zone):
                # This can't be an error because of the condition above
                result |= self.allDecisionsInZone(item)
            else:  # it's a decision
                result.add(item)

        return result

    def zoneHierarchyLevel(self, zone: base.Zone) -> int:
        """
        Returns the hierarchy level of the given zone, as stored in its
        zone info.

        Raises a `MissingZoneError` if the specified zone does not
        exist.

        For example:

        >>> d = DecisionGraph()
        >>> d.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.createZone('l1Z', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> d.createZone('l5Z', 5)
        ZoneInfo(level=5, parents=set(), contents=set())
        >>> d.zoneHierarchyLevel('Z')
        0
        >>> d.zoneHierarchyLevel('l1Z')
        1
        >>> d.zoneHierarchyLevel('l5Z')
        5
        >>> d.zoneHierarchyLevel('madeup')
        Traceback (most recent call last):
        ...
        exploration.core.MissingZoneError...
        """
        info = self.getZoneInfo(zone)
        if info is None:
            raise MissingZoneError(f"Zone {zone!r} dose not exist.")

        return info.level

    def zoneParents(
        self,
        zoneOrDecision: Union[base.Zone, base.DecisionID]
    ) -> Set[base.Zone]:
        """
        Returns the set of all zones which directly contain the target
        zone or decision.

        Raises a `MissingDecisionError` if the target is neither a valid
        zone nor a valid decision.

        Returns a copy, not a live editable set.

        Example:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.createZone('level0', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('level1', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> g.createZone('level2', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> g.createZone('level3', 3)
        ZoneInfo(level=3, parents=set(), contents=set())
        >>> g.addDecisionToZone('A', 'level0')
        >>> g.addDecisionToZone('B', 'level0')
        >>> g.addZoneToZone('level0', 'level1')
        >>> g.addZoneToZone('level1', 'level2')
        >>> g.addZoneToZone('level2', 'level3')
        >>> g.addDecisionToZone('B', 'level2')  # Direct w/ skips
        >>> sorted(g.zoneParents(0))
        ['level0']
        >>> sorted(g.zoneParents(1))
        ['level0', 'level2']
        """
        if zoneOrDecision in self.zones:
            zoneOrDecision = cast(base.Zone, zoneOrDecision)
            info = cast(base.ZoneInfo, self.getZoneInfo(zoneOrDecision))
            return copy.copy(info.parents)
        elif zoneOrDecision in self:
            return self.nodes[zoneOrDecision].get('zones', set())
        else:
            raise MissingDecisionError(
                f"Name {zoneOrDecision!r} is neither a valid zone nor a"
                f" valid decision."
            )

    def zoneAncestors(
        self,
        zoneOrDecision: Union[base.Zone, base.DecisionID],
        exclude: Set[base.Zone] = set()
    ) -> Set[base.Zone]:
        """
        Returns the set of zones which contain the target zone or
        decision, either directly or indirectly. The target is not
        included in the set.

        Any ones listed in the `exclude` set are also excluded, as are
        any of their ancestors which are not also ancestors of the
        target zone via another path of inclusion.

        Raises a `MissingDecisionError` if the target is nether a valid
        zone nor a valid decision.

        Example:

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.createZone('level0', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('level1', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> g.createZone('level2', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> g.createZone('level3', 3)
        ZoneInfo(level=3, parents=set(), contents=set())
        >>> g.addDecisionToZone('A', 'level0')
        >>> g.addDecisionToZone('B', 'level0')
        >>> g.addZoneToZone('level0', 'level1')
        >>> g.addZoneToZone('level1', 'level2')
        >>> g.addZoneToZone('level2', 'level3')
        >>> g.addDecisionToZone('B', 'level2')  # Direct w/ skips
        >>> sorted(g.zoneAncestors(0))
        ['level0', 'level1', 'level2', 'level3']
        >>> sorted(g.zoneAncestors(1))
        ['level0', 'level1', 'level2', 'level3']
        >>> sorted(g.zoneParents(0))
        ['level0']
        >>> sorted(g.zoneParents(1))
        ['level0', 'level2']
        """
        # Copy is important here!
        result = set(self.zoneParents(zoneOrDecision))
        result -= exclude
        for parent in copy.copy(result):
            # Recursively dig up ancestors, but exclude
            # results-so-far to avoid re-enumerating when there are
            # multiple braided inclusion paths.
            result |= self.zoneAncestors(parent, result | exclude)

        return result

    def zoneEdges(self, zone: base.Zone) -> Optional[
        Tuple[
            Set[Tuple[base.DecisionID, base.Transition]],
            Set[Tuple[base.DecisionID, base.Transition]]
        ]
    ]:
        """
        Given a zone to look at, finds all of the transitions which go
        out of and into that zone, ignoring internal transitions between
        decisions in the zone. This includes all decisions in sub-zones.
        The return value is a pair of sets for outgoing and then
        incoming transitions, where each transition is specified as a
        (sourceID, transitionName) pair.

        Returns `None` if the target zone isn't yet fully defined.

        Note that this takes time proportional to *all* edges plus *all*
        nodes in the graph no matter how large or small the zone in
        question is.

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.addDecision('C')
        2
        >>> g.addDecision('D')
        3
        >>> g.addTransition('A', 'up', 'B', 'down')
        >>> g.addTransition('B', 'right', 'C', 'left')
        >>> g.addTransition('C', 'down', 'D', 'up')
        >>> g.addTransition('D', 'left', 'A', 'right')
        >>> g.addTransition('A', 'tunnel', 'C', 'tunnel')
        >>> g.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('ZZ', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> g.addZoneToZone('Z', 'ZZ')
        >>> g.addDecisionToZone('A', 'Z')
        >>> g.addDecisionToZone('B', 'Z')
        >>> g.addDecisionToZone('D', 'ZZ')
        >>> outgoing, incoming = g.zoneEdges('Z')  # TODO: Sort for testing
        >>> sorted(outgoing)
        [(0, 'right'), (0, 'tunnel'), (1, 'right')]
        >>> sorted(incoming)
        [(2, 'left'), (2, 'tunnel'), (3, 'left')]
        >>> outgoing, incoming = g.zoneEdges('ZZ')
        >>> sorted(outgoing)
        [(0, 'tunnel'), (1, 'right'), (3, 'up')]
        >>> sorted(incoming)
        [(2, 'down'), (2, 'left'), (2, 'tunnel')]
        >>> g.zoneEdges('madeup') is None
        True
        """
        # Find the interior nodes
        try:
            interior = self.allDecisionsInZone(zone)
        except MissingZoneError:
            return None

        # Set up our result
        results: Tuple[
            Set[Tuple[base.DecisionID, base.Transition]],
            Set[Tuple[base.DecisionID, base.Transition]]
        ] = (set(), set())

        # Because finding incoming edges requires searching the entire
        # graph anyways, it's more efficient to just consider each edge
        # once.
        for fromDecision in self:
            fromThere = self[fromDecision]
            for toDecision in fromThere:
                for transition in fromThere[toDecision]:
                    sourceIn = fromDecision in interior
                    destIn = toDecision in interior
                    if sourceIn and not destIn:
                        results[0].add((fromDecision, transition))
                    elif destIn and not sourceIn:
                        results[1].add((fromDecision, transition))

        return results

    def replaceZonesInHierarchy(
        self,
        target: base.AnyDecisionSpecifier,
        zone: base.Zone,
        level: int
    ) -> None:
        """
        This method replaces one or more zones which contain the
        specified `target` decision with a specific zone, at a specific
        level in the zone hierarchy (see `zoneHierarchyLevel`). If the
        named zone doesn't yet exist, it will be created.

        To do this, it looks at all zones which contain the target
        decision directly or indirectly (see `zoneAncestors`) and which
        are at the specified level.

        - Any direct children of those zones which are ancestors of the
            target decision are removed from those zones and placed into
            the new zone instead, regardless of their levels. Indirect
            children are not affected (except perhaps indirectly via
            their parents' ancestors changing).
        - The new zone is placed into every direct parent of those
            zones, regardless of their levels (those parents are by
            definition all ancestors of the target decision).
        - If there were no zones at the target level, every zone at the
            next level down which is an ancestor of the target decision
            (or just that decision if the level is 0) is placed into the
            new zone as a direct child (and is removed from any previous
            parents it had). In this case, the new zone will also be
            added as a sub-zone to every ancestor of the target decision
            at the level above the specified level, if there are any.
            * In this case, if there are no zones at the level below the
                specified level, the highest level of zones smaller than
                that is treated as the level below, down to targeting
                the decision itself.
            * Similarly, if there are no zones at the level above the
                specified level but there are zones at a higher level,
                the new zone will be added to each of the zones in the
                lowest level above the target level that has zones in it.

        A `MissingDecisionError` will be raised if the specified
        decision is not valid, or if the decision is left as default but
        there is no current decision in the exploration.

        An `InvalidLevelError` will be raised if the level is less than
        zero.

        Example:

        >>> g = DecisionGraph()
        >>> g.addDecision('decision')
        0
        >>> g.addDecision('alternate')
        1
        >>> g.createZone('zone0', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('zone1', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> g.createZone('zone2.1', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> g.createZone('zone2.2', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> g.createZone('zone3', 3)
        ZoneInfo(level=3, parents=set(), contents=set())
        >>> g.addDecisionToZone('decision', 'zone0')
        >>> g.addDecisionToZone('alternate', 'zone0')
        >>> g.addZoneToZone('zone0', 'zone1')
        >>> g.addZoneToZone('zone1', 'zone2.1')
        >>> g.addZoneToZone('zone1', 'zone2.2')
        >>> g.addZoneToZone('zone2.1', 'zone3')
        >>> g.addZoneToZone('zone2.2', 'zone3')
        >>> g.zoneHierarchyLevel('zone0')
        0
        >>> g.zoneHierarchyLevel('zone1')
        1
        >>> g.zoneHierarchyLevel('zone2.1')
        2
        >>> g.zoneHierarchyLevel('zone2.2')
        2
        >>> g.zoneHierarchyLevel('zone3')
        3
        >>> sorted(g.decisionsInZone('zone0'))
        [0, 1]
        >>> sorted(g.zoneAncestors('zone0'))
        ['zone1', 'zone2.1', 'zone2.2', 'zone3']
        >>> g.subZones('zone1')
        {'zone0'}
        >>> g.zoneParents('zone0')
        {'zone1'}
        >>> g.replaceZonesInHierarchy('decision', 'new0', 0)
        >>> g.zoneParents('zone0')
        {'zone1'}
        >>> g.zoneParents('new0')
        {'zone1'}
        >>> sorted(g.zoneAncestors('zone0'))
        ['zone1', 'zone2.1', 'zone2.2', 'zone3']
        >>> sorted(g.zoneAncestors('new0'))
        ['zone1', 'zone2.1', 'zone2.2', 'zone3']
        >>> g.decisionsInZone('zone0')
        {1}
        >>> g.decisionsInZone('new0')
        {0}
        >>> sorted(g.subZones('zone1'))
        ['new0', 'zone0']
        >>> g.zoneParents('new0')
        {'zone1'}
        >>> g.replaceZonesInHierarchy('decision', 'new1', 1)
        >>> sorted(g.zoneAncestors(0))
        ['new0', 'new1', 'zone2.1', 'zone2.2', 'zone3']
        >>> g.subZones('zone1')
        {'zone0'}
        >>> g.subZones('new1')
        {'new0'}
        >>> g.zoneParents('new0')
        {'new1'}
        >>> sorted(g.zoneParents('zone1'))
        ['zone2.1', 'zone2.2']
        >>> sorted(g.zoneParents('new1'))
        ['zone2.1', 'zone2.2']
        >>> g.zoneParents('zone2.1')
        {'zone3'}
        >>> g.zoneParents('zone2.2')
        {'zone3'}
        >>> sorted(g.subZones('zone2.1'))
        ['new1', 'zone1']
        >>> sorted(g.subZones('zone2.2'))
        ['new1', 'zone1']
        >>> sorted(g.allDecisionsInZone('zone2.1'))
        [0, 1]
        >>> sorted(g.allDecisionsInZone('zone2.2'))
        [0, 1]
        >>> g.replaceZonesInHierarchy('decision', 'new2', 2)
        >>> g.zoneParents('zone2.1')
        {'zone3'}
        >>> g.zoneParents('zone2.2')
        {'zone3'}
        >>> g.subZones('zone2.1')
        {'zone1'}
        >>> g.subZones('zone2.2')
        {'zone1'}
        >>> g.subZones('new2')
        {'new1'}
        >>> g.zoneParents('new2')
        {'zone3'}
        >>> g.allDecisionsInZone('zone2.1')
        {1}
        >>> g.allDecisionsInZone('zone2.2')
        {1}
        >>> g.allDecisionsInZone('new2')
        {0}
        >>> sorted(g.subZones('zone3'))
        ['new2', 'zone2.1', 'zone2.2']
        >>> g.zoneParents('zone3')
        set()
        >>> sorted(g.allDecisionsInZone('zone3'))
        [0, 1]
        >>> g.replaceZonesInHierarchy('decision', 'new3', 3)
        >>> sorted(g.subZones('zone3'))
        ['zone2.1', 'zone2.2']
        >>> g.subZones('new3')
        {'new2'}
        >>> g.zoneParents('zone3')
        set()
        >>> g.zoneParents('new3')
        set()
        >>> g.allDecisionsInZone('zone3')
        {1}
        >>> g.allDecisionsInZone('new3')
        {0}
        >>> g.replaceZonesInHierarchy('decision', 'new4', 5)
        >>> g.subZones('new4')
        {'new3'}
        >>> g.zoneHierarchyLevel('new4')
        5

        Another example of level collapse when trying to replace a zone
        at a level above :

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.createZone('level0', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.createZone('level1', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> g.createZone('level2', 2)
        ZoneInfo(level=2, parents=set(), contents=set())
        >>> g.createZone('level3', 3)
        ZoneInfo(level=3, parents=set(), contents=set())
        >>> g.addDecisionToZone('B', 'level0')
        >>> g.addZoneToZone('level0', 'level1')
        >>> g.addZoneToZone('level1', 'level2')
        >>> g.addZoneToZone('level2', 'level3')
        >>> g.addDecisionToZone('A', 'level3') # missing some zone levels
        >>> g.zoneHierarchyLevel('level3')
        3
        >>> g.replaceZonesInHierarchy('A', 'newFirst', 1)
        >>> g.zoneHierarchyLevel('newFirst')
        1
        >>> g.decisionsInZone('newFirst')
        {0}
        >>> g.decisionsInZone('level3')
        set()
        >>> sorted(g.allDecisionsInZone('level3'))
        [0, 1]
        >>> g.subZones('newFirst')
        set()
        >>> sorted(g.subZones('level3'))
        ['level2', 'newFirst']
        >>> g.zoneParents('newFirst')
        {'level3'}
        >>> g.replaceZonesInHierarchy('A', 'newSecond', 2)
        >>> g.zoneHierarchyLevel('newSecond')
        2
        >>> g.decisionsInZone('newSecond')
        set()
        >>> g.allDecisionsInZone('newSecond')
        {0}
        >>> g.subZones('newSecond')
        {'newFirst'}
        >>> g.zoneParents('newSecond')
        {'level3'}
        >>> g.zoneParents('newFirst')
        {'newSecond'}
        >>> sorted(g.subZones('level3'))
        ['level2', 'newSecond']
        """
        tID = self.resolveDecision(target)

        if level < 0:
            raise InvalidLevelError(
                f"Target level must be positive (got {level})."
            )

        info = self.getZoneInfo(zone)
        if info is None:
            info = self.createZone(zone, level)
        elif level != info.level:
            raise InvalidLevelError(
                f"Target level ({level}) does not match the level of"
                f" the target zone ({zone!r} at level {info.level})."
            )

        # Collect both parents & ancestors
        parents = self.zoneParents(tID)
        ancestors = set(self.zoneAncestors(tID))

        # Map from levels to sets of zones from the ancestors pool
        levelMap: Dict[int, Set[base.Zone]] = {}
        highest = -1
        for ancestor in ancestors:
            ancestorLevel = self.zoneHierarchyLevel(ancestor)
            levelMap.setdefault(ancestorLevel, set()).add(ancestor)
            if ancestorLevel > highest:
                highest = ancestorLevel

        # Figure out if we have target zones to replace or not
        reparentDecision = False
        if level in levelMap:
            # If there are zones at the target level,
            targetZones = levelMap[level]

            above = set()
            below = set()

            for replaced in targetZones:
                above |= self.zoneParents(replaced)
                below |= self.subZones(replaced)
                if replaced in parents:
                    reparentDecision = True

            # Only ancestors should be reparented
            below &= ancestors

        else:
            # Find levels w/ zones in them above + below
            levelBelow = level - 1
            levelAbove = level + 1
            below = levelMap.get(levelBelow, set())
            above = levelMap.get(levelAbove, set())

            while len(below) == 0 and levelBelow > 0:
                levelBelow -= 1
                below = levelMap.get(levelBelow, set())

            if len(below) == 0:
                reparentDecision = True

            while len(above) == 0 and levelAbove < highest:
                levelAbove += 1
                above = levelMap.get(levelAbove, set())

        # Handle re-parenting zones below
        for under in below:
            for parent in self.zoneParents(under):
                if parent in ancestors:
                    self.removeZoneFromZone(under, parent)
            self.addZoneToZone(under, zone)

        # Add this zone to each parent
        for parent in above:
            self.addZoneToZone(zone, parent)

        # Re-parent the decision itself if necessary
        if reparentDecision:
            # (using set() here to avoid size-change-during-iteration)
            for parent in set(parents):
                self.removeDecisionFromZone(tID, parent)
            self.addDecisionToZone(tID, zone)

    def getReciprocal(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> Optional[base.Transition]:
        """
        Returns the reciprocal edge for the specified transition from the
        specified decision (see `setReciprocal`). Returns
        `None` if no reciprocal has been established for that
        transition, or if that decision or transition does not exist.
        """
        dID = self.resolveDecision(decision)

        dest = self.getDestination(dID, transition)
        if dest is not None:
            info = cast(
                TransitionProperties,
                self.edges[dID, dest, transition]  # type:ignore
            )
            recip = info.get("reciprocal")
            if recip is not None and not isinstance(recip, base.Transition):
                raise ValueError(f"Invalid reciprocal value: {repr(recip)}")
            return recip
        else:
            return None

    def setReciprocal(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        reciprocal: Optional[base.Transition],
        setBoth: bool = True,
        cleanup: bool = True
    ) -> None:
        """
        Sets the 'reciprocal' transition for a particular transition from
        a particular decision, and removes the reciprocal property from
        any old reciprocal transition.

        Raises a `MissingDecisionError` or a `MissingTransitionError` if
        the specified decision or transition does not exist.

        Raises an `InvalidDestinationError` if the reciprocal transition
        does not exist, or if it does exist but does not lead back to
        the decision the transition came from.

        If `setBoth` is True (the default) then the transition which is
        being identified as a reciprocal will also have its reciprocal
        property set, pointing back to the primary transition being
        modified, and any old reciprocal of that transition will have its
        reciprocal set to None. If you want to create a situation with
        non-exclusive reciprocals, use `setBoth=False`.

        If `cleanup` is True (the default) then abandoned reciprocal
        transitions (for both edges if `setBoth` was true) have their
        reciprocal properties removed. Set `cleanup` to false if you want
        to retain them, although this will result in non-exclusive
        reciprocal relationships.

        If the `reciprocal` value is None, this deletes the reciprocal
        value entirely, and if `setBoth` is true, it does this for the
        previous reciprocal edge as well. No error is raised in this case
        when there was not already a reciprocal to delete.

        Note that one should remove a reciprocal relationship before
        redirecting either edge of the pair in a way that gives it a new
        reciprocal, since otherwise, a later attempt to remove the
        reciprocal with `setBoth` set to True (the default) will end up
        deleting the reciprocal information from the other edge that was
        already modified. There is no way to reliably detect and avoid
        this, because two different decisions could (and often do in
        practice) have transitions with identical names, meaning that the
        reciprocal value will still be the same, but it will indicate a
        different edge in virtue of the destination of the edge changing.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('G')
        0
        >>> g.addDecision('H')
        1
        >>> g.addDecision('I')
        2
        >>> g.addTransition('G', 'up', 'H', 'down')
        >>> g.addTransition('G', 'next', 'H', 'prev')
        >>> g.addTransition('H', 'next', 'I', 'prev')
        >>> g.addTransition('H', 'return', 'G')
        >>> g.setReciprocal('G', 'up', 'next') # Error w/ destinations
        Traceback (most recent call last):
        ...
        exploration.core.InvalidDestinationError...
        >>> g.setReciprocal('G', 'up', 'none') # Doesn't exist
        Traceback (most recent call last):
        ...
        exploration.core.MissingTransitionError...
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') is None
        True
        >>> g.setReciprocal('G', 'up', 'return')
        >>> g.getReciprocal('G', 'up')
        'return'
        >>> g.getReciprocal('H', 'down') is None
        True
        >>> g.getReciprocal('H', 'return')
        'up'
        >>> g.setReciprocal('H', 'return', None) # remove the reciprocal
        >>> g.getReciprocal('G', 'up') is None
        True
        >>> g.getReciprocal('H', 'down') is None
        True
        >>> g.getReciprocal('H', 'return') is None
        True
        >>> g.setReciprocal('G', 'up', 'down', setBoth=False) # one-way
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down') is None
        True
        >>> g.getReciprocal('H', 'return') is None
        True
        >>> g.setReciprocal('H', 'return', 'up', setBoth=False) # non-sym
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down') is None
        True
        >>> g.getReciprocal('H', 'return')
        'up'
        >>> g.setReciprocal('H', 'down', 'up') # setBoth not needed
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') # unchanged
        'up'
        >>> g.setReciprocal('G', 'up', 'return', cleanup=False) # no cleanup
        >>> g.getReciprocal('G', 'up')
        'return'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') # unchanged
        'up'
        >>> # Cleanup only applies to reciprocal if setBoth is true
        >>> g.setReciprocal('H', 'down', 'up', setBoth=False)
        >>> g.getReciprocal('G', 'up')
        'return'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') # not cleaned up w/out setBoth
        'up'
        >>> g.setReciprocal('H', 'down', 'up') # with cleanup and setBoth
        >>> g.getReciprocal('G', 'up')
        'down'
        >>> g.getReciprocal('H', 'down')
        'up'
        >>> g.getReciprocal('H', 'return') is None # cleaned up
        True
        """
        dID = self.resolveDecision(decision)

        dest = self.destination(dID, transition) # possible KeyError
        if reciprocal is None:
            rDest = None
        else:
            rDest = self.getDestination(dest, reciprocal)

        # Set or delete reciprocal property
        if reciprocal is None:
            # Delete the property
            info = self.edges[dID, dest, transition]  # type:ignore

            old = info.pop('reciprocal')
            if setBoth:
                rDest = self.getDestination(dest, old)
                if rDest != dID:
                    raise RuntimeError(
                        f"Invalid reciprocal {old!r} for transition"
                        f" {transition!r} from {self.identityOf(dID)}:"
                        f" destination is {rDest}."
                    )
                rInfo = self.edges[dest, dID, old]  # type:ignore
                if 'reciprocal' in rInfo:
                    del rInfo['reciprocal']
        else:
            # Set the property, checking for errors first
            if rDest is None:
                raise MissingTransitionError(
                    f"Reciprocal transition {reciprocal!r} for"
                    f" transition {transition!r} from decision"
                    f" {self.identityOf(dID)} does not exist at"
                    f" decision {self.identityOf(dest)}"
                )

            if rDest != dID:
                raise InvalidDestinationError(
                    f"Reciprocal transition {reciprocal!r} from"
                    f" decision {self.identityOf(dest)} does not lead"
                    f" back to decision {self.identityOf(dID)}."
                )

            eProps = self.edges[dID, dest, transition]  # type:ignore [index]
            abandoned = eProps.get('reciprocal')
            eProps['reciprocal'] = reciprocal
            if cleanup and abandoned not in (None, reciprocal):
                aProps = self.edges[dest, dID, abandoned]  # type:ignore
                if 'reciprocal' in aProps:
                    del aProps['reciprocal']

            if setBoth:
                rProps = self.edges[dest, dID, reciprocal]  # type:ignore
                revAbandoned = rProps.get('reciprocal')
                rProps['reciprocal'] = transition
                # Sever old reciprocal relationship
                if cleanup and revAbandoned not in (None, transition):
                    raProps = self.edges[
                        dID,  # type:ignore
                        dest,
                        revAbandoned
                    ]
                    del raProps['reciprocal']

    def getReciprocalPair(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition
    ) -> Optional[Tuple[base.DecisionID, base.Transition]]:
        """
        Returns a tuple containing both the destination decision ID and
        the transition at that decision which is the reciprocal of the
        specified destination & transition. Returns `None` if no
        reciprocal has been established for that transition, or if that
        decision or transition does not exist.

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.addDecision('C')
        2
        >>> g.addTransition('A', 'up', 'B', 'down')
        >>> g.addTransition('B', 'right', 'C', 'left')
        >>> g.addTransition('A', 'oneway', 'C')
        >>> g.getReciprocalPair('A', 'up')
        (1, 'down')
        >>> g.getReciprocalPair('B', 'down')
        (0, 'up')
        >>> g.getReciprocalPair('B', 'right')
        (2, 'left')
        >>> g.getReciprocalPair('C', 'left')
        (1, 'right')
        >>> g.getReciprocalPair('C', 'up') is None
        True
        >>> g.getReciprocalPair('Q', 'up') is None
        True
        >>> g.getReciprocalPair('A', 'tunnel') is None
        True
        """
        try:
            dID = self.resolveDecision(decision)
        except MissingDecisionError:
            return None

        reciprocal = self.getReciprocal(dID, transition)
        if reciprocal is None:
            return None
        else:
            destination = self.getDestination(dID, transition)
            if destination is None:
                return None
            else:
                return (destination, reciprocal)

    def addDecision(
        self,
        name: base.DecisionName,
        domain: Optional[base.Domain] = None,
        tags: Optional[Dict[base.Tag, base.TagValue]] = None,
        annotations: Optional[List[base.Annotation]] = None
    ) -> base.DecisionID:
        """
        Adds a decision to the graph, without any transitions yet. Each
        decision will be assigned an ID so name collisions are allowed,
        but it's usually best to keep names unique at least within each
        zone. If no domain is provided, the `DEFAULT_DOMAIN` will be
        used for the decision's domain. A dictionary of tags and/or a
        list of annotations (strings in both cases) may be provided.

        Returns the newly-assigned `DecisionID` for the decision it
        created.

        Emits a `DecisionCollisionWarning` if a decision with the
        provided name already exists and the `WARN_OF_NAME_COLLISIONS`
        global variable is set to `True`.
        """
        # Defaults
        if domain is None:
            domain = base.DEFAULT_DOMAIN
        if tags is None:
            tags = {}
        if annotations is None:
            annotations = []

        # Error checking
        if name in self.nameLookup and WARN_OF_NAME_COLLISIONS:
            warnings.warn(
                (
                    f"Adding decision {name!r}: Another decision with"
                    f" that name already exists."
                ),
                DecisionCollisionWarning
            )

        dID = self._assignID()

        # Add the decision
        self.add_node(
            dID,
            name=name,
            domain=domain,
            tags=tags,
            annotations=annotations
        )
        #TODO: Elide tags/annotations if they're empty?

        # Track it in our `nameLookup` dictionary
        self.nameLookup.setdefault(name, []).append(dID)

        return dID

    def addIdentifiedDecision(
        self,
        dID: base.DecisionID,
        name: base.DecisionName,
        domain: Optional[base.Domain] = None,
        tags: Optional[Dict[base.Tag, base.TagValue]] = None,
        annotations: Optional[List[base.Annotation]] = None
    ) -> None:
        """
        Adds a new decision to the graph using a specific decision ID,
        rather than automatically assigning a new decision ID like
        `addDecision` does. Otherwise works like `addDecision`.

        Raises a `MechanismCollisionError` if the specified decision ID
        is already in use.
        """
        # Defaults
        if domain is None:
            domain = base.DEFAULT_DOMAIN
        if tags is None:
            tags = {}
        if annotations is None:
            annotations = []

        # Error checking
        if dID in self.nodes:
            raise MechanismCollisionError(
                f"Cannot add a node with id {dID} and name {name!r}:"
                f" that ID is already used by node {self.identityOf(dID)}"
            )

        if name in self.nameLookup and WARN_OF_NAME_COLLISIONS:
            warnings.warn(
                (
                    f"Adding decision {name!r}: Another decision with"
                    f" that name already exists."
                ),
                DecisionCollisionWarning
            )

        # Add the decision
        self.add_node(
            dID,
            name=name,
            domain=domain,
            tags=tags,
            annotations=annotations
        )
        #TODO: Elide tags/annotations if they're empty?

        # Track it in our `nameLookup` dictionary
        self.nameLookup.setdefault(name, []).append(dID)

    def addTransition(
        self,
        fromDecision: base.AnyDecisionSpecifier,
        name: base.Transition,
        toDecision: base.AnyDecisionSpecifier,
        reciprocal: Optional[base.Transition] = None,
        tags: Optional[Dict[base.Tag, base.TagValue]] = None,
        annotations: Optional[List[base.Annotation]] = None,
        revTags: Optional[Dict[base.Tag, base.TagValue]] = None,
        revAnnotations: Optional[List[base.Annotation]] = None,
        requires: Optional[base.Requirement] = None,
        consequence: Optional[base.Consequence] = None,
        revRequires: Optional[base.Requirement] = None,
        revConsequece: Optional[base.Consequence] = None
    ) -> None:
        """
        Adds a transition connecting two decisions. A specifier for each
        decision is required, as is a name for the transition. If a
        `reciprocal` is provided, a reciprocal edge will be added in the
        opposite direction using that name; by default only the specified
        edge is added. A `TransitionCollisionError` will be raised if the
        `reciprocal` matches the name of an existing edge at the
        destination decision.

        Both decisions must already exist, or a `MissingDecisionError`
        will be raised.

        A dictionary of tags and/or a list of annotations may be
        provided. Tags and/or annotations for the reverse edge may also
        be specified if one is being added.

        The `requires`, `consequence`, `revRequires`, and `revConsequece`
        arguments specify requirements and/or consequences of the new
        outgoing and reciprocal edges.
        """
        # Defaults
        if tags is None:
            tags = {}
        if annotations is None:
            annotations = []
        if revTags is None:
            revTags = {}
        if revAnnotations is None:
            revAnnotations = []

        # Error checking
        fromID = self.resolveDecision(fromDecision)
        toID = self.resolveDecision(toDecision)

        # Note: have to check this first so we don't add the forward edge
        # and then error out after a side effect!
        if (
            reciprocal is not None
        and self.getDestination(toDecision, reciprocal) is not None
        ):
            raise TransitionCollisionError(
                f"Cannot add a transition from"
                f" {self.identityOf(fromDecision)} to"
                f" {self.identityOf(toDecision)} with reciprocal edge"
                f" {reciprocal!r}: {reciprocal!r} is already used as an"
                f" edge name at {self.identityOf(toDecision)}."
            )

        # Add the edge
        self.add_edge(
            fromID,
            toID,
            key=name,
            tags=tags,
            annotations=annotations
        )
        self.setTransitionRequirement(fromDecision, name, requires)
        if consequence is not None:
            self.setConsequence(fromDecision, name, consequence)
        if reciprocal is not None:
            # Add the reciprocal edge
            self.add_edge(
                toID,
                fromID,
                key=reciprocal,
                tags=revTags,
                annotations=revAnnotations
            )
            self.setReciprocal(fromID, name, reciprocal)
            self.setTransitionRequirement(
                toDecision,
                reciprocal,
                revRequires
            )
            if revConsequece is not None:
                self.setConsequence(toDecision, reciprocal, revConsequece)

    def removeTransition(
        self,
        fromDecision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        removeReciprocal=False
    ) -> Union[
        TransitionProperties,
        Tuple[TransitionProperties, TransitionProperties]
    ]:
        """
        Removes a transition. If `removeReciprocal` is true (False is the
        default) any reciprocal transition will also be removed (but no
        error will occur if there wasn't a reciprocal).

        For each removed transition, *every* transition that targeted
        that transition as its reciprocal will have its reciprocal set to
        `None`, to avoid leaving any invalid reciprocal values.

        Raises a `KeyError` if either the target decision or the target
        transition does not exist.

        Returns a transition properties dictionary with the properties
        of the removed transition, or if `removeReciprocal` is true,
        returns a pair of such dictionaries for the target transition
        and its reciprocal.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.addTransition('A', 'up', 'B', 'down', tags={'wide'})
        >>> g.addTransition('A', 'in', 'B', 'out') # we won't touch this
        >>> g.addTransition('A', 'next', 'B')
        >>> g.setReciprocal('A', 'next', 'down', setBoth=False)
        >>> p = g.removeTransition('A', 'up')
        >>> p['tags']
        {'wide'}
        >>> g.destinationsFrom('A')
        {'in': 1, 'next': 1}
        >>> g.destinationsFrom('B')
        {'down': 0, 'out': 0}
        >>> g.getReciprocal('B', 'down') is None
        True
        >>> g.getReciprocal('A', 'next') # Asymmetrical left over
        'down'
        >>> g.getReciprocal('A', 'in') # not affected
        'out'
        >>> g.getReciprocal('B', 'out') # not affected
        'in'
        >>> # Now with removeReciprocal set to True
        >>> g.addTransition('A', 'up', 'B') # add this back in
        >>> g.setReciprocal('A', 'up', 'down') # sets both
        >>> p = g.removeTransition('A', 'up', removeReciprocal=True)
        >>> g.destinationsFrom('A')
        {'in': 1, 'next': 1}
        >>> g.destinationsFrom('B')
        {'out': 0}
        >>> g.getReciprocal('A', 'next') is None
        True
        >>> g.getReciprocal('A', 'in') # not affected
        'out'
        >>> g.getReciprocal('B', 'out') # not affected
        'in'
        >>> g.removeTransition('A', 'none')
        Traceback (most recent call last):
        ...
        exploration.core.MissingTransitionError...
        >>> g.removeTransition('Z', 'nope')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        """
        # Resolve target ID
        fromID = self.resolveDecision(fromDecision)

        # raises if either is missing:
        destination = self.destination(fromID, transition)
        reciprocal = self.getReciprocal(fromID, transition)

        # Get dictionaries of parallel & antiparallel edges to be
        # checked for invalid reciprocals after removing edges
        # Note: these will update live as we remove edges
        allAntiparallel = self[destination][fromID]
        allParallel = self[fromID][destination]

        # Remove the target edge
        fProps = self.getTransitionProperties(fromID, transition)
        self.remove_edge(fromID, destination, transition)

        # Clean up any dangling reciprocal values
        for tProps in allAntiparallel.values():
            if tProps.get('reciprocal') == transition:
                del tProps['reciprocal']

        # Remove the reciprocal if requested
        if removeReciprocal and reciprocal is not None:
            rProps = self.getTransitionProperties(destination, reciprocal)
            self.remove_edge(destination, fromID, reciprocal)

            # Clean up any dangling reciprocal values
            for tProps in allParallel.values():
                if tProps.get('reciprocal') == reciprocal:
                    del tProps['reciprocal']

            return (fProps, rProps)
        else:
            return fProps

    def addMechanism(
        self,
        name: base.MechanismName,
        where: Optional[base.AnyDecisionSpecifier] = None
    ) -> base.MechanismID:
        """
        Creates a new mechanism with the given name at the specified
        decision, returning its assigned ID. If `where` is `None`, it
        creates a global mechanism. Raises a `MechanismCollisionError`
        if a mechanism with the same name already exists at a specified
        decision (or already exists as a global mechanism).

        Note that if the decision is deleted, the mechanism will be as
        well.

        Since `MechanismState`s are not tracked by `DecisionGraph`s but
        instead are part of a `State`, the mechanism won't be in any
        particular state, which means it will be treated as being in the
        `base.DEFAULT_MECHANISM_STATE`.
        """
        if where is None:
            mechs = self.globalMechanisms
            dID = None
        else:
            dID = self.resolveDecision(where)
            mechs = self.nodes[dID].setdefault('mechanisms', {})

        if name in mechs:
            if dID is None:
                raise MechanismCollisionError(
                    f"A global mechanism named {name!r} already exists."
                )
            else:
                raise MechanismCollisionError(
                    f"A mechanism named {name!r} already exists at"
                    f" decision {self.identityOf(dID)}."
                )

        mID = self._assignMechanismID()
        mechs[name] = mID
        self.mechanisms[mID] = (dID, name)
        return mID

    def mechanismsAt(
        self,
        decision: base.AnyDecisionSpecifier
    ) -> Dict[base.MechanismName, base.MechanismID]:
        """
        Returns a dictionary mapping mechanism names to their IDs for
        all mechanisms at the specified decision.
        """
        dID = self.resolveDecision(decision)

        return self.nodes[dID]['mechanisms']

    def mechanismDetails(
        self,
        mID: base.MechanismID
    ) -> Optional[Tuple[Optional[base.DecisionID], base.MechanismName]]:
        """
        Returns a tuple containing the decision ID and mechanism name
        for the specified mechanism. Returns `None` if there is no
        mechanism with that ID. For global mechanisms, `None` is used in
        place of a decision ID.
        """
        return self.mechanisms.get(mID)

    def deleteMechanism(self, mID: base.MechanismID) -> None:
        """
        Deletes the specified mechanism.
        """
        name, dID = self.mechanisms.pop(mID)

        del self.nodes[dID]['mechanisms'][name]

    def localLookup(
        self,
        startFrom: Union[
            base.AnyDecisionSpecifier,
            Collection[base.AnyDecisionSpecifier]
        ],
        findAmong: Callable[
            ['DecisionGraph', Union[Set[base.DecisionID], str]],
            Optional[LookupResult]
        ],
        fallbackLayerName: Optional[str] = "fallback",
        fallbackToAllDecisions: bool = True
    ) -> Optional[LookupResult]:
        """
        Looks up some kind of result in the graph by starting from a
        base set of decisions and widening the search iteratively based
        on zones. This first searches for result(s) in the set of
        decisions given, then in the set of all decisions which are in
        level-0 zones containing those decisions, then in level-1 zones,
        etc. When it runs out of relevant zones, it will check all
        decisions which are in any domain that a decision from the
        initial search set is in, and then if `fallbackLayerName` is a
        string, it will provide that string instead of a set of decision
        IDs to the `findAmong` function as the next layer to search.
        After the `fallbackLayerName` is used, if
        `fallbackToAllDecisions` is `True` (the default) a final search
        will be run on all decisions in the graph. The provided
        `findAmong` function is called on each successive decision ID
        set, until it generates a non-`None` result. We stop and return
        that non-`None` result as soon as one is generated. But if none
        of the decision sets consulted generate non-`None` results, then
        the entire result will be `None`.
        """
        # Normalize starting decisions to a set
        if isinstance(startFrom, (int, str, base.DecisionSpecifier)):
            startFrom = set([startFrom])

        # Resolve decision IDs; convert to list
        searchArea: Union[Set[base.DecisionID], str] = set(
            self.resolveDecision(spec) for spec in startFrom
        )

        # Find all ancestor zones & all relevant domains
        allAncestors = set()
        relevantDomains = set()
        for startingDecision in searchArea:
            allAncestors |= self.zoneAncestors(startingDecision)
            relevantDomains.add(self.domainFor(startingDecision))

        # Build layers dictionary
        ancestorLayers: Dict[int, Set[base.Zone]] = {}
        for zone in allAncestors:
            info = self.getZoneInfo(zone)
            assert info is not None
            level = info.level
            ancestorLayers.setdefault(level, set()).add(zone)

        searchLayers: LookupLayersList = (
            cast(LookupLayersList, [None])
          + cast(LookupLayersList, sorted(ancestorLayers.keys()))
          + cast(LookupLayersList, ["domains"])
        )
        if fallbackLayerName is not None:
            searchLayers.append("fallback")

        if fallbackToAllDecisions:
            searchLayers.append("all")

        # Continue our search through zone layers
        for layer in searchLayers:
            # Update search area on subsequent iterations
            if layer == "domains":
                searchArea = set()
                for relevant in relevantDomains:
                    searchArea |= self.allDecisionsInDomain(relevant)
            elif layer == "fallback":
                assert fallbackLayerName is not None
                searchArea = fallbackLayerName
            elif layer == "all":
                searchArea = set(self.nodes)
            elif layer is not None:
                layer = cast(int, layer)  # must be an integer
                searchZones = ancestorLayers[layer]
                searchArea = set()
                for zone in searchZones:
                    searchArea |= self.allDecisionsInZone(zone)
            # else it's the first iteration and we use the starting
            # searchArea

            searchResult: Optional[LookupResult] = findAmong(
                self,
                searchArea
            )

            if searchResult is not None:
                return searchResult

        # Didn't find any non-None results.
        return None

    @staticmethod
    def uniqueMechanismFinder(name: base.MechanismName) -> Callable[
        ['DecisionGraph', Union[Set[base.DecisionID], str]],
        Optional[base.MechanismID]
    ]:
        """
        Returns a search function that looks for the given mechanism ID,
        suitable for use with `localLookup`. The finder will raise a
        `MechanismCollisionError` if it finds more than one mechanism
        with the specified name at the same level of the search.
        """
        def namedMechanismFinder(
            graph: 'DecisionGraph',
            searchIn: Union[Set[base.DecisionID], str]
        ) -> Optional[base.MechanismID]:
            """
            Generated finder function for `localLookup` to find a unique
            mechanism by name.
            """
            candidates: List[base.DecisionID] = []

            if searchIn == "fallback":
                if name in graph.globalMechanisms:
                    candidates = [graph.globalMechanisms[name]]

            else:
                assert isinstance(searchIn, set)
                for dID in searchIn:
                    mechs = graph.nodes[dID].get('mechanisms', {})
                    if name in mechs:
                        candidates.append(mechs[name])

            if len(candidates) > 1:
                raise MechanismCollisionError(
                    f"There are {len(candidates)} mechanisms named {name!r}"
                    f" in the search area ({len(searchIn)} decisions(s))."
                )
            elif len(candidates) == 1:
                return candidates[0]
            else:
                return None

        return namedMechanismFinder

    def lookupMechanism(
        self,
        startFrom: Union[
            base.AnyDecisionSpecifier,
            Collection[base.AnyDecisionSpecifier]
        ],
        name: base.MechanismName
    ) -> base.MechanismID:
        """
        Looks up the mechanism with the given name 'closest' to the
        given decision or set of decisions. First it looks for a
        mechanism with that name that's at one of those decisions. Then
        it starts looking in level-0 zones which contain any of them,
        then in level-1 zones, and so on. If it finds two mechanisms
        with the target name during the same search pass, it raises a
        `MechanismCollisionError`, but if it finds one it returns it.
        Raises a `MissingMechanismError` if there is no mechanisms with
        that name among global mechanisms (searched after the last
        applicable level of zones) or anywhere in the graph (which is the
        final level of search after checking global mechanisms).

        For example:

        >>> d = DecisionGraph()
        >>> d.addDecision('A')
        0
        >>> d.addDecision('B')
        1
        >>> d.addDecision('C')
        2
        >>> d.addDecision('D')
        3
        >>> d.addDecision('E')
        4
        >>> d.addMechanism('switch', 'A')
        0
        >>> d.addMechanism('switch', 'B')
        1
        >>> d.addMechanism('switch', 'C')
        2
        >>> d.addMechanism('lever', 'D')
        3
        >>> d.addMechanism('lever', None)  # global
        4
        >>> d.createZone('Z1', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.createZone('Z2', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> d.createZone('Zup', 1)
        ZoneInfo(level=1, parents=set(), contents=set())
        >>> d.addDecisionToZone('A', 'Z1')
        >>> d.addDecisionToZone('B', 'Z1')
        >>> d.addDecisionToZone('C', 'Z2')
        >>> d.addDecisionToZone('D', 'Z2')
        >>> d.addDecisionToZone('E', 'Z1')
        >>> d.addZoneToZone('Z1', 'Zup')
        >>> d.addZoneToZone('Z2', 'Zup')
        >>> d.lookupMechanism(set(), 'switch')  # 3x among all decisions
        Traceback (most recent call last):
        ...
        exploration.core.MechanismCollisionError...
        >>> d.lookupMechanism(set(), 'lever')  # 1x global > 1x all
        4
        >>> d.lookupMechanism({'D'}, 'lever')  # local
        3
        >>> d.lookupMechanism({'A'}, 'lever')  # found at D via Zup
        3
        >>> d.lookupMechanism({'A', 'D'}, 'lever')  # local again
        3
        >>> d.lookupMechanism({'A'}, 'switch')  # local
        0
        >>> d.lookupMechanism({'B'}, 'switch')  # local
        1
        >>> d.lookupMechanism({'C'}, 'switch')  # local
        2
        >>> d.lookupMechanism({'A', 'B'}, 'switch')  # ambiguous
        Traceback (most recent call last):
        ...
        exploration.core.MechanismCollisionError...
        >>> d.lookupMechanism({'A', 'B', 'C'}, 'switch')  # ambiguous
        Traceback (most recent call last):
        ...
        exploration.core.MechanismCollisionError...
        >>> d.lookupMechanism({'B', 'D'}, 'switch')  # not ambiguous
        1
        >>> d.lookupMechanism({'E', 'D'}, 'switch')  # ambiguous at L0 zone
        Traceback (most recent call last):
        ...
        exploration.core.MechanismCollisionError...
        >>> d.lookupMechanism({'E'}, 'switch')  # ambiguous at L0 zone
        Traceback (most recent call last):
        ...
        exploration.core.MechanismCollisionError...
        >>> d.lookupMechanism({'D'}, 'switch')  # found at L0 zone
        2
        """
        result = self.localLookup(
            startFrom,
            DecisionGraph.uniqueMechanismFinder(name)
        )
        if result is None:
            raise MissingMechanismError(
                f"No mechanism named {name!r}"
            )
        else:
            return result

    def resolveMechanism(
        self,
        specifier: base.AnyMechanismSpecifier,
        startFrom: Union[
            None,
            base.AnyDecisionSpecifier,
            Collection[base.AnyDecisionSpecifier]
        ] = None
    ) -> base.MechanismID:
        """
        Works like `lookupMechanism`, except it accepts a
        `base.AnyMechanismSpecifier` which may have position information
        baked in, and so the `startFrom` information is optional. If
        position information isn't specified in the mechanism specifier
        and startFrom is not provided, the mechanism is searched for at
        the global scope and then in the entire graph. On the other
        hand, if the specifier includes any position information, the
        startFrom value provided here will be ignored.
        """
        if isinstance(specifier, base.MechanismID):
            return specifier

        elif isinstance(specifier, base.MechanismName):
            if startFrom is None:
                startFrom = set()
            return self.lookupMechanism(startFrom, specifier)

        elif isinstance(specifier, tuple) and len(specifier) == 4:
            domain, zone, decision, mechanism = specifier
            if domain is None and zone is None and decision is None:
                if startFrom is None:
                    startFrom = set()
                return self.lookupMechanism(startFrom, mechanism)

            elif decision is not None:
                startFrom = {
                    self.resolveDecision(
                        base.DecisionSpecifier(domain, zone, decision)
                    )
                }
                return self.lookupMechanism(startFrom, mechanism)

            else:  # decision is None but domain and/or zone aren't
                startFrom = set()
                if zone is not None:
                    baseStart = self.allDecisionsInZone(zone)
                else:
                    baseStart = set(self)

                if domain is None:
                    startFrom = baseStart
                else:
                    for dID in baseStart:
                        if self.domainFor(dID) == domain:
                            startFrom.add(dID)
                return self.lookupMechanism(startFrom, mechanism)

        else:
            raise TypeError(
                f"Invalid mechanism specifier: {repr(specifier)}"
                f"\n(Must be a mechanism ID, mechanism name, or"
                f" mechanism specifier tuple)"
            )

    def walkConsequenceMechanisms(
        self,
        consequence: base.Consequence,
        searchFrom: Set[base.DecisionID]
    ) -> Generator[base.MechanismID, None, None]:
        """
        Yields each requirement in the given `base.Consequence`,
        including those in `base.Condition`s, `base.ConditionalSkill`s
        within `base.Challenge`s, and those set or toggled by
        `base.Effect`s. The `searchFrom` argument specifies where to
        start searching for mechanisms, since requirements include them
        by name, not by ID.
        """
        for part in base.walkParts(consequence):
            if isinstance(part, dict):
                if 'skills' in part:  # a Challenge
                    for cSkill in part['skills'].walk():
                        if isinstance(cSkill, base.ConditionalSkill):
                            yield from self.walkRequirementMechanisms(
                                cSkill.requirement,
                                searchFrom
                            )
                elif 'condition' in part:  # a Condition
                    yield from self.walkRequirementMechanisms(
                        part['condition'],
                        searchFrom
                    )
                elif 'value' in part:  # an Effect
                    val = part['value']
                    if part['type'] == 'set':
                        if (
                            isinstance(val, tuple)
                        and len(val) == 2
                        and isinstance(val[1], base.State)
                        ):
                            yield from self.walkRequirementMechanisms(
                                base.ReqMechanism(val[0], val[1]),
                                searchFrom
                            )
                    elif part['type'] == 'toggle':
                        if isinstance(val, tuple):
                            assert len(val) == 2
                            yield from self.walkRequirementMechanisms(
                                base.ReqMechanism(val[0], '_'),
                                  # state part is ignored here
                                searchFrom
                            )

    def walkRequirementMechanisms(
        self,
        req: base.Requirement,
        searchFrom: Set[base.DecisionID]
    ) -> Generator[base.MechanismID, None, None]:
        """
        Given a requirement, yields any mechanisms mentioned in that
        requirement, in depth-first traversal order.
        """
        for part in req.walk():
            if isinstance(part, base.ReqMechanism):
                mech = part.mechanism
                yield self.resolveMechanism(
                    mech,
                    startFrom=searchFrom
                )

    def addUnexploredEdge(
        self,
        fromDecision: base.AnyDecisionSpecifier,
        name: base.Transition,
        destinationName: Optional[base.DecisionName] = None,
        reciprocal: Optional[base.Transition] = 'return',
        toDomain: Optional[base.Domain] = None,
        placeInZone: Union[base.Zone, type[base.DefaultZone], None] = None,
        tags: Optional[Dict[base.Tag, base.TagValue]] = None,
        annotations: Optional[List[base.Annotation]] = None,
        revTags: Optional[Dict[base.Tag, base.TagValue]] = None,
        revAnnotations: Optional[List[base.Annotation]] = None,
        requires: Optional[base.Requirement] = None,
        consequence: Optional[base.Consequence] = None,
        revRequires: Optional[base.Requirement] = None,
        revConsequece: Optional[base.Consequence] = None
    ) -> base.DecisionID:
        """
        Adds a transition connecting to a new decision named `'_u.-n-'`
        where '-n-' is the number of unknown decisions (named or not)
        that have ever been created in this graph (or using the
        specified destination name if one is provided). This represents
        a transition to an unknown destination. The destination node
        gets tagged 'unconfirmed'.

        This also adds a reciprocal transition in the reverse direction,
        unless `reciprocal` is set to `None`. The reciprocal will use
        the provided name (default is 'return'). The new decision will
        be in the same domain as the decision it's connected to, unless
        `toDecision` is specified, in which case it will be in that
        domain.

        The new decision will not be placed into any zones, unless
        `placeInZone` is specified, in which case it will be placed into
        that zone. If that zone needs to be created, it will be created
        at level 0; in that case that zone will be added to any
        grandparent zones of the decision we're branching off of. If
        `placeInZone` is set to `base.DefaultZone`, then the new
        decision will be placed into each parent zone of the decision
        we're branching off of, as long as the new decision is in the
        same domain as the decision we're branching from (otherwise only
        an explicit `placeInZone` would apply).

        The ID of the decision that was created is returned.

        A `MissingDecisionError` will be raised if the starting decision
        does not exist, a `TransitionCollisionError` will be raised if
        it exists but already has a transition with the given name, and a
        `DecisionCollisionWarning` will be issued if a decision with the
        specified destination name already exists (won't happen when
        using an automatic name).

        Lists of tags and/or annotations (strings in both cases) may be
        provided. These may also be provided for the reciprocal edge.

        Similarly, requirements and/or consequences for either edge may
        be provided.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addUnexploredEdge('A', 'up')
        1
        >>> g.nameFor(1)
        '_u.0'
        >>> g.decisionTags(1)
        {'unconfirmed': 1}
        >>> g.addUnexploredEdge('A', 'right', 'B')
        2
        >>> g.nameFor(2)
        'B'
        >>> g.decisionTags(2)
        {'unconfirmed': 1}
        >>> g.addUnexploredEdge('A', 'down', None, 'up')
        3
        >>> g.nameFor(3)
        '_u.2'
        >>> g.addUnexploredEdge(
        ...    '_u.0',
        ...    'beyond',
        ...    toDomain='otherDomain',
        ...    tags={'fast':1},
        ...    revTags={'slow':1},
        ...    annotations=['comment'],
        ...    revAnnotations=['one', 'two'],
        ...    requires=base.ReqCapability('dash'),
        ...    revRequires=base.ReqCapability('super dash'),
        ...    consequence=[base.effect(gain='super dash')],
        ...    revConsequece=[base.effect(lose='super dash')]
        ... )
        4
        >>> g.nameFor(4)
        '_u.3'
        >>> g.domainFor(4)
        'otherDomain'
        >>> g.transitionTags('_u.0', 'beyond')
        {'fast': 1}
        >>> g.transitionAnnotations('_u.0', 'beyond')
        ['comment']
        >>> g.getTransitionRequirement('_u.0', 'beyond')
        ReqCapability('dash')
        >>> e = g.getConsequence('_u.0', 'beyond')
        >>> e == [base.effect(gain='super dash')]
        True
        >>> g.transitionTags('_u.3', 'return')
        {'slow': 1}
        >>> g.transitionAnnotations('_u.3', 'return')
        ['one', 'two']
        >>> g.getTransitionRequirement('_u.3', 'return')
        ReqCapability('super dash')
        >>> e = g.getConsequence('_u.3', 'return')
        >>> e == [base.effect(lose='super dash')]
        True
        """
        # Defaults
        if tags is None:
            tags = {}
        if annotations is None:
            annotations = []
        if revTags is None:
            revTags = {}
        if revAnnotations is None:
            revAnnotations = []

        # Resolve ID
        fromID = self.resolveDecision(fromDecision)
        if toDomain is None:
            toDomain = self.domainFor(fromID)

        if name in self.destinationsFrom(fromID):
            raise TransitionCollisionError(
                f"Cannot add a new edge {name!r}:"
                f" {self.identityOf(fromDecision)} already has an"
                f" outgoing edge with that name."
            )

        if destinationName in self.nameLookup and WARN_OF_NAME_COLLISIONS:
            warnings.warn(
                (
                    f"Cannot add a new unexplored node"
                    f" {destinationName!r}: A decision with that name"
                    f" already exists.\n(Leave destinationName as None"
                    f" to use an automatic name.)"
                ),
                DecisionCollisionWarning
            )

        # Create the new unexplored decision and add the edge
        if destinationName is None:
            toName = '_u.' + str(self.unknownCount)
        else:
            toName = destinationName
        self.unknownCount += 1
        newID = self.addDecision(toName, domain=toDomain)
        self.addTransition(
            fromID,
            name,
            newID,
            tags=tags,
            annotations=annotations
        )
        self.setTransitionRequirement(fromID, name, requires)
        if consequence is not None:
            self.setConsequence(fromID, name, consequence)

        # Add it to a zone if requested
        if (
            placeInZone is base.DefaultZone
        and toDomain == self.domainFor(fromID)
        ):
            # Add to each parent of the from decision
            for parent in self.zoneParents(fromID):
                self.addDecisionToZone(newID, parent)
        elif placeInZone is not None:
            # Otherwise add it to one specific zone, creating that zone
            # at level 0 if necessary
            assert isinstance(placeInZone, base.Zone)
            if self.getZoneInfo(placeInZone) is None:
                self.createZone(placeInZone, 0)
                # Add new zone to each grandparent of the from decision
                for parent in self.zoneParents(fromID):
                    for grandparent in self.zoneParents(parent):
                        self.addZoneToZone(placeInZone, grandparent)
            self.addDecisionToZone(newID, placeInZone)

        # Create the reciprocal edge
        if reciprocal is not None:
            self.addTransition(
                newID,
                reciprocal,
                fromID,
                tags=revTags,
                annotations=revAnnotations
            )
            self.setTransitionRequirement(newID, reciprocal, revRequires)
            if revConsequece is not None:
                self.setConsequence(newID, reciprocal, revConsequece)
            # Set as a reciprocal
            self.setReciprocal(fromID, name, reciprocal)

        # Tag the destination as 'unconfirmed'
        self.tagDecision(newID, 'unconfirmed')

        # Return ID of new destination
        return newID

    def retargetTransition(
        self,
        fromDecision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        newDestination: base.AnyDecisionSpecifier,
        swapReciprocal=True,
        errorOnNameColision=True
    ) -> Optional[base.Transition]:
        """
        Given a particular decision and a transition at that decision,
        changes that transition so that it goes to the specified new
        destination instead of wherever it was connected to before. If
        the new destination is the same as the old one, no changes are
        made.

        If `swapReciprocal` is set to True (the default) then any
        reciprocal edge at the old destination will be deleted, and a
        new reciprocal edge from the new destination with equivalent
        properties to the original reciprocal will be created, pointing
        to the origin of the specified transition. If `swapReciprocal`
        is set to False, then the reciprocal relationship with any old
        reciprocal edge will be removed, but the old reciprocal edge
        will not be changed.

        Note that if `errorOnNameColision` is True (the default), then
        if the reciprocal transition has the same name as a transition
        which already exists at the new destination node, a
        `TransitionCollisionError` will be thrown. However, if it is set
        to False, the reciprocal transition will be renamed with a suffix
        to avoid any possible name collisions. Either way, the name of
        the reciprocal transition (possibly just changed) will be
        returned, or None if there was no reciprocal transition.

        ## Example

        >>> g = DecisionGraph()
        >>> for fr, to, nm in [
        ...     ('A', 'B', 'up'),
        ...     ('A', 'B', 'up2'),
        ...     ('B', 'A', 'down'),
        ...     ('B', 'B', 'self'),
        ...     ('B', 'C', 'next'),
        ...     ('C', 'B', 'prev')
        ... ]:
        ...     if g.getDecision(fr) is None:
        ...        g.addDecision(fr)
        ...     if g.getDecision(to) is None:
        ...         g.addDecision(to)
        ...     g.addTransition(fr, nm, to)
        0
        1
        2
        >>> g.setReciprocal('A', 'up', 'down')
        >>> g.setReciprocal('B', 'next', 'prev')
        >>> g.destination('A', 'up')
        1
        >>> g.destination('B', 'down')
        0
        >>> g.retargetTransition('A', 'up', 'C')
        'down'
        >>> g.destination('A', 'up')
        2
        >>> g.getDestination('B', 'down') is None
        True
        >>> g.destination('C', 'down')
        0
        >>> g.addTransition('A', 'next', 'B')
        >>> g.addTransition('B', 'prev', 'A')
        >>> g.setReciprocal('A', 'next', 'prev')
        >>> # Can't swap a reciprocal in a way that would collide names
        >>> g.getReciprocal('C', 'prev')
        'next'
        >>> g.retargetTransition('C', 'prev', 'A')
        Traceback (most recent call last):
        ...
        exploration.core.TransitionCollisionError...
        >>> g.retargetTransition('C', 'prev', 'A', swapReciprocal=False)
        'next'
        >>> g.destination('C', 'prev')
        0
        >>> g.destination('A', 'next') # not changed
        1
        >>> # Reciprocal relationship is severed:
        >>> g.getReciprocal('C', 'prev') is None
        True
        >>> g.getReciprocal('B', 'next') is None
        True
        >>> # Swap back so we can do another demo
        >>> g.retargetTransition('C', 'prev', 'B', swapReciprocal=False)
        >>> # Note return value was None here because there was no reciprocal
        >>> g.setReciprocal('C', 'prev', 'next')
        >>> # Swap reciprocal by renaming it
        >>> g.retargetTransition('C', 'prev', 'A', errorOnNameColision=False)
        'next.1'
        >>> g.getReciprocal('C', 'prev')
        'next.1'
        >>> g.destination('C', 'prev')
        0
        >>> g.destination('A', 'next.1')
        2
        >>> g.destination('A', 'next')
        1
        >>> # Note names are the same but these are from different nodes
        >>> g.getReciprocal('A', 'next')
        'prev'
        >>> g.getReciprocal('A', 'next.1')
        'prev'
        """
        fromID = self.resolveDecision(fromDecision)
        newDestID = self.resolveDecision(newDestination)

        # Figure out the old destination of the transition we're swapping
        oldDestID = self.destination(fromID, transition)
        reciprocal = self.getReciprocal(fromID, transition)

        # If thew new destination is the same, we don't do anything!
        if oldDestID == newDestID:
            return reciprocal

        # First figure out reciprocal business so we can error out
        # without making changes if we need to
        if swapReciprocal and reciprocal is not None:
            reciprocal = self.rebaseTransition(
                oldDestID,
                reciprocal,
                newDestID,
                swapReciprocal=False,
                errorOnNameColision=errorOnNameColision
            )

        # Handle the forward transition...
        # Find the transition properties
        tProps = self.getTransitionProperties(fromID, transition)

        # Delete the edge
        self.removeEdgeByKey(fromID, transition)

        # Add the new edge
        self.addTransition(fromID, transition, newDestID)

        # Reapply the transition properties
        self.setTransitionProperties(fromID, transition, **tProps)

        # Handle the reciprocal transition if there is one...
        if reciprocal is not None:
            if not swapReciprocal:
                # Then sever the relationship, but only if that edge
                # still exists (we might be in the middle of a rebase)
                check = self.getDestination(oldDestID, reciprocal)
                if check is not None:
                    self.setReciprocal(
                        oldDestID,
                        reciprocal,
                        None,
                        setBoth=False # Other transition was deleted already
                    )
            else:
                # Establish new reciprocal relationship
                self.setReciprocal(
                    fromID,
                    transition,
                    reciprocal
                )

        return reciprocal

    def rebaseTransition(
        self,
        fromDecision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        newBase: base.AnyDecisionSpecifier,
        swapReciprocal=True,
        errorOnNameColision=True
    ) -> base.Transition:
        """
        Given a particular destination and a transition at that
        destination, changes that transition's origin to a new base
        decision. If the new source is the same as the old one, no
        changes are made.

        If `swapReciprocal` is set to True (the default) then any
        reciprocal edge at the destination will be retargeted to point
        to the new source so that it can remain a reciprocal. If
        `swapReciprocal` is set to False, then the reciprocal
        relationship with any old reciprocal edge will be removed, but
        the old reciprocal edge will not be otherwise changed.

        Note that if `errorOnNameColision` is True (the default), then
        if the transition has the same name as a transition which
        already exists at the new source node, a
        `TransitionCollisionError` will be raised. However, if it is set
        to False, the transition will be renamed with a suffix to avoid
        any possible name collisions. Either way, the (possibly new) name
        of the transition that was rebased will be returned.

        ## Example

        >>> g = DecisionGraph()
        >>> for fr, to, nm in [
        ...     ('A', 'B', 'up'),
        ...     ('A', 'B', 'up2'),
        ...     ('B', 'A', 'down'),
        ...     ('B', 'B', 'self'),
        ...     ('B', 'C', 'next'),
        ...     ('C', 'B', 'prev')
        ... ]:
        ...     if g.getDecision(fr) is None:
        ...        g.addDecision(fr)
        ...     if g.getDecision(to) is None:
        ...         g.addDecision(to)
        ...     g.addTransition(fr, nm, to)
        0
        1
        2
        >>> g.setReciprocal('A', 'up', 'down')
        >>> g.setReciprocal('B', 'next', 'prev')
        >>> g.destination('A', 'up')
        1
        >>> g.destination('B', 'down')
        0
        >>> g.rebaseTransition('B', 'down', 'C')
        'down'
        >>> g.destination('A', 'up')
        2
        >>> g.getDestination('B', 'down') is None
        True
        >>> g.destination('C', 'down')
        0
        >>> g.addTransition('A', 'next', 'B')
        >>> g.addTransition('B', 'prev', 'A')
        >>> g.setReciprocal('A', 'next', 'prev')
        >>> # Can't rebase in a way that would collide names
        >>> g.rebaseTransition('B', 'next', 'A')
        Traceback (most recent call last):
        ...
        exploration.core.TransitionCollisionError...
        >>> g.rebaseTransition('B', 'next', 'A', errorOnNameColision=False)
        'next.1'
        >>> g.destination('C', 'prev')
        0
        >>> g.destination('A', 'next') # not changed
        1
        >>> # Collision is avoided by renaming
        >>> g.destination('A', 'next.1')
        2
        >>> # Swap without reciprocal
        >>> g.getReciprocal('A', 'next.1')
        'prev'
        >>> g.getReciprocal('C', 'prev')
        'next.1'
        >>> g.rebaseTransition('A', 'next.1', 'B', swapReciprocal=False)
        'next.1'
        >>> g.getReciprocal('C', 'prev') is None
        True
        >>> g.destination('C', 'prev')
        0
        >>> g.getDestination('A', 'next.1') is None
        True
        >>> g.destination('A', 'next')
        1
        >>> g.destination('B', 'next.1')
        2
        >>> g.getReciprocal('B', 'next.1') is None
        True
        >>> # Rebase in a way that creates a self-edge
        >>> g.rebaseTransition('A', 'next', 'B')
        'next'
        >>> g.getDestination('A', 'next') is None
        True
        >>> g.destination('B', 'next')
        1
        >>> g.destination('B', 'prev') # swapped as a reciprocal
        1
        >>> g.getReciprocal('B', 'next') # still reciprocals
        'prev'
        >>> g.getReciprocal('B', 'prev')
        'next'
        >>> # And rebasing of a self-edge also works
        >>> g.rebaseTransition('B', 'prev', 'A')
        'prev'
        >>> g.destination('A', 'prev')
        1
        >>> g.destination('B', 'next')
        0
        >>> g.getReciprocal('B', 'next') # still reciprocals
        'prev'
        >>> g.getReciprocal('A', 'prev')
        'next'
        >>> # We've effectively reversed this edge/reciprocal pair
        >>> # by rebasing twice
        """
        fromID = self.resolveDecision(fromDecision)
        newBaseID = self.resolveDecision(newBase)

        # If thew new base is the same, we don't do anything!
        if newBaseID == fromID:
            return transition

        # First figure out reciprocal business so we can swap it later
        # without making changes if we need to
        destination = self.destination(fromID, transition)
        reciprocal = self.getReciprocal(fromID, transition)
        # Check for an already-deleted reciprocal
        if (
            reciprocal is not None
        and self.getDestination(destination, reciprocal) is None
        ):
            reciprocal = None

        # Handle the base swap...
        # Find the transition properties
        tProps = self.getTransitionProperties(fromID, transition)

        # Check for a collision
        targetDestinations = self.destinationsFrom(newBaseID)
        if transition in targetDestinations:
            if errorOnNameColision:
                raise TransitionCollisionError(
                    f"Cannot rebase transition {transition!r} from"
                    f" {self.identityOf(fromDecision)}: it would be a"
                    f" duplicate transition name at the new base"
                    f" decision {self.identityOf(newBase)}."
                )
            else:
                # Figure out a good fresh name
                newName = utils.uniqueName(
                    transition,
                    targetDestinations
                )
        else:
            newName = transition

        # Delete the edge
        self.removeEdgeByKey(fromID, transition)

        # Add the new edge
        self.addTransition(newBaseID, newName, destination)

        # Reapply the transition properties
        self.setTransitionProperties(newBaseID, newName, **tProps)

        # Handle the reciprocal transition if there is one...
        if reciprocal is not None:
            if not swapReciprocal:
                # Then sever the relationship
                self.setReciprocal(
                    destination,
                    reciprocal,
                    None,
                    setBoth=False # Other transition was deleted already
                )
            else:
                # Otherwise swap the reciprocal edge
                self.retargetTransition(
                    destination,
                    reciprocal,
                    newBaseID,
                    swapReciprocal=False
                )

                # And establish a new reciprocal relationship
                self.setReciprocal(
                    newBaseID,
                    newName,
                    reciprocal
                )

        # Return the new name in case it was changed
        return newName

    # TODO: zone merging!

    # TODO: Double-check that exploration vars get updated when this is
    # called!
    def mergeDecisions(
        self,
        merge: base.AnyDecisionSpecifier,
        mergeInto: base.AnyDecisionSpecifier,
        errorOnNameColision=True
    ) -> Dict[base.Transition, base.Transition]:
        """
        Merges two decisions, deleting the first after transferring all
        of its incoming and outgoing edges to target the second one,
        whose name is retained. The second decision will be added to any
        zones that the first decision was a member of. If either decision
        does not exist, a `MissingDecisionError` will be raised. If
        `merge` and `mergeInto` are the same, then nothing will be
        changed.

        Unless `errorOnNameColision` is set to False, a
        `TransitionCollisionError` will be raised if the two decisions
        have outgoing transitions with the same name. If
        `errorOnNameColision` is set to False, then such edges will be
        renamed using a suffix to avoid name collisions, with edges
        connected to the second decision retaining their original names
        and edges that were connected to the first decision getting
        renamed.

        Any mechanisms located at the first decision will be moved to the
        merged decision.

        The tags and annotations of the merged decision are added to the
        tags and annotations of the merge target. If there are shared
        tags, the values from the merge target will override those of
        the merged decision. If this is undesired behavior, clear/edit
        the tags/annotations of the merged decision before the merge.

        The 'unconfirmed' tag is treated specially: if both decisions have
        it it will be retained, but otherwise it will be dropped even if
        one of the situations had it before.

        The domain of the second decision is retained.

        Returns a dictionary mapping each original transition name to
        its new name in cases where transitions get renamed; this will
        be empty when no re-naming occurs, including when
        `errorOnNameColision` is True. If there were any transitions
        connecting the nodes that were merged, these become self-edges
        of the merged node (and may be renamed if necessary).
        Note that all renamed transitions were originally based on the
        first (merged) node, since transitions of the second (merge
        target) node are not renamed.

        ## Example

        >>> g = DecisionGraph()
        >>> for fr, to, nm in [
        ...     ('A', 'B', 'up'),
        ...     ('A', 'B', 'up2'),
        ...     ('B', 'A', 'down'),
        ...     ('B', 'B', 'self'),
        ...     ('B', 'C', 'next'),
        ...     ('C', 'B', 'prev'),
        ...     ('A', 'C', 'right')
        ... ]:
        ...     if g.getDecision(fr) is None:
        ...        g.addDecision(fr)
        ...     if g.getDecision(to) is None:
        ...         g.addDecision(to)
        ...     g.addTransition(fr, nm, to)
        0
        1
        2
        >>> g.getDestination('A', 'up')
        1
        >>> g.getDestination('B', 'down')
        0
        >>> sorted(g)
        [0, 1, 2]
        >>> g.setReciprocal('A', 'up', 'down')
        >>> g.setReciprocal('B', 'next', 'prev')
        >>> g.mergeDecisions('C', 'B')
        {}
        >>> g.destinationsFrom('A')
        {'up': 1, 'up2': 1, 'right': 1}
        >>> g.destinationsFrom('B')
        {'down': 0, 'self': 1, 'prev': 1, 'next': 1}
        >>> 'C' in g
        False
        >>> g.mergeDecisions('A', 'A') # does nothing
        {}
        >>> # Can't merge non-existent decision
        >>> g.mergeDecisions('A', 'Z')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        >>> g.mergeDecisions('Z', 'A')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        >>> # Can't merge decisions w/ shared edge names
        >>> g.addDecision('D')
        3
        >>> g.addTransition('D', 'next', 'A')
        >>> g.addTransition('A', 'prev', 'D')
        >>> g.setReciprocal('D', 'next', 'prev')
        >>> g.mergeDecisions('D', 'B') # both have a 'next' transition
        Traceback (most recent call last):
        ...
        exploration.core.TransitionCollisionError...
        >>> # Auto-rename colliding edges
        >>> g.mergeDecisions('D', 'B', errorOnNameColision=False)
        {'next': 'next.1'}
        >>> g.destination('B', 'next') # merge target unchanged
        1
        >>> g.destination('B', 'next.1') # merged decision name changed
        0
        >>> g.destination('B', 'prev') # name unchanged (no collision)
        1
        >>> g.getReciprocal('B', 'next') # unchanged (from B)
        'prev'
        >>> g.getReciprocal('B', 'next.1') # from A
        'prev'
        >>> g.getReciprocal('A', 'prev') # from B
        'next.1'

        ## Folding four nodes into a 2-node loop

        >>> g = DecisionGraph()
        >>> g.addDecision('X')
        0
        >>> g.addDecision('Y')
        1
        >>> g.addTransition('X', 'next', 'Y', 'prev')
        >>> g.addDecision('preX')
        2
        >>> g.addDecision('postY')
        3
        >>> g.addTransition('preX', 'next', 'X', 'prev')
        >>> g.addTransition('Y', 'next', 'postY', 'prev')
        >>> g.mergeDecisions('preX', 'Y', errorOnNameColision=False)
        {'next': 'next.1'}
        >>> g.destinationsFrom('X')
        {'next': 1, 'prev': 1}
        >>> g.destinationsFrom('Y')
        {'prev': 0, 'next': 3, 'next.1': 0}
        >>> 2 in g
        False
        >>> g.destinationsFrom('postY')
        {'prev': 1}
        >>> g.mergeDecisions('postY', 'X', errorOnNameColision=False)
        {'prev': 'prev.1'}
        >>> g.destinationsFrom('X')
        {'next': 1, 'prev': 1, 'prev.1': 1}
        >>> g.destinationsFrom('Y') # order 'cause of 'next' re-target
        {'prev': 0, 'next.1': 0, 'next': 0}
        >>> 2 in g
        False
        >>> 3 in g
        False
        >>> # Reciprocals are tangled...
        >>> g.getReciprocal(0, 'prev')
        'next.1'
        >>> g.getReciprocal(0, 'prev.1')
        'next'
        >>> g.getReciprocal(1, 'next')
        'prev.1'
        >>> g.getReciprocal(1, 'next.1')
        'prev'
        >>> # Note: one merge cannot handle both extra transitions
        >>> # because their reciprocals are crossed (e.g., prev.1 <-> next)
        >>> # (It would merge both edges but the result would retain
        >>> # 'next.1' instead of retaining 'next'.)
        >>> g.mergeTransitions('X', 'prev.1', 'prev', mergeReciprocal=False)
        >>> g.mergeTransitions('Y', 'next.1', 'next', mergeReciprocal=True)
        >>> g.destinationsFrom('X')
        {'next': 1, 'prev': 1}
        >>> g.destinationsFrom('Y')
        {'prev': 0, 'next': 0}
        >>> # Reciprocals were salvaged in second merger
        >>> g.getReciprocal('X', 'prev')
        'next'
        >>> g.getReciprocal('Y', 'next')
        'prev'

        ## Merging with tags/requirements/annotations/consequences

        >>> g = DecisionGraph()
        >>> g.addDecision('X')
        0
        >>> g.addDecision('Y')
        1
        >>> g.addDecision('Z')
        2
        >>> g.addTransition('X', 'next', 'Y', 'prev')
        >>> g.addTransition('X', 'down', 'Z', 'up')
        >>> g.tagDecision('X', 'tag0', 1)
        >>> g.tagDecision('Y', 'tag1', 10)
        >>> g.tagDecision('Y', 'unconfirmed')
        >>> g.tagDecision('Z', 'tag1', 20)
        >>> g.tagDecision('Z', 'tag2', 30)
        >>> g.tagTransition('X', 'next', 'ttag1', 11)
        >>> g.tagTransition('Y', 'prev', 'ttag2', 22)
        >>> g.tagTransition('X', 'down', 'ttag3', 33)
        >>> g.tagTransition('Z', 'up', 'ttag4', 44)
        >>> g.annotateDecision('Y', 'annotation 1')
        >>> g.annotateDecision('Z', 'annotation 2')
        >>> g.annotateDecision('Z', 'annotation 3')
        >>> g.annotateTransition('Y', 'prev', 'trans annotation 1')
        >>> g.annotateTransition('Y', 'prev', 'trans annotation 2')
        >>> g.annotateTransition('Z', 'up', 'trans annotation 3')
        >>> g.setTransitionRequirement(
        ...     'X',
        ...     'next',
        ...     base.ReqCapability('power')
        ... )
        >>> g.setTransitionRequirement(
        ...     'Y',
        ...     'prev',
        ...     base.ReqTokens('token', 1)
        ... )
        >>> g.setTransitionRequirement(
        ...     'X',
        ...     'down',
        ...     base.ReqCapability('power2')
        ... )
        >>> g.setTransitionRequirement(
        ...     'Z',
        ...     'up',
        ...     base.ReqTokens('token2', 2)
        ... )
        >>> g.setConsequence(
        ...     'Y',
        ...     'prev',
        ...     [base.effect(gain="power2")]
        ... )
        >>> g.mergeDecisions('Y', 'Z')
        {}
        >>> g.destination('X', 'next')
        2
        >>> g.destination('X', 'down')
        2
        >>> g.destination('Z', 'prev')
        0
        >>> g.destination('Z', 'up')
        0
        >>> g.decisionTags('X')
        {'tag0': 1}
        >>> g.decisionTags('Z')  # note that 'unconfirmed' is removed
        {'tag1': 20, 'tag2': 30}
        >>> g.transitionTags('X', 'next')
        {'ttag1': 11}
        >>> g.transitionTags('X', 'down')
        {'ttag3': 33}
        >>> g.transitionTags('Z', 'prev')
        {'ttag2': 22}
        >>> g.transitionTags('Z', 'up')
        {'ttag4': 44}
        >>> g.decisionAnnotations('Z')
        ['annotation 2', 'annotation 3', 'annotation 1']
        >>> g.transitionAnnotations('Z', 'prev')
        ['trans annotation 1', 'trans annotation 2']
        >>> g.transitionAnnotations('Z', 'up')
        ['trans annotation 3']
        >>> g.getTransitionRequirement('X', 'next')
        ReqCapability('power')
        >>> g.getTransitionRequirement('Z', 'prev')
        ReqTokens('token', 1)
        >>> g.getTransitionRequirement('X', 'down')
        ReqCapability('power2')
        >>> g.getTransitionRequirement('Z', 'up')
        ReqTokens('token2', 2)
        >>> g.getConsequence('Z', 'prev') == [
        ...     {
        ...         'type': 'gain',
        ...         'applyTo': 'active',
        ...         'value': 'power2',
        ...         'charges': None,
        ...         'delay': None,
        ...         'hidden': False
        ...     }
        ... ]
        True

        ## Merging into node without tags

        >>> g = DecisionGraph()
        >>> g.addDecision('X')
        0
        >>> g.addDecision('Y')
        1
        >>> g.tagDecision('Y', 'unconfirmed')  # special handling
        >>> g.tagDecision('Y', 'tag', 'value')
        >>> g.mergeDecisions('Y', 'X')
        {}
        >>> g.decisionTags('X')
        {'tag': 'value'}
        >>> 0 in g  # Second argument remains
        True
        >>> 1 in g  # First argument is deleted
        False
        """
        # Resolve IDs
        mergeID = self.resolveDecision(merge)
        mergeIntoID = self.resolveDecision(mergeInto)

        # Create our result as an empty dictionary
        result: Dict[base.Transition, base.Transition] = {}

        # Short-circuit if the two decisions are the same
        if mergeID == mergeIntoID:
            return result

        # MissingDecisionErrors from here if either doesn't exist
        allNewOutgoing = set(self.destinationsFrom(mergeID))
        allOldOutgoing = set(self.destinationsFrom(mergeIntoID))
        # Find colliding transition names
        collisions = allNewOutgoing & allOldOutgoing
        if len(collisions) > 0 and errorOnNameColision:
            raise TransitionCollisionError(
                f"Cannot merge decision {self.identityOf(merge)} into"
                f" decision {self.identityOf(mergeInto)}: the decisions"
                f" share {len(collisions)} transition names:"
                f" {collisions}\n(Note that errorOnNameColision was set"
                f" to True, set it to False to allow the operation by"
                f" renaming half of those transitions.)"
            )

        # Record zones that will have to change after the merge
        zoneParents = self.zoneParents(mergeID)

        # First, swap all incoming edges, along with their reciprocals
        # This will include self-edges, which will be retargeted and
        # whose reciprocals will be rebased in the process, leading to
        # the possibility of a missing edge during the loop
        for source, incoming in self.allEdgesTo(mergeID):
            # Skip this edge if it was already swapped away because it's
            # a self-loop with a reciprocal whose reciprocal was
            # processed earlier in the loop
            if incoming not in self.destinationsFrom(source):
                continue

            # Find corresponding outgoing edge
            outgoing = self.getReciprocal(source, incoming)

            # Swap both edges to new destination
            newOutgoing = self.retargetTransition(
                source,
                incoming,
                mergeIntoID,
                swapReciprocal=True,
                errorOnNameColision=False # collisions were detected above
            )
            # Add to our result if the name of the reciprocal was
            # changed
            if (
                outgoing is not None
            and newOutgoing is not None
            and outgoing != newOutgoing
            ):
                result[outgoing] = newOutgoing

        # Next, swap any remaining outgoing edges (which didn't have
        # reciprocals, or they'd already be swapped, unless they were
        # self-edges previously). Note that in this loop, there can't be
        # any self-edges remaining, although there might be connections
        # between the merging nodes that need to become self-edges
        # because they used to be a self-edge that was half-retargeted
        # by the previous loop.
        # Note: a copy is used here to avoid iterating over a changing
        # dictionary
        for stillOutgoing in copy.copy(self.destinationsFrom(mergeID)):
            newOutgoing = self.rebaseTransition(
                mergeID,
                stillOutgoing,
                mergeIntoID,
                swapReciprocal=True,
                errorOnNameColision=False # collisions were detected above
            )
            if stillOutgoing != newOutgoing:
                result[stillOutgoing] = newOutgoing

        # At this point, there shouldn't be any remaining incoming or
        # outgoing edges!
        assert self.degree(mergeID) == 0

        # Merge tags & annotations
        # Note that these operations affect the underlying graph
        destTags = self.decisionTags(mergeIntoID)
        destUnvisited = 'unconfirmed' in destTags
        sourceTags = self.decisionTags(mergeID)
        sourceUnvisited = 'unconfirmed' in sourceTags
        # Copy over only new tags, leaving existing tags alone
        for key in sourceTags:
            if key not in destTags:
                destTags[key] = sourceTags[key]

        if int(destUnvisited) + int(sourceUnvisited) == 1:
            del destTags['unconfirmed']

        self.decisionAnnotations(mergeIntoID).extend(
            self.decisionAnnotations(mergeID)
        )

        # Transfer zones
        for zone in zoneParents:
            self.addDecisionToZone(mergeIntoID, zone)

        # Delete the old node
        self.removeDecision(mergeID)

        return result

    def removeDecision(self, decision: base.AnyDecisionSpecifier) -> None:
        """
        Deletes the specified decision from the graph, updating
        attendant structures like zones. Note that the ID of the deleted
        node will NOT be reused, unless it's specifically provided to
        `addIdentifiedDecision`.

        For example:

        >>> dg = DecisionGraph()
        >>> dg.addDecision('A')
        0
        >>> dg.addDecision('B')
        1
        >>> list(dg)
        [0, 1]
        >>> 1 in dg
        True
        >>> 'B' in dg.nameLookup
        True
        >>> dg.removeDecision('B')
        >>> 1 in dg
        False
        >>> list(dg)
        [0]
        >>> 'B' in dg.nameLookup
        False
        >>> dg.addDecision('C')  # doesn't re-use ID
        2
        """
        dID = self.resolveDecision(decision)

        # Remove the target from all zones:
        for zone in self.zones:
            self.removeDecisionFromZone(dID, zone)

        # Remove the node but record the current name
        name = self.nodes[dID]['name']
        self.remove_node(dID)

        # Clean up the nameLookup entry
        luInfo = self.nameLookup[name]
        luInfo.remove(dID)
        if len(luInfo) == 0:
            self.nameLookup.pop(name)

        # TODO: Clean up edges?

    def renameDecision(
        self,
        decision: base.AnyDecisionSpecifier,
        newName: base.DecisionName
    ):
        """
        Renames a decision. The decision retains its old ID.

        Generates a `DecisionCollisionWarning` if a decision using the new
        name already exists and `WARN_OF_NAME_COLLISIONS` is enabled.

        Example:

        >>> g = DecisionGraph()
        >>> g.addDecision('one')
        0
        >>> g.addDecision('three')
        1
        >>> g.addTransition('one', '>', 'three')
        >>> g.addTransition('three', '<', 'one')
        >>> g.tagDecision('three', 'hi')
        >>> g.annotateDecision('three', 'note')
        >>> g.destination('one', '>')
        1
        >>> g.destination('three', '<')
        0
        >>> g.renameDecision('three', 'two')
        >>> g.resolveDecision('one')
        0
        >>> g.resolveDecision('two')
        1
        >>> g.resolveDecision('three')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        >>> g.destination('one', '>')
        1
        >>> g.nameFor(1)
        'two'
        >>> g.getDecision('three') is None
        True
        >>> g.destination('two', '<')
        0
        >>> g.decisionTags('two')
        {'hi': 1}
        >>> g.decisionAnnotations('two')
        ['note']
        """
        dID = self.resolveDecision(decision)

        if newName in self.nameLookup and WARN_OF_NAME_COLLISIONS:
            warnings.warn(
                (
                    f"Can't rename {self.identityOf(decision)} as"
                    f" {newName!r} because a decision with that name"
                    f" already exists."
                ),
                DecisionCollisionWarning
            )

        # Update name in node
        oldName = self.nodes[dID]['name']
        self.nodes[dID]['name'] = newName

        # Update nameLookup entries
        oldNL = self.nameLookup[oldName]
        oldNL.remove(dID)
        if len(oldNL) == 0:
            self.nameLookup.pop(oldName)
        self.nameLookup.setdefault(newName, []).append(dID)

    def mergeTransitions(
        self,
        fromDecision: base.AnyDecisionSpecifier,
        merge: base.Transition,
        mergeInto: base.Transition,
        mergeReciprocal=True
    ) -> None:
        """
        Given a decision and two transitions that start at that decision,
        merges the first transition into the second transition, combining
        their transition properties (using `mergeProperties`) and
        deleting the first transition. By default any reciprocal of the
        first transition is also merged into the reciprocal of the
        second, although you can set `mergeReciprocal` to `False` to
        disable this in which case the old reciprocal will lose its
        reciprocal relationship, even if the transition that was merged
        into does not have a reciprocal.

        If the two names provided are the same, nothing will happen.

        If the two transitions do not share the same destination, they
        cannot be merged, and an `InvalidDestinationError` will result.
        Use `retargetTransition` beforehand to ensure that they do if you
        want to merge transitions with different destinations.

        A `MissingDecisionError` or `MissingTransitionError` will result
        if the decision or either transition does not exist.

        If merging reciprocal properties was requested and the first
        transition does not have a reciprocal, then no reciprocal
        properties change. However, if the second transition does not
        have a reciprocal and the first does, the first transition's
        reciprocal will be set to the reciprocal of the second
        transition, and that transition will not be deleted as usual.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addDecision('B')
        1
        >>> g.addTransition('A', 'up', 'B')
        >>> g.addTransition('B', 'down', 'A')
        >>> g.setReciprocal('A', 'up', 'down')
        >>> # Merging a transition with no reciprocal
        >>> g.addTransition('A', 'up2', 'B')
        >>> g.mergeTransitions('A', 'up2', 'up')
        >>> g.getDestination('A', 'up2') is None
        True
        >>> g.getDestination('A', 'up')
        1
        >>> # Merging a transition with a reciprocal & tags
        >>> g.addTransition('A', 'up2', 'B')
        >>> g.addTransition('B', 'down2', 'A')
        >>> g.setReciprocal('A', 'up2', 'down2')
        >>> g.tagTransition('A', 'up2', 'one')
        >>> g.tagTransition('B', 'down2', 'two')
        >>> g.mergeTransitions('B', 'down2', 'down')
        >>> g.getDestination('A', 'up2') is None
        True
        >>> g.getDestination('A', 'up')
        1
        >>> g.getDestination('B', 'down2') is None
        True
        >>> g.getDestination('B', 'down')
        0
        >>> # Merging requirements uses ReqAll (i.e., 'and' logic)
        >>> g.addTransition('A', 'up2', 'B')
        >>> g.setTransitionProperties(
        ...     'A',
        ...     'up2',
        ...     requirement=base.ReqCapability('dash')
        ... )
        >>> g.setTransitionProperties('A', 'up',
        ...     requirement=base.ReqCapability('slide'))
        >>> g.mergeTransitions('A', 'up2', 'up')
        >>> g.getDestination('A', 'up2') is None
        True
        >>> repr(g.getTransitionRequirement('A', 'up'))
        "ReqAll([ReqCapability('dash'), ReqCapability('slide')])"
        >>> # Errors if destinations differ, or if something is missing
        >>> g.mergeTransitions('A', 'down', 'up')
        Traceback (most recent call last):
        ...
        exploration.core.MissingTransitionError...
        >>> g.mergeTransitions('Z', 'one', 'two')
        Traceback (most recent call last):
        ...
        exploration.core.MissingDecisionError...
        >>> g.addDecision('C')
        2
        >>> g.addTransition('A', 'down', 'C')
        >>> g.mergeTransitions('A', 'down', 'up')
        Traceback (most recent call last):
        ...
        exploration.core.InvalidDestinationError...
        >>> # Merging a reciprocal onto an edge that doesn't have one
        >>> g.addTransition('A', 'down2', 'C')
        >>> g.addTransition('C', 'up2', 'A')
        >>> g.setReciprocal('A', 'down2', 'up2')
        >>> g.tagTransition('C', 'up2', 'narrow')
        >>> g.getReciprocal('A', 'down') is None
        True
        >>> g.mergeTransitions('A', 'down2', 'down')
        >>> g.getDestination('A', 'down2') is None
        True
        >>> g.getDestination('A', 'down')
        2
        >>> g.getDestination('C', 'up2')
        0
        >>> g.getReciprocal('A', 'down')
        'up2'
        >>> g.getReciprocal('C', 'up2')
        'down'
        >>> g.transitionTags('C', 'up2')
        {'narrow': 1}
        >>> # Merging without a reciprocal
        >>> g.addTransition('C', 'up', 'A')
        >>> g.mergeTransitions('C', 'up2', 'up', mergeReciprocal=False)
        >>> g.getDestination('C', 'up2') is None
        True
        >>> g.getDestination('C', 'up')
        0
        >>> g.transitionTags('C', 'up') # tag gets merged
        {'narrow': 1}
        >>> g.getDestination('A', 'down')
        2
        >>> g.getReciprocal('A', 'down') is None
        True
        >>> g.getReciprocal('C', 'up') is None
        True
        >>> # Merging w/ normal reciprocals
        >>> g.addDecision('D')
        3
        >>> g.addDecision('E')
        4
        >>> g.addTransition('D', 'up', 'E', 'return')
        >>> g.addTransition('E', 'down', 'D')
        >>> g.mergeTransitions('E', 'return', 'down')
        >>> g.getDestination('D', 'up')
        4
        >>> g.getDestination('E', 'down')
        3
        >>> g.getDestination('E', 'return') is None
        True
        >>> g.getReciprocal('D', 'up')
        'down'
        >>> g.getReciprocal('E', 'down')
        'up'
        >>> # Merging w/ weird reciprocals
        >>> g.addTransition('E', 'return', 'D')
        >>> g.setReciprocal('E', 'return', 'up', setBoth=False)
        >>> g.getReciprocal('D', 'up')
        'down'
        >>> g.getReciprocal('E', 'down')
        'up'
        >>> g.getReciprocal('E', 'return') # shared
        'up'
        >>> g.mergeTransitions('E', 'return', 'down')
        >>> g.getDestination('D', 'up')
        4
        >>> g.getDestination('E', 'down')
        3
        >>> g.getDestination('E', 'return') is None
        True
        >>> g.getReciprocal('D', 'up')
        'down'
        >>> g.getReciprocal('E', 'down')
        'up'
        """
        fromID = self.resolveDecision(fromDecision)

        # Short-circuit in the no-op case
        if merge == mergeInto:
            return

        # These lines will raise a MissingDecisionError or
        # MissingTransitionError if needed
        dest1 = self.destination(fromID, merge)
        dest2 = self.destination(fromID, mergeInto)

        if dest1 != dest2:
            raise InvalidDestinationError(
                f"Cannot merge transition {merge!r} into transition"
                f" {mergeInto!r} from decision"
                f" {self.identityOf(fromDecision)} because their"
                f" destinations are different ({self.identityOf(dest1)}"
                f" and {self.identityOf(dest2)}).\nNote: you can use"
                f" `retargetTransition` to change the destination of a"
                f" transition."
            )

        # Find and the transition properties
        props1 = self.getTransitionProperties(fromID, merge)
        props2 = self.getTransitionProperties(fromID, mergeInto)
        merged = mergeProperties(props1, props2)
        # Note that this doesn't change the reciprocal:
        self.setTransitionProperties(fromID, mergeInto, **merged)

        # Merge the reciprocal properties if requested
        # Get reciprocal to merge into
        reciprocal = self.getReciprocal(fromID, mergeInto)
        # Get reciprocal that needs cleaning up
        altReciprocal = self.getReciprocal(fromID, merge)
        # If the reciprocal to be merged actually already was the
        # reciprocal to merge into, there's nothing to do here
        if altReciprocal != reciprocal:
            if not mergeReciprocal:
                # In this case, we sever the reciprocal relationship if
                # there is a reciprocal
                if altReciprocal is not None:
                    self.setReciprocal(dest1, altReciprocal, None)
                    # By default setBoth takes care of the other half
            else:
                # In this case, we try to merge reciprocals
                # If altReciprocal is None, we don't need to do anything
                if altReciprocal is not None:
                    # Was there already a reciprocal or not?
                    if reciprocal is None:
                        # altReciprocal becomes the new reciprocal and is
                        # not deleted
                        self.setReciprocal(
                            fromID,
                            mergeInto,
                            altReciprocal
                        )
                    else:
                        # merge reciprocal properties
                        props1 = self.getTransitionProperties(
                            dest1,
                            altReciprocal
                        )
                        props2 = self.getTransitionProperties(
                            dest2,
                            reciprocal
                        )
                        merged = mergeProperties(props1, props2)
                        self.setTransitionProperties(
                            dest1,
                            reciprocal,
                            **merged
                        )

                        # delete the old reciprocal transition
                        self.remove_edge(dest1, fromID, altReciprocal)

        # Delete the old transition (reciprocal deletion/severance is
        # handled above if necessary)
        self.remove_edge(fromID, dest1, merge)

    def isConfirmed(self, decision: base.AnyDecisionSpecifier) -> bool:
        """
        Returns `True` or `False` depending on whether or not the
        specified decision has been confirmed. Uses the presence or
        absence of the 'unconfirmed' tag to determine this.

        Note: 'unconfirmed' is used instead of 'confirmed' so that large
        graphs with many confirmed nodes will be smaller when saved.
        """
        dID = self.resolveDecision(decision)

        return 'unconfirmed' not in self.nodes[dID]['tags']

    def replaceUnconfirmed(
        self,
        fromDecision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        connectTo: Optional[base.AnyDecisionSpecifier] = None,
        reciprocal: Optional[base.Transition] = None,
        requirement: Optional[base.Requirement] = None,
        applyConsequence: Optional[base.Consequence] = None,
        placeInZone: Union[type[base.DefaultZone], base.Zone, None] = None,
        forceNew: bool = False,
        tags: Optional[Dict[base.Tag, base.TagValue]] = None,
        annotations: Optional[List[base.Annotation]] = None,
        revRequires: Optional[base.Requirement] = None,
        revConsequence: Optional[base.Consequence] = None,
        revTags: Optional[Dict[base.Tag, base.TagValue]] = None,
        revAnnotations: Optional[List[base.Annotation]] = None,
        decisionTags: Optional[Dict[base.Tag, base.TagValue]] = None,
        decisionAnnotations: Optional[List[base.Annotation]] = None
    ) -> Tuple[
        Dict[base.Transition, base.Transition],
        Dict[base.Transition, base.Transition]
    ]:
        """
        Given a decision and an edge name in that decision, where the
        named edge leads to a decision with an unconfirmed exploration
        state (see `isConfirmed`), renames the unexplored decision on
        the other end of that edge using the given `connectTo` name, or
        if a decision using that name already exists, merges the
        unexplored decision into that decision. If `connectTo` is a
        `DecisionSpecifier` whose target doesn't exist, it will be
        treated as just a name, but if it's an ID and it doesn't exist,
        you'll get a `MissingDecisionError`. If a `reciprocal` is provided,
        a reciprocal edge will be added using that name connecting the
        `connectTo` decision back to the original decision. If this
        transition already exists, it must also point to a node which is
        also unexplored, and which will also be merged into the
        `fromDecision` node.

        If `connectTo` is not given (or is set to `None` explicitly)
        then the name of the unexplored decision will not be changed,
        unless that name has the form `'_u.-n-'` where `-n-` is a positive
        integer (i.e., the form given to automatically-named unknown
        nodes). In that case, the name will be changed to `'_x.-n-'` using
        the same number, or a higher number if that name is already taken.

        If the destination is being renamed or if the destination's
        exploration state counts as unexplored, the exploration state of
        the destination will be set to 'exploring'.

        If a `placeInZone` is specified, the destination will be placed
        directly into that zone (even if it already existed and has zone
        information), and it will be removed from any other zones it had
        been a direct member of. If `placeInZone` is set to
        `DefaultZone`, then the destination will be placed into each zone
        which is a direct parent of the origin, but only if the
        destination is not an already-explored existing decision AND
        it is not already in any zones (in those cases no zone changes
        are made). This will also remove it from any previous zones it
        had been a part of. If `placeInZone` is left as `None` (the
        default) no zone changes are made.

        If `placeInZone` is specified and that zone didn't already exist,
        it will be created as a new level-0 zone and will be added as a
        sub-zone of each zone that's a direct parent of any level-0 zone
        that the origin is a member of.

        If `forceNew` is specified, then the destination will just be
        renamed, even if another decision with the same name already
        exists. It's an error to use `forceNew` with a decision ID as
        the destination.

        Any additional edges pointing to or from the unknown node(s)
        being replaced will also be re-targeted at the now-discovered
        known destination(s) if necessary. These edges will retain their
        reciprocal names, or if this would cause a name clash, they will
        be renamed with a suffix (see `retargetTransition`).

        The return value is a pair of dictionaries mapping old names to
        new ones that just includes the names which were changed. The
        first dictionary contains renamed transitions that are outgoing
        from the new destination node (which used to be outgoing from
        the unexplored node). The second dictionary contains renamed
        transitions that are outgoing from the source node (which used
        to be outgoing from the unexplored node attached to the
        reciprocal transition; if there was no reciprocal transition
        specified then this will always be an empty dictionary).

        An `ExplorationStatusError` will be raised if the destination
        of the specified transition counts as visited (see
        `hasBeenVisited`). An `ExplorationStatusError` will also be
        raised if the `connectTo`'s `reciprocal` transition does not lead
        to an unconfirmed decision (it's okay if this second transition
        doesn't exist). A `TransitionCollisionError` will be raised if
        the unconfirmed destination decision already has an outgoing
        transition with the specified `reciprocal` which does not lead
        back to the `fromDecision`.

        The transition properties (requirement, consequences, tags,
        and/or annotations) of the replaced transition will be copied
        over to the new transition. Transition properties from the
        reciprocal transition will also be copied for the newly created
        reciprocal edge. Properties for any additional edges to/from the
        unknown node will also be copied.

        Also, any transition properties on existing forward or reciprocal
        edges from the destination node with the indicated reverse name
        will be merged with those from the target transition. Note that
        this merging process may introduce corruption of complex
        transition consequences. TODO: Fix that!

        Any tags and annotations are added to copied tags/annotations,
        but specified requirements, and/or consequences will replace
        previous requirements/consequences, rather than being added to
        them.

        ## Example

        >>> g = DecisionGraph()
        >>> g.addDecision('A')
        0
        >>> g.addUnexploredEdge('A', 'up')
        1
        >>> g.destination('A', 'up')
        1
        >>> g.destination('_u.0', 'return')
        0
        >>> g.replaceUnconfirmed('A', 'up', 'B', 'down')
        ({}, {})
        >>> g.destination('A', 'up')
        1
        >>> g.nameFor(1)
        'B'
        >>> g.destination('B', 'down')
        0
        >>> g.getDestination('B', 'return') is None
        True
        >>> '_u.0' in g.nameLookup
        False
        >>> g.getReciprocal('A', 'up')
        'down'
        >>> g.getReciprocal('B', 'down')
        'up'
        >>> # Two unexplored edges to the same node:
        >>> g.addDecision('C')
        2
        >>> g.addTransition('B', 'next', 'C')
        >>> g.addTransition('C', 'prev', 'B')
        >>> g.setReciprocal('B', 'next', 'prev')
        >>> g.addUnexploredEdge('A', 'next', 'D', 'prev')
        3
        >>> g.addTransition('C', 'down', 'D')
        >>> g.addTransition('D', 'up', 'C')
        >>> g.setReciprocal('C', 'down', 'up')
        >>> g.replaceUnconfirmed('C', 'down')
        ({}, {})
        >>> g.destination('C', 'down')
        3
        >>> g.destination('A', 'next')
        3
        >>> g.destinationsFrom('D')
        {'prev': 0, 'up': 2}
        >>> g.decisionTags('D')
        {}
        >>> # An unexplored transition which turns out to connect to a
        >>> # known decision, with name collisions
        >>> g.addUnexploredEdge('D', 'next', reciprocal='prev')
        4
        >>> g.tagDecision('_u.2', 'wet')
        >>> g.addUnexploredEdge('B', 'next', reciprocal='prev') # edge taken
        Traceback (most recent call last):
        ...
        exploration.core.TransitionCollisionError...
        >>> g.addUnexploredEdge('A', 'prev', reciprocal='next')
        5
        >>> g.tagDecision('_u.3', 'dry')
        >>> # Add transitions that will collide when merged
        >>> g.addUnexploredEdge('_u.2', 'up') # collides with A/up
        6
        >>> g.addUnexploredEdge('_u.3', 'prev') # collides with D/prev
        7
        >>> g.getReciprocal('A', 'prev')
        'next'
        >>> g.replaceUnconfirmed('A', 'prev', 'D', 'next') # two gone
        ({'prev': 'prev.1'}, {'up': 'up.1'})
        >>> g.destination('A', 'prev')
        3
        >>> g.destination('D', 'next')
        0
        >>> g.getReciprocal('A', 'prev')
        'next'
        >>> g.getReciprocal('D', 'next')
        'prev'
        >>> # Note that further unexplored structures are NOT merged
        >>> # even if they match against existing structures...
        >>> g.destination('A', 'up.1')
        6
        >>> g.destination('D', 'prev.1')
        7
        >>> '_u.2' in g.nameLookup
        False
        >>> '_u.3' in g.nameLookup
        False
        >>> g.decisionTags('D') # tags are merged
        {'dry': 1}
        >>> g.decisionTags('A')
        {'wet': 1}
        >>> # Auto-renaming an anonymous unexplored node
        >>> g.addUnexploredEdge('B', 'out')
        8
        >>> g.replaceUnconfirmed('B', 'out')
        ({}, {})
        >>> '_u.6' in g
        False
        >>> g.destination('B', 'out')
        8
        >>> g.nameFor(8)
        '_x.6'
        >>> g.destination('_x.6', 'return')
        1
        >>> # Placing a node into a zone
        >>> g.addUnexploredEdge('B', 'through')
        9
        >>> g.getDecision('E') is None
        True
        >>> g.replaceUnconfirmed(
        ...     'B',
        ...     'through',
        ...     'E',
        ...     'back',
        ...     placeInZone='Zone'
        ... )
        ({}, {})
        >>> g.getDecision('E')
        9
        >>> g.destination('B', 'through')
        9
        >>> g.destination('E', 'back')
        1
        >>> g.zoneParents(9)
        {'Zone'}
        >>> g.addUnexploredEdge('E', 'farther')
        10
        >>> g.replaceUnconfirmed(
        ...     'E',
        ...     'farther',
        ...     'F',
        ...     'closer',
        ...     placeInZone=base.DefaultZone
        ... )
        ({}, {})
        >>> g.destination('E', 'farther')
        10
        >>> g.destination('F', 'closer')
        9
        >>> g.zoneParents(10)
        {'Zone'}
        >>> g.addUnexploredEdge('F', 'backwards', placeInZone='Enoz')
        11
        >>> g.replaceUnconfirmed(
        ...     'F',
        ...     'backwards',
        ...     'G',
        ...     'forwards',
        ...     placeInZone=base.DefaultZone
        ... )
        ({}, {})
        >>> g.destination('F', 'backwards')
        11
        >>> g.destination('G', 'forwards')
        10
        >>> g.zoneParents(11)  # not changed since it already had a zone
        {'Enoz'}
        >>> # TODO: forceNew example
        """

        # Defaults
        if tags is None:
            tags = {}
        if annotations is None:
            annotations = []
        if revTags is None:
            revTags = {}
        if revAnnotations is None:
            revAnnotations = []
        if decisionTags is None:
            decisionTags = {}
        if decisionAnnotations is None:
            decisionAnnotations = []

        # Resolve source
        fromID = self.resolveDecision(fromDecision)

        # Figure out destination decision
        oldUnexplored = self.destination(fromID, transition)
        if self.isConfirmed(oldUnexplored):
            raise ExplorationStatusError(
                f"Transition {transition!r} from"
                f" {self.identityOf(fromDecision)} does not lead to an"
                f" unconfirmed decision (it leads to"
                f" {self.identityOf(oldUnexplored)} which is not tagged"
                f" 'unconfirmed')."
            )

        # Resolve destination
        newName: Optional[base.DecisionName] = None
        connectID: Optional[base.DecisionID] = None
        if forceNew:
            if isinstance(connectTo, base.DecisionID):
                raise TypeError(
                    f"connectTo cannot be a decision ID when forceNew"
                    f" is True. Got: {self.identityOf(connectTo)}"
                )
            elif isinstance(connectTo, base.DecisionSpecifier):
                newName = connectTo.name
            elif isinstance(connectTo, base.DecisionName):
                newName = connectTo
            elif connectTo is None:
                oldName = self.nameFor(oldUnexplored)
                if (
                    oldName.startswith('_u.')
                and oldName[3:].isdigit()
                ):
                    newName = utils.uniqueName('_x.' + oldName[3:], self)
                else:
                    newName = oldName
            else:
                raise TypeError(
                    f"Invalid connectTo value: {connectTo!r}"
                )
        elif connectTo is not None:
            try:
                connectID = self.resolveDecision(connectTo)
                # leave newName as None
            except MissingDecisionError:
                if isinstance(connectTo, int):
                    raise
                elif isinstance(connectTo, base.DecisionSpecifier):
                    newName = connectTo.name
                    # The domain & zone are ignored here
                else:  # Must just be a string
                    assert isinstance(connectTo, str)
                    newName = connectTo
        else:
            # If connectTo name wasn't specified, use current name of
            # unknown node unless it's a default name
            oldName = self.nameFor(oldUnexplored)
            if (
                oldName.startswith('_u.')
            and oldName[3:].isdigit()
            ):
                newName = utils.uniqueName('_x.' + oldName[3:], self)
            else:
                newName = oldName

        # One or the other should be valid at this point
        assert connectID is not None or newName is not None

        # Check that the old unknown doesn't have a reciprocal edge that
        # would collide with the specified return edge
        if reciprocal is not None:
            revFromUnknown = self.getDestination(oldUnexplored, reciprocal)
            if revFromUnknown not in (None, fromID):
                raise TransitionCollisionError(
                    f"Transition {reciprocal!r} from"
                    f" {self.identityOf(oldUnexplored)} exists and does"
                    f" not lead back to {self.identityOf(fromDecision)}"
                    f" (it leads to {self.identityOf(revFromUnknown)})."
                )

        # Remember old reciprocal edge for future merging in case
        # it's not reciprocal
        oldReciprocal = self.getReciprocal(fromID, transition)

        # Apply any new tags or annotations, or create a new node
        needsZoneInfo = False
        if connectID is not None:
            # Before applying tags, check if we need to error out
            # because of a reciprocal edge that points to a known
            # destination:
            if reciprocal is not None:
                otherOldUnknown: Optional[
                    base.DecisionID
                ] = self.getDestination(
                    connectID,
                    reciprocal
                )
                if (
                    otherOldUnknown is not None
                and self.isConfirmed(otherOldUnknown)
                ):
                    raise ExplorationStatusError(
                        f"Reciprocal transition {reciprocal!r} from"
                        f" {self.identityOf(connectTo)} does not lead"
                        f" to an unconfirmed decision (it leads to"
                        f" {self.identityOf(otherOldUnknown)})."
                    )
            self.tagDecision(connectID, decisionTags)
            self.annotateDecision(connectID, decisionAnnotations)
            # Still needs zone info if the place we're connecting to was
            # unconfirmed up until now, since unconfirmed nodes don't
            # normally get zone info when they're created.
            if not self.isConfirmed(connectID):
                needsZoneInfo = True

            # First, merge the old unknown with the connectTo node...
            destRenames = self.mergeDecisions(
                oldUnexplored,
                connectID,
                errorOnNameColision=False
            )
        else:
            needsZoneInfo = True
            if len(self.zoneParents(oldUnexplored)) > 0:
                needsZoneInfo = False
            assert newName is not None
            self.renameDecision(oldUnexplored, newName)
            connectID = oldUnexplored
            # In this case there can't be an other old unknown
            otherOldUnknown = None
            destRenames = {}  # empty

        # Check for domain mismatch to stifle zone updates:
        fromDomain = self.domainFor(fromID)
        if connectID is None:
            destDomain = self.domainFor(oldUnexplored)
        else:
            destDomain = self.domainFor(connectID)

        # Stifle zone updates if there's a mismatch
        if fromDomain != destDomain:
            needsZoneInfo = False

        # Records renames that happen at the source (from node)
        sourceRenames = {}  # empty for now

        assert connectID is not None

        # Apply the new zone if there is one
        if placeInZone is not None:
            if placeInZone is base.DefaultZone:
                # When using DefaultZone, changes are only made for new
                # destinations which don't already have any zones and
                # which are in the same domain as the departing node:
                # they get placed into each zone parent of the source
                # decision.
                if needsZoneInfo:
                    # Remove destination from all current parents
                    removeFrom = set(self.zoneParents(connectID))  # copy
                    for parent in removeFrom:
                        self.removeDecisionFromZone(connectID, parent)
                    # Add it to parents of origin
                    for parent in self.zoneParents(fromID):
                        self.addDecisionToZone(connectID, parent)
            else:
                placeInZone = cast(base.Zone, placeInZone)
                # Create the zone if it doesn't already exist
                if self.getZoneInfo(placeInZone) is None:
                    self.createZone(placeInZone, 0)
                    # Add it to each grandparent of the from decision
                    for parent in self.zoneParents(fromID):
                        for grandparent in self.zoneParents(parent):
                            self.addZoneToZone(placeInZone, grandparent)
                # Remove destination from all current parents
                for parent in set(self.zoneParents(connectID)):
                    self.removeDecisionFromZone(connectID, parent)
                # Add it to the specified zone
                self.addDecisionToZone(connectID, placeInZone)

        # Next, if there is a reciprocal name specified, we do more...
        if reciprocal is not None:
            # Figure out what kind of merging needs to happen
            if otherOldUnknown is None:
                if revFromUnknown is None:
                    # Just create the desired reciprocal transition, which
                    # we know does not already exist
                    self.addTransition(connectID, reciprocal, fromID)
                    otherOldReciprocal = None
                else:
                    # Reciprocal exists, as revFromUnknown
                    otherOldReciprocal = None
            else:
                otherOldReciprocal = self.getReciprocal(
                    connectID,
                    reciprocal
                )
                # we need to merge otherOldUnknown into our fromDecision
                sourceRenames = self.mergeDecisions(
                    otherOldUnknown,
                    fromID,
                    errorOnNameColision=False
                )
                # Unvisited tag after merge only if both were

            # No matter what happened we ensure the reciprocal
            # relationship is set up:
            self.setReciprocal(fromID, transition, reciprocal)

            # Now we might need to merge some transitions:
            # - Any reciprocal of the target transition should be merged
            #   with reciprocal (if it was already reciprocal, that's a
            #   no-op).
            # - Any reciprocal of the reciprocal transition from the target
            #   node (leading to otherOldUnknown) should be merged with
            #   the target transition, even if it shared a name and was
            #   renamed as a result.
            # - If reciprocal was renamed during the initial merge, those
            #   transitions should be merged.

            # Merge old reciprocal into reciprocal
            if oldReciprocal is not None:
                oldRev = destRenames.get(oldReciprocal, oldReciprocal)
                if self.getDestination(connectID, oldRev) is not None:
                    # Note that we don't want to auto-merge the reciprocal,
                    # which is the target transition
                    self.mergeTransitions(
                        connectID,
                        oldRev,
                        reciprocal,
                        mergeReciprocal=False
                    )
                    # Remove it from the renames map
                    if oldReciprocal in destRenames:
                        del destRenames[oldReciprocal]

            # Merge reciprocal reciprocal from otherOldUnknown
            if otherOldReciprocal is not None:
                otherOldRev = sourceRenames.get(
                    otherOldReciprocal,
                    otherOldReciprocal
                )
                # Note that the reciprocal is reciprocal, which we don't
                # need to merge
                self.mergeTransitions(
                    fromID,
                    otherOldRev,
                    transition,
                    mergeReciprocal=False
                )
                # Remove it from the renames map
                if otherOldReciprocal in sourceRenames:
                    del sourceRenames[otherOldReciprocal]

            # Merge any renamed reciprocal onto reciprocal
            if reciprocal in destRenames:
                extraRev = destRenames[reciprocal]
                self.mergeTransitions(
                    connectID,
                    extraRev,
                    reciprocal,
                    mergeReciprocal=False
                )
                # Remove it from the renames map
                del destRenames[reciprocal]

        # Accumulate new tags & annotations for the transitions
        self.tagTransition(fromID, transition, tags)
        self.annotateTransition(fromID, transition, annotations)

        if reciprocal is not None:
            self.tagTransition(connectID, reciprocal, revTags)
            self.annotateTransition(connectID, reciprocal, revAnnotations)

        # Override copied requirement/consequences for the transitions
        if requirement is not None:
            self.setTransitionRequirement(
                fromID,
                transition,
                requirement
            )
        if applyConsequence is not None:
            self.setConsequence(
                fromID,
                transition,
                applyConsequence
            )

        if reciprocal is not None:
            if revRequires is not None:
                self.setTransitionRequirement(
                    connectID,
                    reciprocal,
                    revRequires
                )
            if revConsequence is not None:
                self.setConsequence(
                    connectID,
                    reciprocal,
                    revConsequence
                )

        # Remove 'unconfirmed' tag if it was present
        self.untagDecision(connectID, 'unconfirmed')

        # Final checks
        assert self.getDestination(fromDecision, transition) == connectID
        useConnect: base.AnyDecisionSpecifier
        useRev: Optional[str]
        if connectTo is None:
            useConnect = connectID
        else:
            useConnect = connectTo
        if reciprocal is None:
            useRev = self.getReciprocal(fromDecision, transition)
        else:
            useRev = reciprocal
        if useRev is not None:
            try:
                assert self.getDestination(useConnect, useRev) == fromID
            except AmbiguousDecisionSpecifierError:
                assert self.getDestination(connectID, useRev) == fromID

        # Return our final rename dictionaries
        return (destRenames, sourceRenames)

    def endingID(self, name: base.DecisionName) -> base.DecisionID:
        """
        Returns the decision ID for the ending with the specified name.
        Endings are disconnected decisions in the `ENDINGS_DOMAIN`; they
        don't normally include any zone information. If no ending with
        the specified name already existed, then a new ending with that
        name will be created and its Decision ID will be returned.

        If a new decision is created, it will be tagged as unconfirmed.

        Note that endings mostly aren't special: they're normal
        decisions in a separate singular-focalized domain. However, some
        parts of the exploration and journal machinery treat them
        differently (in particular, taking certain actions via
        `advanceSituation` while any decision in the `ENDINGS_DOMAIN` is
        active is an error.
        """
        # Create our new ending decision if we need to
        try:
            endID = self.resolveDecision(
                base.DecisionSpecifier(ENDINGS_DOMAIN, None, name)
            )
        except MissingDecisionError:
            # Create a new decision for the ending
            endID = self.addDecision(name, domain=ENDINGS_DOMAIN)
            # Tag it as unconfirmed
            self.tagDecision(endID, 'unconfirmed')

        return endID

    def triggerGroupID(self, name: base.DecisionName) -> base.DecisionID:
        """
        Given the name of a trigger group, returns the ID of the special
        node representing that trigger group in the `TRIGGERS_DOMAIN`.
        If the specified group didn't already exist, it will be created.

        Trigger group decisions are not special: they just exist in a
        separate spreading-focalized domain and have a few API methods to
        access them, but all the normal decision-related API methods
        still work. Their intended use is for sets of global triggers,
        by attaching actions with the 'trigger' tag to them and then
        activating or deactivating them as needed.
        """
        result = self.getDecision(
            base.DecisionSpecifier(TRIGGERS_DOMAIN, None, name)
        )
        if result is None:
            return self.addDecision(name, domain=TRIGGERS_DOMAIN)
        else:
            return result

    @staticmethod
    def example(which: Literal['simple', 'abc']) -> 'DecisionGraph':
        """
        Returns one of a number of example decision graphs, depending on
        the string given. It returns a fresh copy each time. The graphs
        are:

        - 'simple': Three nodes named 'A', 'B', and 'C' with IDs 0, 1,
            and 2, each connected to the next in the sequence by a
            'next' transition with reciprocal 'prev'. In other words, a
            simple little triangle. There are no tags, annotations,
            requirements, consequences, mechanisms, or equivalences.
        - 'abc': A more complicated 3-node setup that introduces a
            little bit of everything. In this graph, we have the same
            three nodes, but different transitions:

                * From A you can go 'left' to B with reciprocal 'right'.
                * From A you can also go 'up_left' to B with reciprocal
                    'up_right'. These transitions both require the
                    'grate' mechanism (which is at decision A) to be in
                    state 'open'.
                * From A you can go 'down' to C with reciprocal 'up'.

            (In this graph, B and C are not directly connected to each
            other.)

            The graph has two level-0 zones 'zoneA' and 'zoneB', along
            with a level-1 zone 'upZone'. Decisions A and C are in
            zoneA while B is in zoneB; zoneA is in upZone, but zoneB is
            not.

            The decision A has annotation:

                'This is a multi-word "annotation."'

            The transition 'down' from A has annotation:

                "Transition 'annotation.'"

            Decision B has tags 'b' with value 1 and 'tag2' with value
            '"value"'.

            Decision C has tag 'aw"ful' with value "ha'ha'".

            Transition 'up' from C has tag 'fast' with value 1.

            At decision C there are actions 'grab_helmet' and
            'pull_lever'.

            The 'grab_helmet' transition requires that you don't have
            the 'helmet' capability, and gives you that capability,
            deactivating with delay 3.

            The 'pull_lever' transition requires that you do have the
            'helmet' capability, and takes away that capability, but it
            also gives you 1 token, and if you have 2 tokens (before
            getting the one extra), it sets the 'grate' mechanism (which
            is a decision A) to state 'open' and deactivates.

            The graph has an equivalence: having the 'helmet' capability
            satisfies requirements for the 'grate' mechanism to be in the
            'open' state.

        """
        result = DecisionGraph()
        if which == 'simple':
            result.addDecision('A')  # id 0
            result.addDecision('B')  # id 1
            result.addDecision('C')  # id 2
            result.addTransition('A', 'next', 'B', 'prev')
            result.addTransition('B', 'next', 'C', 'prev')
            result.addTransition('C', 'next', 'A', 'prev')
        elif which == 'abc':
            result.addDecision('A')  # id 0
            result.addDecision('B')  # id 1
            result.addDecision('C')  # id 2
            result.createZone('zoneA', 0)
            result.createZone('zoneB', 0)
            result.createZone('upZone', 1)
            result.addZoneToZone('zoneA', 'upZone')
            result.addDecisionToZone('A', 'zoneA')
            result.addDecisionToZone('B', 'zoneB')
            result.addDecisionToZone('C', 'zoneA')
            result.addTransition('A', 'left', 'B', 'right')
            result.addTransition('A', 'up_left', 'B', 'up_right')
            result.addTransition('A', 'down', 'C', 'up')
            result.setTransitionRequirement(
                'A',
                'up_left',
                base.ReqMechanism('grate', 'open')
            )
            result.setTransitionRequirement(
                'B',
                'up_right',
                base.ReqMechanism('grate', 'open')
            )
            result.annotateDecision('A', 'This is a multi-word "annotation."')
            result.annotateTransition('A', 'down', "Transition 'annotation.'")
            result.tagDecision('B', 'b')
            result.tagDecision('B', 'tag2', '"value"')
            result.tagDecision('C', 'aw"ful', "ha'ha")
            result.tagTransition('C', 'up', 'fast')
            result.addMechanism('grate', 'A')
            result.addAction(
                'C',
                'grab_helmet',
                base.ReqNot(base.ReqCapability('helmet')),
                [
                    base.effect(gain='helmet'),
                    base.effect(deactivate=True, delay=3)
                ]
            )
            result.addAction(
                'C',
                'pull_lever',
                base.ReqCapability('helmet'),
                [
                    base.effect(lose='helmet'),
                    base.effect(gain=('token', 1)),
                    base.condition(
                        base.ReqTokens('token', 2),
                        [
                            base.effect(set=('grate', 'open')),
                            base.effect(deactivate=True)
                        ]
                    )
                ]
            )
            result.addEquivalence(
                base.ReqCapability('helmet'),
                (0, 'open')
            )
        else:
            raise ValueError(f"Invalid example name: {which!r}")

        return result


#---------------------------#
# DiscreteExploration class #
#---------------------------#

def emptySituation() -> base.Situation:
    """
    Creates and returns an empty situation: A situation that has an
    empty `DecisionGraph`, an empty `State`, a 'pending' decision type
    with `None` as the action taken, no tags, and no annotations.
    """
    return base.Situation(
        graph=DecisionGraph(),
        state=base.emptyState(),
        type='pending',
        action=None,
        saves={},
        tags={},
        annotations=[]
    )


class DiscreteExploration:
    """
    A list of `Situations` each of which contains a `DecisionGraph`
    representing exploration over time, with `States` containing
    `FocalContext` information for each step and 'taken' values for the
    transition selected (at a particular decision) in that step. Each
    decision graph represents a new state of the world (and/or new
    knowledge about a persisting state of the world), and the 'taken'
    transition in one situation transition indicates which option was
    selected, or what event happened to cause update(s). Depending on the
    resolution, it could represent a close record of every decision made
    or a more coarse set of snapshots from gameplay with more time in
    between.

    The steps of the exploration can also be tagged and annotated (see
    `tagStep` and `annotateStep`).

    When a new `DiscreteExploration` is created, it starts out with an
    empty `Situation` that contains an empty `DecisionGraph`. Use the
    `start` method to name the starting decision point and set things up
    for other methods.

    Tracking of player goals and destinations is also possible (see the
    `quest`, `progress`, `complete`, `destination`, and `arrive` methods).
    TODO: That
    """
    def __init__(self) -> None:
        self.situations: List[base.Situation] = [
            base.Situation(
                graph=DecisionGraph(),
                state=base.emptyState(),
                type='pending',
                action=None,
                saves={},
                tags={},
                annotations=[]
            )
        ]

    # Note: not hashable

    def __eq__(self, other):
        """
        Equality checker. `DiscreteExploration`s can only be equal to
        other `DiscreteExploration`s, not to other kinds of things.
        """
        if not isinstance(other, DiscreteExploration):
            return False
        else:
            return self.situations == other.situations

    @staticmethod
    def fromGraph(
        graph: DecisionGraph,
        state: Optional[base.State] = None
    ) -> 'DiscreteExploration':
        """
        Creates an exploration which has just a single step whose graph
        is the entire specified graph, with the specified decision as
        the primary decision (if any). The graph is copied, so that
        changes to the exploration will not modify it. A starting state
        may also be specified if desired, although if not an empty state
        will be used (a provided starting state is NOT copied, but used
        directly).

        Example:

        >>> g = DecisionGraph()
        >>> g.addDecision('Room1')
        0
        >>> g.addDecision('Room2')
        1
        >>> g.addTransition('Room1', 'door', 'Room2', 'door')
        >>> e = DiscreteExploration.fromGraph(g)
        >>> len(e)
        1
        >>> e.getSituation().graph == g
        True
        >>> e.getActiveDecisions()
        set()
        >>> e.primaryDecision() is None
        True
        >>> e.observe('Room1', 'hatch')
        2
        >>> e.getSituation().graph == g
        False
        >>> e.getSituation().graph.destinationsFrom('Room1')
        {'door': 1, 'hatch': 2}
        >>> g.destinationsFrom('Room1')
        {'door': 1}
        """
        result = DiscreteExploration()
        result.situations[0] = base.Situation(
            graph=copy.deepcopy(graph),
            state=base.emptyState() if state is None else state,
            type='pending',
            action=None,
            saves={},
            tags={},
            annotations=[]
        )
        return result

    def __len__(self) -> int:
        """
        The 'length' of an exploration is the number of steps.
        """
        return len(self.situations)

    def __getitem__(self, i: int) -> base.Situation:
        """
        Indexing an exploration returns the situation at that step.
        """
        return self.situations[i]

    def __iter__(self) -> Iterator[base.Situation]:
        """
        Iterating over an exploration yields each `Situation` in order.
        """
        for i in range(len(self)):
            yield self[i]

    def getSituation(self, step: int = -1) -> base.Situation:
        """
        Returns a `base.Situation` named tuple detailing the state of
        the exploration at a given step (or at the current step if no
        argument is given). Note that this method works the same
        way as indexing the exploration: see `__getitem__`.

        Raises an `IndexError` if asked for a step that's out-of-range.
        """
        return self[step]

    def primaryDecision(self, step: int = -1) -> Optional[base.DecisionID]:
        """
        Returns the current primary `base.DecisionID`, or the primary
        decision from a specific step if one is specified. This may be
        `None` for some steps, but mostly it's the destination of the
        transition taken in the previous step.
        """
        return self[step].state['primaryDecision']

    def effectiveCapabilities(
        self,
        step: int = -1
    ) -> base.CapabilitySet:
        """
        Returns the effective capability set for the specified step
        (default is the last/current step). See
        `base.effectiveCapabilities`.
        """
        return base.effectiveCapabilitySet(self.getSituation(step).state)

    def getCommonContext(
        self,
        step: Optional[int] = None
    ) -> base.FocalContext:
        """
        Returns the common `FocalContext` at the specified step, or at
        the current step if no argument is given. Raises an `IndexError`
        if an invalid step is specified.
        """
        if step is None:
            step = -1
        state = self.getSituation(step).state
        return state['common']

    def getActiveContext(
        self,
        step: Optional[int] = None
    ) -> base.FocalContext:
        """
        Returns the active `FocalContext` at the specified step, or at
        the current step if no argument is provided. Raises an
        `IndexError` if an invalid step is specified.
        """
        if step is None:
            step = -1
        state = self.getSituation(step).state
        return state['contexts'][state['activeContext']]

    def addFocalContext(self, name: base.FocalContextName) -> None:
        """
        Adds a new empty focal context to our set of focal contexts (see
        `emptyFocalContext`). Use `setActiveContext` to swap to it.
        Raises a `FocalContextCollisionError` if the name is already in
        use.
        """
        contextMap = self.getSituation().state['contexts']
        if name in contextMap:
            raise FocalContextCollisionError(
                f"Cannot add focal context {name!r}: a focal context"
                f" with that name already exists."
            )
        contextMap[name] = base.emptyFocalContext()

    def setActiveContext(self, which: base.FocalContextName) -> None:
        """
        Sets the active context to the named focal context, creating it
        if it did not already exist (makes changes to the current
        situation only). Does not add an exploration step (use
        `advanceSituation` with a 'swap' action for that).
        """
        state = self.getSituation().state
        contextMap = state['contexts']
        if which not in contextMap:
            self.addFocalContext(which)
        state['activeContext'] = which

    def createDomain(
        self,
        name: base.Domain,
        focalization: base.DomainFocalization = 'singular',
        makeActive: bool = False,
        inCommon: Union[bool, Literal["both"]] = "both"
    ) -> None:
        """
        Creates a new domain with the given focalization type, in either
        the common context (`inCommon` = `True`) the active context
        (`inCommon` = `False`) or both (the default; `inCommon` = 'both').
        The domain's focalization will be set to the given
        `focalization` value (default 'singular') and it will have no
        active decisions. Raises a `DomainCollisionError` if a domain
        with the specified name already exists.

        Creates the domain in the current situation.

        If `makeActive` is set to `True` (default is `False`) then the
        domain will be made active in whichever context(s) it's created
        in.
        """
        now = self.getSituation()
        state = now.state
        modify = []
        if inCommon in (True, "both"):
            modify.append(('common', state['common']))
        if inCommon in (False, "both"):
            acName = state['activeContext']
            modify.append(
                ('current ({repr(acName)})', state['contexts'][acName])
            )

        for (fcType, fc) in modify:
            if name in fc['focalization']:
                raise DomainCollisionError(
                    f"Cannot create domain {repr(name)} because a"
                    f" domain with that name already exists in the"
                    f" {fcType} focal context."
                )
            fc['focalization'][name] = focalization
            if makeActive:
                fc['activeDomains'].add(name)
            if focalization == "spreading":
                fc['activeDecisions'][name] = set()
            elif focalization == "plural":
                fc['activeDecisions'][name] = {}
            else:
                fc['activeDecisions'][name] = None

    def activateDomain(
        self,
        domain: base.Domain,
        activate: bool = True,
        inContext: base.ContextSpecifier = "active"
    ) -> None:
        """
        Sets the given domain as active (or inactive if 'activate' is
        given as `False`) in the specified context (default "active").

        Modifies the current situation.
        """
        fc: base.FocalContext
        if inContext == "active":
            fc = self.getActiveContext()
        elif inContext == "common":
            fc = self.getCommonContext()

        if activate:
            fc['activeDomains'].add(domain)
        else:
            try:
                fc['activeDomains'].remove(domain)
            except KeyError:
                pass

    def createTriggerGroup(
        self,
        name: base.DecisionName
    ) -> base.DecisionID:
        """
        Creates a new trigger group with the given name, returning the
        decision ID for that trigger group. If this is the first trigger
        group being created, also creates the `TRIGGERS_DOMAIN` domain
        as a spreading-focalized domain that's active in the common
        context (but does NOT set the created trigger group as an active
        decision in that domain).

        You can use 'goto' effects to activate trigger domains via
        consequences, and 'retreat' effects to deactivate them.

        Creating a second trigger group with the same name as another
        results in a `ValueError`.

        TODO: Retreat effects
        """
        ctx = self.getCommonContext()
        if TRIGGERS_DOMAIN not in ctx['focalization']:
            self.createDomain(
                TRIGGERS_DOMAIN,
                focalization='spreading',
                makeActive=True,
                inCommon=True
            )

        graph = self.getSituation().graph
        if graph.getDecision(
            base.DecisionSpecifier(TRIGGERS_DOMAIN, None, name)
        ) is not None:
            raise ValueError(
                f"Cannot create trigger group {name!r}: a trigger group"
                f" with that name already exists."
            )

        return self.getSituation().graph.triggerGroupID(name)

    def toggleTriggerGroup(
        self,
        name: base.DecisionName,
        setActive: Union[bool, None] = None
    ):
        """
        Toggles whether the specified trigger group (a decision in the
        `TRIGGERS_DOMAIN`) is active or not. Pass `True` or `False` as
        the `setActive` argument (instead of the default `None`) to set
        the state directly instead of toggling it.

        Note that trigger groups are decisions in a spreading-focalized
        domain, so they can be activated or deactivated by the 'goto'
        and 'retreat' effects as well.

        This does not affect whether the `TRIGGERS_DOMAIN` itself is
        active (normally it would always be active).

        Raises a `MissingDecisionError` if the specified trigger group
        does not exist yet, including when the entire `TRIGGERS_DOMAIN`
        does not exist. Raises a `KeyError` if the target group exists
        but the `TRIGGERS_DOMAIN` has not been set up properly.
        """
        ctx = self.getCommonContext()
        tID = self.getSituation().graph.resolveDecision(
            base.DecisionSpecifier(TRIGGERS_DOMAIN, None, name)
        )
        activeGroups = ctx['activeDecisions'][TRIGGERS_DOMAIN]
        assert isinstance(activeGroups, set)
        if tID in activeGroups:
            if setActive is not True:
                activeGroups.remove(tID)
        else:
            if setActive is not False:
                activeGroups.add(tID)

    def getActiveDecisions(
        self,
        step: Optional[int] = None,
        inCommon: Union[bool, Literal["both"]] = "both"
    ) -> Set[base.DecisionID]:
        """
        Returns the set of active decisions at the given step index, or
        at the current step if no step is specified. Raises an
        `IndexError` if the step index is out of bounds (see `__len__`).
        May return an empty set if no decisions are active.

        If `inCommon` is set to "both" (the default) then decisions
        active in either the common or active context are returned. Set
        it to `True` or `False` to return only decisions active in the
        common (when `True`) or  active (when `False`) context.
        """
        if step is None:
            step = -1
        state = self.getSituation(step).state
        if inCommon == "both":
            return base.combinedDecisionSet(state)
        elif inCommon is True:
            return base.activeDecisionSet(state['common'])
        elif inCommon is False:
            return base.activeDecisionSet(
                state['contexts'][state['activeContext']]
            )
        else:
            raise ValueError(
                f"Invalid inCommon value {repr(inCommon)} (must be"
                f" 'both', True, or False)."
            )

    def setActiveDecisionsAtStep(
        self,
        step: int,
        domain: base.Domain,
        activate: Union[
            base.DecisionID,
            Dict[base.FocalPointName, Optional[base.DecisionID]],
            Set[base.DecisionID]
        ],
        inCommon: bool = False
    ) -> None:
        """
        Changes the activation status of decisions in the active
        `FocalContext` at the specified step, for the specified domain
        (see `currentActiveContext`). Does this without adding an
        exploration step, which is unusual: normally you should use
        another method like `warp` to update active decisions.

        Note that this does not change which domains are active, and
        setting active decisions in inactive domains does not make those
        decisions active overall.

        Which decisions to activate or deactivate are specified as
        either a single `DecisionID`, a list of them, or a set of them,
        depending on the `DomainFocalization` setting in the selected
        `FocalContext` for the specified domain. A `TypeError` will be
        raised if the wrong kind of decision information is provided. If
        the focalization context does not have any focalization value for
        the domain in question, it will be set based on the kind of
        active decision information specified.

        A `MissingDecisionError` will be raised if a decision is
        included which is not part of the current `DecisionGraph`.
        The provided information will overwrite the previous active
        decision information.

        If `inCommon` is set to `True`, then decisions are activated or
        deactivated in the common context, instead of in the active
        context.

        Example:

        >>> e = DiscreteExploration()
        >>> e.getActiveDecisions()
        set()
        >>> graph = e.getSituation().graph
        >>> graph.addDecision('A')
        0
        >>> graph.addDecision('B')
        1
        >>> graph.addDecision('C')
        2
        >>> e.setActiveDecisionsAtStep(0, 'main', 0)
        >>> e.getActiveDecisions()
        {0}
        >>> e.setActiveDecisionsAtStep(0, 'main', 1)
        >>> e.getActiveDecisions()
        {1}
        >>> graph = e.getSituation().graph
        >>> graph.addDecision('One', domain='numbers')
        3
        >>> graph.addDecision('Two', domain='numbers')
        4
        >>> graph.addDecision('Three', domain='numbers')
        5
        >>> graph.addDecision('Bear', domain='animals')
        6
        >>> graph.addDecision('Spider', domain='animals')
        7
        >>> graph.addDecision('Eel', domain='animals')
        8
        >>> ac = e.getActiveContext()
        >>> ac['focalization']['numbers'] = 'plural'
        >>> ac['focalization']['animals'] = 'spreading'
        >>> ac['activeDecisions']['numbers'] = {'a': None, 'b': None}
        >>> ac['activeDecisions']['animals'] = set()
        >>> cc = e.getCommonContext()
        >>> cc['focalization']['numbers'] = 'plural'
        >>> cc['focalization']['animals'] = 'spreading'
        >>> cc['activeDecisions']['numbers'] = {'z': None}
        >>> cc['activeDecisions']['animals'] = set()
        >>> e.setActiveDecisionsAtStep(0, 'numbers', {'a': 3, 'b': 3})
        >>> e.getActiveDecisions()
        {1}
        >>> e.activateDomain('numbers')
        >>> e.getActiveDecisions()
        {1, 3}
        >>> e.setActiveDecisionsAtStep(0, 'numbers', {'a': 4, 'b': None})
        >>> e.getActiveDecisions()
        {1, 4}
        >>> # Wrong domain for the decision ID:
        >>> e.setActiveDecisionsAtStep(0, 'main', 3)
        Traceback (most recent call last):
        ...
        ValueError...
        >>> # Wrong domain for one of the decision IDs:
        >>> e.setActiveDecisionsAtStep(0, 'numbers', {'a': 2, 'b': None})
        Traceback (most recent call last):
        ...
        ValueError...
        >>> # Wrong kind of decision information provided.
        >>> e.setActiveDecisionsAtStep(0, 'numbers', 3)
        Traceback (most recent call last):
        ...
        TypeError...
        >>> e.getActiveDecisions()
        {1, 4}
        >>> e.setActiveDecisionsAtStep(0, 'animals', {6, 7})
        >>> e.getActiveDecisions()
        {1, 4}
        >>> e.activateDomain('animals')
        >>> e.getActiveDecisions()
        {1, 4, 6, 7}
        >>> e.setActiveDecisionsAtStep(0, 'animals', {8})
        >>> e.getActiveDecisions()
        {8, 1, 4}
        >>> e.setActiveDecisionsAtStep(1, 'main', 2)  # invalid step
        Traceback (most recent call last):
        ...
        IndexError...
        >>> e.setActiveDecisionsAtStep(0, 'novel', 0)  # domain mismatch
        Traceback (most recent call last):
        ...
        ValueError...

        Example of active/common contexts:

        >>> e = DiscreteExploration()
        >>> graph = e.getSituation().graph
        >>> graph.addDecision('A')
        0
        >>> graph.addDecision('B')
        1
        >>> e.activateDomain('main', inContext="common")
        >>> e.setActiveDecisionsAtStep(0, 'main', 0, inCommon=True)
        >>> e.getActiveDecisions()
        {0}
        >>> e.setActiveDecisionsAtStep(0, 'main', None)
        >>> e.getActiveDecisions()
        {0}
        >>> # (Still active since it's active in the common context)
        >>> e.setActiveDecisionsAtStep(0, 'main', 1)
        >>> e.getActiveDecisions()
        {0, 1}
        >>> e.setActiveDecisionsAtStep(0, 'main', 1, inCommon=True)
        >>> e.getActiveDecisions()
        {1}
        >>> e.setActiveDecisionsAtStep(0, 'main', None, inCommon=True)
        >>> e.getActiveDecisions()
        {1}
        >>> # (Still active since it's active in the active context)
        >>> e.setActiveDecisionsAtStep(0, 'main', None)
        >>> e.getActiveDecisions()
        set()
        """
        now = self.getSituation(step)
        graph = now.graph
        if inCommon:
            context = self.getCommonContext(step)
        else:
            context = self.getActiveContext(step)

        defaultFocalization: base.DomainFocalization = 'singular'
        if isinstance(activate, base.DecisionID):
            defaultFocalization = 'singular'
        elif isinstance(activate, dict):
            defaultFocalization = 'plural'
        elif isinstance(activate, set):
            defaultFocalization = 'spreading'
        elif domain not in context['focalization']:
            raise TypeError(
                f"Domain {domain!r} has no focalization in the"
                f" {'common' if inCommon else 'active'} context,"
                f" and the specified position doesn't imply one."
            )

        focalization = base.getDomainFocalization(
            context,
            domain,
            defaultFocalization
        )

        # Check domain & existence of decision(s) in question
        if activate is None:
            pass
        elif isinstance(activate, base.DecisionID):
            if activate not in graph:
                raise MissingDecisionError(
                    f"There is no decision {activate} at step {step}."
                )
            if graph.domainFor(activate) != domain:
                raise ValueError(
                    f"Can't set active decisions in domain {domain!r}"
                    f" to decision {graph.identityOf(activate)} because"
                    f" that decision is in actually in domain"
                    f" {graph.domainFor(activate)!r}."
                )
        elif isinstance(activate, dict):
            for fpName, pos in activate.items():
                if pos is None:
                    continue
                if pos not in graph:
                    raise MissingDecisionError(
                        f"There is no decision {pos} at step {step}."
                    )
                if graph.domainFor(pos) != domain:
                    raise ValueError(
                        f"Can't set active decision for focal point"
                        f" {fpName!r} in domain {domain!r}"
                        f" to decision {graph.identityOf(pos)} because"
                        f" that decision is in actually in domain"
                        f" {graph.domainFor(pos)!r}."
                    )
        elif isinstance(activate, set):
            for pos in activate:
                if pos not in graph:
                    raise MissingDecisionError(
                        f"There is no decision {pos} at step {step}."
                    )
                if graph.domainFor(pos) != domain:
                    raise ValueError(
                        f"Can't set {graph.identityOf(pos)} as an"
                        f" active decision in domain {domain!r} to"
                        f" decision because that decision is in"
                        f" actually in domain {graph.domainFor(pos)!r}."
                    )
        else:
            raise TypeError(
                f"Domain {domain!r} has no focalization in the"
                f" {'common' if inCommon else 'active'} context,"
                f" and the specified position doesn't imply one:"
                f"\n{activate!r}"
            )

        if focalization == 'singular':
            if activate is None or isinstance(activate, base.DecisionID):
                if activate is not None:
                    targetDomain = graph.domainFor(activate)
                    if activate not in graph:
                        raise MissingDecisionError(
                            f"There is no decision {activate} in the"
                            f" graph at step {step}."
                        )
                    elif targetDomain != domain:
                        raise ValueError(
                            f"At step {step}, decision {activate} cannot"
                            f" be the active decision for domain"
                            f" {repr(domain)} because it is in a"
                            f" different domain ({repr(targetDomain)})."
                        )
                context['activeDecisions'][domain] = activate
            else:
                raise TypeError(
                    f"{'Common' if inCommon else 'Active'} focal"
                    f" context at step {step} has {repr(focalization)}"
                    f" focalization for domain {repr(domain)}, so the"
                    f" active decision must be a single decision or"
                    f" None.\n(You provided: {repr(activate)})"
                )
        elif focalization == 'plural':
            if (
                isinstance(activate, dict)
            and all(
                    isinstance(k, base.FocalPointName)
                    for k in activate.keys()
                )
            and all(
                    v is None or isinstance(v, base.DecisionID)
                    for v in activate.values()
                )
            ):
                for v in activate.values():
                    if v is not None:
                        targetDomain = graph.domainFor(v)
                        if v not in graph:
                            raise MissingDecisionError(
                                f"There is no decision {v} in the graph"
                                f" at step {step}."
                            )
                        elif targetDomain != domain:
                            raise ValueError(
                                f"At step {step}, decision {activate}"
                                f" cannot be an active decision for"
                                f" domain {repr(domain)} because it is"
                                f" in a different domain"
                                f" ({repr(targetDomain)})."
                            )
                context['activeDecisions'][domain] = activate
            else:
                raise TypeError(
                    f"{'Common' if inCommon else 'Active'} focal"
                    f" context at step {step} has {repr(focalization)}"
                    f" focalization for domain {repr(domain)}, so the"
                    f" active decision must be a dictionary mapping"
                    f" focal point names to decision IDs (or Nones)."
                    f"\n(You provided: {repr(activate)})"
                )
        elif focalization == 'spreading':
            if (
                isinstance(activate, set)
            and all(isinstance(x, base.DecisionID) for x in activate)
            ):
                for x in activate:
                    targetDomain = graph.domainFor(x)
                    if x not in graph:
                        raise MissingDecisionError(
                            f"There is no decision {x} in the graph"
                            f" at step {step}."
                        )
                    elif targetDomain != domain:
                        raise ValueError(
                            f"At step {step}, decision {activate}"
                            f" cannot be an active decision for"
                            f" domain {repr(domain)} because it is"
                            f" in a different domain"
                            f" ({repr(targetDomain)})."
                        )
                context['activeDecisions'][domain] = activate
            else:
                raise TypeError(
                    f"{'Common' if inCommon else 'Active'} focal"
                    f" context at step {step} has {repr(focalization)}"
                    f" focalization for domain {repr(domain)}, so the"
                    f" active decision must be a set of decision IDs"
                    f"\n(You provided: {repr(activate)})"
                )
        else:
            raise RuntimeError(
                f"Invalid focalization value {repr(focalization)} for"
                f" domain {repr(domain)} at step {step}."
            )

    def movementAtStep(self, step: int = -1) -> Tuple[
        Union[base.DecisionID, Set[base.DecisionID], None],
        Optional[base.Transition],
        Union[base.DecisionID, Set[base.DecisionID], None]
    ]:
        """
        Given a step number, returns information about the starting
        decision, transition taken, and destination decision for that
        step. Not all steps have all of those, so some items may be
        `None`.

        For steps where there is no action, where a decision is still
        pending, or where the action type is 'focus', 'swap',
        or 'focalize', the result will be (`None`, `None`, `None`),
        unless a primary decision is available in which case the first
        item in the tuple will be that decision. For 'start' actions, the
        starting position and transition will be `None` (again unless the
        step had a primary decision) but the destination will be the ID
        of the node started at.

        Also, if the action taken has multiple potential or actual start
        or end points, these may be sets of decision IDs instead of
        single IDs.

        Note that the primary decision of the starting state is usually
        used as the from-decision, but in some cases an action dictates
        taking a transition from a different decision, and this function
        will return that decision as the from-decision.

        TODO: Examples!

        TODO: Account for bounce/follow/goto effects!!!
        """
        now = self.getSituation(step)
        action = now.action
        graph = now.graph
        primary = now.state['primaryDecision']

        if action is None:
            return (primary, None, None)

        aType = action[0]
        fromID: Optional[base.DecisionID]
        destID: Optional[base.DecisionID]
        transition: base.Transition
        outcomes: List[bool]

        if aType in ('noAction', 'focus', 'swap', 'focalize'):
            return (primary, None, None)
        elif aType == 'start':
            assert len(action) == 7
            where = cast(
                Union[
                    base.DecisionID,
                    Dict[base.FocalPointName, base.DecisionID],
                    Set[base.DecisionID]
                ],
                action[1]
            )
            if isinstance(where, dict):
                where = set(where.values())
            return (primary, None, where)
        elif aType in ('take', 'explore'):
            if (
                (len(action) == 4 or len(action) == 7)
            and isinstance(action[2], base.DecisionID)
            ):
                fromID = action[2]
                assert isinstance(action[3], tuple)
                transition, outcomes = action[3]
                if (
                    action[0] == "explore"
                and isinstance(action[4], base.DecisionID)
                ):
                    destID = action[4]
                else:
                    destID = graph.getDestination(fromID, transition)
                return (fromID, transition, destID)
            elif (
                (len(action) == 3 or len(action) == 6)
            and isinstance(action[1], tuple)
            and isinstance(action[2], base.Transition)
            and len(action[1]) == 3
            and action[1][0] in get_args(base.ContextSpecifier)
            and isinstance(action[1][1], base.Domain)
            and isinstance(action[1][2], base.FocalPointName)
            ):
                fromID = base.resolvePosition(now, action[1])
                if fromID is None:
                    raise InvalidActionError(
                        f"{aType!r} action at step {step} has position"
                        f" {action[1]!r} which cannot be resolved to a"
                        f" decision."
                    )
                transition, outcomes = action[2]
                if (
                    action[0] == "explore"
                and isinstance(action[3], base.DecisionID)
                ):
                    destID = action[3]
                else:
                    destID = graph.getDestination(fromID, transition)
                return (fromID, transition, destID)
            else:
                raise InvalidActionError(
                    f"Malformed {aType!r} action:\n{repr(action)}"
                )
        elif aType == 'warp':
            if len(action) != 3:
                raise InvalidActionError(
                    f"Malformed 'warp' action:\n{repr(action)}"
                )
            dest = action[2]
            assert isinstance(dest, base.DecisionID)
            if action[1] in get_args(base.ContextSpecifier):
                # Unspecified starting point; find active decisions in
                # same domain if primary is None
                if primary is not None:
                    return (primary, None, dest)
                else:
                    toDomain = now.graph.domainFor(dest)
                    # TODO: Could check destination focalization here...
                    active = self.getActiveDecisions(step)
                    sameDomain = set(
                        dID
                        for dID in active
                        if now.graph.domainFor(dID) == toDomain
                    )
                    if len(sameDomain) == 1:
                        return (
                            list(sameDomain)[0],
                            None,
                            dest
                        )
                    else:
                        return (
                            sameDomain,
                            None,
                            dest
                        )
            else:
                if (
                    not isinstance(action[1], tuple)
                or not len(action[1]) == 3
                or not action[1][0] in get_args(base.ContextSpecifier)
                or not isinstance(action[1][1], base.Domain)
                or not isinstance(action[1][2], base.FocalPointName)
                ):
                    raise InvalidActionError(
                        f"Malformed 'warp' action:\n{repr(action)}"
                    )
                return (
                    base.resolvePosition(now, action[1]),
                    None,
                    dest
                )
        else:
            raise InvalidActionError(
                f"Action taken had invalid action type {repr(aType)}:"
                f"\n{repr(action)}"
            )

    def tagStep(
        self,
        tagOrTags: Union[base.Tag, Dict[base.Tag, base.TagValue]],
        tagValue: Union[
            base.TagValue,
            type[base.NoTagValue]
        ] = base.NoTagValue,
        step: int = -1
    ) -> None:
        """
        Adds a tag (or multiple tags) to the current step, or to a
        specific step if `n` is given as an integer rather than the
        default `None`. A tag value should be supplied when a tag is
        given (unless you want to use the default of `1`), but it's a
        `ValueError` to supply a tag value when a dictionary of tags to
        update is provided.
        """
        if isinstance(tagOrTags, base.Tag):
            if tagValue is base.NoTagValue:
                tagValue = 1

            # Not sure why this is necessary...
            tagValue = cast(base.TagValue, tagValue)

            self.getSituation(step).tags.update({tagOrTags: tagValue})
        else:
            self.getSituation(step).tags.update(tagOrTags)

    def annotateStep(
        self,
        annotationOrAnnotations: Union[
            base.Annotation,
            Sequence[base.Annotation]
        ],
        step: Optional[int] = None
    ) -> None:
        """
        Adds an annotation to the current exploration step, or to a
        specific step if `n` is given as an integer rather than the
        default `None`.
        """
        if step is None:
            step = -1
        if isinstance(annotationOrAnnotations, base.Annotation):
            self.getSituation(step).annotations.append(
                annotationOrAnnotations
            )
        else:
            self.getSituation(step).annotations.extend(
                annotationOrAnnotations
            )

    def hasCapability(
        self,
        capability: base.Capability,
        step: Optional[int] = None,
        inCommon: Union[bool, Literal['both']] = "both"
    ) -> bool:
        """
        Returns True if the player currently had the specified
        capability, at the specified exploration step, and False
        otherwise. Checks the current state if no step is given. Does
        NOT return true if the game state means that the player has an
        equivalent for that capability (see
        `hasCapabilityOrEquivalent`).

        Normally, `inCommon` is set to 'both' by default and so if
        either the common `FocalContext` or the active one has the
        capability, this will return `True`. `inCommon` may instead be
        set to `True` or `False` to ask about just the common (or
        active) focal context.
        """
        state = self.getSituation().state
        commonCapabilities = state['common']['capabilities']\
            ['capabilities']  # noqa
        activeCapabilities = state['contexts'][state['activeContext']]\
            ['capabilities']['capabilities']  # noqa

        if inCommon == 'both':
            return (
                capability in commonCapabilities
             or capability in activeCapabilities
            )
        elif inCommon is True:
            return capability in commonCapabilities
        elif inCommon is False:
            return capability in activeCapabilities
        else:
            raise ValueError(
                f"Invalid inCommon value (must be False, True, or"
                f" 'both'; got {repr(inCommon)})."
            )

    def hasCapabilityOrEquivalent(
        self,
        capability: base.Capability,
        step: Optional[int] = None,
        location: Optional[Set[base.DecisionID]] = None
    ) -> bool:
        """
        Works like `hasCapability`, but also returns `True` if the
        player counts as having the specified capability via an equivalence
        that's part of the current graph. As with `hasCapability`, the
        optional `step` argument is used to specify which step to check,
        with the current step being used as the default.

        The `location` set can specify where to start looking for
        mechanisms; if left unspecified active decisions for that step
        will be used.
        """
        if step is None:
            step = -1
        if location is None:
            location = self.getActiveDecisions(step)
        situation = self.getSituation(step)
        return base.hasCapabilityOrEquivalent(
            capability,
            base.RequirementContext(
                state=situation.state,
                graph=situation.graph,
                searchFrom=location
            )
        )

    def gainCapabilityNow(
        self,
        capability: base.Capability,
        inCommon: bool = False
    ) -> None:
        """
        Modifies the current game state to add the specified `Capability`
        to the player's capabilities. No changes are made to the current
        graph.

        If `inCommon` is set to `True` (default is `False`) then the
        capability will be added to the common `FocalContext` and will
        therefore persist even when a focal context switch happens.
        Normally, it will be added to the currently-active focal
        context.
        """
        state = self.getSituation().state
        if inCommon:
            context = state['common']
        else:
            context = state['contexts'][state['activeContext']]
        context['capabilities']['capabilities'].add(capability)

    def loseCapabilityNow(
        self,
        capability: base.Capability,
        inCommon: Union[bool, Literal['both']] = "both"
    ) -> None:
        """
        Modifies the current game state to remove the specified `Capability`
        from the player's capabilities. Does nothing if the player
        doesn't already have that capability.

        By default, this removes the capability from both the common
        capabilities set and the active `FocalContext`'s capabilities
        set, so that afterwards the player will definitely not have that
        capability. However, if you set `inCommon` to either `True` or
        `False`, it will remove the capability from just the common
        capabilities set (if `True`) or just the active capabilities set
        (if `False`). In these cases, removing the capability from just
        one capability set will not actually remove it in terms of the
        `hasCapability` result if it had been present in the other set.
        Set `inCommon` to "both" to use the default behavior explicitly.
        """
        now = self.getSituation()
        if inCommon in ("both", True):
            context = now.state['common']
            try:
                context['capabilities']['capabilities'].remove(capability)
            except KeyError:
                pass
        elif inCommon in ("both", False):
            context = now.state['contexts'][now.state['activeContext']]
            try:
                context['capabilities']['capabilities'].remove(capability)
            except KeyError:
                pass
        else:
            raise ValueError(
                f"Invalid inCommon value (must be False, True, or"
                f" 'both'; got {repr(inCommon)})."
            )

    def tokenCountNow(self, tokenType: base.Token) -> Optional[int]:
        """
        Returns the number of tokens the player currently has of a given
        type. Returns `None` if the player has never acquired or lost
        tokens of that type.

        This method adds together tokens from the common and active
        focal contexts.
        """
        state = self.getSituation().state
        commonContext = state['common']
        activeContext = state['contexts'][state['activeContext']]
        base = commonContext['capabilities']['tokens'].get(tokenType)
        if base is None:
            return activeContext['capabilities']['tokens'].get(tokenType)
        else:
            return base + activeContext['capabilities']['tokens'].get(
                tokenType,
                0
            )

    def adjustTokensNow(
        self,
        tokenType: base.Token,
        amount: int,
        inCommon: bool = False
    ) -> None:
        """
        Modifies the current game state to add the specified number of
        `Token`s of the given type to the player's tokens. No changes are
        made to the current graph. Reduce the number of tokens by
        supplying a negative amount; note that negative token amounts
        are possible.

        By default, the number of tokens for the current active
        `FocalContext` will be adjusted. However, if `inCommon` is set
        to `True`, then the number of tokens for the common context will
        be adjusted instead.
        """
        # TODO: Custom token caps!
        state = self.getSituation().state
        if inCommon:
            context = state['common']
        else:
            context = state['contexts'][state['activeContext']]
        tokens = context['capabilities']['tokens']
        tokens[tokenType] = tokens.get(tokenType, 0) + amount

    def setTokensNow(
        self,
        tokenType: base.Token,
        amount: int,
        inCommon: bool = False
    ) -> None:
        """
        Modifies the current game state to set number of `Token`s of the
        given type to a specific amount, regardless of the old value. No
        changes are made to the current graph.

        By default this sets the number of tokens for the active
        `FocalContext`. But if you set `inCommon` to `True`, it will
        set the number of tokens in the common context instead.
        """
        # TODO: Custom token caps!
        state = self.getSituation().state
        if inCommon:
            context = state['common']
        else:
            context = state['contexts'][state['activeContext']]
        context['capabilities']['tokens'][tokenType] = amount

    def lookupMechanism(
        self,
        mechanism: base.MechanismName,
        step: Optional[int] = None,
        where: Union[
            Tuple[base.AnyDecisionSpecifier, Optional[base.Transition]],
            Collection[base.AnyDecisionSpecifier],
            None
        ] = None
    ) -> base.MechanismID:
        """
        Looks up a mechanism ID by name, in the graph for the specified
        step. The `where` argument specifies where to start looking,
        which helps disambiguate. It can be a tuple with a decision
        specifier and `None` to start from a single decision, or with a
        decision specifier and a transition name to start from either
        end of that transition. It can also be `None` to look at global
        mechanisms and then all decisions directly, although this
        increases the chance of a `MechanismCollisionError`. Finally, it
        can be some other non-tuple collection of decision specifiers to
        start from that set.

        If no step is specified, uses the current step.
        """
        if step is None:
            step = -1
        situation = self.getSituation(step)
        graph = situation.graph
        searchFrom: Collection[base.AnyDecisionSpecifier]
        if where is None:
            searchFrom = set()
        elif isinstance(where, tuple):
            if len(where) != 2:
                raise ValueError(
                    f"Mechanism lookup location was a tuple with an"
                    f" invalid length (must be length-2 if it's a"
                    f" tuple):\n  {repr(where)}"
                )
            where = cast(
                Tuple[base.AnyDecisionSpecifier, Optional[base.Transition]],
                where
            )
            if where[1] is None:
                searchFrom = {graph.resolveDecision(where[0])}
            else:
                searchFrom = graph.bothEnds(where[0], where[1])
        else:  # must be a collection of specifiers
            searchFrom = cast(Collection[base.AnyDecisionSpecifier], where)
        return graph.lookupMechanism(searchFrom, mechanism)

    def mechanismState(
        self,
        mechanism: base.AnyMechanismSpecifier,
        where: Optional[Set[base.DecisionID]] = None,
        step: int = -1
    ) -> Optional[base.MechanismState]:
        """
        Returns the current state for the specified mechanism (or the
        state at the specified step if a step index is given). `where`
        may be provided as a set of decision IDs to indicate where to
        search for the named mechanism, or a mechanism ID may be provided
        in the first place. Mechanism states are properties of a `State`
        but are not associated with focal contexts.
        """
        situation = self.getSituation(step)
        mID = situation.graph.resolveMechanism(mechanism)
        return situation.state['mechanisms'].get(
            mID,
            base.DEFAULT_MECHANISM_STATE
        )

    def setMechanismStateNow(
        self,
        mechanism: base.AnyMechanismSpecifier,
        toState: base.MechanismState,
        where: Optional[Set[base.DecisionID]] = None
    ) -> None:
        """
        Sets the state of the specified mechanism to the specified
        state. Mechanisms can only be in one state at once, so this
        removes any previous states for that mechanism (note that via
        equivalences multiple mechanism states can count as active).

        The mechanism can be any kind of mechanism specifier (see
        `base.AnyMechanismSpecifier`). If it's not a mechanism ID and
        doesn't have its own position information, the 'where' argument
        can be used to hint where to search for the mechanism.
        """
        now = self.getSituation()
        mID = now.graph.resolveMechanism(mechanism, where)
        if mID is None:
            raise MissingMechanismError(
                f"Couldn't find mechanism for {repr(mechanism)}."
            )
        now.state['mechanisms'][mID] = toState

    def skillLevel(
        self,
        skill: base.Skill,
        step: Optional[int] = None
    ) -> Optional[base.Level]:
        """
        Returns the skill level the player had in a given skill at a
        given step, or for the current step if no step is specified.
        Returns `None` if the player had never acquired or lost levels
        in that skill before the specified step (skill level would count
        as 0 in that case).

        This method adds together levels from the common and active
        focal contexts.
        """
        if step is None:
            step = -1
        state = self.getSituation(step).state
        commonContext = state['common']
        activeContext = state['contexts'][state['activeContext']]
        base = commonContext['capabilities']['skills'].get(skill)
        if base is None:
            return activeContext['capabilities']['skills'].get(skill)
        else:
            return base + activeContext['capabilities']['skills'].get(
                skill,
                0
            )

    def adjustSkillLevelNow(
        self,
        skill: base.Skill,
        levels: base.Level,
        inCommon: bool = False
    ) -> None:
        """
        Modifies the current game state to add the specified number of
        `Level`s of the given skill. No changes are made to the current
        graph. Reduce the skill level by supplying negative levels; note
        that negative skill levels are possible.

        By default, the skill level for the current active
        `FocalContext` will be adjusted. However, if `inCommon` is set
        to `True`, then the skill level for the common context will be
        adjusted instead.
        """
        # TODO: Custom level caps?
        state = self.getSituation().state
        if inCommon:
            context = state['common']
        else:
            context = state['contexts'][state['activeContext']]
        skills = context['capabilities']['skills']
        skills[skill] = skills.get(skill, 0) + levels

    def setSkillLevelNow(
        self,
        skill: base.Skill,
        level: base.Level,
        inCommon: bool = False
    ) -> None:
        """
        Modifies the current game state to set `Skill` `Level` for the
        given skill, regardless of the old value. No changes are made to
        the current graph.

        By default this sets the skill level for the active
        `FocalContext`. But if you set `inCommon` to `True`, it will set
        the skill level in the common context instead.
        """
        # TODO: Custom level caps?
        state = self.getSituation().state
        if inCommon:
            context = state['common']
        else:
            context = state['contexts'][state['activeContext']]
        skills = context['capabilities']['skills']
        skills[skill] = level

    def updateRequirementNow(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        requirement: Optional[base.Requirement]
    ) -> None:
        """
        Updates the requirement for a specific transition in a specific
        decision. Use `None` to remove the requirement for that edge.
        """
        if requirement is None:
            requirement = base.ReqNothing()
        self.getSituation().graph.setTransitionRequirement(
            decision,
            transition,
            requirement
        )

    def isTraversable(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.Transition,
        step: int = -1
    ) -> bool:
        """
        Returns True if the specified transition from the specified
        decision had its requirement satisfied by the game state at the
        specified step (or at the current step if no step is specified).
        Raises an `IndexError` if the specified step doesn't exist, and
        a `KeyError` if the decision or transition specified does not
        exist in the `DecisionGraph` at that step.
        """
        situation = self.getSituation(step)
        req = situation.graph.getTransitionRequirement(decision, transition)
        ctx = base.contextForTransition(situation, decision, transition)
        fromID = situation.graph.resolveDecision(decision)
        return (
            req.satisfied(ctx)
        and (fromID, transition) not in situation.state['deactivated']
        )

    def applyTransitionEffect(
        self,
        whichEffect: base.EffectSpecifier,
        moveWhich: Optional[base.FocalPointName] = None
    ) -> Optional[base.DecisionID]:
        """
        Applies an effect attached to a transition, taking charges and
        delay into account based on the current `Situation`.
        Modifies the effect's trigger count (but may not actually
        trigger the effect if the charges and/or delay values indicate
        not to; see `base.doTriggerEffect`).

        If a specific focal point in a plural-focalized domain is
        triggering the effect, the focal point name should be specified
        via `moveWhich` so that goto `Effect`s can know which focal
        point to move when it's not explicitly specified in the effect.
        TODO: Test this!

        Returns None most of the time, but if a 'goto', 'bounce', or
        'follow' effect was applied, it returns the decision ID for that
        effect's destination, which would override a transition's normal
        destination. If it returns a destination ID, then the exploration
        state will already have been updated to set the position there,
        and further position updates are not needed.

        Note that transition effects which update active decisions will
        also update the exploration status of those decisions to
        'exploring' if they had been in an unvisited status (see
        `updatePosition` and `hasBeenVisited`).

        Note: callers should immediately update situation-based variables
        that might have been changes by a 'revert' effect.
        """
        now = self.getSituation()
        effect, triggerCount = base.doTriggerEffect(now, whichEffect)
        if triggerCount is not None:
            return self.applyExtraneousEffect(
                effect,
                where=whichEffect[:2],
                moveWhich=moveWhich
            )
        else:
            return None

    def applyExtraneousEffect(
        self,
        effect: base.Effect,
        where: Optional[
            Tuple[base.AnyDecisionSpecifier, Optional[base.Transition]]
        ] = None,
        moveWhich: Optional[base.FocalPointName] = None,
        challengePolicy: base.ChallengePolicy = "specified"
    ) -> Optional[base.DecisionID]:
        """
        Applies a single extraneous effect to the state & graph,
        *without* accounting for charges or delay values, since the
        effect is not part of the graph (use `applyTransitionEffect` to
        apply effects that are attached to transitions, which is almost
        always the function you should be using). An associated
        transition for the extraneous effect can be supplied using the
        `where` argument, and effects like 'deactivate' and 'edit' will
        affect it (but the effect's charges and delay values will still
        be ignored).

        If the effect would change the destination of a transition, the
        altered destination ID is returned: 'bounce' effects return the
        provided decision part of `where`, 'goto' effects return their
        target, and 'follow' effects return the destination followed to
        (possibly via chained follows in the extreme case). In all other
        cases, `None` is returned indicating no change to a normal
        destination.

        If a specific focal point in a plural-focalized domain is
        triggering the effect, the focal point name should be specified
        via `moveWhich` so that goto `Effect`s can know which focal
        point to move when it's not explicitly specified in the effect.
        TODO: Test this!

        Note that transition effects which update active decisions will
        also update the exploration status of those decisions to
        'exploring' if they had been in an unvisited status and will
        remove any 'unconfirmed' tag they might still have (see
        `updatePosition` and `hasBeenVisited`).

        The given `challengePolicy` is applied when traversing further
        transitions due to 'follow' effects.

        Note: Anyone calling `applyExtraneousEffect` should update any
        situation-based variables immediately after the call, as a
        'revert' effect may have changed the current graph and/or state.
        """
        typ = effect['type']
        value = effect['value']
        applyTo = effect['applyTo']
        inCommon = applyTo == 'common'

        now = self.getSituation()

        if where is not None:
            if where[1] is not None:
                searchFrom = now.graph.bothEnds(where[0], where[1])
            else:
                searchFrom = {now.graph.resolveDecision(where[0])}
        else:
            searchFrom = None

        # Note: Delay and charges are ignored!

        if typ in ("gain", "lose"):
            value = cast(
                Union[
                    base.Capability,
                    Tuple[base.Token, base.TokenCount],
                    Tuple[Literal['skill'], base.Skill, base.Level],
                ],
                value
            )
            if isinstance(value, base.Capability):
                if typ == "gain":
                    self.gainCapabilityNow(value, inCommon)
                else:
                    self.loseCapabilityNow(value, inCommon)
            elif len(value) == 2:  # must be a token, amount pair
                token, amount = cast(
                    Tuple[base.Token, base.TokenCount],
                    value
                )
                if typ == "lose":
                    amount *= -1
                self.adjustTokensNow(token, amount, inCommon)
            else:  # must be a 'skill', skill, level triple
                _, skill, levels = cast(
                    Tuple[Literal['skill'], base.Skill, base.Level],
                    value
                )
                if typ == "lose":
                    levels *= -1
                self.adjustSkillLevelNow(skill, levels, inCommon)

        elif typ == "set":
            value = cast(
                Union[
                    Tuple[base.Token, base.TokenCount],
                    Tuple[base.AnyMechanismSpecifier, base.MechanismState],
                    Tuple[Literal['skill'], base.Skill, base.Level],
                ],
                value
            )
            if len(value) == 2:  # must be a token or mechanism pair
                if isinstance(value[1], base.TokenCount):  # token
                    token, amount = cast(
                        Tuple[base.Token, base.TokenCount],
                        value
                    )
                    self.setTokensNow(token, amount, inCommon)
                else: # mechanism
                    mechanism, state = cast(
                        Tuple[
                            base.AnyMechanismSpecifier,
                            base.MechanismState
                        ],
                        value
                    )
                    self.setMechanismStateNow(mechanism, state, searchFrom)
            else:  # must be a 'skill', skill, level triple
                _, skill, level = cast(
                    Tuple[Literal['skill'], base.Skill, base.Level],
                    value
                )
                self.setSkillLevelNow(skill, level, inCommon)

        elif typ == "toggle":
            # Length-1 list just toggles a capability on/off based on current
            # state (not attending to equivalents):
            if isinstance(value, List):  # capabilities list
                value = cast(List[base.Capability], value)
                if len(value) == 0:
                    raise ValueError(
                        "Toggle effect has empty capabilities list."
                    )
                if len(value) == 1:
                    capability = value[0]
                    if self.hasCapability(capability, inCommon=False):
                        self.loseCapabilityNow(capability, inCommon=False)
                    else:
                        self.gainCapabilityNow(capability)
                else:
                    # Otherwise toggle all powers off, then one on,
                    # based on the first capability that's currently on.
                    # Note we do NOT count equivalences.

                    # Find first capability that's on:
                    firstIndex: Optional[int] = None
                    for i, capability in enumerate(value):
                        if self.hasCapability(capability):
                            firstIndex = i
                            break

                    # Turn them all off:
                    for capability in value:
                        self.loseCapabilityNow(capability, inCommon=False)
                        # TODO: inCommon for the check?

                    if firstIndex is None:
                        self.gainCapabilityNow(value[0])
                    else:
                        self.gainCapabilityNow(
                            value[(firstIndex + 1) % len(value)]
                        )
            else:  # must be a mechanism w/ states list
                mechanism, states = cast(
                    Tuple[
                        base.AnyMechanismSpecifier,
                        List[base.MechanismState]
                    ],
                    value
                )
                currentState = self.mechanismState(mechanism, searchFrom)
                if len(states) == 1:
                    if currentState == states[0]:
                        # default alternate state
                        self.setMechanismStateNow(
                            mechanism,
                            base.DEFAULT_MECHANISM_STATE,
                            searchFrom
                        )
                    else:
                        self.setMechanismStateNow(
                            mechanism,
                            states[0],
                            searchFrom
                        )
                else:
                    # Find our position in the list, if any
                    try:
                        currentIndex = states.index(cast(str, currentState))
                        # Cast here just because we know that None will
                        # raise a ValueError but we'll catch it, and we
                        # want to suppress the mypy warning about the
                        # option
                    except ValueError:
                        currentIndex = len(states) - 1
                    # Set next state in list as current state
                    nextIndex = (currentIndex + 1) % len(states)
                    self.setMechanismStateNow(
                        mechanism,
                        states[nextIndex],
                        searchFrom
                    )

        elif typ == "deactivate":
            if where is None or where[1] is None:
                raise ValueError(
                    "Can't apply a deactivate effect without specifying"
                    " which transition it applies to."
                )

            decision, transition = cast(
                Tuple[base.AnyDecisionSpecifier, base.Transition],
                where
            )

            dID = now.graph.resolveDecision(decision)
            now.state['deactivated'].add((dID, transition))

        elif typ == "edit":
            value = cast(List[List[commands.Command]], value)
            # If there are no blocks, do nothing
            if len(value) > 0:
                # Apply the first block of commands and then rotate the list
                scope: commands.Scope = {}
                if where is not None:
                    here: base.DecisionID = now.graph.resolveDecision(
                        where[0]
                    )
                    outwards: Optional[base.Transition] = where[1]
                    scope['@'] = here
                    scope['@t'] = outwards
                    if outwards is not None:
                        reciprocal = now.graph.getReciprocal(here, outwards)
                        destination = now.graph.getDestination(here, outwards)
                    else:
                        reciprocal = None
                        destination = None
                    scope['@r'] = reciprocal
                    scope['@d'] = destination
                self.runCommandBlock(value[0], scope)
                value.append(value.pop(0))

        elif typ == "goto":
            if isinstance(value, base.DecisionSpecifier):
                target: base.AnyDecisionSpecifier = value
                # use moveWhich provided as argument
            elif isinstance(value, tuple):
                target, moveWhich = cast(
                    Tuple[base.AnyDecisionSpecifier, base.FocalPointName],
                    value
                )
            else:
                target = cast(base.AnyDecisionSpecifier, value)
                # use moveWhich provided as argument

            destID = now.graph.resolveDecision(target)
            base.updatePosition(now, destID, applyTo, moveWhich)
            return destID

        elif typ == "bounce":
            # Just need to let the caller know they should cancel
            if where is None:
                raise ValueError(
                    "Can't apply a 'bounce' effect without a position"
                    " to apply it from."
                )
            return now.graph.resolveDecision(where[0])

        elif typ == "follow":
            if where is None:
                raise ValueError(
                    f"Can't follow transition {value!r} because there"
                    f" is no position information when applying the"
                    f" effect."
                )
            if where[1] is not None:
                followFrom = now.graph.getDestination(where[0], where[1])
                if followFrom is None:
                    raise ValueError(
                        f"Can't follow transition {value!r} because the"
                        f" position information specifies transition"
                        f" {where[1]!r} from decision"
                        f" {now.graph.identityOf(where[0])} but that"
                        f" transition does not exist."
                    )
            else:
                followFrom = now.graph.resolveDecision(where[0])

            following = cast(base.Transition, value)

            followTo = now.graph.getDestination(followFrom, following)

            if followTo is None:
                raise ValueError(
                    f"Can't follow transition {following!r} because"
                    f" that transition doesn't exist at the specified"
                    f" destination {now.graph.identityOf(followFrom)}."
                )

            if self.isTraversable(followFrom, following):  # skip if not
                # Perform initial position update before following new
                # transition:
                base.updatePosition(
                    now,
                    followFrom,
                    applyTo,
                    moveWhich
                )

                # Apply consequences of followed transition
                fullFollowTo = self.applyTransitionConsequence(
                    followFrom,
                    following,
                    moveWhich,
                    challengePolicy
                )

                # Now update to end of followed transition
                if fullFollowTo is None:
                    base.updatePosition(
                        now,
                        followTo,
                        applyTo,
                        moveWhich
                    )
                    fullFollowTo = followTo

                # Skip the normal update: we've taken care of that plus more
                return fullFollowTo
            else:
                # Normal position updates still applies since follow
                # transition wasn't possible
                return None

        elif typ == "save":
            assert isinstance(value, base.SaveSlot)
            now.saves[value] = copy.deepcopy((now.graph, now.state))

        else:
            raise ValueError(f"Invalid effect type {typ!r}.")

        return None  # default return value if we didn't return above

    def applyExtraneousConsequence(
        self,
        consequence: base.Consequence,
        where: Optional[
            Tuple[base.AnyDecisionSpecifier, Optional[base.Transition]]
        ] = None,
        moveWhich: Optional[base.FocalPointName] = None
    ) -> Optional[base.DecisionID]:
        """
        Applies an extraneous consequence not associated with a
        transition. Unlike `applyTransitionConsequence`, the provided
        `base.Consequence` must already have observed outcomes (see
        `base.observeChallengeOutcomes`). Returns the decision ID for a
        decision implied by a goto, follow, or bounce effect, or `None`
        if no effect implies a destination.

        The `where` and `moveWhich` optional arguments specify which
        decision and/or transition to use as the application position,
        and/or which focal point to move. This affects mechanism lookup
        as well as the end position when 'follow' effects are used.
        Specifically:

        - A 'follow' trigger will search for transitions to follow from
            the destination of the specified transition, or if only a
            decision was supplied, from that decision.
        - Mechanism lookups will start with both ends of the specified
            transition as their search field (or with just the specified
            decision if no transition is included).

        'bounce' effects will cause an error unless position information
        is provided, and will set the position to the base decision
        provided in `where`.

        Note: callers should update any situation-based variables
        immediately after calling this as a 'revert' effect could change
        the current graph and/or state and other changes could get lost
        if they get applied to a stale graph/state.

        # TODO: Examples for goto and follow effects.
        """
        now = self.getSituation()
        searchFrom = set()
        if where is not None:
            if where[1] is not None:
                searchFrom = now.graph.bothEnds(where[0], where[1])
            else:
                searchFrom = {now.graph.resolveDecision(where[0])}

        context = base.RequirementContext(
            state=now.state,
            graph=now.graph,
            searchFrom=searchFrom
        )

        effectIndices = base.observedEffects(context, consequence)
        destID = None
        for index in effectIndices:
            effect = base.consequencePart(consequence, index)
            if not isinstance(effect, dict) or 'value' not in effect:
                raise RuntimeError(
                    f"Invalid effect index {index}: Consequence part at"
                    f" that index is not an Effect. Got:\n{effect}"
                )
            effect = cast(base.Effect, effect)
            destID = self.applyExtraneousEffect(
                effect,
                where,
                moveWhich
            )
            # technically this variable is not used later in this
            # function, but the `applyExtraneousEffect` call means it
            # needs an update, so we're doing that in case someone later
            # adds code to this function that uses 'now' after this
            # point.
            now = self.getSituation()

        return destID

    def applyTransitionConsequence(
        self,
        decision: base.AnyDecisionSpecifier,
        transition: base.AnyTransition,
        moveWhich: Optional[base.FocalPointName] = None,
        policy: base.ChallengePolicy = "specified",
        fromIndex: Optional[int] = None,
        toIndex: Optional[int] = None
    ) -> Optional[base.DecisionID]:
        """
        Applies the effects of the specified transition to the current
        graph and state, possibly overriding observed outcomes using
        outcomes specified as part of a `base.TransitionWithOutcomes`.

        The `where` and `moveWhich` function serve the same purpose as
        for `applyExtraneousEffect`. If `where` is `None`, then the
        effects will be applied as extraneous effects, meaning that
        their delay and charges values will be ignored and their trigger
        count will not be tracked. If `where` is supplied

        Returns either None to indicate that the position update for the
        transition should apply as usual, or a decision ID indicating
        another destination which has already been applied by a
        transition effect.

        If `fromIndex` and/or `toIndex` are specified, then only effects
        which have indices between those two (inclusive) will be
        applied, and other effects will neither apply nor be updated in
        any way. Note that `onlyPart` does not override the challenge
        policy: if the effects in the specified part are not applied due
        to a challenge outcome, they still won't happen, including
        challenge outcomes outside of that part. Also, outcomes for
        challenges of the entire consequence are re-observed if the
        challenge policy implies it.

        Note: Anyone calling this should update any situation-based
        variables immediately after the call, as a 'revert' effect may
        have changed the current graph and/or state.
        """
        now = self.getSituation()
        dID = now.graph.resolveDecision(decision)

        transitionName, outcomes = base.nameAndOutcomes(transition)

        searchFrom = set()
        searchFrom = now.graph.bothEnds(dID, transitionName)

        context = base.RequirementContext(
            state=now.state,
            graph=now.graph,
            searchFrom=searchFrom
        )

        consequence = now.graph.getConsequence(dID, transitionName)

        # Make sure that challenge outcomes are known
        if policy != "specified":
            base.resetChallengeOutcomes(consequence)
        useUp = outcomes[:]
        base.observeChallengeOutcomes(
            context,
            consequence,
            location=searchFrom,
            policy=policy,
            knownOutcomes=useUp
        )
        if len(useUp) > 0:
            raise ValueError(
                f"More outcomes specified than challenges observed in"
                f" consequence:\n{consequence}"
                f"\nRemaining outcomes:\n{useUp}"
            )

        # Figure out which effects apply, and apply each of them
        effectIndices = base.observedEffects(context, consequence)
        if fromIndex is None:
            fromIndex = 0

        altDest = None
        for index in effectIndices:
            if (
                index >= fromIndex
            and (toIndex is None or index <= toIndex)
            ):
                thisDest = self.applyTransitionEffect(
                    (dID, transitionName, index),
                    moveWhich
                )
                if thisDest is not None:
                    altDest = thisDest
                # TODO: What if this updates state with 'revert' to a
                # graph that doesn't contain the same effects?
                # TODO: Update 'now' and 'context'?!
        return altDest

    def allDecisions(self) -> List[base.DecisionID]:
        """
        Returns the list of all decisions which existed at any point
        within the exploration. Example:

        >>> ex = DiscreteExploration()
        >>> ex.start('A')
        0
        >>> ex.observe('A', 'right')
        1
        >>> ex.explore('right', 'B', 'left')
        1
        >>> ex.observe('B', 'right')
        2
        >>> ex.allDecisions()  # 'A', 'B', and the unnamed 'right of B'
        [0, 1, 2]
        """
        seen = set()
        result = []
        for situation in self:
            for decision in situation.graph:
                if decision not in seen:
                    result.append(decision)
                    seen.add(decision)

        return result

    def allExploredDecisions(self) -> List[base.DecisionID]:
        """
        Returns the list of all decisions which existed at any point
        within the exploration, excluding decisions whose highest
        exploration status was `noticed` or lower. May still include
        decisions which don't exist in the final situation's graph due to
        things like decision merging. Example:

        >>> ex = DiscreteExploration()
        >>> ex.start('A')
        0
        >>> ex.observe('A', 'right')
        1
        >>> ex.explore('right', 'B', 'left')
        1
        >>> ex.observe('B', 'right')
        2
        >>> graph = ex.getSituation().graph
        >>> graph.addDecision('C')  # add isolated decision; doesn't set status
        3
        >>> ex.hasBeenVisited('C')
        False
        >>> ex.allExploredDecisions()
        [0, 1]
        >>> ex.setExplorationStatus('C', 'exploring')
        >>> ex.allExploredDecisions()  # 2 is the decision right from 'B'
        [0, 1, 3]
        >>> ex.setExplorationStatus('A', 'explored')
        >>> ex.allExploredDecisions()
        [0, 1, 3]
        >>> ex.setExplorationStatus('A', 'unknown')
        >>> # remains visisted in an earlier step
        >>> ex.allExploredDecisions()
        [0, 1, 3]
        >>> ex.setExplorationStatus('C', 'unknown')  # not explored earlier
        >>> ex.allExploredDecisions()  # 2 is the decision right from 'B'
        [0, 1]
        """
        seen = set()
        result = []
        for situation in self:
            graph = situation.graph
            for decision in graph:
                if (
                    decision not in seen
                and base.hasBeenVisited(situation, decision)
                ):
                    result.append(decision)
                    seen.add(decision)

        return result

    def allVisitedDecisions(self) -> List[base.DecisionID]:
        """
        Returns the list of all decisions which existed at any point
        within the exploration and which were visited at least once.
        Usually all of these will be present in the final situation's
        graph, but sometimes merging or other factors means there might
        be some that won't be. Being present on the game state's 'active'
        list in a step for its domain is what counts as "being visited,"
        which means that nodes which were passed through directly via a
        'follow' effect won't be counted, for example.

        This should usually correspond with the absence of the
        'unconfirmed' tag.

        Example:

        >>> ex = DiscreteExploration()
        >>> ex.start('A')
        0
        >>> ex.observe('A', 'right')
        1
        >>> ex.explore('right', 'B', 'left')
        1
        >>> ex.observe('B', 'right')
        2
        >>> ex.getSituation().graph.addDecision('C')  # add isolated decision
        3
        >>> av = ex.allVisitedDecisions()
        >>> av
        [0, 1]
        >>> all(  # no decisions in the 'visited' list are tagged
        ...     'unconfirmed' not in ex.getSituation().graph.decisionTags(d)
        ...     for d in av
        ... )
        True
        >>> graph = ex.getSituation().graph
        >>> 'unconfirmed' in graph.decisionTags(0)
        False
        >>> 'unconfirmed' in graph.decisionTags(1)
        False
        >>> 'unconfirmed' in graph.decisionTags(2)
        True
        >>> 'unconfirmed' in graph.decisionTags(3)  # not tagged; not explored
        False
        """
        seen = set()
        result = []
        for step in range(len(self)):
            active = self.getActiveDecisions(step)
            for dID in active:
                if dID not in seen:
                    result.append(dID)
                    seen.add(dID)

        return result

    def start(
        self,
        decision: base.AnyDecisionSpecifier,
        startCapabilities: Optional[base.CapabilitySet] = None,
        setMechanismStates: Optional[
            Dict[base.MechanismID, base.MechanismState]
        ] = None,
        setCustomState: Optional[dict] = None,
        decisionType: base.DecisionType = "imposed"
    ) -> base.DecisionID:
        """
        Sets the initial position information for a newly-relevant
        domain for the current focal context. Creates a new decision
        if the decision is specified by name or `DecisionSpecifier` and
        that decision doesn't already exist. Returns the decision ID for
        the newly-placed decision (or for the specified decision if it
        already existed).

        Raises a `BadStart` error if the current focal context already
        has position information for the specified domain.

        - The given `startCapabilities` replaces any existing
            capabilities for the current focal context, although you can
            leave it as the default `None` to avoid that and retain any
            capabilities that have been set up already.
        - The given `setMechanismStates` and `setCustomState`
            dictionaries override all previous mechanism states & custom
            states in the new situation. Leave these as the default
            `None` to maintain those states.
        - If created, the decision will be placed in the DEFAULT_DOMAIN
            domain unless it's specified as a `base.DecisionSpecifier`
            with a domain part, in which case that domain is used.
        - If specified as a `base.DecisionSpecifier` with a zone part
            and a new decision needs to be created, the decision will be
            added to that zone, creating it at level 0 if necessary,
            although otherwise no zone information will be changed.
        - Resets the decision type to "pending" and the action taken to
            `None`. Sets the decision type of the previous situation to
            'imposed' (or the specified `decisionType`) and sets an
            appropriate 'start' action for that situation.
        - Tags the step with 'start'.
        - Even in a plural- or spreading-focalized domain, you still need
            to pick one decision to start at.
        """
        now = self.getSituation()

        startID = now.graph.getDecision(decision)
        zone = None
        domain = base.DEFAULT_DOMAIN
        if startID is None:
            if isinstance(decision, base.DecisionID):
                raise MissingDecisionError(
                    f"Cannot start at decision {decision} because no"
                    f" decision with that ID exists. Supply a name or"
                    f" DecisionSpecifier if you need the start decision"
                    f" to be created automatically."
                )
            elif isinstance(decision, base.DecisionName):
                decision = base.DecisionSpecifier(
                    domain=None,
                    zone=None,
                    name=decision
                )
            startID = now.graph.addDecision(
                decision.name,
                domain=decision.domain
            )
            zone = decision.zone
            if decision.domain is not None:
                domain = decision.domain

        if zone is not None:
            if now.graph.getZoneInfo(zone) is None:
                now.graph.createZone(zone, 0)
            now.graph.addDecisionToZone(startID, zone)

        action: base.ExplorationAction = (
            'start',
            startID,
            startID,
            domain,
            startCapabilities,
            setMechanismStates,
            setCustomState
        )

        self.advanceSituation(action, decisionType)

        return startID

    def hasBeenVisited(
        self,
        decision: base.AnyDecisionSpecifier,
        step: int = -1
    ):
        """
        Returns whether or not the specified decision has been visited in
        the specified step (default current step).
        """
        return base.hasBeenVisited(self.getSituation(step), decision)

    def setExplorationStatus(
        self,
        decision: base.AnyDecisionSpecifier,
        status: base.ExplorationStatus,
        upgradeOnly: bool = False
    ):
        """
        Updates the current exploration status of a specific decision in
        the current situation. If `upgradeOnly` is true (default is
        `False` then the update will only apply if the new exploration
        status counts as 'more-explored' than the old one (see
        `base.moreExplored`).
        """
        base.setExplorationStatus(
            self.getSituation(),
            decision,
            status,
            upgradeOnly
        )

    def getExplorationStatus(
        self,
        decision: base.AnyDecisionSpecifier,
        step: int = -1
    ):
        """
        Returns the exploration status of the specified decision at the
        specified step (default is last step). Decisions whose
        exploration status has never been set will have a default status
        of 'unknown'.
        """
        situation = self.getSituation(step)
        dID = situation.graph.resolveDecision(decision)
        return situation.state['exploration'].get(dID, 'unknown')

    def deduceTransitionDetailsAtStep(
        self,
        step: int,
        transition: base.Transition,
        fromDecision: Optional[base.AnyDecisionSpecifier] = None,
        whichFocus: Optional[base.FocalPointSpecifier] = None,
        inCommon: Union[bool, Literal["auto"]] = "auto"
    ) -> Tuple[
        base.ContextSpecifier,
        base.DecisionID,
        base.DecisionID,
        Optional[base.FocalPointSpecifier]
    ]:
        """
        Given just a transition name which the player intends to take in
        a specific step, deduces the `ContextSpecifier` for which
        context should be updated, the source and destination
        `DecisionID`s for the transition, and if the destination
        decision's domain is plural-focalized, the `FocalPointName`
        specifying which focal point should be moved.

        Because many of those things are ambiguous, you may get an
        `AmbiguousTransitionError` when things are underspecified, and
        there are options for specifying some of the extra information
        directly:

        - `fromDecision` may be used to specify the source decision.
        - `whichFocus` may be used to specify the focal point (within a
            particular context/domain) being updated. When focal point
            ambiguity remains and this is unspecified, the
            alphabetically-earliest relevant focal point will be used
            (either among all focal points which activate the source
            decision, if there are any, or among all focal points for
            the entire domain of the destination decision).
        - `inCommon` (a `ContextSpecifier`) may be used to specify which
            context to update. The default of "auto" will cause the
            active context to be selected unless it does not activate
            the source decision, in which case the common context will
            be selected.

        A `MissingDecisionError` will be raised if there are no current
        active decisions (e.g., before `start` has been called), and a
        `MissingTransitionError` will be raised if the listed transition
        does not exist from any active decision (or from the specified
        decision if `fromDecision` is used).
        """
        now = self.getSituation(step)
        active = self.getActiveDecisions(step)
        if len(active) == 0:
            raise MissingDecisionError(
                f"There are no active decisions from which transition"
                f" {repr(transition)} could be taken at step {step}."
            )

        # All source/destination decision pairs for transitions with the
        # given transition name.
        allDecisionPairs: Dict[base.DecisionID, base.DecisionID] = {}

        # TODO: When should we be trimming the active decisions to match
        # any alterations to the graph?
        for dID in active:
            outgoing = now.graph.destinationsFrom(dID)
            if transition in outgoing:
                allDecisionPairs[dID] = outgoing[transition]

        if len(allDecisionPairs) == 0:
            raise MissingTransitionError(
                f"No transitions named {repr(transition)} are outgoing"
                f" from active decisions at step {step}."
                f"\nActive decisions are:"
                f"\n{now.graph.namesListing(active)}"
            )

        if (
            fromDecision is not None
        and fromDecision not in allDecisionPairs
        ):
            raise MissingTransitionError(
                f"{fromDecision} was specified as the source decision"
                f" for traversing transition {repr(transition)} but"
                f" there is no transition of that name from that"
                f" decision at step {step}."
                f"\nValid source decisions are:"
                f"\n{now.graph.namesListing(allDecisionPairs)}"
            )
        elif fromDecision is not None:
            fromID = now.graph.resolveDecision(fromDecision)
            destID = allDecisionPairs[fromID]
            fromDomain = now.graph.domainFor(fromID)
        elif len(allDecisionPairs) == 1:
            fromID, destID = list(allDecisionPairs.items())[0]
            fromDomain = now.graph.domainFor(fromID)
        else:
            fromID = None
            destID = None
            fromDomain = None
            # Still ambiguous; resolve this below

        # Use whichFocus if provided
        if whichFocus is not None:
            # Type/value check for whichFocus
            if (
                not isinstance(whichFocus, tuple)
             or len(whichFocus) != 3
             or whichFocus[0] not in ("active", "common")
             or not isinstance(whichFocus[1], base.Domain)
             or not isinstance(whichFocus[2], base.FocalPointName)
            ):
                raise ValueError(
                    f"Invalid whichFocus value {repr(whichFocus)}."
                    f"\nMust be a length-3 tuple with 'active' or 'common'"
                    f" as the first element, a Domain as the second"
                    f" element, and a FocalPointName as the third"
                    f" element."
                )

            # Resolve focal point specified
            fromID = base.resolvePosition(
                now,
                whichFocus
            )
            if fromID is None:
                raise MissingTransitionError(
                    f"Focal point {repr(whichFocus)} was specified as"
                    f" the transition source, but that focal point does"
                    f" not have a position."
                )
            else:
                destID = now.graph.destination(fromID, transition)
                fromDomain = now.graph.domainFor(fromID)

        elif fromID is None:  # whichFocus is None, so it can't disambiguate
            raise AmbiguousTransitionError(
                f"Transition {repr(transition)} was selected for"
                f" disambiguation, but there are multiple transitions"
                f" with that name from currently-active decisions, and"
                f" neither fromDecision nor whichFocus adequately"
                f" disambiguates the specific transition taken."
                f"\nValid source decisions at step {step} are:"
                f"\n{now.graph.namesListing(allDecisionPairs)}"
            )

        # At this point, fromID, destID, and fromDomain have
        # been resolved.
        if fromID is None or destID is None or fromDomain is None:
            raise RuntimeError(
                f"One of fromID, destID, or fromDomain was None after"
                f" disambiguation was finished:"
                f"\nfromID: {fromID}, destID: {destID}, fromDomain:"
                f" {repr(fromDomain)}"
            )

        # Now figure out which context activated the source so we know
        # which focal point we're moving:
        context = self.getActiveContext()
        active = base.activeDecisionSet(context)
        using: base.ContextSpecifier = "active"
        if fromID not in active:
            context = self.getCommonContext(step)
            using = "common"

        destDomain = now.graph.domainFor(destID)
        if (
            whichFocus is None
        and base.getDomainFocalization(context, destDomain) == 'plural'
        ):
            # Need to figure out which focal point is moving; use the
            # alphabetically earliest one that's positioned at the
            # fromID, or just the earliest one overall if none of them
            # are there.
            contextFocalPoints: Dict[
                base.FocalPointName,
                Optional[base.DecisionID]
            ] = cast(
                Dict[base.FocalPointName, Optional[base.DecisionID]],
                context['activeDecisions'][destDomain]
            )
            if not isinstance(contextFocalPoints, dict):
                raise RuntimeError(
                    f"Active decisions specifier for domain"
                    f" {repr(destDomain)} with plural focalization has"
                    f" a non-dictionary value."
                )

            if fromDomain == destDomain:
                focalCandidates = [
                    fp
                    for fp, pos in contextFocalPoints.items()
                    if pos == fromID
                ]
            else:
                focalCandidates = list(contextFocalPoints)

            whichFocus = (using, destDomain, min(focalCandidates))

        # Now whichFocus has been set if it wasn't already specified;
        # might still be None if it's not relevant.
        return (using, fromID, destID, whichFocus)

    def advanceSituation(
        self,
        action: base.ExplorationAction,
        decisionType: base.DecisionType = "active",
        challengePolicy: base.ChallengePolicy = "specified"
    ) -> Tuple[base.Situation, Set[base.DecisionID]]:
        """
        Given an `ExplorationAction`, sets that as the action taken in
        the current situation, and adds a new situation with the results
        of that action. A `DoubleActionError` will be raised if the
        current situation already has an action specified, and/or has a
        decision type other than 'pending'. By default the type of the
        decision will be 'active' but another `DecisionType` can be
        specified via the `decisionType` parameter.

        If the action specified is `('noAction',)`, then the new
        situation will be a copy of the old one; this represents waiting
        or being at an ending (a decision type other than 'pending'
        should be used).

        Although `None` can appear as the action entry in situations
        with pending decisions, you cannot call `advanceSituation` with
        `None` as the action.

        If the action includes taking a transition whose requirements
        are not satisfied, the transition will still be taken (and any
        consequences applied) but a `TransitionBlockedWarning` will be
        issued.

        A `ChallengePolicy` may be specified, the default is 'specified'
        which requires that outcomes are pre-specified. If any other
        policy is set, the challenge outcomes will be reset before
        re-resolving them according to the provided policy.

        The new situation will have decision type 'pending' and `None`
        as the action.

        The new situation created as a result of the action is returned,
        along with the set of destination decision IDs, including
        possibly a modified destination via 'bounce', 'goto', and/or
        'follow' effects. For actions that don't have a destination, the
        second part of the returned tuple will be an empty set. Multiple
        IDs may be in the set when using a start action in a plural- or
        spreading-focalized domain, for example.

        If the action updates active decisions (including via transition
        effects) this will also update the exploration status of those
        decisions to 'exploring' if they had been in an unvisited
        status (see `updatePosition` and `hasBeenVisited`). This
        includes decisions traveled through but not ultimately arrived
        at via 'follow' effects.

        If any decisions are active in the `ENDINGS_DOMAIN`, attempting
        to 'warp', 'explore', 'take', or 'start' will raise an
        `InvalidActionError`.
        """
        now = self.getSituation()
        if now.type != 'pending' or now.action is not None:
            raise DoubleActionError(
                f"Attempted to take action {repr(action)} at step"
                f" {len(self) - 1}, but an action and/or decision type"
                f" had already been specified:"
                f"\nAction: {repr(now.action)}"
                f"\nType: {repr(now.type)}"
            )

        # Update the now situation to add in the decision type and
        # action taken:
        revised = base.Situation(
            now.graph,
            now.state,
            decisionType,
            action,
            now.saves,
            now.tags,
            now.annotations
        )
        self.situations[-1] = revised

        # Separate update process when reverting (this branch returns)
        if (
            action is not None
        and isinstance(action, tuple)
        and len(action) == 3
        and action[0] == 'revertTo'
        and isinstance(action[1], base.SaveSlot)
        and isinstance(action[2], set)
        and all(isinstance(x, str) for x in action[2])
        ):
            _, slot, aspects = action
            if slot not in now.saves:
                raise KeyError(
                    f"Cannot load save slot {slot!r} because no save"
                    f" data has been established for that slot."
                )
            load = now.saves[slot]
            rGraph, rState = base.revertedState(
                (now.graph, now.state),
                load,
                aspects
            )
            reverted = base.Situation(
                graph=rGraph,
                state=rState,
                type='pending',
                action=None,
                saves=copy.deepcopy(now.saves),
                tags={},
                annotations=[]
            )
            self.situations.append(reverted)
            # Apply any active triggers (edits reverted)
            self.applyActiveTriggers()
            # Figure out destinations set to return
            newDestinations = set()
            newPr = rState['primaryDecision']
            if newPr is not None:
                newDestinations.add(newPr)
            return (reverted, newDestinations)

        # TODO: These deep copies are expensive time-wise. Can we avoid
        # them? Probably not.
        newGraph = copy.deepcopy(now.graph)
        newState = copy.deepcopy(now.state)
        newSaves = copy.copy(now.saves)  # a shallow copy
        newTags: Dict[base.Tag, base.TagValue] = {}
        newAnnotations: List[base.Annotation] = []
        updated = base.Situation(
            graph=newGraph,
            state=newState,
            type='pending',
            action=None,
            saves=newSaves,
            tags=newTags,
            annotations=newAnnotations
        )

        targetContext: base.FocalContext

        # Now that action effects have been imprinted into the updated
        # situation, append it to our situations list
        self.situations.append(updated)

        # Figure out effects of the action:
        if action is None:
            raise InvalidActionError(
                "None cannot be used as an action when advancing the"
                " situation."
            )

        aLen = len(action)

        destIDs = set()

        if (
            action[0] in ('start', 'take', 'explore', 'warp')
        and any(
                newGraph.domainFor(d) == ENDINGS_DOMAIN
                for d in self.getActiveDecisions()
            )
        ):
            activeEndings = [
                d
                for d in self.getActiveDecisions()
                if newGraph.domainFor(d) == ENDINGS_DOMAIN
            ]
            raise InvalidActionError(
                f"Attempted to {action[0]!r} while an ending was"
                f" active. Active endings are:\n{activeEndings}"
            )

        if action == ('noAction',):
            # No updates needed
            pass

        elif (
            not isinstance(action, tuple)
         or (action[0] not in get_args(base.ExplorationActionType))
         or not (2 <= aLen <= 7)
        ):
            raise InvalidActionError(
                f"Invalid ExplorationAction tuple (must be a tuple that"
                f" starts with an ExplorationActionType and has 2-6"
                f" entries if it's not ('noAction',)):"
                f"\n{repr(action)}"
            )

        elif action[0] == 'start':
            (
                _,
                positionSpecifier,
                primary,
                domain,
                capabilities,
                mechanismStates,
                customState
            ) = cast(
                Tuple[
                    Literal['start'],
                    Union[
                        base.DecisionID,
                        Dict[base.FocalPointName, base.DecisionID],
                        Set[base.DecisionID]
                    ],
                    Optional[base.DecisionID],
                    base.Domain,
                    Optional[base.CapabilitySet],
                    Optional[Dict[base.MechanismID, base.MechanismState]],
                    Optional[dict]
                ],
                action
            )
            targetContext = newState['contexts'][
                newState['activeContext']
            ]

            targetFocalization = base.getDomainFocalization(
                targetContext,
                domain
            )  # sets up 'singular' as default if

            # Check if there are any already-active decisions.
            if targetContext['activeDecisions'][domain] is not None:
                raise BadStart(
                    f"Cannot start in domain {repr(domain)} because"
                    f" that domain already has a position. 'start' may"
                    f" only be used with domains that don't yet have"
                    f" any position information."
                )

            # Make the domain active
            if domain not in targetContext['activeDomains']:
                targetContext['activeDomains'].add(domain)

            # Check position info matches focalization type and update
            # exploration statuses
            if isinstance(positionSpecifier, base.DecisionID):
                if targetFocalization != 'singular':
                    raise BadStart(
                        f"Invalid position specifier"
                        f" {repr(positionSpecifier)} (type"
                        f" {type(positionSpecifier)}). Domain"
                        f" {repr(domain)} has {targetFocalization}"
                        f" focalization."
                    )
                base.setExplorationStatus(
                    updated,
                    positionSpecifier,
                    'exploring',
                    upgradeOnly=True
                )
                destIDs.add(positionSpecifier)
            elif isinstance(positionSpecifier, dict):
                if targetFocalization != 'plural':
                    raise BadStart(
                        f"Invalid position specifier"
                        f" {repr(positionSpecifier)} (type"
                        f" {type(positionSpecifier)}). Domain"
                        f" {repr(domain)} has {targetFocalization}"
                        f" focalization."
                    )
                destIDs |= set(positionSpecifier.values())
            elif isinstance(positionSpecifier, set):
                if targetFocalization != 'spreading':
                    raise BadStart(
                        f"Invalid position specifier"
                        f" {repr(positionSpecifier)} (type"
                        f" {type(positionSpecifier)}). Domain"
                        f" {repr(domain)} has {targetFocalization}"
                        f" focalization."
                    )
                destIDs |= positionSpecifier
            else:
                raise TypeError(
                    f"Invalid position specifier"
                    f" {repr(positionSpecifier)} (type"
                    f" {type(positionSpecifier)}). It must be a"
                    f" DecisionID, a dictionary from FocalPointNames to"
                    f" DecisionIDs, or a set of DecisionIDs, according"
                    f" to the focalization of the relevant domain."
                )

            # Put specified position(s) in place
            # TODO: This cast is really silly...
            targetContext['activeDecisions'][domain] = cast(
                Union[
                    None,
                    base.DecisionID,
                    Dict[base.FocalPointName, Optional[base.DecisionID]],
                    Set[base.DecisionID]
                ],
                positionSpecifier
            )

            # Set primary decision
            newState['primaryDecision'] = primary

            # Set capabilities
            if capabilities is not None:
                targetContext['capabilities'] = capabilities

            # Set mechanism states
            if mechanismStates is not None:
                newState['mechanisms'] = mechanismStates

            # Set custom state
            if customState is not None:
                newState['custom'] = customState

        elif action[0] in ('explore', 'take', 'warp'):  # similar handling
            assert (
                len(action) == 3
             or len(action) == 4
             or len(action) == 6
             or len(action) == 7
            )
            # Set up necessary variables
            cSpec: base.ContextSpecifier = "active"
            fromID: Optional[base.DecisionID] = None
            takeTransition: Optional[base.Transition] = None
            outcomes: List[bool] = []
            destID: base.DecisionID  # No starting value as it's not optional
            moveInDomain: Optional[base.Domain] = None
            moveWhich: Optional[base.FocalPointName] = None

            # Figure out target context
            if isinstance(action[1], str):
                if action[1] not in get_args(base.ContextSpecifier):
                    raise InvalidActionError(
                        f"Action specifies {repr(action[1])} context,"
                        f" but that's not a valid context specifier."
                        f" The valid options are:"
                        f"\n{repr(get_args(base.ContextSpecifier))}"
                    )
                else:
                    cSpec = cast(base.ContextSpecifier, action[1])
            else:  # Must be a `FocalPointSpecifier`
                cSpec, moveInDomain, moveWhich = cast(
                    base.FocalPointSpecifier,
                    action[1]
                )
                assert moveInDomain is not None

            # Grab target context to work in
            if cSpec == 'common':
                targetContext = newState['common']
            else:
                targetContext = newState['contexts'][
                    newState['activeContext']
                ]

            # Check focalization of the target domain
            if moveInDomain is not None:
                fType = base.getDomainFocalization(
                    targetContext,
                    moveInDomain
                )
                if (
                    (
                        isinstance(action[1], str)
                    and fType == 'plural'
                    ) or (
                        not isinstance(action[1], str)
                    and fType != 'plural'
                    )
                ):
                    raise ImpossibleActionError(
                        f"Invalid ExplorationAction (moves in"
                        f" plural-focalized domains must include a"
                        f" FocalPointSpecifier, while moves in"
                        f" non-plural-focalized domains must not."
                        f" Domain {repr(moveInDomain)} is"
                        f" {fType}-focalized):"
                        f"\n{repr(action)}"
                    )

            if action[0] == "warp":
                # It's a warp, so destination is specified directly
                if not isinstance(action[2], base.DecisionID):
                    raise TypeError(
                        f"Invalid ExplorationAction tuple (third part"
                        f" must be a decision ID for 'warp' actions):"
                        f"\n{repr(action)}"
                    )
                else:
                    destID = cast(base.DecisionID, action[2])

            elif aLen == 4 or aLen == 7:
                # direct 'take' or 'explore'
                fromID = cast(base.DecisionID, action[2])
                takeTransition, outcomes = cast(
                    base.TransitionWithOutcomes,
                    action[3]  # type: ignore [misc]
                )
                if (
                    not isinstance(fromID, base.DecisionID)
                 or not isinstance(takeTransition, base.Transition)
                ):
                    raise InvalidActionError(
                        f"Invalid ExplorationAction tuple (for 'take' or"
                        f" 'explore', if the length is 4/7, parts 2-4"
                        f" must be a context specifier, a decision ID, and a"
                        f" transition name. Got:"
                        f"\n{repr(action)}"
                    )

                try:
                    destID = newGraph.destination(fromID, takeTransition)
                except MissingDecisionError:
                    raise ImpossibleActionError(
                        f"Invalid ExplorationAction: move from decision"
                        f" {fromID} is invalid because there is no"
                        f" decision with that ID in the current"
                        f" graph."
                        f"\nValid decisions are:"
                        f"\n{newGraph.namesListing(newGraph)}"
                    )
                except MissingTransitionError:
                    valid = newGraph.destinationsFrom(fromID)
                    listing = newGraph.destinationsListing(valid)
                    raise ImpossibleActionError(
                        f"Invalid ExplorationAction: move from decision"
                        f" {newGraph.identityOf(fromID)}"
                        f" along transition {repr(takeTransition)} is"
                        f" invalid because there is no such transition"
                        f" at that decision."
                        f"\nValid transitions there are:"
                        f"\n{listing}"
                    )
                targetActive = targetContext['activeDecisions']
                if moveInDomain is not None:
                    activeInDomain = targetActive[moveInDomain]
                    if (
                        (
                            isinstance(activeInDomain, base.DecisionID)
                        and fromID != activeInDomain
                        )
                     or (
                            isinstance(activeInDomain, set)
                        and fromID not in activeInDomain
                        )
                     or (
                            isinstance(activeInDomain, dict)
                        and fromID not in activeInDomain.values()
                        )
                    ):
                        raise ImpossibleActionError(
                            f"Invalid ExplorationAction: move from"
                            f" decision {fromID} is invalid because"
                            f" that decision is not active in domain"
                            f" {repr(moveInDomain)} in the current"
                            f" graph."
                            f"\nValid decisions are:"
                            f"\n{newGraph.namesListing(newGraph)}"
                        )

            elif aLen == 3 or aLen == 6:
                # 'take' or 'explore' focal point
                # We know that moveInDomain is not None here.
                assert moveInDomain is not None
                if not isinstance(action[2], base.Transition):
                    raise InvalidActionError(
                        f"Invalid ExplorationAction tuple (for 'take'"
                        f" actions if the second part is a"
                        f" FocalPointSpecifier the third part must be a"
                        f" transition name):"
                        f"\n{repr(action)}"
                    )

                takeTransition, outcomes = cast(
                    base.TransitionWithOutcomes,
                    action[2]
                )
                targetActive = targetContext['activeDecisions']
                activeInDomain = cast(
                    Dict[base.FocalPointName, Optional[base.DecisionID]],
                    targetActive[moveInDomain]
                )
                if (
                    moveInDomain is not None
                and (
                        not isinstance(activeInDomain, dict)
                     or moveWhich not in activeInDomain
                    )
                ):
                    raise ImpossibleActionError(
                        f"Invalid ExplorationAction: move of focal"
                        f" point {repr(moveWhich)} in domain"
                        f" {repr(moveInDomain)} is invalid because"
                        f" that domain does not have a focal point"
                        f" with that name."
                    )
                fromID = activeInDomain[moveWhich]
                if fromID is None:
                    raise ImpossibleActionError(
                        f"Invalid ExplorationAction: move of focal"
                        f" point {repr(moveWhich)} in domain"
                        f" {repr(moveInDomain)} is invalid because"
                        f" that focal point does not have a position"
                        f" at this step."
                    )
                try:
                    destID = newGraph.destination(fromID, takeTransition)
                except MissingDecisionError:
                    raise ImpossibleActionError(
                        f"Invalid exploration state: focal point"
                        f" {repr(moveWhich)} in domain"
                        f" {repr(moveInDomain)} specifies decision"
                        f" {fromID} as the current position, but"
                        f" that decision does not exist!"
                    )
                except MissingTransitionError:
                    valid = newGraph.destinationsFrom(fromID)
                    listing = newGraph.destinationsListing(valid)
                    raise ImpossibleActionError(
                        f"Invalid ExplorationAction: move of focal"
                        f" point {repr(moveWhich)} in domain"
                        f" {repr(moveInDomain)} along transition"
                        f" {repr(takeTransition)} is invalid because"
                        f" that focal point is at decision"
                        f" {newGraph.identityOf(fromID)} and that"
                        f" decision does not have an outgoing"
                        f" transition with that name.\nValid"
                        f" transitions from that decision are:"
                        f"\n{listing}"
                    )

            else:
                raise InvalidActionError(
                    f"Invalid ExplorationAction: unrecognized"
                    f" 'explore', 'take' or 'warp' format:"
                    f"\n{action}"
                )

            # If we're exploring, update information for the destination
            if action[0] == 'explore':
                zone = cast(
                    Union[base.Zone, None, type[base.DefaultZone]],
                    action[-1]
                )
                recipName = cast(Optional[base.Transition], action[-2])
                destOrName = cast(
                    Union[base.DecisionName, base.DecisionID, None],
                    action[-3]
                )
                if isinstance(destOrName, base.DecisionID):
                    destID = destOrName

                if fromID is None or takeTransition is None:
                    raise ImpossibleActionError(
                        f"Invalid ExplorationAction: exploration"
                        f" has unclear origin decision or transition."
                        f" Got:\n{action}"
                    )

                currentDest = newGraph.destination(fromID, takeTransition)
                if not newGraph.isConfirmed(currentDest):
                    newGraph.replaceUnconfirmed(
                        fromID,
                        takeTransition,
                        destOrName,
                        recipName,
                        placeInZone=zone,
                        forceNew=not isinstance(destOrName, base.DecisionID)
                    )
                else:
                    # Otherwise, since the destination already existed
                    # and was hooked up at the right decision, no graph
                    # edits need to be made, unless we need to rename
                    # the reciprocal.
                    # TODO: Do we care about zones here?
                    if recipName is not None:
                        oldReciprocal = newGraph.getReciprocal(
                            fromID,
                            takeTransition
                        )
                        if (
                            oldReciprocal is not None
                        and oldReciprocal != recipName
                        ):
                            newGraph.addTransition(
                                destID,
                                recipName,
                                fromID,
                                None
                            )
                            newGraph.setReciprocal(
                                destID,
                                recipName,
                                takeTransition,
                                setBoth=True
                            )
                            newGraph.mergeTransitions(
                                destID,
                                oldReciprocal,
                                recipName
                            )

            # If we are moving along a transition, check requirements
            # and apply transition effects *before* updating our
            # position, and check that they don't cancel the normal
            # position update
            finalDest = None
            if takeTransition is not None:
                assert fromID is not None  # both or neither
                if not self.isTraversable(fromID, takeTransition):
                    req = now.graph.getTransitionRequirement(
                        fromID,
                        takeTransition
                    )
                    # TODO: Alter warning message if transition is
                    # deactivated vs. requirement not satisfied
                    warnings.warn(
                        (
                            f"The requirements for transition"
                            f" {takeTransition!r} from decision"
                            f" {now.graph.identityOf(fromID)} are"
                            f" not met at step {len(self) - 1} (or that"
                            f" transition has been deactivated):\n{req}"
                        ),
                        TransitionBlockedWarning
                    )

                # Apply transition consequences to our new state and
                # figure out if we need to skip our normal update or not
                finalDest = self.applyTransitionConsequence(
                    fromID,
                    (takeTransition, outcomes),
                    moveWhich,
                    challengePolicy
                )

            # Check moveInDomain
            destDomain = newGraph.domainFor(destID)
            if moveInDomain is not None and moveInDomain != destDomain:
                raise ImpossibleActionError(
                    f"Invalid ExplorationAction: move specified"
                    f" domain {repr(moveInDomain)} as the domain of"
                    f" the focal point to move, but the destination"
                    f" of the move is {now.graph.identityOf(destID)}"
                    f" which is in domain {repr(destDomain)}, so focal"
                    f" point {repr(moveWhich)} cannot be moved there."
                )

            # Now that we know where we're going, update position
            # information (assuming it wasn't already set):
            if finalDest is None:
                finalDest = destID
                base.updatePosition(
                    updated,
                    destID,
                    cSpec,
                    moveWhich
                )

            destIDs.add(finalDest)

        elif action[0] == "focus":
            # Figure out target context
            action = cast(
                Tuple[
                    Literal['focus'],
                    base.ContextSpecifier,
                    Set[base.Domain],
                    Set[base.Domain]
                ],
                action
            )
            contextSpecifier: base.ContextSpecifier = action[1]
            if contextSpecifier == 'common':
                targetContext = newState['common']
            else:
                targetContext = newState['contexts'][
                    newState['activeContext']
                ]

            # Just need to swap out active domains
            goingOut, comingIn = cast(
                Tuple[Set[base.Domain], Set[base.Domain]],
                action[2:]
            )
            if (
                not isinstance(goingOut, set)
             or not isinstance(comingIn, set)
             or not all(isinstance(d, base.Domain) for d in goingOut)
             or not all(isinstance(d, base.Domain) for d in comingIn)
            ):
                raise InvalidActionError(
                    f"Invalid ExplorationAction tuple (must have 4"
                    f" parts if the first part is 'focus' and"
                    f" the third and fourth parts must be sets of"
                    f" domains):"
                    f"\n{repr(action)}"
                )
            activeSet = targetContext['activeDomains']
            for dom in goingOut:
                try:
                    activeSet.remove(dom)
                except KeyError:
                    warnings.warn(
                        (
                            f"Domain {repr(dom)} was deactivated at"
                            f" step {len(self)} but it was already"
                            f" inactive at that point."
                        ),
                        InactiveDomainWarning
                    )
            # TODO: Also warn for doubly-activated domains?
            activeSet |= comingIn

            # destIDs remains empty in this case

        elif action[0] == 'swap':  # update which `FocalContext` is active
            newContext = cast(base.FocalContextName, action[1])
            if newContext not in newState['contexts']:
                raise MissingFocalContextError(
                    f"'swap' action with target {repr(newContext)} is"
                    f" invalid because no context with that name"
                    f" exists."
                )
            newState['activeContext'] = newContext

            # destIDs remains empty in this case

        elif action[0] == 'focalize':  # create new `FocalContext`
            newContext = cast(base.FocalContextName, action[1])
            if newContext in newState['contexts']:
                raise FocalContextCollisionError(
                    f"'focalize' action with target {repr(newContext)}"
                    f" is invalid because a context with that name"
                    f" already exists."
                )
            newState['contexts'][newContext] = base.emptyFocalContext()
            newState['activeContext'] = newContext

            # destIDs remains empty in this case

        # revertTo is handled above
        else:
            raise InvalidActionError(
                f"Invalid ExplorationAction tuple (first item must be"
                f" an ExplorationActionType, and tuple must be length-1"
                f" if the action type is 'noAction'):"
                f"\n{repr(action)}"
            )

        # Apply any active triggers
        followTo = self.applyActiveTriggers()
        if followTo is not None:
            destIDs.add(followTo)
            # TODO: Re-work to work with multiple position updates in
            # different focal contexts, domains, and/or for different
            # focal points in plural-focalized domains.

        return (updated, destIDs)

    def applyActiveTriggers(self) -> Optional[base.DecisionID]:
        """
        Finds all actions with the 'trigger' tag attached to currently
        active decisions, and applies their effects if their requirements
        are met (ordered by decision-ID with ties broken alphabetically
        by action name).

        'bounce', 'goto' and 'follow' effects may apply. However, any
        new triggers that would be activated because of decisions
        reached by such effects will not apply. Note that 'bounce'
        effects update position to the decision where the action was
        attached, which is usually a no-op. This function returns the
        decision ID of the decision reached by the last decision-moving
        effect applied, or `None` if no such effects triggered.

        TODO: What about situations where positions are updated in
        multiple domains or multiple foal points in a plural domain are
        independently updated?

        TODO: Tests for this!
        """
        active = self.getActiveDecisions()
        now = self.getSituation()
        graph = now.graph
        finalFollow = None
        for decision in sorted(active):
            for action in graph.decisionActions(decision):
                if (
                    'trigger' in graph.transitionTags(decision, action)
                and self.isTraversable(decision, action)
                ):
                    followTo = self.applyTransitionConsequence(
                        decision,
                        action
                    )
                    if followTo is not None:
                        # TODO: How will triggers interact with
                        # plural-focalized domains? Probably need to fix
                        # this to detect moveWhich based on which focal
                        # points are at the decision where the transition
                        # is, and then apply this to each of them?
                        base.updatePosition(now, followTo)
                        finalFollow = followTo

        return finalFollow

    def explore(
        self,
        transition: base.AnyTransition,
        destination: Union[base.DecisionName, base.DecisionID, None],
        reciprocal: Optional[base.Transition] = None,
        zone: Union[
            base.Zone,
            type[base.DefaultZone],
            None
        ] = base.DefaultZone,
        fromDecision: Optional[base.AnyDecisionSpecifier] = None,
        whichFocus: Optional[base.FocalPointSpecifier] = None,
        inCommon: Union[bool, Literal["auto"]] = "auto",
        decisionType: base.DecisionType = "active",
        challengePolicy: base.ChallengePolicy = "specified"
    ) -> base.DecisionID:
        """
        Adds a new situation to the exploration representing the
        traversal of the specified transition (possibly with outcomes
        specified for challenges among that transitions consequences).
        Uses `deduceTransitionDetailsAtStep` to figure out from the
        transition name which specific transition is taken (and which
        focal point is updated if necessary). This uses the
        `fromDecision`, `whichFocus`, and `inCommon` optional
        parameters, and also determines whether to update the common or
        the active `FocalContext`. Sets the exploration status of the
        decision explored to 'exploring'. Returns the decision ID for
        the destination reached, accounting for goto/bounce/follow
        effects that might have triggered.

        The `destination` will be used to name the newly-explored
        decision, except when it's a `DecisionID`, in which case that
        decision must be unvisited, and we'll connect the specified
        transition to that decision.

        The focalization of the destination domain in the context to be
        updated determines how active decisions are changed:

        - If the destination domain is focalized as 'single', then in
            the subsequent `Situation`, the destination decision will
            become the single active decision in that domain.
        - If it's focalized as 'plural', then one of the
            `FocalPointName`s for that domain will be moved to activate
            that decision; which one can be specified using `whichFocus`
            or if left unspecified, will be deduced: if the starting
            decision is in the same domain, then the
            alphabetically-earliest focal point which is at the starting
            decision will be moved. If the starting position is in a
            different domain, then the alphabetically earliest focal
            point among all focal points in the destination domain will
            be moved.
        - If it's focalized as 'spreading', then the destination
            decision will be added to the set of active decisions in
            that domain, without removing any.

        The transition named must have been pointing to an unvisited
        decision (see `hasBeenVisited`), and the name of that decision
        will be updated if a `destination` value is given (a
        `DecisionCollisionWarning` will be issued if the destination
        name is a duplicate of another name in the graph, although this
        is not an error). Additionally:

        - If a `reciprocal` name is specified, the reciprocal transition
            will be renamed using that name, or created with that name if
            it didn't already exist. If reciprocal is left as `None` (the
            default) then no change will be made to the reciprocal
            transition, and it will not be created if it doesn't exist.
        - If a `zone` is specified, the newly-explored decision will be
            added to that zone (and that zone will be created at level 0
            if it didn't already exist). If `zone` is set to `None` then
            it will not be added to any new zones. If `zone` is left as
            the default (the `DefaultZone` class) then the explored
            decision will be added to each zone that the decision it was
            explored from is a part of. If a zone needs to be created,
            that zone will be added as a sub-zone of each zone which is a
            parent of a zone that directly contains the origin decision.
        - An `ExplorationStatusError` will be raised if the specified
            transition leads to a decision whose `ExplorationStatus` is
            'exploring' or higher (i.e., `hasBeenVisited`). (Use
            `returnTo` instead to adjust things when a transition to an
            unknown destination turns out to lead to an already-known
            destination.)
        - A `TransitionBlockedWarning` will be issued if the specified
            transition is not traversable given the current game state
            (but in that last case the step will still be taken).
        - By default, the decision type for the new step will be
            'active', but a `decisionType` value can be specified to
            override that.
        - By default, the 'mostLikely' `ChallengePolicy` will be used to
            resolve challenges in the consequence of the transition
            taken, but an alternate policy can be supplied using the
            `challengePolicy` argument.
        """
        now = self.getSituation()

        transitionName, outcomes = base.nameAndOutcomes(transition)

        # Deduce transition details from the name + optional specifiers
        (
            using,
            fromID,
            destID,
            whichFocus
        ) = self.deduceTransitionDetailsAtStep(
            -1,
            transitionName,
            fromDecision,
            whichFocus,
            inCommon
        )

        # Issue a warning if the destination name is already in use
        if destination is not None:
            if isinstance(destination, base.DecisionName):
                try:
                    existingID = now.graph.resolveDecision(destination)
                    collision = existingID != destID
                except MissingDecisionError:
                    collision = False
                except AmbiguousDecisionSpecifierError:
                    collision = True

                if collision and WARN_OF_NAME_COLLISIONS:
                    warnings.warn(
                        (
                            f"The destination name {repr(destination)} is"
                            f" already in use when exploring transition"
                            f" {repr(transition)} from decision"
                            f" {now.graph.identityOf(fromID)} at step"
                            f" {len(self) - 1}."
                        ),
                        DecisionCollisionWarning
                    )

        # TODO: Different terminology for "exploration state above
        # noticed" vs. "DG thinks it's been visited"...
        if (
            self.hasBeenVisited(destID)
        ):
            raise ExplorationStatusError(
                f"Cannot explore to decision"
                f" {now.graph.identityOf(destID)} because it has"
                f" already been visited. Use returnTo instead of"
                f" explore when discovering a connection back to a"
                f" previously-explored decision."
            )

        if (
            isinstance(destination, base.DecisionID)
        and self.hasBeenVisited(destination)
        ):
            raise ExplorationStatusError(
                f"Cannot explore to decision"
                f" {now.graph.identityOf(destination)} because it has"
                f" already been visited. Use returnTo instead of"
                f" explore when discovering a connection back to a"
                f" previously-explored decision."
            )

        actionTaken: base.ExplorationAction = (
            'explore',
            using,
            fromID,
            (transitionName, outcomes),
            destination,
            reciprocal,
            zone
        )
        if whichFocus is not None:
            # A move-from-specific-focal-point action
            actionTaken = (
                'explore',
                whichFocus,
                (transitionName, outcomes),
                destination,
                reciprocal,
                zone
            )

        # Advance the situation, applying transition effects and
        # updating the destination decision.
        _, finalDest = self.advanceSituation(
            actionTaken,
            decisionType,
            challengePolicy
        )

        # TODO: Is this assertion always valid?
        assert len(finalDest) == 1
        return next(x for x in finalDest)

    def returnTo(
        self,
        transition: base.AnyTransition,
        destination: base.AnyDecisionSpecifier,
        reciprocal: Optional[base.Transition] = None,
        fromDecision: Optional[base.AnyDecisionSpecifier] = None,
        whichFocus: Optional[base.FocalPointSpecifier] = None,
        inCommon: Union[bool, Literal["auto"]] = "auto",
        decisionType: base.DecisionType = "active",
        challengePolicy: base.ChallengePolicy = "specified"
    ) -> base.DecisionID:
        """
        Adds a new graph to the exploration that replaces the given
        transition at the current position (which must lead to an unknown
        node, or a `MissingDecisionError` will result). The new
        transition will connect back to the specified destination, which
        must already exist (or a different `ValueError` will be raised).
        Returns the decision ID for the destination reached.

        Deduces transition details using the optional `fromDecision`,
        `whichFocus`, and `inCommon` arguments in addition to the
        `transition` value; see `deduceTransitionDetailsAtStep`.

        If a `reciprocal` transition is specified, that transition must
        either not already exist in the destination decision or lead to
        an unknown region; it will be replaced (or added) as an edge
        leading back to the current position.

        The `decisionType` and `challengePolicy` optional arguments are
        used for `advanceSituation`.

        A `TransitionBlockedWarning` will be issued if the requirements
        for the transition are not met, but the step will still be taken.
        Raises a `MissingDecisionError` if there is no current
        transition.
        """
        now = self.getSituation()

        transitionName, outcomes = base.nameAndOutcomes(transition)

        # Deduce transition details from the name + optional specifiers
        (
            using,
            fromID,
            destID,
            whichFocus
        ) = self.deduceTransitionDetailsAtStep(
            -1,
            transitionName,
            fromDecision,
            whichFocus,
            inCommon
        )

        # Replace with connection to existing destination
        destID = now.graph.resolveDecision(destination)
        if not self.hasBeenVisited(destID):
            raise ExplorationStatusError(
                f"Cannot return to decision"
                f" {now.graph.identityOf(destID)} because it has NOT"
                f" already been at least partially explored. Use"
                f" explore instead of returnTo when discovering a"
                f" connection to a previously-unexplored decision."
            )

        now.graph.replaceUnconfirmed(
            fromID,
            transitionName,
            destID,
            reciprocal
        )

        # A move-from-decision action
        actionTaken: base.ExplorationAction = (
            'take',
            using,
            fromID,
            (transitionName, outcomes)
        )
        if whichFocus is not None:
            # A move-from-specific-focal-point action
            actionTaken = ('take', whichFocus, (transitionName, outcomes))

        # Next, advance the situation, applying transition effects
        _, finalDest = self.advanceSituation(
            actionTaken,
            decisionType,
            challengePolicy
        )

        assert len(finalDest) == 1
        return next(x for x in finalDest)

    def takeAction(
        self,
        action: base.AnyTransition,
        requires: Optional[base.Requirement] = None,
        consequence: Optional[base.Consequence] = None,
        fromDecision: Optional[base.AnyDecisionSpecifier] = None,
        whichFocus: Optional[base.FocalPointSpecifier] = None,
        inCommon: Union[bool, Literal["auto"]] = "auto",
        decisionType: base.DecisionType = "active",
        challengePolicy: base.ChallengePolicy = "specified"
    ) -> base.DecisionID:
        """
        Adds a new graph to the exploration based on taking the given
        action, which must be a self-transition in the graph. If the
        action does not already exist in the graph, it will be created.
        Either way if requirements and/or a consequence are supplied,
        the requirements and consequence of the action will be updated
        to match them, and those are the requirements/consequence that
        will count.

        Returns the decision ID for the decision reached, which normally
        is the same action you were just at, but which might be altered
        by goto, bounce, and/or follow effects.

        Issues a `TransitionBlockedWarning` if the current game state
        doesn't satisfy the requirements for the action.

        The `fromDecision`, `whichFocus`, and `inCommon` arguments are
        used for `deduceTransitionDetailsAtStep`, while `decisionType`
        and `challengePolicy` are used for `advanceSituation`.

        When an action is being created, `fromDecision` (or
        `whichFocus`) must be specified, since the source decision won't
        be deducible from the transition name. Note that if a transition
        with the given name exists from *any* active decision, it will
        be used instead of creating a new action (possibly resulting in
        an error if it's not a self-loop transition). Also, you may get
        an `AmbiguousTransitionError` if several transitions with that
        name exist; in that case use `fromDecision` and/or `whichFocus`
        to disambiguate.
        """
        now = self.getSituation()
        graph = now.graph

        actionName, outcomes = base.nameAndOutcomes(action)

        try:
            (
                using,
                fromID,
                destID,
                whichFocus
            ) = self.deduceTransitionDetailsAtStep(
                -1,
                actionName,
                fromDecision,
                whichFocus,
                inCommon
            )

            if destID != fromID:
                raise ValueError(
                    f"Cannot take action {repr(action)} because it's a"
                    f" transition to another decision, not an action"
                    f" (use explore, returnTo, and/or retrace instead)."
                )

        except MissingTransitionError:
            using = 'active'
            if inCommon is True:
                using = 'common'

            if fromDecision is not None:
                fromID = graph.resolveDecision(fromDecision)
            elif whichFocus is not None:
                maybeFromID = base.resolvePosition(now, whichFocus)
                if maybeFromID is None:
                    raise MissingDecisionError(
                        f"Focal point {repr(whichFocus)} was specified"
                        f" in takeAction but that focal point doesn't"
                        f" have a position."
                    )
                else:
                    fromID = maybeFromID
            else:
                raise AmbiguousTransitionError(
                    f"Taking action {repr(action)} is ambiguous because"
                    f" the source decision has not been specified via"
                    f" either fromDecision or whichFocus, and we"
                    f" couldn't find an existing action with that name."
                )

            # Since the action doesn't exist, add it:
            graph.addAction(fromID, actionName, requires, consequence)

        # Update the transition requirement/consequence if requested
        # (before the action is taken)
        if requires is not None:
            graph.setTransitionRequirement(fromID, actionName, requires)
        if consequence is not None:
            graph.setConsequence(fromID, actionName, consequence)

        # A move-from-decision action
        actionTaken: base.ExplorationAction = (
            'take',
            using,
            fromID,
            (actionName, outcomes)
        )
        if whichFocus is not None:
            # A move-from-specific-focal-point action
            actionTaken = ('take', whichFocus, (actionName, outcomes))

        _, finalDest = self.advanceSituation(
            actionTaken,
            decisionType,
            challengePolicy
        )

        assert len(finalDest) in (0, 1)
        if len(finalDest) == 1:
            return next(x for x in finalDest)
        else:
            return fromID

    def retrace(
        self,
        transition: base.AnyTransition,
        fromDecision: Optional[base.AnyDecisionSpecifier] = None,
        whichFocus: Optional[base.FocalPointSpecifier] = None,
        inCommon: Union[bool, Literal["auto"]] = "auto",
        decisionType: base.DecisionType = "active",
        challengePolicy: base.ChallengePolicy = "specified"
    ) -> base.DecisionID:
        """
        Adds a new graph to the exploration based on taking the given
        transition, which must already exist and which must not lead to
        an unknown region. Returns the ID of the destination decision,
        accounting for goto, bounce, and/or follow effects.

        Issues a `TransitionBlockedWarning` if the current game state
        doesn't satisfy the requirements for the transition.

        The `fromDecision`, `whichFocus`, and `inCommon` arguments are
        used for `deduceTransitionDetailsAtStep`, while `decisionType`
        and `challengePolicy` are used for `advanceSituation`.
        """
        now = self.getSituation()

        transitionName, outcomes = base.nameAndOutcomes(transition)

        (
            using,
            fromID,
            destID,
            whichFocus
        ) = self.deduceTransitionDetailsAtStep(
            -1,
            transitionName,
            fromDecision,
            whichFocus,
            inCommon
        )

        visited = self.hasBeenVisited(destID)
        confirmed = now.graph.isConfirmed(destID)
        if not confirmed:
            raise ExplorationStatusError(
                f"Cannot retrace transition {transition!r} from"
                f" decision {now.graph.identityOf(fromID)} because it"
                f" leads to an unconfirmed decision.\nUse"
                f" `DiscreteExploration.explore` and provide"
                f" destination decision details instead."
            )
        if not visited:
            raise ExplorationStatusError(
                f"Cannot retrace transition {transition!r} from"
                f" decision {now.graph.identityOf(fromID)} because it"
                f" leads to an unvisited decision.\nUse"
                f" `DiscreteExploration.explore` and provide"
                f" destination decision details instead."
            )

        # A move-from-decision action
        actionTaken: base.ExplorationAction = (
            'take',
            using,
            fromID,
            (transitionName, outcomes)
        )
        if whichFocus is not None:
            # A move-from-specific-focal-point action
            actionTaken = ('take', whichFocus, (transitionName, outcomes))

        _, finalDest = self.advanceSituation(
            actionTaken,
            decisionType,
        challengePolicy
    )

        assert len(finalDest) == 1
        return next(x for x in finalDest)

    def warp(
        self,
        destination: base.AnyDecisionSpecifier,
        consequence: Optional[base.Consequence] = None,
        domain: Optional[base.Domain] = None,
        zone: Union[
            base.Zone,
            type[base.DefaultZone],
            None
        ] = base.DefaultZone,
        whichFocus: Optional[base.FocalPointSpecifier] = None,
        inCommon: Union[bool] = False,
        decisionType: base.DecisionType = "active",
        challengePolicy: base.ChallengePolicy = "specified"
    ) -> base.DecisionID:
        """
        Adds a new graph to the exploration that's a copy of the current
        graph, with the position updated to be at the destination without
        actually creating a transition from the old position to the new
        one. Returns the ID of the decision warped to (accounting for
        any goto or follow effects triggered).

        Any provided consequences are applied, but are not associated
        with any transition (so any delays and charges are ignored, and
        'bounce' effects don't actually cancel the warp). 'goto' or
        'follow' effects might change the warp destination; 'follow'
        effects take the original destination as their starting point.
        Any mechanisms mentioned in extra consequences will be found
        based on the destination. Outcomes in supplied challenges should
        be pre-specified, or else they will be resolved with the
        `challengePolicy`.

        `whichFocus` may be specified when the destination domain's
        focalization is 'plural' but for 'singular' or 'spreading'
        destination domains it is not allowed. `inCommon` determines
        whether the common or the active focal context is updated
        (default is to update the active context). The `decisionType`
        and `challengePolicy` are used for `advanceSituation`.

        - If the destination did not already exist, it will be created.
            Initially, it will be disconnected from all other decisions.
            In this case, the `domain` value can be used to put it in a
            non-default domain.
        - The position is set to the specified destination, and if a
            `consequence` is specified it is applied. Note that
            'deactivate' effects are NOT allowed, and 'edit' effects
            must establish their own transition target because there is
            no transition that the effects are being applied to.
        - If the destination had been unexplored, its exploration status
            will be set to 'exploring'.
        - If a `zone` is specified, the destination will be added to that
            zone (even if the destination already existed) and that zone
            will be created (as a level-0 zone) if need be. If `zone` is
            set to `None`, then no zone will be applied. If `zone` is
            left as the default (`DefaultZone`) and the focalization of
            the destination domain is 'singular' or 'plural' and the
            destination is newly created and there is an origin and the
            origin is in the same domain as the destination, then the
            destination will be added to all zones that the origin was a
            part of if the destination is newly created, but otherwise
            the destination will not be added to any zones. If the
            specified zone has to be created and there's an origin
            decision, it will be added as a sub-zone to all parents of
            zones directly containing the origin, as long as the origin
            is in the same domain as the destination.
        """
        now = self.getSituation()
        graph = now.graph

        fromID: Optional[base.DecisionID]

        new = False
        try:
            destID = graph.resolveDecision(destination)
        except MissingDecisionError:
            if isinstance(destination, tuple):
                # just the name; ignore zone/domain
                destination = destination[-1]

            if not isinstance(destination, base.DecisionName):
                raise TypeError(
                    f"Warp destination {repr(destination)} does not"
                    f" exist, and cannot be created as it is not a"
                    f" decision name."
                )
            destID = graph.addDecision(destination, domain)
            graph.tagDecision(destID, 'unconfirmed')
            self.setExplorationStatus(destID, 'unknown')
            new = True

        using: base.ContextSpecifier
        if inCommon:
            targetContext = self.getCommonContext()
            using = "common"
        else:
            targetContext = self.getActiveContext()
            using = "active"

        destDomain = graph.domainFor(destID)
        targetFocalization = base.getDomainFocalization(
            targetContext,
            destDomain
        )
        if targetFocalization == 'singular':
            targetActive = targetContext['activeDecisions']
            if destDomain in targetActive:
                fromID = cast(
                    base.DecisionID,
                    targetContext['activeDecisions'][destDomain]
                )
            else:
                fromID = None
        elif targetFocalization == 'plural':
            if whichFocus is None:
                raise AmbiguousTransitionError(
                    f"Warping to {repr(destination)} is ambiguous"
                    f" becuase domain {repr(destDomain)} has plural"
                    f" focalization, and no whichFocus value was"
                    f" specified."
                )

            fromID = base.resolvePosition(
                self.getSituation(),
                whichFocus
            )
        else:
            fromID = None

        # Handle zones
        if zone is base.DefaultZone:
            if (
                new
            and fromID is not None
            and graph.domainFor(fromID) == destDomain
            ):
                for prevZone in graph.zoneParents(fromID):
                    graph.addDecisionToZone(destination, prevZone)
            # Otherwise don't update zones
        elif zone is not None:
            # Newness is ignored when a zone is specified
            zone = cast(base.Zone, zone)
            # Create the zone at level 0 if it didn't already exist
            if graph.getZoneInfo(zone) is None:
                graph.createZone(zone, 0)
                # Add the newly created zone to each 2nd-level parent of
                # the previous decision if there is one and it's in the
                # same domain
                if (
                    fromID is not None
                and graph.domainFor(fromID) == destDomain
                ):
                    for prevZone in graph.zoneParents(fromID):
                        for prevUpper in graph.zoneParents(prevZone):
                            graph.addZoneToZone(zone, prevUpper)
            # Finally add the destination to the (maybe new) zone
            graph.addDecisionToZone(destID, zone)
        # else don't touch zones

        # Encode the action taken
        actionTaken: base.ExplorationAction
        if whichFocus is None:
            actionTaken = (
                'warp',
                using,
                destID
            )
        else:
            actionTaken = (
                'warp',
                whichFocus,
                destID
            )

        # Advance the situation
        _, finalDests = self.advanceSituation(
            actionTaken,
            decisionType,
            challengePolicy
        )
        now = self.getSituation()  # updating just in case

        assert len(finalDests) == 1
        finalDest = next(x for x in finalDests)

        # Apply additional consequences:
        if consequence is not None:
            altDest = self.applyExtraneousConsequence(
                consequence,
                where=(destID, None),
                # TODO: Mechanism search from both ends?
                moveWhich=(
                    whichFocus[-1]
                    if whichFocus is not None
                    else None
                )
            )
            if altDest is not None:
                finalDest = altDest
            now = self.getSituation()  # updating just in case

        return finalDest

    def wait(
        self,
        consequence: Optional[base.Consequence] = None,
        decisionType: base.DecisionType = "active",
        challengePolicy: base.ChallengePolicy = "specified"
    ) -> Optional[base.DecisionID]:
        """
        Adds a wait step. If a consequence is specified, it is applied,
        although it will not have any position/transition information
        available during resolution/application.

        A decision type other than "active" and/or a challenge policy
        other than "specified" can be included (see `advanceSituation`).

        The "pending" decision type may not be used, a `ValueError` will
        result. This allows None as the action for waiting while
        preserving the pending/None type/action combination for
        unresolved situations.

        If a goto or follow effect in the applied consequence implies a
        position update, this will return the new destination ID;
        otherwise it will return `None`. Triggering a 'bounce' effect
        will be an error, because there is no position information for
        the effect.
        """
        if decisionType == "pending":
            raise ValueError(
                "The 'pending' decision type may not be used for"
                " wait actions."
            )
        self.advanceSituation(('noAction',), decisionType, challengePolicy)
        now = self.getSituation()
        if consequence is not None:
            if challengePolicy != "specified":
                base.resetChallengeOutcomes(consequence)
            observed = base.observeChallengeOutcomes(
                base.RequirementContext(
                    state=now.state,
                    graph=now.graph,
                    searchFrom=set()
                ),
                consequence,
                location=None,  # No position info
                policy=challengePolicy,
                knownOutcomes=None  # bake outcomes into the consequence
            )
            # No location information since we might have multiple
            # active decisions and there's no indication of which one
            # we're "waiting at."
            finalDest = self.applyExtraneousConsequence(observed)
            now = self.getSituation()  # updating just in case

            return finalDest
        else:
            return None

    def revert(
        self,
        slot: base.SaveSlot = base.DEFAULT_SAVE_SLOT,
        aspects: Optional[Set[str]] = None,
        decisionType: base.DecisionType = "active"
    ) -> None:
        """
        Reverts the game state to a previously-saved game state (saved
        via a 'save' effect). The save slot name and set of aspects to
        revert are required. By default, all aspects except the graph
        are reverted.
        """
        if aspects is None:
            aspects = set()

        action: base.ExplorationAction = ("revertTo", slot, aspects)

        self.advanceSituation(action, decisionType)

    def observeAll(
        self,
        where: base.AnyDecisionSpecifier,
        *transitions: Union[
            base.Transition,
            Tuple[base.Transition, base.AnyDecisionSpecifier],
            Tuple[
                base.Transition,
                base.AnyDecisionSpecifier,
                base.Transition
            ]
        ]
    ) -> List[base.DecisionID]:
        """
        Observes one or more new transitions, applying changes to the
        current graph. The transitions can be specified in one of three
        ways:

        1. A transition name. The transition will be created and will
            point to a new unexplored node.
        2. A pair containing a transition name and a destination
            specifier. If the destination does not exist it will be
            created as an unexplored node, although in that case the
            decision specifier may not be an ID.
        3. A triple containing a transition name, a destination
            specifier, and a reciprocal name. Works the same as the pair
            case but also specifies the name for the reciprocal
            transition.

        The new transitions are outgoing from specified decision.

        Yields the ID of each decision connected to, whether those are
        new or existing decisions.
        """
        now = self.getSituation()
        fromID = now.graph.resolveDecision(where)
        result = []
        for entry in transitions:
            if isinstance(entry, base.Transition):
                result.append(self.observe(fromID, entry))
            else:
                result.append(self.observe(fromID, *entry))
        return result

    def observe(
        self,
        where: base.AnyDecisionSpecifier,
        transition: base.Transition,
        destination: Optional[base.AnyDecisionSpecifier] = None,
        reciprocal: Optional[base.Transition] = None
    ) -> base.DecisionID:
        """
        Observes a single new outgoing transition from the specified
        decision. If specified the transition connects to a specific
        destination and/or has a specific reciprocal. The specified
        destination will be created if it doesn't exist, or where no
        destination is specified, a new unexplored decision will be
        added. The ID of the decision connected to is returned.

        Sets the exploration status of the observed destination to
        "noticed" if a destination is specified and needs to be created
        (but not when no destination is specified).

        For example:

        >>> e = DiscreteExploration()
        >>> e.start('start')
        0
        >>> e.observe('start', 'up')
        1
        >>> g = e.getSituation().graph
        >>> g.destinationsFrom('start')
        {'up': 1}
        >>> e.getExplorationStatus(1)  # not given a name: assumed unknown
        'unknown'
        >>> e.observe('start', 'left', 'A')
        2
        >>> g.destinationsFrom('start')
        {'up': 1, 'left': 2}
        >>> g.nameFor(2)
        'A'
        >>> e.getExplorationStatus(2)  # given a name: noticed
        'noticed'
        >>> e.observe('start', 'up2', 1)
        1
        >>> g.destinationsFrom('start')
        {'up': 1, 'left': 2, 'up2': 1}
        >>> e.getExplorationStatus(1)  # existing decision: status unchanged
        'unknown'
        >>> e.observe('start', 'right', 'B', 'left')
        3
        >>> g.destinationsFrom('start')
        {'up': 1, 'left': 2, 'up2': 1, 'right': 3}
        >>> g.nameFor(3)
        'B'
        >>> e.getExplorationStatus(3)  # new + name -> noticed
        'noticed'
        >>> e.observe('start', 'right')  # repeat transition name
        Traceback (most recent call last):
        ...
        exploration.core.TransitionCollisionError...
        >>> e.observe('start', 'right2', 'B', 'left')  # repeat reciprocal
        Traceback (most recent call last):
        ...
        exploration.core.TransitionCollisionError...
        >>> g = e.getSituation().graph
        >>> g.createZone('Z', 0)
        ZoneInfo(level=0, parents=set(), contents=set())
        >>> g.addDecisionToZone('start', 'Z')
        >>> e.observe('start', 'down', 'C', 'up')
        4
        >>> g.destinationsFrom('start')
        {'up': 1, 'left': 2, 'up2': 1, 'right': 3, 'down': 4}
        >>> g.identityOf('C')
        '4 (C)'
        >>> g.zoneParents(4)  # not in any zones, 'cause still unexplored
        set()
        >>> e.observe(
        ...     'C',
        ...     'right',
        ...     base.DecisionSpecifier('main', 'Z2', 'D'),
        ... )  # creates zone
        5
        >>> g.destinationsFrom('C')
        {'up': 0, 'right': 5}
        >>> g.destinationsFrom('D')  # default reciprocal name
        {'return': 4}
        >>> g.identityOf('D')
        '5 (Z2::D)'
        >>> g.zoneParents(5)
        {'Z2'}
        """
        now = self.getSituation()
        fromID = now.graph.resolveDecision(where)

        kwargs: Dict[
            str,
            Union[base.Transition, base.DecisionName, None]
        ] = {}
        if reciprocal is not None:
            kwargs['reciprocal'] = reciprocal

        if destination is not None:
            try:
                destID = now.graph.resolveDecision(destination)
                now.graph.addTransition(
                    fromID,
                    transition,
                    destID,
                    reciprocal
                )
                return destID
            except MissingDecisionError:
                if isinstance(destination, base.DecisionSpecifier):
                    kwargs['toDomain'] = destination.domain
                    kwargs['placeInZone'] = destination.zone
                    kwargs['destinationName'] = destination.name
                elif isinstance(destination, base.DecisionName):
                    kwargs['destinationName'] = destination
                else:
                    assert isinstance(destination, base.DecisionID)
                    # We got to except by failing to resolve, so it's an
                    # invalid ID
                    raise

        result = now.graph.addUnexploredEdge(
            fromID,
            transition,
            **kwargs  # type: ignore [arg-type]
        )
        if 'destinationName' in kwargs:
            self.setExplorationStatus(result, 'noticed', upgradeOnly=True)
        return result

    def observeMechanisms(
        self,
        where: Optional[base.AnyDecisionSpecifier],
        *mechanisms: Union[
            base.MechanismName,
            Tuple[base.MechanismName, base.MechanismState]
        ]
    ) -> List[base.MechanismID]:
        """
        Adds one or more mechanisms to the exploration's current graph,
        located at the specified decision. Global mechanisms can be
        added by using `None` for the location. Mechanisms are named, or
        a (name, state) tuple can be used to set them into a specific
        state. Mechanisms not set to a state will be in the
        `base.DEFAULT_MECHANISM_STATE`.
        """
        now = self.getSituation()
        result = []
        for mSpec in mechanisms:
            setState = None
            if isinstance(mSpec, base.MechanismName):
                result.append(now.graph.addMechanism(mSpec, where))
            elif (
                isinstance(mSpec, tuple)
            and len(mSpec) == 2
            and isinstance(mSpec[0], base.MechanismName)
            and isinstance(mSpec[1], base.MechanismState)
            ):
                result.append(now.graph.addMechanism(mSpec[0], where))
                setState = mSpec[1]
            else:
                raise TypeError(
                    f"Invalid mechanism: {repr(mSpec)} (must be a"
                    f" mechanism name or a (name, state) tuple."
                )

            if setState:
                self.setMechanismStateNow(result[-1], setState)

        return result

    def reZone(
        self,
        zone: base.Zone,
        where: base.AnyDecisionSpecifier,
        replace: Union[base.Zone, int] = 0
    ) -> None:
        """
        Alters the current graph without adding a new exploration step.

        Calls `DecisionGraph.replaceZonesInHierarchy` targeting the
        specified decision. Note that per the logic of that method, ALL
        zones at the specified hierarchy level are replaced, even if a
        specific zone to replace is specified here.

        TODO: not that?

        The level value is either specified via `replace` (default 0) or
        deduced from the zone provided as the `replace` value using
        `DecisionGraph.zoneHierarchyLevel`.
        """
        now = self.getSituation()

        if isinstance(replace, int):
            level = replace
        else:
            level = now.graph.zoneHierarchyLevel(replace)

        now.graph.replaceZonesInHierarchy(where, zone, level)

    def runCommand(
        self,
        command: commands.Command,
        scope: Optional[commands.Scope] = None,
        line: int = -1
    ) -> commands.CommandResult:
        """
        Runs a single `Command` applying effects to the exploration, its
        current graph, and the provided execution context, and returning
        a command result, which contains the modified scope plus
        optional skip and label values (see `CommandResult`). This
        function also directly modifies the scope you give it. Variable
        references in the command are resolved via entries in the
        provided scope. If no scope is given, an empty one is created.

        A line number may be supplied for use in error messages; if left
        out line -1 will be used.

        Raises an error if the command is invalid.

        For commands that establish a value as the 'current value', that
        value will be stored in the '_' variable. When this happens, the
        old contents of '_' are stored in '__' first, and the old
        contents of '__' are discarded. Note that non-automatic
        assignment to '_' does not move the old value to '__'.
        """
        try:
            if scope is None:
                scope = {}

            skip: Union[int, str, None] = None
            label: Optional[str] = None

            if command.command == 'val':
                command = cast(commands.LiteralValue, command)
                result = commands.resolveValue(command.value, scope)
                commands.pushCurrentValue(scope, result)

            elif command.command == 'empty':
                command = cast(commands.EstablishCollection, command)
                collection = commands.resolveVarName(command.collection, scope)
                commands.pushCurrentValue(
                    scope,
                    {
                        'list': [],
                        'tuple': (),
                        'set': set(),
                        'dict': {},
                    }[collection]
                )

            elif command.command == 'append':
                command = cast(commands.AppendValue, command)
                target = scope['_']
                addIt = commands.resolveValue(command.value, scope)
                if isinstance(target, list):
                    target.append(addIt)
                elif isinstance(target, tuple):
                    scope['_'] = target + (addIt,)
                elif isinstance(target, set):
                    target.add(addIt)
                elif isinstance(target, dict):
                    raise TypeError(
                        "'append' command cannot be used with a"
                        " dictionary. Use 'set' instead."
                    )
                else:
                    raise TypeError(
                        f"Invalid current value for 'append' command."
                        f" The current value must be a list, tuple, or"
                        f" set, but it was a '{type(target).__name__}'."
                    )

            elif command.command == 'set':
                command = cast(commands.SetValue, command)
                target = scope['_']
                where = commands.resolveValue(command.location, scope)
                what = commands.resolveValue(command.value, scope)
                if isinstance(target, list):
                    if not isinstance(where, int):
                        raise TypeError(
                            f"Cannot set item in list: index {where!r}"
                            f" is not an integer."
                        )
                    target[where] = what
                elif isinstance(target, tuple):
                    if not isinstance(where, int):
                        raise TypeError(
                            f"Cannot set item in tuple: index {where!r}"
                            f" is not an integer."
                        )
                    if not (
                        0 <= where < len(target)
                    or -1 >= where >= -len(target)
                    ):
                        raise IndexError(
                            f"Cannot set item in tuple at index"
                            f" {where}: Tuple has length {len(target)}."
                        )
                    scope['_'] = target[:where] + (what,) + target[where + 1:]
                elif isinstance(target, set):
                    if what:
                        target.add(where)
                    else:
                        try:
                            target.remove(where)
                        except KeyError:
                            pass
                elif isinstance(target, dict):
                    target[where] = what

            elif command.command == 'pop':
                command = cast(commands.PopValue, command)
                target = scope['_']
                if isinstance(target, list):
                    result = target.pop()
                    commands.pushCurrentValue(scope, result)
                elif isinstance(target, tuple):
                    result = target[-1]
                    updated = target[:-1]
                    scope['__'] = updated
                    scope['_'] = result
                else:
                    raise TypeError(
                        f"Cannot 'pop' from a {type(target).__name__}"
                        f" (current value must be a list or tuple)."
                    )

            elif command.command == 'get':
                command = cast(commands.GetValue, command)
                target = scope['_']
                where = commands.resolveValue(command.location, scope)
                if isinstance(target, list):
                    if not isinstance(where, int):
                        raise TypeError(
                            f"Cannot get item from list: index"
                            f" {where!r} is not an integer."
                        )
                elif isinstance(target, tuple):
                    if not isinstance(where, int):
                        raise TypeError(
                            f"Cannot get item from tuple: index"
                            f" {where!r} is not an integer."
                        )
                elif isinstance(target, set):
                    result = where in target
                    commands.pushCurrentValue(scope, result)
                elif isinstance(target, dict):
                    result = target[where]
                    commands.pushCurrentValue(scope, result)
                else:
                    result = getattr(target, where)
                    commands.pushCurrentValue(scope, result)

            elif command.command == 'remove':
                command = cast(commands.RemoveValue, command)
                target = scope['_']
                where = commands.resolveValue(command.location, scope)
                if isinstance(target, (list, tuple)):
                    # this cast is not correct but suppresses warnings
                    # given insufficient narrowing by MyPy
                    target = cast(Tuple[Any, ...], target)
                    if not isinstance(where, int):
                        raise TypeError(
                            f"Cannot remove item from list or tuple:"
                            f" index {where!r} is not an integer."
                        )
                    scope['_'] = target[:where] + target[where + 1:]
                elif isinstance(target, set):
                    target.remove(where)
                elif isinstance(target, dict):
                    del target[where]
                else:
                    raise TypeError(
                        f"Cannot use 'remove' on a/an"
                        f" {type(target).__name__}."
                    )

            elif command.command == 'op':
                command = cast(commands.ApplyOperator, command)
                left = commands.resolveValue(command.left, scope)
                right = commands.resolveValue(command.right, scope)
                op = command.op
                if op == '+':
                    result = left + right
                elif op == '-':
                    result = left - right
                elif op == '*':
                    result = left * right
                elif op == '/':
                    result = left / right
                elif op == '//':
                    result = left // right
                elif op == '**':
                    result = left ** right
                elif op == '%':
                    result = left % right
                elif op == '^':
                    result = left ^ right
                elif op == '|':
                    result = left | right
                elif op == '&':
                    result = left & right
                elif op == 'and':
                    result = left and right
                elif op == 'or':
                    result = left or right
                elif op == '<':
                    result = left < right
                elif op == '>':
                    result = left > right
                elif op == '<=':
                    result = left <= right
                elif op == '>=':
                    result = left >= right
                elif op == '==':
                    result = left == right
                elif op == 'is':
                    result = left is right
                else:
                    raise RuntimeError("Invalid operator '{op}'.")

                commands.pushCurrentValue(scope, result)

            elif command.command == 'unary':
                command = cast(commands.ApplyUnary, command)
                value = commands.resolveValue(command.value, scope)
                op = command.op
                if op == '-':
                    result = -value
                elif op == '~':
                    result = ~value
                elif op == 'not':
                    result = not value

                commands.pushCurrentValue(scope, result)

            elif command.command == 'assign':
                command = cast(commands.VariableAssignment, command)
                varname = commands.resolveVarName(command.varname, scope)
                value = commands.resolveValue(command.value, scope)
                scope[varname] = value

            elif command.command == 'delete':
                command = cast(commands.VariableDeletion, command)
                varname = commands.resolveVarName(command.varname, scope)
                del scope[varname]

            elif command.command == 'load':
                command = cast(commands.LoadVariable, command)
                varname = commands.resolveVarName(command.varname, scope)
                commands.pushCurrentValue(scope, scope[varname])

            elif command.command == 'call':
                command = cast(commands.FunctionCall, command)
                function = command.function
                if function.startswith('$'):
                    function = commands.resolveValue(function, scope)

                toCall: Callable
                args: Tuple[str, ...]
                kwargs: Dict[str, Any]

                if command.target == 'builtin':
                    toCall = commands.COMMAND_BUILTINS[function]
                    args = (scope['_'],)
                    kwargs = {}
                    if toCall == round:
                        if 'ndigits' in scope:
                            kwargs['ndigits'] = scope['ndigits']
                    elif toCall == range and args[0] is None:
                        start = scope.get('start', 0)
                        stop = scope['stop']
                        step = scope.get('step', 1)
                        args = (start, stop, step)

                else:
                    if command.target == 'stored':
                        toCall = function
                    elif command.target == 'graph':
                        toCall = getattr(self.getSituation().graph, function)
                    elif command.target == 'exploration':
                        toCall = getattr(self, function)
                    else:
                        raise TypeError(
                            f"Invalid call target '{command.target}'"
                            f" (must be one of 'builtin', 'stored',"
                            f" 'graph', or 'exploration'."
                        )

                    # Fill in arguments via kwargs defined in scope
                    args = ()
                    kwargs = {}
                    signature = inspect.signature(toCall)
                    # TODO: Maybe try some type-checking here?
                    for argName, param in signature.parameters.items():
                        if param.kind == inspect.Parameter.VAR_POSITIONAL:
                            if argName in scope:
                                args = args + tuple(scope[argName])
                            # Else leave args as-is
                        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                            # These must have a default
                            if argName in scope:
                                kwargs[argName] = scope[argName]
                        elif param.kind == inspect.Parameter.VAR_KEYWORD:
                            # treat as a dictionary
                            if argName in scope:
                                argsToUse = scope[argName]
                                if not isinstance(argsToUse, dict):
                                    raise TypeError(
                                        f"Variable '{argName}' must"
                                        f" hold a dictionary when"
                                        f" calling function"
                                        f" '{toCall.__name__} which"
                                        f" uses that argument as a"
                                        f" keyword catchall."
                                    )
                                kwargs.update(scope[argName])
                        else:  # a normal parameter
                            if argName in scope:
                                args = args + (scope[argName],)
                            elif param.default == inspect.Parameter.empty:
                                raise TypeError(
                                    f"No variable named '{argName}' has"
                                    f" been defined to supply the"
                                    f" required parameter with that"
                                    f" name for function"
                                    f" '{toCall.__name__}'."
                                )

                result = toCall(*args, **kwargs)
                commands.pushCurrentValue(scope, result)

            elif command.command == 'skip':
                command = cast(commands.SkipCommands, command)
                doIt = commands.resolveValue(command.condition, scope)
                if doIt:
                    skip = commands.resolveValue(command.amount, scope)
                    if not isinstance(skip, (int, str)):
                        raise TypeError(
                            f"Skip amount must be an integer or a label"
                            f" name (got {skip!r})."
                        )

            elif command.command == 'label':
                command = cast(commands.Label, command)
                label = commands.resolveValue(command.name, scope)
                if not isinstance(label, str):
                    raise TypeError(
                        f"Label name must be a string (got {label!r})."
                    )

            else:
                raise ValueError(
                    f"Invalid command type: {command.command!r}"
                )
        except ValueError as e:
            raise commands.CommandValueError(command, line, e)
        except TypeError as e:
            raise commands.CommandTypeError(command, line, e)
        except IndexError as e:
            raise commands.CommandIndexError(command, line, e)
        except KeyError as e:
            raise commands.CommandKeyError(command, line, e)
        except Exception as e:
            raise commands.CommandOtherError(command, line, e)

        return (scope, skip, label)

    def runCommandBlock(
        self,
        block: List[commands.Command],
        scope: Optional[commands.Scope] = None
    ) -> commands.Scope:
        """
        Runs a list of commands, using the given scope (or creating a new
        empty scope if none was provided). Returns the scope after
        running all of the commands, which may also edit the exploration
        and/or the current graph of course.

        Note that if a skip command would skip past the end of the
        block, execution will end. If a skip command would skip before
        the beginning of the block, execution will start from the first
        command.

        Example:

        >>> e = DiscreteExploration()
        >>> scope = e.runCommandBlock([
        ...    commands.command('assign', 'decision', "'START'"),
        ...    commands.command('call', 'exploration', 'start'),
        ...    commands.command('assign', 'where', '$decision'),
        ...    commands.command('assign', 'transition', "'left'"),
        ...    commands.command('call', 'exploration', 'observe'),
        ...    commands.command('assign', 'transition', "'right'"),
        ...    commands.command('call', 'exploration', 'observe'),
        ...    commands.command('call', 'graph', 'destinationsFrom'),
        ...    commands.command('call', 'builtin', 'print'),
        ...    commands.command('assign', 'transition', "'right'"),
        ...    commands.command('assign', 'destination', "'EastRoom'"),
        ...    commands.command('call', 'exploration', 'explore'),
        ... ])
        {'left': 1, 'right': 2}
        >>> scope['decision']
        'START'
        >>> scope['where']
        'START'
        >>> scope['_']  # result of 'explore' call is dest ID
        2
        >>> scope['transition']
        'right'
        >>> scope['destination']
        'EastRoom'
        >>> g = e.getSituation().graph
        >>> len(e)
        3
        >>> len(g)
        3
        >>> g.namesListing(g)
        '  0 (START)\\n  1 (_u.0)\\n  2 (EastRoom)\\n'
        """
        if scope is None:
            scope = {}

        labelPositions: Dict[str, List[int]] = {}

        # Keep going until we've exhausted the commands list
        index = 0
        while index < len(block):

            # Execute the next command
            scope, skip, label = self.runCommand(
                block[index],
                scope,
                index + 1
            )

            # Increment our index, or apply a skip
            if skip is None:
                index = index + 1

            elif isinstance(skip, int):  # Integer skip value
                if skip < 0:
                    index += skip
                    if index < 0:  # can't skip before the start
                        index = 0
                else:
                    index += skip + 1  # may end loop if we skip too far

            else:  # must be a label name
                if skip in labelPositions:  # an established label
                    # We jump to the last previous index, or if there
                    # are none, to the first future index.
                    prevIndices = [
                        x
                        for x in labelPositions[skip]
                        if x < index
                    ]
                    futureIndices = [
                        x
                        for x in labelPositions[skip]
                        if x >= index
                    ]
                    if len(prevIndices) > 0:
                        index = max(prevIndices)
                    else:
                        index = min(futureIndices)
                else:  # must be a forward-reference
                    for future in range(index + 1, len(block)):
                        inspect = block[future]
                        if inspect.command == 'label':
                            inspect = cast(commands.Label, inspect)
                            if inspect.name == skip:
                                index = future
                                break
                    else:
                        raise KeyError(
                            f"Skip command indicated a jump to label"
                            f" {skip!r} but that label had not already"
                            f" been defined and there is no future"
                            f" label with that name either (future"
                            f" labels based on variables cannot be"
                            f" skipped to from above as their names"
                            f" are not known yet)."
                        )

            # If there's a label, record it
            if label is not None:
                labelPositions.setdefault(label, []).append(index)

            # And now the while loop continues, or ends if we're at the
            # end of the commands list.

        # Return the scope object.
        return scope
