'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
import util
import itertools
from turtle import Vec2D
from engine.const import Const
from engine.vector import Vec2d
from engine.model.car.car import Car
from engine.model.layout import Layout
from engine.model.car.junior import Junior
import heapq
from queue import PriorityQueue

# Class: Graph
# -------------
# Utility class
class Graph(object):
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

# Class: IntelligentDriver
# ---------------------
# An intelligent driver that avoids collisions while visiting the given goal locations (or checkpoints) sequentially. 
class IntelligentDriver(Junior):

    # Funciton: Init
    def __init__(self, layout: Layout):
        self.burnInIterations = 30
        self.layout = layout 
        # self.worldGraph = None
        self.transProb = util.loadTransProb()
        self.worldGraph = self.createWorldGraph()
        self.checkPoints = self.layout.getCheckPoints() # a list of single tile locations corresponding to each checkpoint
        
    # ONE POSSIBLE WAY OF REPRESENTING THE GRID WORLD. FEEL FREE TO CREATE YOUR OWN REPRESENTATION.
    # Function: Create World Graph
    # ---------------------
    # Using self.layout of IntelligentDriver, create a graph representing the given layout.
    def createWorldGraph(self):
        nodes = []
        edges = {}
        # create self.worldGraph using self.layout
        # for p1,p2 in self.transProb.keys():
        #     if self.transProb[(p1,p2)] != 0:
        #         if p1 not in nodes:
        #             nodes.append(p1)
        #         if p2 not in nodes:
        #             nodes.append(p2)
        #         if edges.get(p1) == None:
        #             edges[p1] = [p2]
        #         elif p2 not in edges[p1]:
        #             edges[p1].append(p2)
        #         if edges.get(p2) == None:
        #             edges[p2] = [p1]
        #         elif p1 not in edges[p2]:
        #             edges[p2].append(p1)

        numRows, numCols = self.layout.getBeliefRows(), self.layout.getBeliefCols()

        # NODES #
        ## each tile represents a node
        nodes = [(x, y) for x, y in itertools.product(range(numRows), range(numCols))]
        
        # EDGES #
        ## We create an edge between adjacent nodes (nodes at a distance of 1 tile)
        ## avoid the tiles representing walls or blocks#
        ## YOU MAY WANT DIFFERENT NODE CONNECTIONS FOR YOUR OWN IMPLEMENTATION,
        ## FEEL FREE TO MODIFY THE EDGES ACCORDINGLY.

        ## Get the tiles corresponding to the blocks (or obstacles):
        blocks = self.layout.getBlockData()
        blockTiles = []
        for block in blocks:
            row1, col1, row2, col2 = block[1], block[0], block[3], block[2] 
            # some padding to ensure the AutoCar doesn't crash into the blocks due to its size. (optional)
            row1, col1, row2, col2 = row1-1, col1-1, row2+1, col2+1
            blockWidth = col2-col1 
            blockHeight = row2-row1 

            for i in range(blockHeight):
                for j in range(blockWidth):
                    blockTile = (row1+i, col1+j)
                    blockTiles.append(blockTile)

        ## Remove blockTiles from 'nodes'
        # nodes = [x for x in nodes if x not in blockTiles]

        for node in nodes:
            x, y = node[0], node[1]
            adjNodes = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
            
            # only keep allowed (within boundary) adjacent nodes
            adjacentNodes = []
            for tile in adjNodes:
                if tile[0]>=0 and tile[1]>=0 and tile[0]<numRows and tile[1]<numCols:
                    if tile not in blockTiles:
                        adjacentNodes.append(tile)
            edges[node] = []
            for tile in adjacentNodes:
                    if tile not in edges[node]:
                        edges[node].append(tile)
        return Graph(nodes, edges)

    #######################################################################################
    # Function: Get Next Goal Position
    # ---------------------
    # Given the current belief about where other cars are and a graph of how
    # one can driver around the world, chose the next position.
    #######################################################################################
    def getNextGoalPos(self, beliefOfOtherCars: list, parkedCars:list , chkPtsSoFar: int):
        '''
        Input:
        - beliefOfOtherCars: list of beliefs corresponding to all cars
        - parkedCars: list of booleans representing which cars are parked
        - chkPtsSoFar: the number of checkpoints that have been visited so far 
                       Note that chkPtsSoFar will only be updated when the checkpoints are updated in sequential order!
        
        Output:
        - goalPos: The position of the next tile on the path to the next goal location.
        - moveForward: Unset this to make the AutoCar stop and wait.

        Notes:
        - You can explore some files "layout.py", "model.py", "controller.py", etc.
         to find some methods that might help in your implementation. 
        '''
        goalPos = None # next tile 
        moveForward = True

        currPos = self.getPos() # the current 2D location of the AutoCar (refer util.py to convert it to tile (or grid cell) coordinate)
        # BEGIN_YOUR_CODE
        # Dijkstra's Based Implementation. Use weights of 'occupied' as 100000 because max board size is 50 x 50
        distances = {}
        prev_edges = {}
        numpark = 1
        for it in parkedCars:
            if(it):
                numpark +=1
        for node in self.worldGraph.nodes:
            distances[node] = 100000000
            prev_edges[node] = None
        posX = currPos[0]
        posY = currPos[1]
        c = util.xToCol(posX)
        r = util.yToRow(posY)
        priority_queue = []
        heapq.heappush(priority_queue,(0,(r,c)))
        distances[(r,c)] = 0
        prev_edges[(r,c)] = None
        while len(priority_queue) != 0:
            curr = heapq.heappop(priority_queue)
            for dest in self.worldGraph.edges[curr[1]]:
                maxBelief = 0.0
                for belief in beliefOfOtherCars:
                    maxBelief = max(maxBelief,belief.getProb(dest[0],dest[1]))
                weight = maxBelief
                # if maxBelief > 0.15:
                #     weight = 100000
                if distances[dest] > distances[curr[1]] + weight:
                    distances[dest] = distances[curr[1]] + weight
                    prev_edges[dest] = curr[1]
                    heapq.heappush(priority_queue,(distances[dest],dest))
        goalPos = self.checkPoints[chkPtsSoFar]
        next_goal = (goalPos[0],goalPos[1])
        moveForward = (distances[next_goal] <= (1 * (numpark / len(parkedCars))))
        while prev_edges[next_goal] != (r,c):
            next_goal = prev_edges[next_goal] 
        rt_goal = (util.colToX(next_goal[1]),util.rowToY(next_goal[0]))
        return rt_goal, moveForward
        # END_YOUR_CODE
        

    # DO NOT MODIFY THIS METHOD !
    # Function: Get Autonomous Actions
    # --------------------------------
    def getAutonomousActions(self, beliefOfOtherCars: list, parkedCars: list, chkPtsSoFar: int):
        # Don't start until after your burn in iterations have expired
        if self.burnInIterations > 0:
            self.burnInIterations -= 1
            return[]
       
        goalPos, df = self.getNextGoalPos(beliefOfOtherCars, parkedCars, chkPtsSoFar)
        vectorToGoal = goalPos - self.pos
        wheelAngle = -vectorToGoal.get_angle_between(self.dir)
        driveForward = df
        actions = {
            Car.TURN_WHEEL: wheelAngle
        }
        if driveForward:
            actions[Car.DRIVE_FORWARD] = 1.0
        return actions
    
    