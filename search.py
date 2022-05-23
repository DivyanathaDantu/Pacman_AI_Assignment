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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    openStack = util.Stack()
    openStack.push(problem.getStartState())
    closed = []
    result = []
    flag = 1
    while not openStack.isEmpty():
        x = openStack.pop()
        if flag == 2:
            if problem.isGoalState(x[0]):
                return x[1].split(" ")[::-1]
            else:
                child = problem.getSuccessors(x[0])
                closed.append(x[0])
            for c in child:
                if c[0] not in closed:
                    c = list(c)
                    c[1] = c[1] + " " + x[1]
                    c = tuple(c)
                    openStack.push(c)
        else:
            if problem.isGoalState(x):
                return result
            else:
                child = problem.getSuccessors(x)
                closed.append(x)
            for c in child:
                if c[0] not in closed:
                    openStack.push(c)
        flag = 2
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    open_queue = util.Queue()
    open_queue.push(problem.getStartState())
    open_node = []
    closed = []
    result = []
    flag = 1
    while not open_queue.isEmpty():
        x = open_queue.pop()
        if flag == 2:
            open_node.remove(x[0])
            if problem.isGoalState(x[0]):
                return x[1].split(" ")[::-1]
            else:
                child = problem.getSuccessors(x[0])
                closed.append(x[0])
            for c in child:
                if c[0] not in closed and c[0] not in open_node:
                    c = list(c)
                    c[1] = c[1] + " " + x[1]
                    c = tuple(c)
                    open_queue.push(c)
                    open_node.append(c[0])
        else:
            if problem.isGoalState(x):
                return result
            else:
                child = problem.getSuccessors(x)
                closed.append(x)
            for c in child:
                if c[0] not in closed:
                    open_queue.push(c)
                    open_node.append(c[0])
        flag = 2
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    open_queue = util.PriorityQueue()
    open_queue.push(problem.getStartState(), 0)
    open_node = []
    closed = []
    result = []
    result_dict = dict()
    flag = 1
    while not open_queue.isEmpty():
        x = open_queue.pop()
        if flag == 2:
            open_node.remove(x)
            if problem.isGoalState(x):
                return result_dict[x].split(" ")[::-1]
            else:
                child = problem.getSuccessors(x)
                closed.append(x)
            for c in child:
                if c[0] not in closed and c[0] not in open_node:
                    c = list(c)
                    c[1] = c[1] + " " + result_dict[x]
                    c = tuple(c)
                    result_dict[c[0]] = c[1]
                    open_queue.push(c[0], problem.getCostOfActions(c[1].split(" ")[::-1]))
                    open_node.append(c[0])
                elif c[0] in open_node:
                    c = list(c)
                    c[1] = c[1] + " " + result_dict[x]
                    c = tuple(c)
                    new_cost = problem.getCostOfActions(c[1].split(" ")[::-1])
                    old_cost = problem.getCostOfActions(result_dict[c[0]].split(" ")[::-1])
                    if new_cost < old_cost:
                        result_dict[c[0]] = c[1]
                        open_queue.update(c[0], new_cost)
            result_dict.pop(x)
        else:
            if problem.isGoalState(x):
                return result
            else:
                child = problem.getSuccessors(x)
                closed.append(x)
            for c in child:
                if c[0] not in closed:
                    open_queue.push(c[0], problem.getCostOfActions(c[1].split(" ")[::-1]))
                    result_dict[c[0]] = c[1]
                    open_node.append(c[0])
        flag = 2
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    open_queue = util.PriorityQueue()
    open_queue.push(problem.getStartState(), 0)
    open_node = []
    closed = []
    result = []
    result_dict = dict()
    flag = 1
    while not open_queue.isEmpty():
        x = open_queue.pop()
        if flag == 2:
            open_node.remove(x)
            if problem.isGoalState(x):
                return result_dict[x].split(" ")[::-1]
            else:
                child = problem.getSuccessors(x)
                closed.append(x)
            for c in child:
                if c[0] not in closed and c[0] not in open_node:
                    c = list(c)
                    c[1] = c[1] + " " + result_dict[x]
                    c = tuple(c)
                    result_dict[c[0]] = c[1]
                    cost = problem.getCostOfActions(c[1].split(" ")[::-1]) + heuristic(c[0], problem)
                    open_queue.push(c[0], cost)
                    open_node.append(c[0])
                elif c[0] in open_node:
                    c = list(c)
                    c[1] = c[1] + " " + result_dict[x]
                    c = tuple(c)
                    new_cost = problem.getCostOfActions(c[1].split(" ")[::-1])
                    old_cost = problem.getCostOfActions(result_dict[c[0]].split(" ")[::-1])
                    if new_cost < old_cost:
                        result_dict[c[0]] = c[1]
                        open_queue.update(c[0], new_cost + heuristic(c[0], problem))
            result_dict.pop(x)
        else:
            if problem.isGoalState(x):
                return result
            else:
                child = problem.getSuccessors(x)
                closed.append(x)
            for c in child:
                if c[0] not in closed:
                    cost = problem.getCostOfActions(c[1].split(" ")[::-1]) + heuristic(c[0], problem)
                    open_queue.update(c[0], cost)
                    result_dict[c[0]] = c[1]
                    open_node.append(c[0])
        flag = 2
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
