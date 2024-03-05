"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-10-24
- Purpose: Analysis functions for decision graphs an explorations.
"""

from typing import (
    List, Dict, Tuple, Optional, TypeVar, Callable, Union, Any,
    ParamSpec, Concatenate, Set, cast
)

from . import base, core, parsing

import textwrap


#-------------------#
# Text descriptions #
#-------------------#

def describeConsequence(consequence: base.Consequence) -> str:
    """
    Returns a string which concisely describes a consequence list.
    Returns an empty string if given an empty consequence. Examples:

    >>> describeConsequence([])
    ''
    >>> describeConsequence([
    ...     base.effect(gain=('gold', 5), delay=2, charges=3),
    ...     base.effect(lose='flight')
    ... ])
    'gain gold*5 ,2 =3; lose flight'
    >>> from . import commands
    >>> d = describeConsequence([
    ...     base.effect(edit=[
    ...         [
    ...             commands.command('val', '5'),
    ...             commands.command('empty', 'list'),
    ...             commands.command('append')
    ...         ],
    ...         [
    ...             commands.command('val', '11'),
    ...             commands.command('assign', 'var'),
    ...             commands.command('op', '+', '$var', '$var')
    ...         ],
    ...     ])
    ... ])
    >>> d
    'with consequences:\
\\n    edit {\
\\n      val 5;\
\\n      empty list;\
\\n      append $_;\
\\n    } {\
\\n      val 11;\
\\n      assign var $_;\
\\n      op + $var $var;\
\\n    }\
\\n'
    >>> for line in d.splitlines():
    ...     print(line)
    with consequences:
        edit {
          val 5;
          empty list;
          append $_;
        } {
          val 11;
          assign var $_;
          op + $var $var;
        }
    """
    edesc = ''
    pf = parsing.ParseFormat()
    if consequence:
        parts = []
        for item in consequence:
            # TODO: Challenges and Conditions here!
            if 'skills' in item:  # a Challenge
                item = cast(base.Challenge, item)
                parts.append(pf.unparseChallenge(item))
            elif 'value' in item:  # an Effect
                item = cast(base.Effect, item)
                parts.append(pf.unparseEffect(item))
            elif 'condition' in item:  # a Condition
                item = cast(base.Condition, item)
                parts.append(pf.unparseCondition(item))
            else:
                raise TypeError(
                    f"Invalid consequence item (no 'skills', 'value', or"
                    f" 'condition' key found):\n{repr(item)}"
                )
        edesc = '; '.join(parts)
        if len(edesc) > 60 or '\n' in edesc:
            edesc = 'with consequences:\n' + ';\n'.join(
                textwrap.indent(part, '    ')
                for part in parts
            ) + '\n'

    return edesc


def describeProgress(exploration: core.DiscreteExploration) -> str:
    """
    Describes the progress of an exploration by noting each room/zone
    visited and explaining the options visible at each point plus which
    option was taken. Notes powers/tokens gained/lost along the way.
    Returns a string.

    Example:
    >>> from exploration import journal
    >>> e = journal.convertJournal('''\\
    ... S Start::pit
    ... A gain jump
    ... A gain attack
    ... n button check
    ... zz Wilds
    ... o up
    ...   q _flight
    ... o left
    ... x left left_nook right
    ... a geo_rock
    ...   At gain geo*15
    ...   At deactivate
    ... o up
    ...   q _tall_narrow
    ... t right
    ... o right
    ...   q attack
    ... ''')
    >>> for line in describeProgress(e).splitlines():
    ...    print(line)
    Start of the exploration
    Start exploring domain main at 0 (Start::pit)
      Gained capability 'attack'
      Gained capability 'jump'
    At decision 0 (Start::pit)
      In zone Start
      In region Wilds
      There are transitions:
        left to unconfirmed
        up to unconfirmed; requires _flight
      1 note(s) at this step
    Explore left from decision 0 (Start::pit) to 2 (now Start::left_nook)
    At decision 2 (Start::left_nook)
      There are transitions:
        right to 0 (Start::pit)
      There are actions:
        geo_rock
    Do action geo_rock
      Gained 15 geo(s)
    Take right from decision 2 (Start::left_nook) to 0 (Start::pit)
    At decision 0 (Start::pit)
      There are transitions:
        left to 2 (Start::left_nook)
        right to unconfirmed; requires attack
        up to unconfirmed; requires _flight
    Waiting for another action...
    End of the exploration.
    """
    result = ''

    regions: Set[base.Zone] = set()
    zones: Set[base.Zone] = set()
    last: Union[base.DecisionID, Set[base.DecisionID], None] = None
    lastState: base.State = base.emptyState()
    prevCapabilities = base.effectiveCapabilitySet(lastState)
    prevMechanisms = lastState['mechanisms']
    oldActiveDecisions: Set[base.DecisionID] = set()
    for i, situation in enumerate(exploration):
        if i == 0:
            result += "Start of the exploration\n"

        # Extract info
        graph = situation.graph
        activeDecisions = exploration.getActiveDecisions(i)
        newActive = activeDecisions - oldActiveDecisions
        departedFrom = exploration.movementAtStep(i)[0]
        # TODO: use the other parts of this?
        nowZones: Set[base.Zone] = set()
        for active in activeDecisions:
            nowZones |= graph.zoneAncestors(active)
        regionsHere = set(
            z
            for z in nowZones
            if graph.zoneHierarchyLevel(z) == 1
        )
        zonesHere = set(
            z
            for z in nowZones
            if graph.zoneHierarchyLevel(z) == 0
        )
        here = departedFrom
        state = situation.state
        capabilities = base.effectiveCapabilitySet(state)
        mechanisms = state['mechanisms']

        # Describe capabilities gained/lost relative to previous step
        # (i.e., as a result of the previous action)
        gained = (
            capabilities['capabilities']
          - prevCapabilities['capabilities']
        )
        gainedTokens = []
        for tokenType in capabilities['tokens']:
            net = (
                capabilities['tokens'][tokenType]
              - prevCapabilities['tokens'].get(tokenType, 0)
            )
            if net != 0:
                gainedTokens.append((tokenType, net))
        changed = [
            mID
            for mID in list(mechanisms.keys()) + list(prevMechanisms.keys())
            if mechanisms.get(mID) != prevMechanisms.get(mID)
        ]

        for capability in sorted(gained):
            result += f"  Gained capability '{capability}'\n"

        for tokenType, net in gainedTokens:
            if net > 0:
                result += f"  Gained {net} {tokenType}(s)\n"
            else:
                result += f"  Lost {-net} {tokenType}(s)\n"

        for mID in changed:
            oldState = prevMechanisms.get(mID, base.DEFAULT_MECHANISM_STATE)
            newState = mechanisms.get(mID, base.DEFAULT_MECHANISM_STATE)

            details = graph.mechanismDetails(mID)
            if details is None:
                mName = "(unknown)"
            else:
                mName = details[1]
            result += (
                f"  Set mechanism {mID} ({mName}) to {newState} (was"
                f" {oldState})"
            )
            # TODO: Test this!

        if isinstance(departedFrom, base.DecisionID):
            # Print location info
            if here != last:
                if here is None:
                    result += "Without a position...\n"
                elif isinstance(here, set):
                    result += f"With {len(here)} active decisions\n"
                    # TODO: List them using namesListing?
                else:
                    result += f"At decision {graph.identityOf(here)}\n"
            newZones = zonesHere - zones
            for zone in sorted(newZones):
                result += f"  In zone {zone}\n"
            newRegions = regionsHere - regions
            for region in sorted(newRegions):
                result += f"  In region {region}\n"

        elif isinstance(departedFrom, set):  # active in spreading domain
            spreadingDomain = graph.domainFor(list(departedFrom)[0])
            result += (
                f"  In domain {spreadingDomain} with {len(departedFrom)}"
                f" active decisions...\n"
            )

        else:
            assert departedFrom is None

        # Describe new position/positions at start of this step
        if len(newActive) > 1:
            newListing = ', '.join(
                sorted(graph.identityOf(n) for n in newActive)
            )
            result += (
                f"  There are {len(newActive)} new active decisions:"
                f"\n  {newListing}"
            )

        elif len(newActive) == 1:
            here = list(newActive)[0]

            outgoing = graph.destinationsFrom(here)

            transitions = {t: d for (t, d) in outgoing.items() if d != here}
            actions = {t: d for (t, d) in outgoing.items() if d == here}
            if transitions:
                result += "  There are transitions:\n"
                for transition in sorted(transitions):
                    dest = transitions[transition]
                    if not graph.isConfirmed(dest):
                        destSpec = 'unconfirmed'
                    else:
                        destSpec = graph.identityOf(dest)
                    req = graph.getTransitionRequirement(here, transition)
                    rDesc = ''
                    if req != base.ReqNothing():
                        rDesc = f"; requires {req.unparse()}"
                    cDesc = describeConsequence(
                        graph.getConsequence(here, transition)
                    )
                    if cDesc:
                        cDesc = '; ' + cDesc
                    result += (
                        f"    {transition} to {destSpec}{rDesc}{cDesc}\n"
                    )

            if actions:
                result += "  There are actions:\n"
                for action in sorted(actions):
                    req = graph.getTransitionRequirement(here, action)
                    rDesc = ''
                    if req != base.ReqNothing():
                        rDesc = f"; requires {req.unparse()}"
                    cDesc = describeConsequence(
                        graph.getConsequence(here, action)
                    )
                    if cDesc:
                        cDesc = '; ' + cDesc
                    if rDesc or cDesc:
                        desc = (rDesc + cDesc)[2:]  # chop '; ' from either
                        result += f"    {action} ({desc})\n"
                    else:
                        result += f"    {action}\n"

        # note annotations
        if len(situation.annotations) > 0:
            result += (
                f"  {len(situation.annotations)} note(s) at this step\n"
            )

        # Describe action taken
        if situation.action is None and situation.type == "pending":
            result += "Waiting for another action...\n"
        else:
            desc = base.describeExplorationAction(situation, situation.action)
            desc = desc[0].capitalize() + desc[1:]
            result += desc + '\n'

        if i == len(exploration) - 1:
            result += "End of the exploration.\n"

        # Update state variables
        oldActiveDecisions = activeDecisions
        prevCapabilities = capabilities
        prevMechanisms = mechanisms
        regions = regionsHere
        zones = zonesHere
        if here is not None:
            last = here
        lastState = state

    return result


#--------------------#
# Analysis functions #
#--------------------#

def lastIdentity(
    exploration: core.DiscreteExploration,
    decision: base.DecisionID
):
    """
    Returns the `identityOf` result for the specified decision in the
    last step in which that decision existed.
    """
    for i in range(-1, -len(exploration) - 1, -1):
        situation = exploration.getSituation(i)
        try:
            return situation.graph.identityOf(decision)
        except core.MissingDecisionError:
            pass
    raise core.MissingDecisionError(
        f"Decision {decision!r} never existed."
    )


def unexploredBranches(
    graph: core.DecisionGraph,
    context: Optional[base.RequirementContext] = None
) -> List[Tuple[base.DecisionID, base.Transition]]:
    """
    Returns a list of from-decision, transition-at-that-decision pairs
    which each identify an unexplored branch in the given graph.

    When a `context` is provided it only counts options whose
    requirements are satisfied in that `RequirementContext`, and the
    'searchFrom' part of the context will be replaced by both ends of
    each transition tested. This doesn't perfectly map onto actually
    reachability since nodes between where the player is and where the
    option is might force changes in the game state that make it
    un-takeable.

    TODO: add logic to detect trivially-unblocked edges?
    """
    result = []
    # TODO: Fix networkx type stubs for MultiDiGraph!
    for (src, dst, transition) in graph.edges(keys=True):  # type:ignore
        req = graph.getTransitionRequirement(src, transition)
        localContext: Optional[base.RequirementContext] = None
        if context is not None:
            localContext = base.RequirementContext(
                state=context.state,
                graph=context.graph,
                searchFrom=graph.bothEnds(src, transition)
            )
        # Check if this edge goes from a confirmed to an unconfirmed node
        if (
            graph.isConfirmed(src)
        and not graph.isConfirmed(dst)
        and (localContext is None or req.satisfied(localContext))
        ):
            result.append((src, transition))
    return result


def currentDecision(situation: base.Situation) -> str:
    """
    Returns the `identityOf` string for the current decision in a given
    situation.
    """
    return situation.graph.identityOf(situation.state['primaryDecision'])


def countAllUnexploredBranches(situation: base.Situation) -> int:
    """
    Counts the number of unexplored branches in the given situation's
    graph, regardless of traversibility (see `unexploredBranches`).
    """
    return len(unexploredBranches(situation.graph))


def countTraversableUnexploredBranches(situation: base.Situation) -> int:
    """
    Counts the number of traversable unexplored branches (see
    `unexploredBranches`) in a given situation, using the situation's
    game state to determine which branches are traversable or not
    (although this isn't strictly perfect TODO: Fix that).
    """
    context = base.genericContextForSituation(
        situation,
        base.combinedDecisionSet(situation.state)
    )
    return len(unexploredBranches(situation.graph, context))


def countActionsAtDecision(
    graph: core.DecisionGraph,
    decision: base.DecisionID
) -> Optional[int]:
    """
    Given a graph and a particular decision within that graph, returns
    the number of actions available at that decision. Returns None if the
    specified decision does not exist.
    """
    if decision not in graph:
        return None
    return len(graph.decisionActions(decision))


def countBranches(
    graph: core.DecisionGraph,
    decision: base.DecisionID
) -> Optional[int]:
    """
    Computes the number of branches at a particular decision, not
    counting actions. Returns `None` for unvisited and nonexistent
    decisions so that they aren't counted as part of averages.
    """
    if decision not in graph or not graph.isConfirmed(decision):
        return None

    dests = graph.destinationsFrom(decision)
    branches = 0
    for transition, dest in dests.items():
        if dest != decision:
            branches += 1

    return branches


def countRevisits(
    exploration: core.DiscreteExploration,
    decision: base.DecisionID
) -> int:
    """
    Given an `DiscreteExploration` object and a particular `Decision`
    which exists at some point during that exploration, counts the number
    of times that decision was activated after its initial discovery (not
    counting steps where we remain in it due to a wait or action).

    Returns 0 even for decisions that aren't part of the exploration.
    """
    result = 0
    wasActive = False
    for i in range(len(exploration)):
        active = exploration.getActiveDecisions(i)
        if decision in active:
            if not wasActive:
                result += 1
            wasActive = True
        else:
            wasActive = False

    # Make sure not to return -1 for decisions that were never visited
    if result >= 1:
        return result - 1
    else:
        return 0


#-----------------------#
# Generalizer Functions #
#-----------------------#

# Some type variables to make type annotations work
T = TypeVar('T')
P = ParamSpec('P')


def analyzeGraph(
    routine: Callable[Concatenate[core.DecisionGraph, P], T]
) -> Callable[Concatenate[base.Situation, P], T]:
    """
    Wraps a `DecisionGraph` analysis routine (possibly with extra
    arguments), returning a function which applies that analysis to a
    `Situation`.
    """
    def analyzesGraph(
        situation: base.Situation,
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:
        "Created by `analyzeGraph`."
        return routine(situation.graph, *args, **kwargs)

    analyzesGraph.__name__ = routine.__name__ + "InSituation"
    analyzesGraph.__doc__ = f"""
    Application of a graph analysis routine to a situation.

    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return analyzesGraph


def perDecision(
    routine: Callable[[base.Situation, base.DecisionID], T]
) -> Callable[[base.Situation], Dict[base.DecisionID, T]]:
    """
    Returns a wrapped function that applies the given
    individual-decision analysis routine to each decision in a
    situation, returning a dictionary mapping decisions to results.
    """
    def appliedPerDecision(
        situation: base.Situation,
    ) -> Dict[base.DecisionID, T]:
        'Created by `perDecision`.'
        result = {}
        for decision in situation.graph:
            result[decision] = routine(situation, decision)
        return result
    appliedPerDecision.__name__ = routine.__name__ + "PerDecision"
    appliedPerDecision.__doc__ = f"""
    Application of an analysis routine to each decision in a situation,
    returning a dictionary mapping decisions to results. The analysis
    routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return appliedPerDecision


def perExplorationDecision(
    routine: Callable[[core.DiscreteExploration, base.DecisionID], T],
    mode: str = "all"
) -> Callable[[core.DiscreteExploration], Dict[base.DecisionID, T]]:
    """
    Returns a wrapped function that applies the given
    decision-in-exploration analysis routine to each decision in an
    exploration, returning a dictionary mapping decisions to results.

    The `mode` argument controls what we mean by "each decision:" use
    "all" to apply it to all decisions which ever existed, "known" to
    apply it to all decisions which were known at any point, "visited"
    to apply it to all visited decisions, and "final" to apply it to
    each decision in the final decision graph.
    """
    def appliedPerDecision(
        exploration: core.DiscreteExploration,
    ) -> Dict[base.DecisionID, T]:
        'Created by `perExplorationDecision`.'
        result = {}
        now = exploration.getSituation()
        graph = now.graph
        if mode == "all":
            applyTo = exploration.allDecisions()
        elif mode == "known":
            applyTo = exploration.allExploredDecisions()
        elif mode == "visited":
            applyTo = exploration.allVisitedDecisions()
        elif mode == "final":
            applyTo = list(graph)

        for decision in applyTo:
            result[decision] = routine(exploration, decision)

        return result

    appliedPerDecision.__name__ = routine.__name__ + "PerExplorationDecision"
    desc = mode + ' '
    if desc == "all ":
        desc = ''
    appliedPerDecision.__doc__ = f"""
    Application of an analysis routine to each {desc}decision in an
    exploration, returning a dictionary mapping decisions to results. The
    analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return appliedPerDecision


Base = TypeVar('Base', base.Situation, core.DiscreteExploration)
"Either a situation or an exploration."


def sumOfResults(
    routine: Callable[
        [Base],
        Dict[Any, Union[int, float, complex, None]]
    ]
) -> Callable[[Base], Union[int, float, complex]]:
    """
    Given an analysis routine that applies to either a situation or an
    exploration and which returns a dictionary mapping some analysis
    units to individual numerical results, returns a new analysis
    routine which applies to the same input and which returns a single
    number that's the sum of the individual results, ignoring `None`s.
    Returns 0 if there are no results.
    """
    def sumResults(base: Base) -> Union[int, float, complex]:
        "Created by sumOfResults"
        results = routine(base)
        return sum(v for v in results.values() if v is not None)

    sumResults.__name__ = routine.__name__ + "Sum"
    sumResults.__doc__ = f"""
    Sum of analysis results over analysis units.
    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return sumResults


def meanOfResults(
    routine: Callable[
        [Base],
        Dict[Any, Union[int, float, complex, None]]
    ]
) -> Callable[[Base], Union[int, float, complex, None]]:
    """
    Works like `sumOfResults` but returns a function which gives the
    mean, not the sum. The function will return `None` if there are no
    results.
    """
    def meanResult(base: Base) -> Union[int, float, complex, None]:
        "Created by meanOfResults"
        results = routine(base)
        nums = [v for v in results.values() if v is not None]
        if len(nums) == 0:
            return None
        else:
            return sum(nums) / len(nums)

    meanResult.__name__ = routine.__name__ + "Mean"
    meanResult.__doc__ = f"""
    Mean of analysis results over analysis units.
    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return meanResult


def medianOfResults(
    routine: Callable[
        [Base],
        Dict[Any, Union[int, float, None]]
    ]
) -> Callable[[Base], Union[int, float, None]]:
    """
    Works like `sumOfResults` but returns a function which gives the
    median, not the sum. The function will return `None` if there are no
    results.
    """
    def medianResult(base: Base) -> Union[int, float, None]:
        "Created by medianOfResults"
        results = routine(base)
        nums = sorted(v for v in results.values() if v is not None)
        half = len(nums) // 2
        if len(nums) == 0:
            return None
        elif len(nums) % 2 == 0:
            return (nums[half] + nums[half + 1]) / 2
        else:
            return nums[half]

    medianResult.__name__ = routine.__name__ + "Mean"
    medianResult.__doc__ = f"""
    Mean of analysis results over analysis units.
    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return medianResult


def perSituation(
    routine: Callable[[base.Situation], T]
) -> Callable[[core.DiscreteExploration], List[T]]:
    """
    Returns a function which will apply an analysis routine to each
    situation in an exploration, returning a list of results.
    """
    def appliedPerSituation(
        exploration: core.DiscreteExploration
    ) -> List[T]:
        result = []
        for situ in exploration:
            result.append(routine(situ))
        return result

    appliedPerSituation.__name__ = routine.__name__ + "PerSituation"
    appliedPerSituation.__doc__ = f"""
    Analysis routine applied to each situation in an exploration,
    returning a list of results.

    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return appliedPerSituation
