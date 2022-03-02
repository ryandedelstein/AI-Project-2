# multiAgents.py
# --------------
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


from queue import Empty
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # print("Curr Position")
        # print(currentGameState.getPacmanPosition())
        # print("New Position")
        # print(newPos)
        # print("Food")
        # print(newFood.asList())
        # print("Ghost States")
        # print(newGhostStates[0].getPosition())


        "*** YOUR CODE HERE ***"
    
        #get minimum distance to a ghost
        ghost_min = 1000
        for i in newGhostStates:
            ghost_min = min(ghost_min, util.manhattanDistance(newPos, i.getPosition()))
        
        #get minimum distance to a piece of food
        food_min = 10000
        for i in newFood.asList():
            food_min = min(food_min, util.manhattanDistance(newPos, i))

        #create food score: want a value where the closer we are to food the better
        if food_min == 0:
            food_score = 10000
        else:
            food_score = 100/food_min
        
    
        #create ghost score: want a value where close to ghost is worse
        if ghost_min <= 1:
            ghost_score = -10000000
            return ghost_score
        else:
            return food_score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxHelper(gameState, self.depth)
    
    def minimaxHelper(self, gameState, depth):
        # if depth == 0:
        #     return self.evaluationFunction(gameState)

        pacman_actions = gameState.getLegalActions(0)
        curr_agent = 1
        ghost_actions = []
        while curr_agent < gameState.getNumAgents():
            ghost_actions.append(gameState.getLegalActions(curr_agent))
            curr_agent = curr_agent + 1
        action_combos = self.get_all_combos(ghost_actions)
        


        # if depth == 0:
        #     return (None, self.evaluationFunction(gameState))
        # pacman_actions = gameState.getLegalActions(0)
        # curr_agent = 1
        # ghost_actions = []
        # while curr_agent <= gameState.getNumAgents() - 1:
        #     ghost_actions.append(gameState.getLegalActions(curr_agent))
        #     curr_agent = curr_agent + 1
        
        # action_combos = self.get_all_combos(ghost_actions)
        # maximum = (None,-10000000000000)
        # for i in pacman_actions:
        #     curr_pacman_move = gameState.getNextState(0, i)
        #     if curr_pacman_move.isWin():
        #         return (i, 100000000000)
        #     if curr_pacman_move.isLose():
        #         continue
        #     minimum = 100000000000000
        #     for j in action_combos:
        #         newState = curr_pacman_move
        #         for k in range(len(j)):
        #             newState = newState.getNextState(k + 1, j[k])
        #         eval = self.minimaxHelper(newState, depth - 1)[1]
        #         if eval < minimum:
        #             minimum = eval
        #     if minimum > maximum[1]:
        #         maximum = (i, minimum)
        # print(maximum)
        # return maximum[0]
        

    
    def get_all_combos(self, ghost_actions):
        if len(ghost_actions) == 0:
            return []
        next_combos = self.get_all_combos(ghost_actions[1:])
        ret = []
        for i in ghost_actions[0]:
            for j in next_combos:
                ret.append([i] + j)
        return ret
        

        





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
