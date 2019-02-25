
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.visit = {}

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        self.visit[self.currentState.state] = True

        # get all moves
        movables = self.gm.getMovables()
        move = self.currentState.nextChildToVisit

        if self.currentState.state == self.victoryCondition:
            return True
        # print (self.currentState.state)
        # print (movables)
        # print ("///////////////////////")
        while move < len(movables):
            # Get the move, make the move, and get the state
            movable_statement = movables[move]
            self.gm.makeMove(movable_statement)
            next_state = self.gm.getGameState()

            # if next state not visited, explore
            if next_state not in self.visit:
                new_move = GameState(next_state, self.currentState.depth + 1, movable_statement)
                new_move.parent = self.currentState
                self.currentState.children.append(new_move)
                self.currentState.nextChildToVisit = move + 1
                self.currentState = new_move
                break
            else:
                self.gm.reverseMove(movable_statement)
                move += 1

        if (move >= len(movables)):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        return False


                    



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = []
        self.visit = {}
        self.paths = {}

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True 

        self.visit[self.currentState.state] = True
        if self.currentState.depth == 0:
            self.paths[self.currentState.state] = []
        movables = self.gm.getMovables()
        
        for move in movables:
            self.gm.makeMove(move)
            child = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
            self.paths[child.state] = self.paths[self.currentState.state] + [move]
            if child.state not in self.visit:
                self.visit[child.state] = True
                self.queue.append(child)
            self.gm.reverseMove(move)
            self.currentState.children.append(child)

        if self.queue:
            node = self.queue.pop(0)
            same_moves = 0
            path = []
            required_movables = len(self.paths[self.currentState.state])
            node_required_movables = len(self.paths[node.state])
            while same_moves < required_movables and (self.paths[self.currentState.state][same_moves] == self.paths[node.state][same_moves]):
                same_moves += 1

            for ii in range(required_movables-1, same_moves-1, -1):
                self.gm.reverseMove(self.paths[self.currentState.state][ii])


            for move in self.paths[node.state][same_moves:]:
                self.gm.makeMove(move)

            self.currentState = node
            if self.currentState.state == self.victoryCondition:
                return True

        return False
                

