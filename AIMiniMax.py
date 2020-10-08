import time
from copy import deepcopy

import GameState
import random
from tkinter import *
import gc
from tkinter import messagebox


class AI():
    def __init__(self, depth, player_turn):

        self.ControlGold = True
        self.maxDepth = depth
        self.player_turn = player_turn
        self.node_expanded = 0


    def evaluationFunction(self, captureMoves,gameState, goldToMove):
        evalValue = 0

        if goldToMove :
            evalValue = 5 * (gameState.goldFleet -gameState.silverFleet) + 20 * gameState.flagShip + captureMoves
        else:
            evalValue = 3 * (
                        gameState.silverFleet - gameState.goldFleet) + captureMoves

        return evalValue

    # TODO correggere problema quando non ha mosse
    def basicMiniMax(self, depth, validMoves, captureMoves):
        gameState = GameState.GameState()
        # if depth == self.maxDepth or self.gameState.state == False:
        #     return self.evaluationFunction(validMoves, captureMoves)
        # for r in range(len(self.board)):  # number of rows
        #     for c in range(len(self.board[r])):
        #         if gameState.board[r][c] == "gFS":
        # if len(captureMoves) != 0 and gameState.secondMove == 0:
        #     for r in range(len(gameState.board)):  # number of rows
        #         for c in range(len(gameState.board[r])):
        #             # if gameState.board[r][c] == "gFS":
        # for move in captureMoves:
        #     if gameState.board[move.endRow][move.endCol]=="gFS":
        #         return move
        # if gameState.secondMove==0 and gameState.goldToMove:
        #         for r in range(len(gameState.board)):  # number of rows
        #             for c in range(len(gameState.board[r])):
        #                 if gameState.board[r][c] == "gFS":
        #                     for move in validMoves:
        #                         if move.startRow == r and move.startCol == c:
        #                             if move.endRow ==0 or move.endCol==0:
        #                                 return move
        if len(captureMoves) != 0 and gameState.secondMove == 0:

            # for move in captureMoves:
            #     if gameState.board[move.endRow][move.endCol] == "gFS":
            #         return move
            move = random.choice(captureMoves)
            return move
        else:
            return random.choice(validMoves)
        # evalscore,  move = self.minMax(0,)
        # prima funz

        # best_value = float('-inf') if is_max_turn else float('inf')

    def chooseMove(self, validMoves, captureMoves, gameState, play):
        gc.collect()
        """try to predict a move using minmax algorithm"""
        self.node_expanded = 0

        start_time = time.time()

        print("AI is thinking")
        eval_score, selected_Action = self.miniMax(0, validMoves, captureMoves, gameState, play, True)
        print("mossaa", validMoves[selected_Action])
        print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.node_expanded))
        print("--- %s seconds ---" % (time.time() - start_time))
        return (selected_Action, validMoves[selected_Action])


    def nextState(self, move, gameState):
        """return the new state after executing the move"""
        # window = Tk()
        # window.eval("tk::PlaceWindow %s center" % window.winfo_toplevel())
        # window.withdraw()
        nextGameState = deepcopy(gameState)
        nextGameState.DEBUG = False
        nextGameState.makeMove(move)
        return nextGameState


    def miniMax(self,depth, validMoves, captureMoves, state, play,  is_max_turn,):
        gameState = state
        vMoves = len(validMoves)
        cMoves = len(captureMoves)
        if depth == self.maxDepth or not play:
            return self.evaluationFunction(cMoves,state, gameState.goldToMove), ""
        self.node_expanded += 1
        # possible_action = AIElements.get_possible_action(state)
        # validMoves and captureMoves in my case
        vMoves= dict(zip(range(vMoves), validMoves))
        cMoves= dict(zip(range(cMoves), captureMoves)) #TODO togliere mosse sovrascr
        possibleMoves = {**vMoves, **cMoves}
        # possibleCapture = dict(captureMoves[i:i + 2] for i in range(0, len(captureMoves), 2))
        key_of_validMoves= list(possibleMoves.keys())
        random.shuffle(key_of_validMoves)  # randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action in key_of_validMoves:
            new_gameState = self.nextState(possibleMoves[action], gameState)
            eval_child, action_child = self.miniMax(depth + 1, validMoves, captureMoves, new_gameState, play, not is_max_turn)
            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action
        # print("ci arriva", action_target)
        del new_gameState
        return best_value, action_target



        # evalscore,  move = self.minMax(0,)
        # prima funz

        # best_value = float('-inf') if is_max_turn else float('inf')

    def minMaxAlphaBeta(self):
        pass
