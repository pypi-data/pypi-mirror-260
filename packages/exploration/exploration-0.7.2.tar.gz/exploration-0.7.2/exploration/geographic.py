"""
- Authors: Peter Mawhorter
- Consulted: Nissi Awosanya, Kitty Boakye
- Date: 2023-6-8
- Purpose: Types for representing open-world explorations.

Key types in this file are:

- `MetricSpace` (TODO): Represents a variable-dimensional coordinate system
    within which locations can be identified by coordinates.
- `FeatureGraph` (TODO): A graph-based representation of one or more
    navigable physical, virtual, or even abstract spaces, each composed
    of nodes, paths, edges, regions, landmarks, and/or affordances. It
    supports a variety of edge types between nodes, such as "contains"
    and "touches." Each conceptually separate space is marked as a
    domain.
- `FeatureDecision` (TODO): Represents a single decision made about what
    action to take next. Includes information on position(s) in a
    `FeatureGraph` (and possibly also in a `MetricSpace`) and about which
    features are relevant to the decision, plus what the chosen course
    of action was (as a `FeatureAction`).
- `GeographicExploration` (TODO): Represents a single agent's
    exploration progress through a geographic space. Includes zero or
    more `MetricSpace`s, a single list of `FeatureGraph`s representing
    the evolution of a single feature graph through discrete points in
    time, and a single list of `FeatureDecision`s representing the
    decisions made about what to do next at each of those time points.
    Supports cross-reference information between these data structures,
    and also links to multimedia resources such as images, videos, or
    audio files which can in turn be cross-referenced to metric spaces
    (and thence to the other data structures).
"""

from typing import (
    Optional, Union, List, Tuple, Set, Dict
)

import networkx as nx  # type: ignore[import]

from . import base


#--------------#
# Main Classes #
#--------------#

class MissingFeatureError(KeyError):
    """
    An error raised when an invalid feature ID or specifier is
    provided.
    """
    pass


class AmbiguousFeatureSpecifierError(KeyError):
    """
    An error raised when an ambiguous feature specifier is provided.
    Note that if a feature specifier simply doesn't match anything, you
    will get a `MissingFeatureError` instead.
    """
    pass


class FeatureGraph(nx.MultiDiGraph):
    """
    TODO
    A graph-based representation of a navigable physical, virtual, or
    even abstract space, composed of the features such as nodes, paths,
    and regions (see `FeatureType` for the full list of feature types).

    These elements are arranged in a variety of relationships such as
    'contains' or 'touches' (see `FeatureRelationshipType` for the full
    list).
    """
    def __init__(self, mainDomain: base.Domain = "main"):
        """
        Creates an empty `FeatureGraph`.
        """
        self.domains: List[base.Domain] = [mainDomain]
        self.nextID: base.FeatureID = 0
        super().__init__()

    def _register(self) -> base.FeatureID:
        """
        Returns the next ID to use and increments the ID counter.
        """
        result = self.nextID
        self.nextID += 1
        return result

    def findChainedRelations(
        self,
        root: base.FeatureID,
        relation: base.FeatureRelationshipType,
        names: List[base.Feature]
    ) -> Optional[List[base.FeatureID]]:
        """
        Looks for a chain of features whose names match the given list
        of feature names, starting from the feature with the specified
        ID (whose name must match the first name in the list). Each
        feature in the chain must be connected to the next by an edge of
        the given relationship type. Returns `None` if it cannot find
        such a chain. If there are multiple possible chains, returns the
        chain with ties broken towards features with lower IDs, starting
        from the front of the chain.

        For example:

        >>> fg = FeatureGraph.example('chasm')
        >>> root = fg.resolveFeature('east')
        >>> fg.findChainedRelations(root, 'within', ['east', 'main'])
        [1, 0]
        >>> root = fg.resolveFeature('downstairs')
        >>> fg.findChainedRelations(
        ...    root,
        ...    'within',
        ...    ['downstairs', 'house', 'west', 'main']
        ... )
        [17, 15, 2, 0]

        # TODO: Test with ambiguity!
        """
        if self.nodes[root]['name'] != names[0]:
            return None
        elif len(names) == 1:
            return [root]
        elif len(names) == 0:
            raise RuntimeError(
                "Ran out of names to match in findChainedRelations."
            )

        assert len(names) > 1
        remaining = names[1:]

        neighbors = sorted(self.relations(root, relation))
        if len(neighbors) == 0:
            return None
        else:
            for neighbor in neighbors:
                candidate = self.findChainedRelations(
                    neighbor,
                    relation,
                    remaining
                )
                if candidate is not None:
                    return [root] + candidate

            # Couldn't find a single candidate via any neighbor
            return None

    def featureName(self, fID: base.FeatureID) -> base.Feature:
        """
        Returns the name for a feature, given its ID.
        """
        return self.nodes[fID]['name']

    def resolveFeature(
        self,
        spec: base.AnyFeatureSpecifier
    ) -> base.FeatureID:
        """
        Given a `FeatureSpecifier`, returns the feature ID for the
        feature that it specifies, or raises an
        `AmbiguousFeatureSpecifierError` if the specifier is ambiguous.

        Cannot handle strings with multiple parts; use
        `parsing.ParseFormat.parseFeatureSpecifier` first if you need to
        do that.

        For example:

        >>> fg = FeatureGraph.example('chasm')
        >>> import exploration.parsing
        >>> pf = exploration.parsing.ParseFormat()
        >>> fg.resolveFeature('main')
        0
        >>> fg.resolveFeature('east')
        1
        >>> fg.resolveFeature('west')
        2
        >>> fg.resolveFeature(pf.parseFeatureSpecifier('main::west'))
        2
        >>> fg.resolveFeature(pf.parseFeatureSpecifier('main//main::west'))
        2
        >>> fg.resolveFeature(
        ...     base.FeatureSpecifier('main', ['main'], 'west', None)
        ... )
        2
        >>> fg.resolveFeature(base.FeatureSpecifier(None, [], 2, None))
        2
        >>> fg.resolveFeature(2)
        2
        >>> fg.resolveFeature(base.FeatureSpecifier(None, [], 'chasm', None))
        3
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("main//main::chasm"))
        3
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("main//east::chasm"))
        Traceback (most recent call last):
        ...
        exploration.geographic.MissingFeatureError...
        >>> fg.resolveFeature("chasmm")
        Traceback (most recent call last):
        ...
        exploration.geographic.MissingFeatureError...
        >>> fg.resolveFeature("house")
        Traceback (most recent call last):
        ...
        exploration.geographic.AmbiguousFeatureSpecifierError...
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("east::house"))
        6
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("west::house"))
        15
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("east::bridgePath"))
        13
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("west::bridgePath"))
        14
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("crossroads"))
        8
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("east::crossroads"))
        8
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("west::crossroads"))
        Traceback (most recent call last):
        ...
        exploration.geographic.MissingFeatureError...
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("main::crossroads"))
        Traceback (most recent call last):
        ...
        exploration.geographic.MissingFeatureError...
        >>> fg.resolveFeature(
        ...     pf.parseFeatureSpecifier("main::east::crossroads")
        ... )
        8
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("house::basement"))
        16
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("house::openChest"))
        7
        >>> fg.resolveFeature(pf.parseFeatureSpecifier("house::stairs"))
        19
        >>> fg2 = FeatureGraph.example('intercom')
        >>> fg2.resolveFeature("intercom")
        7
        >>> # Direct contains
        >>> fg2.resolveFeature(pf.parseFeatureSpecifier("kitchen::intercom"))
        7
        >>> # Also direct
        >>> fg2.resolveFeature(pf.parseFeatureSpecifier("inside::intercom"))
        7
        >>> # Both
        >>> fg2.resolveFeature(
        ...     pf.parseFeatureSpecifier("inside::kitchen::intercom")
        ... )
        7
        >>> # Indirect
        >>> fg2.resolveFeature(pf.parseFeatureSpecifier("house::intercom"))
        Traceback (most recent call last):
        ...
        exploration.geographic.MissingFeatureError...

        TODO: Test case with ambiguous parents in a lineage!
        """
        spec = base.normalizeFeatureSpecifier(spec)
        # If the feature specifier specifies an ID, return that:
        if isinstance(spec.feature, base.FeatureID):
            return spec.feature

        # Otherwise find all features with matching names:
        matches = [
            node
            for node in self
            if self.nodes[node]['name'] == spec.feature
        ]

        if len(matches) == 0:
            raise MissingFeatureError(
                f"There is no feature named '{spec.feature}'."
            )

        namesToMatch = [spec.feature] + list(reversed(spec.within))
        remaining: List[base.FeatureID] = [
            match
            for match in matches
            if (
                self.findChainedRelations(match, 'within', namesToMatch)
         is not None
            )
        ]

        if len(remaining) == 1:
            return remaining[0]
        else:
            matchDesc = ', '.join(
                f"'{name}'" for name in reversed(spec.within)
            )
            if len(remaining) == 0:
                raise MissingFeatureError(
                    f"There is/are {len(matches)} feature(s) named"
                    f" '{spec.feature}' but none of them are/it isn't"
                    f" within the series of features: {matchDesc}"
                    f"\nf:{spec.feature}\nntm:{namesToMatch}\n"
                    f"mt:{matches}\nrm:{remaining}"
                )
            else: # Must be more than one
                raise AmbiguousFeatureSpecifierError(
                    f"There is/are {len(matches)} feature(s) named"
                    f" '{spec.feature}', and there are still"
                    f" {len(remaining)} of those that are contained in"
                    f" {matchDesc}."
                )

    def featureType(self, fID: base.FeatureID) -> base.FeatureType:
        """
        Returns the feature type for the feature with the given ID.

        For example:

        >>> fg = FeatureGraph()
        >>> fg.addFeature('A', 'region')
        0
        >>> fg.addFeature('B', 'path')
        1
        >>> fg.featureType(0)
        'region'
        >>> fg.featureType(1)
        'path'
        >>> fg.featureType(2)
        Traceback (most recent call last):
        ...
        KeyError...
        >>> # TODO: Turn into an exploration.geographic.MissingFeatureError...
        >>> # Use in combination with resolveFeature if necessary:
        >>> fg.featureType(fg.resolveFeature('A'))
        'region'
        """
        return self.nodes[fID]['fType']

    @staticmethod
    def example(name: Optional[str]):
        """
        Creates and returns one of several example graphs. The available
        graphs are: 'chasm', 'town', 'intercom', and 'scripts'. 'chasm'
        is the default when no name is given. Descriptions of each are
        included below.

        ### Canyon

        Includes all available feature types, and all available relation
        types. Includes mild feature name ambiguity (disambiguable by
        region).

        - One main region, called 'main'.
        - Two subregions called 'east' and 'west'.
        - An edge between them called 'chasm' with a path called
          'bridge' that touches it. The chasm is tagged with a 'flight'
          power requirement. The bridge is tagged with an
          'openBridgeGate' requirement.
            * The east side of bridge has an affordance called 'bridgeLever'
              which is also in the east region, and the effect is to grant
              openBridgeGate. It requires (and consumes) a single
              'bridgeToken' token and is not repeatable.
        - In the east region, there is a node named 'house' with a
          single-use affordance attached called openChest that grants a
          single bridgeToken.
        - There is a path 'housePath' from the house that leads to a node
          called 'crossroads'. Paths from crossroads lead to startingGrove
          ('startPath') and to the bridge ('bridgePath'). (These paths touch
          the things they lead to.)
        - The landmark 'windmill' is at the crossroads.
        - In the west region, a path from the bridge (also named
          'bridgePath') leads to a node also named 'house.'
            * In this house, there are three regions: 'basement',
              'downstairs' and 'upstairs.' All three regions are connected
              with a path 'stairs.'
            * The downstairs is tagged as an entrance of the house (from the
              south part of the house to the south part of the downstairs).
              There is another entrance at the east part of the house
              directly into the basement.
        - The east and west regions are partially observable from each
          other. The upstairs and downstairs region of the west house can
          observe the west region, but the basement can't.
        - The west house is positioned 1 kilometer northeast of the
          center of the west region.
        - The east house is positioned TODO

        ### Town

        Has multiple-containment to represent paths that traverse
        through multiple regions, and also paths that cross at an
        intersection.

        - Top level regions called 'town' (id 0) and 'outside' (id 10).
        - An edge 'wall' (id 9) between them (touching both but within
          neither).
        - Regions 'market' (id 3), 'eastResidences' (id 4),
          'southResidences' (id 5), and 'castleHill' (id 1) within the
          town.
        - A node 'castle' (id 2) within the 'castleHill'.
        - A node 'marketSquare' (id 6) in the market.
        - Paths 'ringRoad' (id 7) and 'mainRoad' (id 8) in the town.
          Both of them touch the marketSquare.
            * 'ringRoad' is additionally within the market,
              eastResidences, and southResidences.
            * mainRoad is additionally within the market, castleHill,
              and outside.
            * mainRoad also touches the castle and the wall.

        ### Intercom

        Has complicated containment relationships, but few other
        relationships.

        - A top-level region named 'swamp' (id 0)
        - Regions 'eastSwamp', 'westSwamp', and 'midSwamp' inside of
          that (ids 1, 2, and 3 respectively). Conceptually, there's a
          bit of overlap between the mid and the two other regions; it
          touches both of them.
        - A node 'house' (id 4) that's in both the midSwamp and the
          westSwamp.
        - A region 'inside' (id 5) that's inside the house.
        - A region 'kitchen' (id 6) that's inside the 'inside.'
        - An affordance 'intercom' (id 7) that's inside both the kitchen
          and the 'inside.'

        ### Scripts

        This graph has complex affordances and triggers set up to
        represent mobile + interactive NPCs, as well as including an
        entity to represent the player's avatar. It has:

        - A region 'library' (id 0)
        - Regions '1stFloor', '2ndFloor', and '3rdFloor' within the
            library (ids 1, 2, and 3). These are positioned relative to
            each other using above/below.
        - A path 'lowerStairs' (id 4) whose bottom part is within the
            1st floor and whose top part is within the 2nd floor.
        - A path 'upperStairs' (id 5) whose bottom part is within the
            2nd floor and whose top part is within the 3rd floor. This
            path requires the '3rdFloorKey' to traverse.
        - An entity 'librarian' which is in the 1st floor. The librarian
            TODO
        """
        if name is None:
            name = 'chasm'

        fg = FeatureGraph()
        if name == 'chasm':
            fg.addFeature('main', 'region') # 0
            east = fg.addFeature('east', 'region', 'main') # 1
            west = fg.addFeature('west', 'region', 'main') # 2

            chasm = fg.addFeature('chasm', 'edge', 'main') # 3
            fg.relateFeatures(
                base.feature('east', 'west'),
                'touches',
                base.feature('chasm', 'east')
            )
            fg.relateFeatures(
                base.feature('west', 'east'),
                'touches',
                base.feature('chasm', 'west')
            )
            fg.tagFeature(chasm, 'requires', 'flight')

            bridge = fg.addFeature('bridge', 'path', 'main') # 4
            fg.relateFeatures(
                'bridge',
                'touches',
                base.feature('chasm', 'middle')
            )
            fg.relateFeatures(
                'bridge',
                'touches',
                base.feature('east', 'west')
            )
            fg.relateFeatures(
                'bridge',
                'touches',
                base.feature('west', 'east')
            )
            fg.tagFeature(
                bridge,
                'requires',
                base.ReqCapability('openBridgeGate')
            )

            bridgeLever = fg.addFeature('bridgeLever', 'affordance') # 5
            fg.relateFeatures(
                'bridgeLever',
                'within',
                base.feature('east', 'west')
            )
            fg.relateFeatures(
                'bridgeLever',
                'touches',
                base.feature('bridge', 'east')
            )
            fg.tagFeature(
                bridgeLever,
                'requires',
                base.ReqTokens('bridgeToken', 1)
            )
            # TODO: Bundle these into a single Consequence?
            fg.addEffect(
                'bridgeLever',
                'do',
                base.featureEffect(deactivate=True)
            )
            fg.addEffect(
                'bridgeLever',
                'do',
                base.featureEffect(gain='openBridgeGate')
            )
            # TODO: Use a mechanism for this instead?
            fg.addEffect(
                'bridgeLever',
                'do',
                base.featureEffect(lose='bridgeToken*1')
            )

            fg.addFeature('house', 'node') # 6
            fg.relateFeatures(
                'house',
                'within',
                base.feature('east', 'middle')
            )

            fg.addFeature('openChest', 'affordance') # 7
            fg.relateFeatures('openChest', 'within', 'house')
            fg.addEffect(
                'openChest',
                'do',
                base.featureEffect(deactivate=True)
            )
            fg.addEffect(
                'openChest',
                'do',
                base.featureEffect(gain=('bridgeToken', 1))
            )

            fg.addFeature('crossroads', 'node', 'east') # 8
            fg.addFeature('windmill', 'landmark', 'east') # 9
            fg.relateFeatures(
                'windmill',
                'touches',
                base.feature('crossroads', 'northeast')
            )

            fg.addFeature('housePath', 'path', 'east') # 10
            fg.relateFeatures(
                base.feature('housePath', 'east'),
                'touches',
                base.feature('house', 'west')
            )
            fg.relateFeatures(
                base.feature('housePath', 'west'),
                'touches',
                base.feature('crossroads', 'east')
            )

            fg.addFeature('startPath', 'path', 'east') # 11
            fg.relateFeatures(
                base.feature('startPath', 'south'),
                'touches',
                base.feature('crossroads', 'north')
            )

            fg.addFeature(
                'startingGrove',
                'node',
                base.feature('east', 'north')
            ) # 12
            fg.relateFeatures(
                base.feature('startingGrove', 'south'),
                'touches',
                base.feature('startPath', 'north')
            )

            fg.addFeature(
                'bridgePath',
                'path',
                base.feature('east', 'west')
            ) # 13
            fg.relateFeatures(
                base.feature('bridgePath', 'west'),
                'touches',
                base.feature('bridge', 'east')
            )
            fg.relateFeatures(
                base.feature('bridgePath', 'east'),
                'touches',
                base.feature('crossroads', 'west')
            )

            fg.addFeature('bridgePath', 'path', 'west') # 14
            fg.relateFeatures(
                base.feature('bridgePath', within=('west',)),
                'touches',
                base.feature('bridge', 'west')
            )

            h2ID = fg.addFeature(
                'house',
                'node',
                base.feature('west', 'middle')) # 15
            fg.relateFeatures(
                base.FeatureSpecifier(None, [], h2ID, 'south'),
                'touches',
                base.feature('bridgePath', 'east', within=('west',))
            )

            fg.addFeature(
                'basement',
                'region',
                base.feature('house', 'bottom', within=('west',))
            ) # 16
            fg.addFeature(
                'downstairs',
                'region',
                base.featurePart(h2ID, 'middle')
            ) # 17
            fg.addFeature('upstairs', 'region', base.featurePart(h2ID, 'top'))
            # 18
            fg.addFeature('stairs', 'path', h2ID) # 19

            fg.relateFeatures(
                base.feature('stairs', 'bottom'),
                'touches',
                base.feature('basement', 'north')
            )
            fg.relateFeatures(
                base.feature('stairs', 'middle'),
                'touches',
                base.feature('downstairs', 'north')
            )
            fg.relateFeatures(
                base.feature('stairs', 'top'),
                'touches',
                base.feature('upstairs', 'north')
            )
            fg.relateFeatures(
                base.feature('downstairs', 'south'),
                'entranceFor',
                base.feature('house', 'south', within=('west',))
            )
            fg.relateFeatures(
                base.feature('house', 'east', within=('west',)),
                'enterTo',
                base.feature('basement', 'east')
            )

            fg.relateFeatures('east', 'observable', 'west')
            fg.tagRelation(east, 'observable', west, 'partial')
            fg.relateFeatures('west', 'observable', 'east')
            fg.tagRelation(west, 'observable', east, 'partial')

            fg.relateFeatures('downstairs', 'observable', 'west')
            fg.relateFeatures('upstairs', 'observable', 'west')

        elif name == 'town':
            fg.addFeature('town', 'region') # 0
            fg.addFeature('castleHill', 'region', 'town') # 1
            fg.addFeature('castle', 'node', 'castleHill') # 2
            fg.addFeature('market', 'region', 'town') # 3
            fg.addFeature('eastResidences', 'region', 'town') # 4
            fg.addFeature('southResidences', 'region', 'town') # 5
            fg.addFeature('marketSquare', 'node', 'market') # 6
            fg.addFeature('ringRoad', 'path', 'town') # 7
            fg.relateFeatures('ringRoad', 'within', 'market')
            fg.relateFeatures('ringRoad', 'within', 'eastResidences')
            fg.relateFeatures('ringRoad', 'within', 'southResidences')
            fg.relateFeatures('ringRoad', 'touches', 'marketSquare')
            fg.addFeature('mainRoad', 'path', 'town') # 8
            fg.relateFeatures('mainRoad', 'within', 'castleHill')
            fg.relateFeatures('mainRoad', 'touches', 'castle')
            fg.relateFeatures('mainRoad', 'within', 'market')
            fg.relateFeatures('mainRoad', 'touches', 'marketSquare')
            fg.addFeature('wall', 'edge') # 9
            fg.relateFeatures('wall', 'touches', 'town')
            fg.relateFeatures('wall', 'touches', 'mainRoad')
            fg.addFeature('outside', 'region') # 10
            fg.relateFeatures('outside', 'touches', 'wall')
            fg.relateFeatures('outside', 'contains', 'mainRoad')

        elif name == 'intercom':
            fg.addFeature('swamp', 'region') # 0
            fg.addFeature('eastSwamp', 'region', 'swamp') # 1
            fg.addFeature('westSwamp', 'region', 'swamp') # 2
            fg.addFeature('midSwamp', 'region', 'swamp') # 3
            # Overlap:
            fg.relateFeatures('midSwamp', 'touches', 'eastSwamp')
            fg.relateFeatures('midSwamp', 'touches', 'westSwamp')
            fg.addFeature('house', 'node', 'midSwamp') # 4
            fg.relateFeatures('house', 'within', 'westSwamp') # Overlap
            fg.addFeature('inside', 'region', 'house') # 5
            fg.relateFeatures('inside', 'entranceFor', 'house')
            fg.addFeature('kitchen', 'region', 'inside') # 6
            fg.addFeature('intercom', 'affordance', 'kitchen') # 7
            fg.relateFeatures('intercom', 'within', 'inside') # Inside both

        return fg

    def listFeatures(self) -> List[
        Tuple[base.FeatureID, base.Feature, base.FeatureType]
    ]:
        """
        Returns a list of tuples containing the id, name, and type of
        each feature in the graph. Note that names are not necessarily
        unique.

        For example:

        >>> fg = FeatureGraph()
        >>> fg.addFeature('R', 'region')
        0
        >>> fg.addFeature('N', 'node', 'R')
        1
        >>> fg.addFeature('N', 'node', 'R')
        2
        >>> fg.addFeature('P', 'path', 'R')
        3
        >>> fg.listFeatures()
        [(0, 'R', 'region'), (1, 'N', 'node'), (2, 'N', 'node'),\
 (3, 'P', 'path')]
        """
        result: List[
            Tuple[base.FeatureID, base.Feature, base.FeatureType]
        ] = []
        for fID in self:
            result.append(
                (fID, self.nodes[fID]['name'], self.nodes[fID]['fType'])
            )

        return result

    def fullSpecifier(
        self,
        fID: base.FeatureID,
        part: Optional[base.Part] = None
    ) -> base.FeatureSpecifier:
        """
        Returns the fully-qualified feature specifier for the feature
        with the given ID. When multiple parent features are available
        to select from, chooses the shortest possible component list,
        breaking ties towards components with lower ID integers (i.e.,
        those created earlier). Note that in the case of repeated name
        collisions and/or top-level name collisions, the resulting fully
        qualified specifier may still be ambiguous! This is mostly
        intended for helping provide a human-recognizable shorthand for
        a node rather than creating unambiguous representations (use the
        ID you already have for that).

        A part may be specified for inclusion in the returned specifier;
        otherwise the part slot of the specifier will be `None`.

        TODO: Support numeric disambiguation and mix that in here?

        For example:

        >>> fg = FeatureGraph.example('intercom')
        >>> # Accessible from both a child and parent regions (unusual)
        >>> fg.fullSpecifier(4)
        FeatureSpecifier(domain='main', within=['swamp', 'westSwamp'],\
 feature='house', part=None)
        >>> # Note tie broken towards smaller-ID feature here
        >>> fg.fullSpecifier(7)
        FeatureSpecifier(domain='main', within=['swamp', 'westSwamp',\
 'house', 'inside'], feature='intercom', part=None)
        >>> # Note shorter 'within' list was chosen here.
        >>> fg.fullSpecifier(0)
        FeatureSpecifier(domain='main', within=[], feature='swamp',\
 part=None)
        >>> fg.fullSpecifier(0, 'top')
        FeatureSpecifier(domain='main', within=[], feature='swamp',\
 part='top')
        >>> # example of ambiguous specifiers:
        >>> fg.addFeature('swamp', 'region')
        8
        >>> fg.fullSpecifier(0)
        FeatureSpecifier(domain='main', within=[], feature='swamp',\
 part=None)
        >>> fg.fullSpecifier(8)
        FeatureSpecifier(domain='main', within=[], feature='swamp',\
 part=None)
        """
        parents = self.relations(fID, 'within')
        best = base.FeatureSpecifier(
            domain=self.nodes[fID]['domain'],
            within=[],
            feature=self.nodes[fID]['name'],
            part=part
        )
        for par in sorted(parents, reverse=True):
            option = self.fullSpecifier(par)
            if isinstance(option.feature, base.FeatureID):
                amended = list(option.within) + [
                    self.featureName(option.feature)
                ]
            else:
                amended = list(option.within) + [option.feature]
            if (
                best.within == []
             or len(amended) <= len(best.within)
            ):
                best = base.FeatureSpecifier(
                    domain=best.domain,
                    within=amended,
                    feature=best.feature,
                    part=part
                )

        return best

    def allRelations(
        self,
        feature: base.AnyFeatureSpecifier
    ) -> Dict[base.FeatureRelationshipType, Set[base.FeatureID]]:
        """
        Given a feature specifier, returns a dictionary where each key
        is a relationship type string, and the value for each key is a
        set of `FeatureID`s for the features that the specified feature
        has that relationship to. Only outgoing relationships are
        listed, and only relationship types for which there is at least
        one relation are included in the dictionary.

        For example:

        >>> fg = FeatureGraph.example("chasm")
        >>> fg.allRelations("chasm")
        {'within': {0}, 'touches': {1, 2, 4}}
        >>> fg.allRelations("bridge")
        {'within': {0}, 'touches': {1, 2, 3, 5, 13, 14}}
        >>> fg.allRelations("downstairs")
        {'within': {15}, 'entranceFor': {15}, 'touches': {19},\
 'observable': {2}}
        """
        fID = self.resolveFeature(feature)
        result: Dict[base.FeatureRelationshipType, Set[base.FeatureID]] = {}
        for _, dest, info in self.edges(fID, data=True):
            rel = info['rType']
            if rel not in result:
                result[rel] = set()
            result[rel].add(dest)
        return result

    def relations(
        self,
        fID: base.FeatureID,
        relationship: base.FeatureRelationshipType
    ) -> Set[base.FeatureID]:
        """
        Returns the set of feature IDs for each feature with the
        specified relationship from the specified feature (specified by
        feature ID only). Only direct relations with the specified
        relationship are included in the list, indirect relations are
        not.

        For example:

        >>> fg = FeatureGraph.example('town')
        >>> t = fg.resolveFeature('town')
        >>> ms = fg.resolveFeature('marketSquare')
        >>> rr = fg.resolveFeature('ringRoad')
        >>> mr = fg.resolveFeature('mainRoad')
        >>> fg.relations(ms, 'touches') == {rr, mr}
        True
        >>> mk = fg.resolveFeature('market')
        >>> fg.relations(ms, 'within') == {mk}
        True
        >>> sr = fg.resolveFeature('southResidences')
        >>> er = fg.resolveFeature('eastResidences')
        >>> ch = fg.resolveFeature('castleHill')
        >>> os = fg.resolveFeature('outside')
        >>> fg.relations(rr, 'within') == {t, mk, sr, er}
        True
        >>> fg.relations(mr, 'within') == {t, ch, mk, os}
        True
        >>> fg.relations(rr, 'touches') == {ms}
        True
        >>> c = fg.resolveFeature('castle')
        >>> w = fg.resolveFeature('wall')
        >>> fg.relations(mr, 'touches') == {ms, c, w}
        True
        >>> fg.relations(sr, 'touches')
        set()
        """
        results = set()
        for _, dest, info in self.edges(fID, data=True):
            if info['rType'] == relationship:
                results.add(dest)
        return results

    def domain(self, fID: base.FeatureID) -> base.Domain:
        """
        Returns the domain that the specified feature is in.

        For example:

        >>> fg = FeatureGraph()
        >>> fg.addFeature('main', 'node', domain='menu')
        0
        >>> fg.addFeature('world', 'region', domain='main')
        1
        >>> fg.addFeature('', 'region', domain='NPCs')
        2
        >>> fg.domain(0)
        'menu'
        >>> fg.domain(1)
        'main'
        >>> fg.domain(2)
        'NPCs'
        """
        if fID not in self:
            raise MissingFeatureError(f"There is no feature with ID {fID}.")
        return self.nodes[fID]['domain']

    def addFeature(
        self,
        name: base.Feature,
        featureType: base.FeatureType,
        within: Optional[base.AnyFeatureSpecifier] = None,
        domain: Optional[base.Domain] = None
    ) -> base.FeatureID:
        """
        Adds a new feature to the graph. You must specify the feature
        type, and you may specify another feature which you want to put
        the new feature inside of (i.e., a 'within' relationship and
        reciprocal 'contains' relationship will be set up). Also, you
        may specify a domain for the feature; if you don't specify one,
        the domain will default to 'main'. Returns the feature ID
        assigned to the new feature.

        For example:

        >>> fg = FeatureGraph()
        >>> fg.addFeature('world', 'region')
        0
        >>> fg.addFeature('continent', 'region', 'world')
        1
        >>> fg.addFeature('valley', 'region', 'continent')
        2
        >>> fg.addFeature('mountains', 'edge', 'continent')
        3
        >>> fg.addFeature('menu', 'node', domain='menu')
        4
        >>> fg.relations(0, 'contains')
        {1}
        >>> fg.relations(1, 'contains')
        {2, 3}
        >>> fg.relations(2, 'within')
        {1}
        >>> fg.relations(1, 'within')
        {0}
        >>> fg.domain(0)
        'main'
        >>> fg.domain(4)
        'menu'
        """
        fID = self._register()
        if domain is None:
            domain = 'main'
        self.add_node(fID, name=name, fType=featureType, domain=domain)
        self.nodes[fID]['domain'] = domain

        if within is not None:
            containerID = self.resolveFeature(within)
            # Might raise AmbiguousFeatureSpecifierError
            self.relateFeatures(fID, 'within', containerID)
        return fID

    def relateFeatures(
        self,
        source: base.AnyFeatureSpecifier,
        relType: base.FeatureRelationshipType,
        destination: base.AnyFeatureSpecifier
    ) -> None:
        """
        Adds a new relationship between two features. May also add a
        reciprocal relationship for relations that have fixed
        reciprocals. The list of reciprocals is:

        - 'contains' and 'within' are required reciprocals of each
          other.
        - 'touches' is its own required reciprocal.
        - 'observable' does not have a required reciprocal.
        - 'positioned' does not have a required reciprocal.
        - 'entranceFor' and 'enterTo' are each others' required
          reciprocal.

        The type of the relationship is stored in the 'rType' slot of the
        edge that represents it. If parts are specified for either the
        source or destination features, these are stored in the
        sourcePart and destPart tags for both the edge and its
        reciprocal. (Note that 'rType' is not a tag, it's a slot directly
        on the edge).

        For example:

        >>> fg = FeatureGraph()
        >>> fg.addFeature('south', 'region')
        0
        >>> fg.addFeature('north', 'region')
        1
        >>> fg.relateFeatures('south', 'touches', 'north')
        >>> fg.allRelations(0)
        {'touches': {1}}
        >>> fg.allRelations(1)
        {'touches': {0}}
        >>> # Multiple relations between the same pair of features:
        >>> fg.relateFeatures('north', 'observable', 'south')
        >>> fg.allRelations(0)
        {'touches': {1}}
        >>> fg.allRelations(1)
        {'touches': {0}, 'observable': {0}}
        >>> # Self-relations are allowed even though they usually don't
        >>> # make sense
        >>> fg.relateFeatures('north', 'observable', 'north')
        >>> fg.allRelations(1)
        {'touches': {0}, 'observable': {0, 1}}
        >>> fg.relateFeatures('north', 'observable', 'north')
        >>> fg.addFeature('world', 'region')
        2
        >>> fg.relateFeatures('world', 'contains', 'south')
        >>> fg.relateFeatures('north', 'within', 'world')
        >>> fg.allRelations(0)
        {'touches': {1}, 'within': {2}}
        >>> fg.allRelations(1)
        {'touches': {0}, 'observable': {0, 1}, 'within': {2}}
        >>> fg.allRelations(2)
        {'contains': {0, 1}}
        >>> # Part specifiers are tagged on the relationship
        >>> fg.relateFeatures(
        ...     base.feature('south', 'south'),
        ...     'entranceFor',
        ...     base.feature('world', 'top')
        ... )
        >>> fg.allRelations(2)
        {'contains': {0, 1}, 'enterTo': {0}}
        >>> fg.allRelations(0)
        {'touches': {1}, 'within': {2}, 'entranceFor': {2}}
        >>> fg.relationTags(0, 'within', 2)
        {}
        >>> fg.relationTags(0, 'entranceFor', 2)
        {'sourcePart': 'south', 'destPart': 'top'}
        >>> fg.relationTags(2, 'enterTo', 0)
        {'sourcePart': 'top', 'destPart': 'south'}
        """
        nSource = base.normalizeFeatureSpecifier(source)
        nDest = base.normalizeFeatureSpecifier(destination)
        sID = self.resolveFeature(nSource)
        dID = self.resolveFeature(nDest)
        sPart = nSource.part
        dPart = nDest.part

        self.add_edge(sID, dID, relType, rType=relType)
        if sPart is not None:
            self.tagRelation(sID, relType, dID, 'sourcePart', sPart)
        if dPart is not None:
            self.tagRelation(sID, relType, dID, 'destPart', dPart)

        recipType = base.FREL_RECIPROCALS.get(relType)
        if recipType is not None:
            self.add_edge(dID, sID, recipType, rType=recipType)
            if dPart is not None:
                self.tagRelation(dID, recipType, sID, 'sourcePart', dPart)
            if sPart is not None:
                self.tagRelation(dID, recipType, sID, 'destPart', sPart)

    def addEffect(
        self,
        feature: base.AnyFeatureSpecifier,
        affordance: base.FeatureAffordance,
        effect: base.FeatureEffect
    ) -> None:
        """
        Adds an effect that will be triggered when the specified
        `Affordance` of the given feature is used.

        TODO: Examples
        """
        # TODO

    def tagFeature(
        self,
        fID: base.FeatureID,
        tag: base.Tag,
        val: Union[None, base.TagValue, base.TagUpdateFunction] = None
    ) -> Union[base.TagValue, type[base.NoTagValue]]:
        """
        Adds (or updates) the specified tag on the specified feature. A
        value of 1 is used if no value is specified.

        Returns the old value for the specified tag, or the special
        object `base.NoTagValue` if the tag didn't yet have a value.

        For example:

        >>> fg = FeatureGraph()
        >>> fg.addFeature('mountains', 'region')
        0
        >>> fg.addFeature('town', 'node', 'mountains')
        1
        >>> fg.tagFeature(1, 'town')
        <class 'exploration.base.NoTagValue'>
        >>> fg.tagFeature(0, 'geographicFeature')
        <class 'exploration.base.NoTagValue'>
        >>> fg.tagFeature(0, 'difficulty', 3)
        <class 'exploration.base.NoTagValue'>
        >>> fg.featureTags(0)
        {'geographicFeature': 1, 'difficulty': 3}
        >>> fg.featureTags(1)
        {'town': 1}
        >>> fg.tagFeature(1, 'town', 'yes')
        1
        >>> fg.featureTags(1)
        {'town': 'yes'}
        """
        if val is None:
            val = 1
        tdict: Dict[base.Tag, base.TagValue] = self.nodes[
            fID
        ].setdefault('tags', {})
        oldVal = tdict.get(tag, base.NoTagValue)
        if callable(val):
            tdict[tag] = val(tdict, tag, tdict.get(tag))
        else:
            tdict[tag] = val
        return oldVal

    def featureTags(
        self,
        fID: base.FeatureID
    ) -> Dict[base.Tag, base.TagValue]:
        """
        Returns the dictionary containing all tags applied to the
        specified feature. Tags applied without a value will have the
        integer 1 as their value.

        For example:

        >>> fg = FeatureGraph()
        >>> fg.addFeature('swamp', 'region')
        0
        >>> fg.addFeature('plains', 'region')
        1
        >>> fg.tagFeature(0, 'difficulty', 3)
        <class 'exploration.base.NoTagValue'>
        >>> fg.tagFeature(0, 'wet')
        <class 'exploration.base.NoTagValue'>
        >>> fg.tagFeature(1, 'amenities', ['grass', 'wind'])
        <class 'exploration.base.NoTagValue'>
        >>> fg.featureTags(0)
        {'difficulty': 3, 'wet': 1}
        >>> fg.featureTags(1)
        {'amenities': ['grass', 'wind']}
        """
        return self.nodes[fID].setdefault('tags', {})

    def tagRelation(
        self,
        sourceID: base.FeatureID,
        rType: base.FeatureRelationshipType,
        destID: base.FeatureID,
        tag: base.Tag,
        val: Union[None, base.TagValue, base.TagUpdateFunction] = None
    ) -> Union[base.TagValue, type[base.NoTagValue]]:
        """
        Adds (or updates) the specified tag on the specified
        relationship. A value of 1 is used if no value is specified. The
        relationship is identified using its source feature ID,
        relationship type, and destination feature ID.

        Returns the old value of the tag, or if the tag did not yet
        exist, the special `base.NoTagValue` class to indicate that.

        For example:

        >>> fg = FeatureGraph()
        >>> fg.addFeature('plains', 'region')
        0
        >>> fg.addFeature('town', 'node', 'plains') # Creates contains rel
        1
        >>> fg.tagRelation(0, 'contains', 1, 'destPart', 'south')
        <class 'exploration.base.NoTagValue'>
        >>> fg.tagRelation(1, 'within', 0, 'newTag')
        <class 'exploration.base.NoTagValue'>
        >>> fg.relationTags(0, 'contains', 1)
        {'destPart': 'south'}
        >>> fg.relationTags(1, 'within', 0)
        {'newTag': 1}
        >>> fg.tagRelation(0, 'contains', 1, 'destPart', 'north')
        'south'
        >>> fg.relationTags(0, 'contains', 1)
        {'destPart': 'north'}
        """
        if val is None:
            val = 1
        # TODO: Fix up networkx.MultiDiGraph type hints
        tdict: Dict[base.Tag, base.TagValue] = self.edges[
            sourceID,  # type:ignore [index]
            destID,
            rType
        ].setdefault('tags', {})
        oldVal = tdict.get(tag, base.NoTagValue)
        if callable(val):
            tdict[tag] = val(tdict, tag, tdict.get(tag))
        else:
            tdict[tag] = val
        return oldVal

    def relationTags(
        self,
        sourceID: base.FeatureID,
        relType: base.FeatureRelationshipType,
        destID: base.FeatureID
    ) -> Dict[base.Tag, base.TagValue]:
        """
        Returns a dictionary containing all of the tags applied to the
        specified relationship.

        >>> fg = FeatureGraph()
        >>> fg.addFeature('swamp', 'region')
        0
        >>> fg.addFeature('plains', 'region')
        1
        >>> fg.addFeature('road', 'path')
        2
        >>> fg.addFeature('pond', 'region')
        3
        >>> fg.relateFeatures('road', 'within', base.feature('swamp', 'east'))
        >>> fg.relateFeatures('road', 'within', base.feature('plains', 'west'))
        >>> fg.relateFeatures('pond', 'within', 'swamp')
        >>> fg.tagRelation(0, 'contains', 2, 'testTag', 'Val')
        <class 'exploration.base.NoTagValue'>
        >>> fg.tagRelation(2, 'within', 0, 'testTag', 'Val2')
        <class 'exploration.base.NoTagValue'>
        >>> fg.relationTags(0, 'contains', 2)
        {'sourcePart': 'east', 'testTag': 'Val'}
        >>> fg.relationTags(2, 'within', 0)
        {'destPart': 'east', 'testTag': 'Val2'}
        """
        return self.edges[
            sourceID, # type:ignore [index]
            destID,
            relType
        ].setdefault('tags', {})


def checkFeatureAction(
    graph: FeatureGraph,
    action: base.FeatureAction,
    featureType: base.FeatureType
) -> bool:
    """
    Checks that the feature type and affordance match, and that the
    optional parts present make sense given the feature type.
    Returns `True` if things make sense and `False` if not.

    Also, a feature graph is needed to be able to figure out the
    type of the subject feature.

    The rules are:

    1. The feature type of the subject feature must be listed in the
        `FEATURE_TYPE_AFFORDANCES` dictionary for the affordance
        specified.
    2. Each optional slot has some affordance types it's incompatible with:
        - 'direction' may not be used with 'scrutinize', 'do', or
            'interact'.
        - 'part' may not be used with 'do'.
        - 'destination' may not be used with 'do' or 'interact'.
    """
    fID = graph.resolveFeature(action['subject'])
    fType = graph.featureType(fID)
    affordance = action['affordance']
    if fType not in base.FEATURE_TYPE_AFFORDANCES[affordance]:
        return False
    if action.get('direction') is not None:
        if affordance in {'scrutinize', 'do', 'interact'}:
            return False
    if action.get('part') is not None:
        if affordance == 'do':
            return False
    if action.get('destination') is not None:
        if affordance in {'do', 'interact'}:
            return False
    return True


def move():
    """
    The move() function of the feature graph.
    """
    # TODO
    pass


class GeographicExploration:
    """
    Unifies the various partial representations into a combined
    representation, with cross-references between them. It can contain:

    - Zero or more `MetricSpace`s to represent things like 2D or 3D game
        spaces (or in some cases 4D+ including time and/or some other
        relevant dimension(s)). A 1D metric space can also be used to
        represent time independently, and several might be used for
        real-world time, play-time elapsed, and in-game time-of-day, for
        example. Correspondences between metric spaces can be added.
    - A single list containing one `FeatureGraph` per exploration step.
        These feature graphs represent how the explorer's knowledge of
        the space evolves over time, and/or how the space itself changes
        as the exploration progresses.
    - A matching list of `FeatureDecision`s which details key decisions
        made by the explorer and activities that were engaged in as a
        result.
    - A second matching list of exploration status maps, which each
        associate one `ExplorationState` with each feature in the
        current `FeatureGraph`.
    - A third matching list of game state dictionaries holding both
        custom and conventional game state information, such as
        position/territory information for each domain in the current
        `FeatureGraph`.
    """
    # TODO
