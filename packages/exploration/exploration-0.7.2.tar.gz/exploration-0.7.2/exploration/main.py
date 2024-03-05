"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-10-15
- Purpose: Main API entry points to support the `__main__.py` script.
"""

from __future__ import annotations

import argparse
import pathlib
import textwrap
import sys
import csv
import networkx as nx  # type: ignore

from typing import (
    Literal, Optional, Union, get_args, TypeAlias, List, Callable, Dict,
    Sequence
)

from . import journal
from . import core
from . import base
from . import analysis
from . import parsing


#------------#
# File input #
#------------#

SourceType: TypeAlias = Literal[
    "graph",
    "dot",
    "exploration",
    "journal",
]
"""
The file types we recognize.
"""


def determineFileType(filename: str) -> SourceType:
    if filename.endswith('.dcg'):
        return 'graph'
    elif filename.endswith('.dot'):
        return 'dot'
    elif filename.endswith('.exp'):
        return 'exploration'
    elif filename.endswith('.exj'):
        return 'journal'
    else:
        raise ValueError(
            f"Could not determine the file type of file '{filename}':"
            f" it does not end with '.dcg', '.dot', '.exp', or '.exj'."
        )


def loadDecisionGraph(path: pathlib.Path) -> core.DecisionGraph:
    """
    Loads a JSON-encoded decision graph from a file. The extension
    should normally be '.dcg'.
    """
    with path.open('r', encoding='utf-8-sig') as fInput:
        return parsing.loadCustom(fInput, core.DecisionGraph)


def saveDecisionGraph(
    path: pathlib.Path,
    graph: core.DecisionGraph
) -> None:
    """
    Saves a decision graph encoded as JSON in the specified file. The
    file should normally have a '.dcg' extension.
    """
    with path.open('w', encoding='utf-8') as fOutput:
        parsing.saveCustom(graph, fOutput)


def loadDotFile(path: pathlib.Path) -> core.DecisionGraph:
    """
    Loads a `core.DecisionGraph` form the file at the specified path
    (whose extension should normally be '.dot'). The file format is the
    GraphViz "dot" format.
    """
    with path.open('r', encoding='utf-8-sig') as fInput:
        dot = fInput.read()
        try:
            return parsing.parseDot(dot)
        except parsing.DotParseError:
            raise parsing.DotParseError(
                "Failed to parse Dot file contents:\n\n"
              + dot
              + "\n\n(See error above for specific parsing issue.)"
            )


def saveDotFile(path: pathlib.Path, graph: core.DecisionGraph) -> None:
    """
    Saves a `core.DecisionGraph` as a GraphViz "dot" file. The file
    extension should normally be ".dot".
    """
    dotStr = parsing.toDot(graph, clusterLevels=[])
    with path.open('w', encoding='utf-8') as fOutput:
        fOutput.write(dotStr)


def loadExploration(path: pathlib.Path) -> core.DiscreteExploration:
    """
    Loads a JSON-encoded `core.DiscreteExploration` object from the file
    at the specified path. The extension should normally be '.exp'.
    """
    with path.open('r', encoding='utf-8-sig') as fInput:
        return parsing.loadCustom(fInput, core.DiscreteExploration)


def saveExploration(
    path: pathlib.Path,
    exploration: core.DiscreteExploration
) -> None:
    """
    Saves a `core.DiscreteExploration` object as JSON in the specified
    file. The file extension should normally be '.exp'.
    """
    with path.open('w', encoding='utf-8') as fOutput:
        parsing.saveCustom(exploration, fOutput)


def loadJournal(path: pathlib.Path) -> core.DiscreteExploration:
    """
    Loads a `core.DiscreteExploration` object from a journal file
    (extension should normally be '.exj'). Uses the
    `journal.convertJournal` function.
    """
    with path.open('r', encoding='utf-8-sig') as fInput:
        return journal.convertJournal(fInput.read())


def saveAsJournal(
    path: pathlib.Path,
    exploration: core.DiscreteExploration
) -> None:
    """
    Saves a `core.DiscreteExploration` object as a text journal in the
    specified file. The file extension should normally be '.exj'.

    TODO: This?!
    """
    raise NotImplementedError(
        "DiscreteExploration-to-journal conversion is not implemented"
        " yet."
    )


def loadSource(
    path: pathlib.Path,
    formatOverride: Optional[SourceType] = None
) -> Union[core.DecisionGraph, core.DiscreteExploration]:
    """
    Loads either a `core.DecisionGraph` or a `core.DiscreteExploration`
    from the specified file, depending on its file extension (or the
    specified format given as `formatOverride` if there is one).
    """
    if formatOverride is not None:
        format = formatOverride
    else:
        format = determineFileType(str(path))

    if format == "graph":
        return loadDecisionGraph(path)
    if format == "dot":
        return loadDotFile(path)
    elif format == "exploration":
        return loadExploration(path)
    elif format == "journal":
        return loadJournal(path)
    else:
        raise ValueError(
            f"Unrecognized file format '{format}' (recognized formats"
            f" are 'graph', 'exploration', and 'journal')."
        )


#---------------------#
# Analysis tool lists #
#---------------------#

AnalysisResult: TypeAlias = Union[None, bool, str, int, float, complex]
"""
A type alias for values we're willing to accept as analysis results.
These are going to be written to a CSV file that we want to be
human-readable.
"""

STEPWISE_DECISION_ANALYSIS_TOOLS: Dict[
    str,
    Callable[[base.Situation, base.DecisionID], AnalysisResult]
] = {
    "actionCount": analysis.analyzeGraph(analysis.countActionsAtDecision),
    "branchCount": analysis.analyzeGraph(analysis.countBranches)
}
"""
The analysis functions to apply to each decision in each step when
analyzing an exploration, and the names for each.
"""

STEP_ANALYSIS_TOOLS: Dict[
    str,
    Callable[[base.Situation], AnalysisResult]
] = {
    "currentDecision": analysis.currentDecision,
    "unexploredCount": analysis.countAllUnexploredBranches,
    "traversableUnexploredCount": analysis.countTraversableUnexploredBranches,
    "meanActions": analysis.meanOfResults(
        analysis.perDecision(
            analysis.analyzeGraph(analysis.countActionsAtDecision)
        )
    ),
    "meanBranches": analysis.meanOfResults(
        analysis.perDecision(
            analysis.analyzeGraph(analysis.countBranches)
        )
    ),
}
"""
The analysis functions to apply to each step when analyzing an
exploration, and the names for each.
"""

DECISION_ANALYSIS_TOOLS: Dict[
    str,
    Callable[
        [core.DiscreteExploration, base.DecisionID],
        AnalysisResult
    ]
] = {
    "identity": analysis.lastIdentity,
    "isVisited": lambda e, d: d in e.allVisitedDecisions(),
    "revisitCount": analysis.countRevisits,
}
"""
The analysis functions to apply once to each decision in an exploration,
and the names for each.
"""

WHOLE_ANALYSIS_TOOLS: Dict[
    str,
    Callable[[core.DiscreteExploration], AnalysisResult]
] = {
    "stepCount": lambda e: len(e),
    "finalDecisionCount": lambda e: len(e.getSituation().graph),
    "meanRevisits": analysis.meanOfResults(
        analysis.perExplorationDecision(
            analysis.countRevisits,
            mode="visited"
        )
    )
}
"""
The analysis functions to apply to entire explorations, and the names
for each.
"""


#---------------#
# API Functions #
#---------------#

def show(
    source: pathlib.Path,
    formatOverride: Optional[SourceType] = None,
    step: int = -1
) -> None:
    """
    Shows the graph or exploration stored in the `source` file. You will
    need to have the `matplotlib` library installed. Consider using the
    interactive interface provided by the `explorationViewer` module
    instead. The file extension is used to determine how to load the data,
    although the `--format` option may override this. '.dcg' files are
    assumed to be decision graphs in JSON format, '.exp' files are assumed
    to be exploration objects in JSON format, and '.exj' files are assumed
    to be exploration journals in the default journal format. If the object
    that gets loaded is an exploration, the final graph for that
    exploration will be displayed, or a specific graph may be selected
    using `--step`.
    """
    obj = loadSource(source, formatOverride)
    if isinstance(obj, core.DiscreteExploration):
        obj = obj.getSituation(step).graph

    import matplotlib.pyplot # type: ignore

    # This draws the graph in a new window that pops up. You have to close
    # the window to end the program.
    nx.draw(obj)
    matplotlib.pyplot.show()


def analyze(
    source: pathlib.Path,
    formatOverride: Optional[SourceType] = None,
    destination: Optional[pathlib.Path] = None,
    applyTools: Optional[List[str]] = None
) -> None:
    """
    Analyzes the exploration stored in the `source` file. The file
    extension is used to determine how to load the data, although this
    may be overridden by the `--format` option. Normally, '.exp' files
    are treated as JSON-encoded exploration objects, while '.exj' files
    are treated as journals using the default journal format.

    This applies a number of analysis functions to produce a CSV file
    showing per-decision-per-step, per-decision, per-step, and
    per-exploration metrics. A subset of the available metrics may be
    selected by passing a list of strings for the `applyTools` argument.
    See the `STEPWISE_DECISION_ANALYSIS_TOOLS`, `STEP_ANALYSIS_TOOLS`,
    `DECISION_ANALYSIS_TOOLS`, and `WHOLE_ANALYSIS_TOOLS` dictionaries
    for tool names.

    If no output file is specified, the output will be printed out.
    """
    # Load our source exploration object:
    obj = loadSource(source, formatOverride)
    if isinstance(obj, core.DecisionGraph):
        obj = core.DiscreteExploration.fromGraph(obj)

    exploration: core.DiscreteExploration = obj

    # Apply all of the analysis functions (or only just those that are
    # selected using applyTools):

    wholeRows: List[List[AnalysisResult]] = [['Whole exploration metrics:']]
    # One row per tool
    for tool in WHOLE_ANALYSIS_TOOLS:
        if (applyTools is None) or (tool in applyTools):
            wholeRows.append(
                [tool, WHOLE_ANALYSIS_TOOLS[tool](exploration)]
            )

    decisionRows: List[Sequence[AnalysisResult]] = [
        ['Per-decision metrics:']
    ]
    # One row per tool; one column per decision
    decisionList = exploration.allDecisions()
    columns = ['Metric ↓/Decision →'] + decisionList
    decisionRows.append(columns)
    for tool in DECISION_ANALYSIS_TOOLS:
        if (applyTools is None) or (tool in applyTools):
            row: List[AnalysisResult] = [tool]
            decisionRows.append(row)
            for decision in decisionList:
                row.append(
                    DECISION_ANALYSIS_TOOLS[tool](exploration, decision)
                )

    stepRows: List[Sequence[AnalysisResult]] = [
        ['Per-step metrics:']
    ]
    # One row per exploration step; one column per tool
    columns = ['Step ↓/Metric →']
    stepRows.append(columns)
    for i, situation in enumerate(exploration):
        row = [i]
        stepRows.append(row)
        for tool in STEP_ANALYSIS_TOOLS:
            if (applyTools is None) or (tool in applyTools):
                if i == 0:
                    columns.append(tool)
                row.append(STEP_ANALYSIS_TOOLS[tool](situation))

    stepwiseRows: List[Sequence[AnalysisResult]] = [
        ['Per-decision-per-step, metrics (one table per metric):']
    ]
    # For each tool; one row per exploration step and one column per
    # decision
    decisionList = exploration.allDecisions()
    columns = ['Step ↓/Decision →'] + decisionList
    identities = ['Decision names:'] + [
        analysis.lastIdentity(exploration, d)
        for d in decisionList
    ]
    for tool in STEPWISE_DECISION_ANALYSIS_TOOLS:
        if (applyTools is None) or (tool in applyTools):
            stepwiseRows.append([tool])
            stepwiseRows.append(columns)
            stepwiseRows.append(identities)
            for i, situation in enumerate(exploration):
                row = [i]
                stepwiseRows.append(row)
                for decision in decisionList:
                    row.append(
                        STEPWISE_DECISION_ANALYSIS_TOOLS[tool](
                            situation,
                            decision
                        )
                    )

    # Build a grid containing just the non-empty analysis categories, so
    # that if you deselect some tools you get a smaller CSV file:
    grid: List[Sequence[AnalysisResult]] = []
    if len(wholeRows) > 1:
        grid.extend(wholeRows)
    for block in decisionRows, stepRows, stepwiseRows:
        if len(block) > 1:
            if grid:
                grid.append([])  # spacer
            grid.extend(block)

    # Figure out our destination stream:
    if destination is None:
        outStream = sys.stdout
        closeIt = False
    else:
        outStream = open(destination, 'w')
        closeIt = True

    # Create a CSV writer for our stream
    writer = csv.writer(outStream)

    # Write out our grid to the file
    try:
        writer.writerows(grid)
    finally:
        if closeIt:
            outStream.close()


def convert(
    source: pathlib.Path,
    destination: pathlib.Path,
    inputFormatOverride: Optional[SourceType] = None,
    outputFormatOverride: Optional[SourceType] = None,
    step: int = -1
) -> None:
    """
    Converts between exploration and graph formats. By default, formats
    are determined by file extensions, but using the `--format` and
    `--output-format` options can override this. The available formats
    are:

    - '.dcg' A `core.DecisionGraph` stored in JSON format.
    - '.dot' A `core.DecisionGraph` stored as a GraphViz DOT file.
    - '.exp' A `core.DiscreteExploration` stored in JSON format.
    - '.exj' A `core.DiscreteExploration` stored as a journal (see
        `journal.JournalObserver`; TODO: writing this format).

    When converting a decision graph into an exploration format, the
    resulting exploration will have a single starting step containing
    the entire specified graph. When converting an exploration into a
    decision graph format, only the current graph will be saved, unless
    `--step` is used to specify a different step index to save.
    """
    # TODO journal writing
    obj = loadSource(source, inputFormatOverride)

    if outputFormatOverride is None:
        outputFormat = determineFileType(str(destination))
    else:
        outputFormat = outputFormatOverride

    if outputFormat in ("graph", "dot"):
        if isinstance(obj, core.DiscreteExploration):
            graph = obj.getSituation(step).graph
        else:
            graph = obj
        if outputFormat == "graph":
            saveDecisionGraph(destination, graph)
        else:
            saveDotFile(destination, graph)
    else:
        if isinstance(obj, core.DecisionGraph):
            exploration = core.DiscreteExploration.fromGraph(obj)
        else:
            exploration = obj
        if outputFormat == "exploration":
            saveExploration(destination, exploration)
        else:
            saveAsJournal(destination, exploration)


INSPECTOR_HELP = """
Available commands:

- 'help' or '?': List commands.
- 'done', 'quit', 'q', or 'exit': Quit the inspector.
- 'f' or 'follow': Follow the primary decision when changing steps. Also
    changes to that decision immediately. Toggles off if on.
- 'cd' or 'goto': Change focus decision to the named decision. Cancels
    follow mode.
- 'ls' or 'list' or 'destinations': Lists transitions at this decision
    and their destinations, as well as any mechanisms at this decision.
- 'lst' or 'steps': Lists each step of the exploration along with the
    primary decision at each step.
- 'st' or 'step': Switches to the specified step (an index)
- 'n' or 'next': Switches to the next step.
- 'p' or 'prev' or 'previous': Switches to the previous step.
- 't' or 'take': Change focus decision to the decision which is the
    destination of the specified transition at the current focused
    decision.
- 'prm' or 'primary': Displays the current primary decision.
- 'a' or 'active': Lists all currently active decisions
- 'u' or 'unexplored': Lists all unexplored transitions at the current
    step.
- 'x' or 'explorable': Lists all unexplored transitions at the current
    step which are traversable based on the current state. (TODO:
    make this more accurate).
- 'r' or 'reachable': TODO
- 'A' or 'all': Lists all decisions at the current step.
- 'M' or 'mechanisms': Lists all mechanisms at the current step.
"""


def inspect(
    source: pathlib.Path,
    formatOverride: Optional[SourceType] = None
) -> None:
    """
    Inspects the graph or exploration stored in the `source` file,
    launching an interactive command line for inspecting properties of
    decisions, transitions, and situations. The file extension is used
    to determine how to load the data, although the `--format` option
    may override this. '.dcg' files are assumed to be decision graphs in
    JSON format, '.exp' files are assumed to be exploration objects in
    JSON format, and '.exj' files are assumed to be exploration journals
    in the default journal format. If the object that gets loaded is a
    graph, a 1-step exploration containing just that graph will be
    created to inspect. Inspector commands are listed in the
    `INSPECTOR_HELP` variable.
    """
    print(f"Loading exploration from {source!r}...")
    # Load our exploration
    exploration = loadSource(source, formatOverride)
    if isinstance(exploration, core.DecisionGraph):
        exploration = core.DiscreteExploration.fromGraph(exploration)

    print(
        f"Inspecting exploration with {len(exploration)} step(s) and"
        f" {len(exploration.allDecisions())} decision(s):"
    )
    print("('h' for help)")

    # Set up tracking variables:
    step = len(exploration) - 1
    here: Optional[base.DecisionID] = exploration.primaryDecision(step)
    graph = exploration.getSituation(step).graph
    follow = True

    pf = parsing.ParseFormat()

    if here is None:
        print("Note: There are no decisions in the final graph.")

    while True:
        # Re-establish the prompt
        prompt = "> "
        if here is not None and here in graph:
            prompt = graph.identityOf(here) + "> "
        elif here is not None:
            prompt = f"{here} (?)> "

        # Prompt for the next command
        fullCommand = input(prompt).split()

        # Track number of invalid commands so we can quit after 10 in a row
        invalidCommands = 0

        if len(fullCommand) == 0:
            cmd = ''
            args = ''
        else:
            cmd = fullCommand[0]
            args = ' '.join(fullCommand[1:])

        # Do what the command says
        invalid = False
        if cmd in ("help", '?'):
            # Displays help message
            if len(args.strip()) > 0:
                print("(help does not accept any arguments)")
            print(INSPECTOR_HELP)
        elif cmd in ("done", "exit", "quit", "q"):
            # Exits the inspector
            if len(args.strip()) > 0:
                print("(quit does not accept any arguments)")
            print("Bye.")
            break
        elif cmd in ("f", "follow"):
            if follow:
                follow = False
                print("Stopped following")
            else:
                follow = True
                here = exploration.primaryDecision(step)
                print(f"Now following at: {graph.identityOf(here)}")
        elif cmd in ("cd", "goto"):
            # Changes focus to a specific decision
            try:
                target = pf.parseDecisionSpecifier(args)
                target = graph.resolveDecision(target)
                here = target
                follow = False
                print(f"now at: {graph.identityOf(target)}")
            except Exception:
                print("(invalid decision specifier)")
        elif cmd in ("ls", "list", "destinations"):
            fromID: Optional[base.AnyDecisionSpecifier] = None
            if args.strip():
                fromID = pf.parseDecisionSpecifier(args)
                fromID = graph.resolveDecision(fromID)
            else:
                fromID = here

            if fromID is None:
                print(
                    "(no focus decision and no decision specified;"
                    " nothing to list; use 'cd' to specify a decision,"
                    " or 'all' to list all decisions)"
                )
            else:
                outgoing = graph.destinationsFrom(fromID)
                info = graph.identityOf(fromID)
                if len(outgoing) > 0:
                    print(f"Destinations from {info}:")
                    print(graph.destinationsListing(outgoing))
                else:
                    print("No outgoing transitions from {info}.")
        elif cmd in ("lst", "steps"):
            total = len(exploration)
            print(f"{total} step(s):")
            for step in range(total):
                pr = exploration.primaryDecision(step)
                situ = exploration.getSituation(step)
                stGraph = situ.graph
                identity = stGraph.identityOf(pr)
                print(f"  {step} at {identity}")
            print(f"({total} total step(s))")
        elif cmd in ("st", "step"):
            stepTo = int(args.strip())
            if stepTo < 0:
                stepTo += len(exploration)
            if stepTo < 0:
                print(
                    f"Invalid step {args!r} (too negative; min is"
                    f" {-len(exploration)})"
                )
            if stepTo >= len(exploration):
                print(
                    f"Invalid step {args!r} (too large; max is"
                    f" {len(exploration) - 1})"
                )

            step = stepTo
            graph = exploration.getSituation(step).graph
            if follow:
                here = exploration.primaryDecision(step)
                print(f"Followed to: {graph.identityOf(here)}")
        elif cmd in ("n", "next"):
            if step == -1 or step >= len(exploration) - 2:
                print("Can't step beyond the last step.")
            else:
                step += 1
                graph = exploration.getSituation(step).graph
                if here not in graph:
                    here = None
            print(f"At step {step}")
            if follow:
                here = exploration.primaryDecision(step)
                print(f"Followed to: {graph.identityOf(here)}")
        elif cmd in ("p", "prev"):
            if step == 0 or step <= -len(exploration) + 2:
                print("Can't step before the first step.")
            else:
                step -= 1
                graph = exploration.getSituation(step).graph
                if here not in graph:
                    here = None
            print(f"At step {step}")
            if follow:
                here = exploration.primaryDecision(step)
                print(f"Followed to: {graph.identityOf(here)}")
        elif cmd in ("t", "take"):
            if here is None:
                print(
                    "(no focus decision, so can't take transitions. Use"
                    " 'cd' to specify a decision first.)"
                )
            else:
                dest = graph.getDestination(here, args)
                if dest is None:
                    print(
                        f"Invalid transition {args!r} (no destination for"
                        f" that transition from {graph.identityOf(here)}"
                    )
                here = dest
        elif cmd in ("prm", "primary"):
            pr = exploration.primaryDecision(step)
            if pr is None:
                print("Step {step} has no primary decision")
            else:
                print(
                    f"Primary decision for step {step} is:"
                    f" {graph.identityOf(pr)}"
                )
        elif cmd in ("a", "active"):
            active = exploration.getActiveDecisions(step)
            print(f"Active decisions at step {step}:")
            print(graph.namesListing(active))
        elif cmd in ("u", "unexplored"):
            unx = analysis.unexploredBranches(graph)
            fin = ':' if len(unx) > 0 else '.'
            print(f"{len(unx)} unexplored branch(es){fin}")
            for frID, unTr in unx:
                print(f"take {unTr} at {graph.identityOf(frID)}")
        elif cmd in ("x", "explorable"):
            ctx = base.genericContextForSituation(
                exploration.getSituation(step)
            )
            unx = analysis.unexploredBranches(graph, ctx)
            fin = ':' if len(unx) > 0 else '.'
            print(f"{len(unx)} unexplored branch(es){fin}")
            for frID, unTr in unx:
                print(f"take {unTr} at {graph.identityOf(frID)}")
        elif cmd in ("r", "reachable"):
            print("TODO: Reachable does not work yet.")
        elif cmd in ("A", "all"):
            print(
                f"There are {len(graph)} decision(s) at step {step}:"
            )
            for decision in graph.nodes():
                print(f"  {graph.identityOf(decision)}")
        elif cmd in ("M", "mechanisms"):
            count = len(graph.mechanisms)
            fin = ':' if count > 0 else '.'
            print(
                f"There are {count} mechanism(s) at step {step}{fin}"
            )
            for mID in graph.mechanisms:
                where, name = graph.mechanisms[mID]
                state = exploration.mechanismState(mID, step=step)
                if where is None:
                    print(f"  {name!r} (global) in state {state!r}")
                else:
                    info = graph.identityOf(where)
                    print(f"  {name!r} at {info} in state {state!r}")
        else:
            invalid = True

        if invalid:
            if invalidCommands >= 10:
                print("Too many invalid commands; exiting.")
                break
            else:
                if invalidCommands >= 8:
                    print("{invalidCommands} invalid commands so far,")
                    print("inspector will stop after 10 invalid commands...")
                print(f"Unknown command {cmd!r}...")
                invalidCommands += 1
                print(INSPECTOR_HELP)
        else:
            invalidCommands = 0


#--------------#
# Parser setup #
#--------------#

parser = argparse.ArgumentParser(
    prog="python -m exploration",
    description="""\
Runs various commands for processing exploration graphs and journals,
and for converting between them or displaying them in various formats.
"""
)
subparsers = parser.add_subparsers(
    title="commands",
    description="The available commands are:",
    help="use these with -h/--help for more details"
)

showParser = subparsers.add_parser(
    'show',
    help="show an exploration",
    description=textwrap.dedent(str(show.__doc__)).strip()
)
showParser.set_defaults(run="show")
showParser.add_argument(
    "source",
    type=pathlib.Path,
    help="The file to load"
)
showParser.add_argument(
    '-f',
    "--format",
    choices=get_args(SourceType),
    help=(
        "Which format the source file is in (normally that can be"
        " determined from the file extension)."
    )
)
showParser.add_argument(
    '-s',
    "--step",
    type=int,
    default=-1,
    help="Which graph step to show (when loading an exploration)."
)

analyzeParser = subparsers.add_parser(
    'analyze',
    help="analyze an exploration",
    description=textwrap.dedent(str(analyze.__doc__)).strip()
)
analyzeParser.set_defaults(run="analyze")
analyzeParser.add_argument(
    "source",
    type=pathlib.Path,
    help="The file holding the exploration to analyze"
)
analyzeParser.add_argument(
    "destination",
    default=None,
    type=pathlib.Path,
    help=(
        "The file name where the output should be written (this file"
        " will be overwritten without warning)."
    )
)
analyzeParser.add_argument(
    '-f',
    "--format",
    choices=get_args(SourceType),
    help=(
        "Which format the source file is in (normally that can be"
        " determined from the file extension)."
    )
)

convertParser = subparsers.add_parser(
    'convert',
    help="convert an exploration",
    description=textwrap.dedent(str(convert.__doc__)).strip()
)
convertParser.set_defaults(run="convert")
convertParser.add_argument(
    "source",
    type=pathlib.Path,
    help="The file holding the graph or exploration to convert."
)
convertParser.add_argument(
    "destination",
    type=pathlib.Path,
    help=(
        "The file name where the output should be written (this file"
        " will be overwritten without warning)."
    )
)
convertParser.add_argument(
    '-f',
    "--format",
    choices=get_args(SourceType),
    help=(
        "Which format the source file is in (normally that can be"
        " determined from the file extension)."
    )
)
convertParser.add_argument(
    '-o',
    "--output-format",
    choices=get_args(SourceType),
    help=(
        "Which format the converted file should be saved as (normally"
        " that is determined from the file extension)."
    )
)
convertParser.add_argument(
    '-s',
    "--step",
    type=int,
    default=-1,
    help=(
        "Which graph step to save (when converting from an exploration"
        " format to a graph format)."
    )
)

if __name__ == "__main__":
    options = parser.parse_args()
    if options.run == "show":
        show(
            options.source,
            formatOverride=options.format,
            step=options.step
        )
    elif options.run == "analyze":
        analyze(
            options.source,
            formatOverride=options.format,
            destination=options.destination
        )
    elif options.run == "convert":
        convert(
            options.source,
            options.destination,
            inputFormatOverride=options.format,
            outputFormatOverride=options.output_format,
            step=options.step
        )
    else:
        raise RuntimeError(
            f"Invalid 'run' default value: '{options.run}'."
        )
