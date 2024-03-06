
from typing import cast

from logging import Logger
from logging import getLogger

from sys import maxsize

from math import atan2
from math import pi
from math import sqrt

from random import seed as randomSeed
from random import randint

from uuid import uuid4
from uuid import UUID

from pyfdl.Configuration import Configuration
from pyfdl.LayoutTypes import LayoutStatus
from pyfdl.LayoutTypes import LayoutStatusCallback
from pyfdl.Node import Node
from pyfdl.Point import Point
from pyfdl.Vector import Vector
from pyfdl.LayoutTypes import Nodes
from pyfdl.Rectangle import Rectangle
from pyfdl.NodeLayoutInformation import NodeLayoutInformation
from pyfdl.NodeLayoutInformation import NodeLayoutInformationList

ORIGIN_POINT: Point = Point(0, 0)


class LayoutEngine:
    """
    Represents a simple diagram consisting of nodes and connections, implementing a
    force-directed algorithm for automatically arranging the nodes.

    The repulsion force is exerted by every node, and each node is repelled
    (however slightly) by every other node.

    The attraction force is exerted on each node by the nodes that are connected to it.
    Isolated nodes are unaffected by this force.
    """

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._configuration: Configuration = Configuration()
        self.id:             UUID          = uuid4()
        self._nodes:         Nodes         = Nodes([])

    @property
    def nodes(self) -> Nodes:
        """

        Returns:  a read-only collection of the nodes in this Diagram.
        """
        return Nodes(self._nodes[:])

    def clear(self):
        """
        Removes all nodes and connections from the diagram.

        Do not access via the property because you get a copy
        """
        self._nodes.clear()

    def containsNode(self, node: Node) -> bool:
        """
        Determines whether the diagram contains the specified node.

        Args:
            node: The node to test.

        Returns:   True if the diagram contains the node.
        """
        ans: bool = False
        if node in self._nodes:
            ans = True

        return ans

    def addNode(self, node: Node) -> bool:
        """
        Adds the specified Node to this Diagram.

        Args:
            node:  The Node to add to the diagram

        Returns:  True if the node was added, False if the node is already on this Diagram.
        """
        assert node is not None, 'node argument cannot be None'

        if node not in self._nodes:
            self._nodes.append(node)
            node.layoutEngine = self
            return True
        else:
            return False

    def removeNode(self, node: Node):
        """
        Removes the specified node from the diagram. Any connected nodes will remain on the diagram.

        Args:
            node:  The node to remove from the diagram.

        Returns:  True if the node belonged to the diagram.
        """
        node.layoutEngine = cast(LayoutEngine, None)

        for otherNode in self._nodes:
            if otherNode != node and node in otherNode.connections:
                otherNode.disConnect(node)

        removed: bool = True
        try:
            self._nodes.remove(node)
        except ValueError:
            self.logger.warning(f'Node not in this diagram. {node=}')
            removed = False

        return removed

    def arrange(self, statusCallback: LayoutStatusCallback, deterministic:  bool = True):
        """
        Runs the force-directed layout algorithm on this Diagram, using the specified parameters.

        TODO:   Update method signature to package the runtime values into a single dataclass aka
        object
        Args:
            statusCallback
            deterministic:  Whether to use a random or deterministic layout.

        """
        # random starting positions can be made deterministic by seeding with a constant
        if deterministic is True:
            randomSeed(1)
        else:
            randomSeed()

        # Python multiplication works different than C#;  We need a real object
        dampingVector: Vector = Vector(direction=0.0, magnitude=self._configuration.damping)
        layoutList:    NodeLayoutInformationList = self._randomizeInitialNodeCoordinates()

        stopCount:  int = 0
        iterations: int = 0

        layoutStatus: LayoutStatus = LayoutStatus()
        while True:
            totalDisplacement: float = 0.0
            for currentMeta in layoutList:
                metaNode: Node = currentMeta.node
                #
                # express the node's current position as a vector, relative to the origin
                #
                magnitude:       int    = LayoutEngine.calculateDistance(a=ORIGIN_POINT, b=metaNode.location)
                direction:       float  = self._getBearingAngle(start=ORIGIN_POINT, end=metaNode.location)
                currentPosition: Vector = Vector(magnitude=magnitude, direction=direction)

                netForce: Vector = self._determineRepulsionBetweenNodes(metaNode=metaNode)
                netForce += self._determineAttractionBetweenConnections(currentLayoutNode=metaNode,
                                                                        springLength=self._configuration.springLength,
                                                                        netForce=netForce)

                # apply net force to node velocity
                currentMeta.velocity = (currentMeta.velocity + netForce) * dampingVector
                # apply velocity to node position
                currentMeta.nextPosition = (currentPosition + currentMeta.velocity).toPoint()

            # move nodes to resultant positions (and calculate total displacement)
            for currentMeta in layoutList:
                metaNode = currentMeta.node
                totalDisplacement += LayoutEngine.calculateDistance(a=metaNode.location, b=currentMeta.nextPosition)
                metaNode.location = currentMeta.nextPosition

            iterations += 1
            if totalDisplacement < self._configuration.minimumTotalDisplacement:
                stopCount += 1
            if stopCount > self._configuration.stopCount:
                break
            if iterations >= self._configuration.maxIterations:
                break

            # center the diagram around the origin
            layoutStatus.totalDisplacement = totalDisplacement
            layoutStatus.stopCount         = stopCount
            layoutStatus.iterations        = iterations
            layoutStatus.maxIterations     = self._configuration.maxIterations

            statusCallback(layoutStatus)
        self._adjustNodes()

    def _adjustNodes(self):
        logicalBounds: Rectangle = self._getDiagramBounds()
        midPoint:      Point     = Point(x=logicalBounds.x + (logicalBounds.width // 2),
                                         y=logicalBounds.y + (logicalBounds.height // 2)
                                         )
        for n in self._nodes:
            node: Node = cast(Node, n)
            node.location -= midPoint
            node.location.x += node.size.width
            node.location.y += node.size.height

    def _determineRepulsionBetweenNodes(self, metaNode: Node) -> Vector:

        netForce: Vector = Vector(magnitude=0, direction=0)

        for other in self._nodes:
            if other != metaNode:
                netForce = netForce + self._calculateRepulsionForce(x=metaNode, y=other)

        return netForce

    def _determineAttractionBetweenConnections(self, currentLayoutNode: Node, springLength: int, netForce: Vector) -> Vector:
        """
        Determine attraction between connections

        Args:
            currentLayoutNode:
            springLength:
            netForce:

        Returns:

        """

        for child in currentLayoutNode.connections:
            netForce += self._calculateAttractionForce(x=currentLayoutNode, y=child, springLength=springLength)

        for p in self._nodes:
            parent: Node = cast(Node, p)
            if currentLayoutNode in parent.connections:
                netForce += self._calculateAttractionForce(x=currentLayoutNode, y=p, springLength=springLength)

        return netForce

    def _randomizeInitialNodeCoordinates(self) -> NodeLayoutInformationList:
        """
        Copy nodes into an array of metadata and randomize initial coordinates for each node

        Returns:  Metadata
        """

        layout: NodeLayoutInformationList = NodeLayoutInformationList([])
        for node in self._nodes:
            diagramNode: Node = node
            minRandomX: int = self._configuration.minPoint.x
            minRandomY: int = self._configuration.minPoint.y
            maxRandomX: int = self._configuration.maxPoint.x
            maxRandomY: int = self._configuration.maxPoint.x

            diagramNode.location = Point(x=randint(minRandomX, maxRandomX), y=randint(minRandomY, maxRandomY))

            layoutInformation: NodeLayoutInformation = NodeLayoutInformation(node=diagramNode,
                                                                             velocity=Vector(magnitude=0, direction=0),
                                                                             nextPosition=Point(),
                                                                             )
            layout.append(layoutInformation)

        return layout

    def _calculateAttractionForce(self, x: Node, y: Node, springLength: float) -> Vector:
        """
        Calculates the attraction force between two connected nodes, using the specified spring length.
        Args:
            x: The node that the force is acting on.x
            y: The node creating the force
            springLength: The length of the spring, in pixels.

        Returns:  A Vector representing the attraction force.
        """
        proximity: int = max(LayoutEngine.calculateDistance(x.location, y.location), 1)
        # Hooke's Law: F = -kx
        stiffnessValue: float = self._configuration.attractionForce
        force: float = stiffnessValue * max(proximity - springLength, 0)
        angle: float = self._getBearingAngle(start=x.location, end=y.location)

        attractionVector: Vector = Vector(magnitude=force, direction=angle)
        return attractionVector

    @classmethod
    def calculateDistance(cls, a: Point, b: Point) -> int:
        """
        Calculates the distance between two points.

        Args:
            a:  The first point
            b:  The second point

        Returns: The pixel distance between the two points.
        """
        xDistance: float = a.x - b.x
        yDistance: float = a.y - b.y

        distance: float = sqrt(pow(xDistance, 2) + pow(yDistance, 2))

        return int(distance)

    def _calculateRepulsionForce(self, x: Node, y: Node) -> Vector:
        """
        Calculates the repulsion force between any two nodes in the diagram

        Coulomb's Law: F = k(Qq/r^2)

        Args:
            x:  The node that the force is acting on.
            y:  The node creating the force.

        Returns:    A Vector representing the repulsion force.
        """
        proximity: int = max(LayoutEngine.calculateDistance(x.location, y.location), 1)
        #  Coulomb's Law: F = k(Qq/r^2)
        coulombLawConstant: int = self._configuration.repulsionForce

        force: float = -(coulombLawConstant / pow(proximity, 2))
        angle: float = self._getBearingAngle(start=x.location, end=y.location)

        vector: Vector = Vector(magnitude=force, direction=angle)

        return vector

    def _getBearingAngle(self, start: Point, end: Point) -> float:
        """
        Calculates the bearing angle from one point to another.

        Args:
            start: The node that the angle is measured from.
            end:   The node that creates the angle.

        Returns: The bearing angle, in degrees.
        """
        x: int = start.x + ((end.x - start.x) // 2)
        y: int = start.y + ((end.y - start.y) // 2)

        half: Point = Point(x=x, y=y)

        diffX: float = float(half.x - start.x)
        diffY: float = float(half.y - start.y)
        # noinspection SpellCheckingInspection
        """
        if diffY == 0.0:
            diffX = 0.001
        if diffY == 0.0:
            diffY = 0.001

        if abs(diffX) > abs(diffY):
            angle: float = tanh(diffY / diffX) * (180.0 / pi)
            if ((diffX < 0) and (diffY > 0)) or ((diffX < 0) and (diffY < 0)):
                angle += 180
        else:
            angle = tanh(diffX / diffY) * (180.0 / pi)
            if ((diffY < 0) and (diffX > 0)) or ((diffY < 0) and (diffX < 0)):
                angle = (180 - (angle + 90))
        """
        if diffY != 0:
            angle: float = atan2(diffY, diffX) * (180.0 / pi)
        else:
            if diffX < 0:
                angle = 180.0
            else:
                angle = 0.0

            # angle = (diffX < 0) ? 180.0: 0.0

        return angle

    def _getDiagramBounds(self) -> Rectangle:
        """
        Determines the logical bounds of the diagram. This is used to center and scale the diagram when drawing.

        Returns:  Rectangle that fits exactly around every node in the diagram.
        """
        minX: int = maxsize
        minY: int = maxsize
        maxX: int = 0
        maxY: int = 0

        for node in self._nodes:
            if node.x < minX:
                minX = node.x
            if node.x > maxX:
                maxX = node.x
            if node.y < minY:
                minY = node.y
            if node.y > maxY:
                maxY = node.y

        rectangle: Rectangle = Rectangle.FromLTRB(minX, minY, maxX, maxY)
        self.logger.info(f'{rectangle=}')
        return rectangle

    def _scalePoint(self, point: Point, scale: float):
        """
        Applies a scaling factor to the specified point, used for zooming.

        Args:
            point:  The coordinates to scale
            scale:  The scaling factor

        Returns:  A point representing the scaled coordinates.
        """

        # return new Point((int)((double) point.X * scale), (int)((double) point.Y * scale));
        x: float = point.x * scale
        y: float = point.y * scale

        return Point(x=int(x), y=int(y))

    def __eq__(self, other) -> bool:

        if isinstance(other, LayoutEngine) is False:
            return False

        return self.id == other.id
