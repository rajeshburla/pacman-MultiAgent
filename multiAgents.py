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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
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

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        value = -10000
        if(Directions.STOP in action):
          return value
        distance = []
        for ghostState in newGhostStates:
          if ghostState.getPosition() == newPos and ghostState.scaredTimer == 0:
            return value

        for food in currentGameState.getFood().asList():
          distance = [manhattanDistance(food,newPos)]
        return (-max(distance))
        #return successorGameState.getScore()

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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        actionValue = self.getValue(gameState, depth, self.index)
        return actionValue[1]
        
        #util.raiseNotDefined()
    def getValue(self, gameState,depth,selfIndex):
      legalActions = []
      legalActions = gameState.getLegalActions()

      if selfIndex==gameState.getNumAgents():
        depth = depth+1
        selfIndex=0
        finalValue = 0
        finalList = []
      if len(legalActions) == 0 or depth==self.depth:
        finalValue = self.evaluationFunction(gameState)
        finalList = [finalValue]
        return finalList
      if selfIndex == 0:
        return self.maxOrMinValue(gameState,depth,selfIndex,[-float("inf")],"MAX")
      else:
        return self.maxOrMinValue(gameState,depth,selfIndex,[float("inf")],"MIN")
    
    def maxOrMinValue(self,gameState,depth,agentIndex, value, maxORmin):
        
        for action in gameState.getLegalActions(agentIndex):
            successorEvaluate = self.getValue(gameState.generateSuccessor(agentIndex, action), 
            depth, agentIndex + 1)
            if maxORmin is "MAX":
              if (successorEvaluate[0] >= value[0]):
                value = [successorEvaluate[0],action]
            elif maxORmin is "MIN":
              if (successorEvaluate[0] <= value[0]):
                value = [successorEvaluate[0],action]
        return value
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        root_value = self.value(gameState,0,self.index,-float("inf"),float("inf"))
        action = root_value[1]
        return action
        
    def value(self,gameState,CurrentDepth,agentIndex,alpha,beta):
        
        if agentIndex == gameState.getNumAgents():
            CurrentDepth = CurrentDepth + 1
            agentIndex = agentIndex = 0
        
        if CurrentDepth == self.depth:
            eval_value =  self.evaluationFunction(gameState)
            return [eval_value]
        
        legal_action = []
        legal_action = gameState.getLegalActions(agentIndex)
        
        if len(legal_action) == 0:
            eval_value =  self.evaluationFunction(gameState)
            return [eval_value]
        
        if agentIndex == 0:
            return self.max_value(gameState,CurrentDepth,agentIndex,alpha,beta)
        else:
            return self.min_value(gameState,CurrentDepth,agentIndex,alpha,beta)
        
    def max_value(self,gameState,CurrentDepth,agentIndex,alpha,beta):
        
        node_value = [-float("inf")]
        
        action_list = []
        action_list = gameState.getLegalActions(agentIndex)
        
        for action in action_list:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            successor_evalvalue = self.value(successor_state, CurrentDepth, agentIndex + 1,alpha,beta)

            successor_evalvalue = successor_evalvalue[0] 
            
            if (successor_evalvalue >= node_value[0]):
                node_value = [successor_evalvalue,action]
            
            max_value = node_value[0]
            
            if max_value > beta:
                return node_value
            
            alpha = max(max_value,alpha)

        return node_value
    
    def min_value(self,gameState,CurrentDepth,agentIndex,alpha,beta):
        
        node_value = [float("inf")]
        
        action_list = []
        action_list = gameState.getLegalActions(agentIndex)
                
        for action in action_list:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            successor_evalvalue = self.value(successor_state, CurrentDepth, agentIndex + 1,alpha,beta)
            
            successor_evalvalue = successor_evalvalue[0] 
            
            if (successor_evalvalue <= node_value[0]):
                node_value = [successor_evalvalue,action]
                
            min_value = node_value[0]
            
            if min_value < alpha:
                return node_value
            
            beta = min(min_value,beta)

        return node_value
        #util.raiseNotDefined()

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

