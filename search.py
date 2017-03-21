"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    """
    From lecture notes:
    initialize frontier using initial state of problem
    initialize explored set to be empty
    while frontier is not empty
    choose a leaf node and remove it from frontier
    if node contains a goal state then return corresponding solution
    if node is not in the explored set
    add node to explored set
    expand the node, adding the resulting nodes to the frontier
    """

    #frontier is list of paths
    #each path is a list of states (leaf)
    #each leaf is a tuple of the current state (location), the action, and the cost
    frontier = [[(problem.getStartState(),"",0)]]
    exploredSet = []

    while frontier:
        #DFS utilizes LIFO to process frontier
        currentPath = frontier[-1]
        currentLeaf = currentPath[-1]
        #remove from frontier
        del frontier[-1]

        #goal check
        if (problem.isGoalState(currentLeaf[0])):
            #remove start node (no movement to start state)
            currentPath.pop(0)
            return [node[1] for node in currentPath]

        if (currentLeaf[0] not in exploredSet):
            exploredSet.append(currentLeaf[0])
        #expand leaf
        for leaf in problem.getSuccessors(currentLeaf[0]):
            if (leaf[0] not in exploredSet):
                frontier.append(currentPath + [leaf])

    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """

    #frontier is list of paths
    #each path is a list of states (leaf)
    #each leaf is a tuple of the current state (location), the action, and the cost
    frontier = [[(problem.getStartState(),"",0)]]
    exploredSet = []

    while frontier:
        #BFS utilizes FIFO to process frontier
        currentPath = frontier.pop(0)
        currentLeaf = currentPath[-1]

        #goal check
        if (problem.isGoalState(currentLeaf[0])):
            #remove start node (no movement to start state)
            currentPath.pop(0)
            return [node[1] for node in currentPath]

        if (currentLeaf[0] not in exploredSet):
            exploredSet.append(currentLeaf[0])
            #expand leaf
            for leaf in problem.getSuccessors(currentLeaf[0]):
                if (leaf[0] not in exploredSet):
                    frontier.append(currentPath + [leaf])


    util.raiseNotDefined()

def uniformCostSearch(problem):
    from util import PriorityQueue

    #frontier is list of paths
    #each path is a list of states (leaf)
    #each leaf is a tuple of the current state (location), the action, and the cost
    "Search the node of least total cost first. "
    frontier = PriorityQueue()
    frontier.push([(problem.getStartState(),"",0)],0)
    exploredSet = []

    while not frontier.isEmpty():
        #PriorityQueue automatically sorts lowest cost to front
        currentPath = frontier.pop()
        currentLeaf = currentPath[-1]

        if (currentLeaf[0] not in exploredSet):
            exploredSet.append(currentLeaf[0])

            if (problem.isGoalState(currentLeaf[0])):
                #remove start node (no movement to start state)
                currentPath.pop(0)
                return [node[1] for node in currentPath]

            #expand leaf
            for leaf in problem.getSuccessors(currentLeaf[0]):
                if (leaf[0] not in exploredSet):
                    frontier.push(currentPath + [leaf], sum(node[2] for node in currentPath + [leaf]))

    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    from util import PriorityQueue

    #frontier is list of paths
    #each path is a list of states (leaf)
    #each leaf is a tuple of the current state (location), the action, and the cost
    frontier = PriorityQueue()
    frontier.push([(problem.getStartState(),"",0)],0)
    exploredSet = []

    while not frontier.isEmpty():
        currentPath = frontier.pop()
        currentLeaf = currentPath[-1]

        if (currentLeaf[0] not in exploredSet):
            exploredSet.append(currentLeaf[0])

            if (problem.isGoalState(currentLeaf[0])):
                #remove start node (no movement to start state)
                currentPath.pop(0)
                return [node[1] for node in currentPath]

            #expand leaf
            for leaf in problem.getSuccessors(currentLeaf[0]):
                if (leaf[0] not in exploredSet):
                    frontier.push(currentPath + [leaf], sum(node[2] for node in currentPath + [leaf]) + heuristic(leaf[0], problem))

    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
