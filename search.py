# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import Queue
from util import PriorityQueue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    #For Depth First Search we use a stack to explore the tree
    leafNodes = Stack()
    currentPath = Stack()
    boardLocation = problem.getStartState()
    totalPath = []
    newPath = []
    visitedNodes = []
    
    """
    This loop runs while the current location is not the goal. Continue
    getting successors unless the current location has already been visited.
    Since this is Depth First Search, path cost does not play into which node
    is explored next. It will keep going down a path until it reaches a dead
    end, at which point it will back track to the nearest unexplored path.
    """
    while problem.isGoalState(boardLocation) == False:
        if boardLocation not in visitedNodes:
            successors = problem.getSuccessors(boardLocation)
            visitedNodes.append(boardLocation)
            
            for child, direction, cost in successors:
                leafNodes.push(child)
                newPath = totalPath + [direction]
                currentPath.push(newPath)
                
        boardLocation = leafNodes.pop()
        totalPath = currentPath.pop()
    
    return totalPath

    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    #For Breadth First Search we use a Queue to explore the tree
    leafNodes = Queue()
    currentPath = Queue()
    boardLocation = problem.getStartState()
    totalPath = []
    newPath = []
    visitedNodes = []
    
    """
    This loop runs while the current location is not the goal. Continue
    getting successors unless the current location has already been visited.
    Since this is Breadth First Search, path cost does not play into which node
    is explored next. It will explore the shallowest nodes before moving to the
    next level in the tree.
    """
    while problem.isGoalState(boardLocation) == False:
        if boardLocation not in visitedNodes:
            successors = problem.getSuccessors(boardLocation)
            visitedNodes.append(boardLocation)
            
            for child, direction, cost in successors:
                leafNodes.push(child)
                newPath = totalPath + [direction]
                currentPath.push(newPath)
                
        boardLocation = leafNodes.pop()
        totalPath = currentPath.pop()
    
    return totalPath

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    #For a Uniform Cost Search we can use a priority Queue to explore the tree
    leafNodes = PriorityQueue()
    currentPath = PriorityQueue()
    totalPath = []
    newPath = []
    visitedNodes = []
    
    leafNodes.push(problem.getStartState(), 0)
    boardLocation = leafNodes.pop()
   
    """
    This loop runs while the current location is not the goal. Continue
    getting successors unless the current location has already been visited.
    This search function takes into account the cost of taking a path to 
    determine which node to explore next.  If every node has an equal
    path cost, it will function exactly the same as Breadth First Search.
    """
    while problem.isGoalState(boardLocation) == False:
        if boardLocation not in visitedNodes:
            successors = problem.getSuccessors(boardLocation)
            visitedNodes.append(boardLocation)
            
            for child, direction, cost in successors:
                newPath = totalPath + [direction]
                pathCost = problem.getCostOfActions(newPath)
                
                if child not in visitedNodes:
                    leafNodes.push(child, pathCost)
                    currentPath.push(newPath, pathCost)
                
        boardLocation = leafNodes.pop()
        totalPath = currentPath.pop()
    
    return totalPath
    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    leafNodes = PriorityQueue()
    currentPath = PriorityQueue()
    totalPath = []
    newPath = []
    visitedNodes = []
    
    leafNodes.push(problem.getStartState(), 0)
    boardLocation = leafNodes.pop()
    
    
    """
    This loop runs while the current location is not the goal. Continue
    getting successors unless the current location has already been visited.
    A* takes into account the cost of taking a path to determine which node
    to explore next, as well as a designated heuristic.  The Manhattan and 
    Euclidian Heuristic are provided in the searchAgent file.
    """
    while problem.isGoalState(boardLocation) == False:
        if boardLocation not in visitedNodes:
            successors = problem.getSuccessors(boardLocation)
            visitedNodes.append(boardLocation)
            
            for child, direction, cost in successors:
                newPath = totalPath + [direction]
                pathCost = problem.getCostOfActions(newPath) + heuristic(child, problem)
                
                if child not in visitedNodes:
                    leafNodes.push(child, pathCost)
                    currentPath.push(newPath, pathCost)
                
        boardLocation = leafNodes.pop()
        totalPath = currentPath.pop()
    
    return totalPath

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch