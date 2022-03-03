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


from hashlib import new
from queue import Empty
from pacman import GameState
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
        return self.maximize_pacman(gameState, self.depth)
    


    #returns pair of form (move, evaluation)
    def maximize_pacman(self, gameState, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        pacman_moves = gameState.getLegalActions(0)
        max_move = None
        maximum = -1000000000
        for i in pacman_moves:
            curr_pacman_position = gameState.getNextState(0, i)
            if curr_pacman_position.isWin() or curr_pacman_position.isLose():
                eval = self.evaluationFunction(curr_pacman_position)
            else:
                eval = self.minimize_ghosts(curr_pacman_position, depth, 1)
            if eval > maximum:
                maximum = eval
                max_move = i

        if depth == self.depth:
            return max_move

        return maximum


    def minimize_ghosts(self, gameState, depth, curr_ghost):
        if curr_ghost ==  gameState.getNumAgents():
            if depth == 1:
                return self.evaluationFunction(gameState)
            else:
                return self.maximize_pacman(gameState, depth - 1)
        

        actions = gameState.getLegalActions(curr_ghost)
        if len(actions)==0:
            return self.evaluationFunction(gameState)
        minimum = 10000000000000
        for curr in actions:
            newState = gameState.getNextState(curr_ghost, curr)
            if newState.isWin() or newState.isLose():
                eval = self.evaluationFunction(newState)
            else:
                eval = self.minimize_ghosts(newState, depth, curr_ghost + 1)
            if eval < minimum:
                minimum = eval
        return minimum

                
                
                

        





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.maximize_pacman_prune(gameState, self.depth, -1000000000000, 100000000000000)


    def maximize_pacman_prune(self, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        pacman_moves = gameState.getLegalActions(0)
        max_move = None
        maximum = -1000000000
        pruning_number = -100000000000
        for i in pacman_moves:
            curr_pacman_position = gameState.getNextState(0, i)
            if curr_pacman_position.isWin() or curr_pacman_position.isLose():
                eval = self.evaluationFunction(curr_pacman_position)
            else:
                eval = self.minimize_ghosts_prune(curr_pacman_position, depth, 1, alpha, beta)
            if eval > maximum:
                maximum = eval
                max_move = i
            pruning_number = max(pruning_number, eval)
            if pruning_number > beta:
                if depth == self.depth:
                    return max_move
                else:
                    return eval
            else:
                alpha = max(alpha, pruning_number)

        if depth == self.depth:
            return max_move

        return maximum


    def minimize_ghosts_prune(self, gameState, depth, curr_ghost, alpha, beta):
        if curr_ghost ==  gameState.getNumAgents():
            if depth == 1:
                return self.evaluationFunction(gameState)
            else:
                return self.maximize_pacman_prune(gameState, depth - 1, alpha, beta)
        

        actions = gameState.getLegalActions(curr_ghost)
        if len(actions)==0:
            return self.evaluationFunction(gameState)
        minimum = 10000000000000
        pruning_number = 100000000000
        for curr in actions:
            newState = gameState.getNextState(curr_ghost, curr)
            if newState.isWin() or newState.isLose():
                eval = self.evaluationFunction(newState)
            else:
                eval = self.minimize_ghosts_prune(newState, depth, curr_ghost + 1, alpha, beta)
            if eval < minimum:
                minimum = eval
            pruning_number = min(eval, pruning_number)
            if pruning_number < alpha:
                return pruning_number
            beta = min(beta, pruning_number)
        return minimum

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
        return self.maximize_pacman(gameState, self.depth)

    def maximize_pacman(self, gameState, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        pacman_moves = gameState.getLegalActions(0)
        max_move = None
        maximum = -1000000000
        for i in pacman_moves:
            curr_pacman_position = gameState.getNextState(0, i)
            if curr_pacman_position.isWin() or curr_pacman_position.isLose():
                eval = self.evaluationFunction(curr_pacman_position)
            else:
                eval = self.expected_ghosts(curr_pacman_position, depth, 1, 0, 0)
            if eval > maximum:
                maximum = eval
                max_move = i

        if depth == self.depth:
            return max_move

        return maximum


    def expected_ghosts(self, gameState, depth, curr_ghost, tot, num):
        if curr_ghost ==  gameState.getNumAgents():
            if depth == 1:
                return self.evaluationFunction(gameState)
            else:
                return self.maximize_pacman(gameState, depth - 1)
        

        actions = gameState.getLegalActions(curr_ghost)
        if len(actions)==0:
            return self.evaluationFunction(gameState)
        for curr in actions:
            newState = gameState.getNextState(curr_ghost, curr)
            if newState.isWin() or newState.isLose():
                eval = self.evaluationFunction(newState)
            else:
                eval = self.expected_ghosts(newState, depth, curr_ghost + 1, tot, num)
            tot = tot + eval
            num = num + 1
        return tot / num

def betterEvaluationFunction(currentGameState):
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsules = currentGameState.getCapsules()

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
        for i in newFood.asList() + capsules:
            food_min = min(food_min, util.manhattanDistance(newPos, i))
        

        #create food score: want a value where the closer we are to food the better
        if food_min == -1:

            food_score = 1000000
        else:
            food_score = currentGameState.getScore() - food_min - len(newFood.asList()) - len(capsules)
        
    
        #create ghost score: want a value where close to ghost is worse
        if ghost_min <= 1:
            ghost_score = -10000000
            return ghost_score
        else:
            ret =  -len(newFood.asList()) - food_min
            return ret
    # """
    # Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    # evaluation function (question 5).

    # DESCRIPTION: <write something here so we know what you did>
    # """
    # "*** YOUR CODE HERE ***"
    # return food_score(currentGameState) + ghost_score(currentGameState)

def food_score(gameState):
    position = gameState.getPacmanPosition()
    food = gameState.getFood().asList()

    score = 0
    food_distances = []
    for i in food:
        food_distances.append(util.manhattanDistance(i, position))
    
    food_distances.sort()

    length = len(food_distances)
    for i in range(length):
        curr = food_distances[i]
        if curr == 0:
            score = score + length * 2
        else:
            score = score + 100*(length - i) / curr
    
    return score

def ghost_score(gameState):
    position = gameState.getPacmanPosition()
    ghosts = gameState.getGhostStates()
    score = 0

    ghost_distances = []
    for i in ghosts:
        ghost_distances.append(util.manhattanDistance(i.getPosition(), position))
    ghost_distances.sort()

    length = len(ghost_distances)
    for i in range(length):
        curr = ghost_distances[i]
        if curr <= 1:
            return -1000000
        else:
            score = score - (length - i) / curr
    
    return score



# Abbreviation
better = betterEvaluationFunction
