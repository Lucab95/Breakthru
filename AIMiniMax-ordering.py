import time
from copy import deepcopy

import GameState
import random
from tkinter import *
import gc
from tkinter import messagebox

MAXDEPTH = 4


class AI():
    def __init__(self, player_turn):

        self.timeRequired = 0
        self.ControlGold = True
        self.maxDepth = MAXDEPTH
        self.player_turn = player_turn
        self.visitedNode = 0
        self.timeLimit=100

    def evaluationFunction(self, gameState, goldToMove):
        """Evaluate the state to decide the most convenient move"""
        win = 0
        fR, fC = gameState.flagShipPosition
        # check if flaghsip gets eaten or if it can escape
        if gameState.flagShip == 0:
            win = -10000000
        elif fR == 0 or fR == 10 or fC == 0 or fC == 10:
            print("win")
            # gameState.stillPlay=False;
            win = 10000000
        evalValue = 5 * gameState.goldFleet - 3 * gameState.silverFleet
        # print(evalValue)
        return evalValue

    def chooseMove(self, state):
        gc.collect()
        """try to predict a move using minmax algorithm"""
        self.visitedNode = 0
        start_time = time.time()
        print("AI is calculating the next move")
        gameState = deepcopy(state)

        eval_score, selectedMove = self.miniMaxAlphaBeta(0, gameState, gameState.stillPlay, gameState.goldToMove,
                                                         float('-inf'), float('inf'),start_time)
        print("AI finished, value = %d, visited node: %d" % (eval_score, self.visitedNode))
        timeSpent = time.time() - start_time
        self.timeRequired += timeSpent
        self.timeRequired = round(self.timeRequired, 3)
        print("--- %s seconds ---" % (timeSpent))
        return (selectedMove)

    def nextState(self, move, gameState):
        """return the new state after executing the move"""
        nextGameState = deepcopy(gameState)
        nextGameState.DEBUG = False
        nextGameState.makeMove(move)
        return nextGameState

    def miniMaxAlphaBeta(self, depth, gameState, stillPlay, goldToMove, alpha, beta ,time):
        # gameState = state
        # for move in validMoves:
        #     if move.pieceMoved == "gFS":
        #         print(move.getNotation())
        # vMoves = len(validMoves)
        # cMoves = len(captureMoves)
        # winMoves = gameState.getSpecificalMoves(gameState.flagShipPosition[0], gameState.flagShipPosition[1])
        # if not stillPlay:

        self.visitedNode += 1
        # print("gioca ancora in aI:",stillPlay)
        if depth == self.maxDepth or not stillPlay:
            return self.evaluationFunction(gameState, gameState.goldToMove), ""
        sortedMoves, captureMoves = gameState.getValidMoves()
        for move in captureMoves:
            sortedMoves.append(move)

        #move ordering
        scoreList = []
        for action in sortedMoves:
            order_state = self.nextState(action, gameState)
            score = self.evaluationFunction(order_state, order_state.goldToMove)
            scoreList.append(score)
        sortedMoves = list(zip(scoreList, sortedMoves))
        # sortedMoves = list(movesWithScores)
        if goldToMove:
            sortedMoves.sort(key=lambda mv: mv[0], reverse=True)
        else:
            sortedMoves.sort(key=lambda mv: mv[0], reverse=False)
        # print(sortedMoves)
        sortedMoves = [move for _, move in sortedMoves]
        # print(sortedMoves)
        if not gameState.goldToMove:
            sortedMoves = sortedMoves[::-1]

        best_value = float('-inf') if goldToMove else float('inf')
        action_target = ""

        for action in sortedMoves:
            new_gameState = self.nextState(action, gameState)
            eval_child, action_child = self.miniMaxAlphaBeta(depth + 1, new_gameState, new_gameState.stillPlay,
                                                             new_gameState.goldToMove, alpha, beta, time)
            if eval_child > 10000:
                gameState.stillPlay = False
            if eval_child < -10000:
                gameState.stillPlay = False
            if goldToMove and best_value < eval_child:
                best_value = eval_child
                action_target = action
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif (not goldToMove) and best_value > eval_child:
                best_value = eval_child
                action_target = action
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
        # print("ci arriva", action_target)
        # del new_gameState
        return best_value, action_target


    # def miniMaxABIDD(self, depth, gameState, stillPlay, goldToMove, alpha, beta):
    #
    #     self.visitedNode += 1
    #     # print("gioca ancora in aI:",stillPlay)
    #     if depth == self.maxDepth or not stillPlay:
    #         return self.evaluationFunction(gameState, gameState.goldToMove), ""
    #     validMoves, captureMoves = gameState.getValidMoves()
    #     for move in captureMoves:
    #         validMoves.append(move)
    #     random.shuffle(validMoves)
    #     vMoves = len(validMoves)
    #     best_value = float('-inf') if goldToMove else float('inf')
    #     action_target = ""
    #     for action in validMoves:
    #         new_gameState = self.nextState(action, gameState)
    #         eval_child, action_child = self.miniMaxAlphaBeta(depth + 1, new_gameState, new_gameState.stillPlay,
    #                                                          new_gameState.goldToMove, alpha, beta)
    #         if eval_child > 10000:
    #             gameState.stillPlay = False
    #         if eval_child < -10000:
    #             gameState.stillPlay = False
    #         if goldToMove and best_value < eval_child:
    #             best_value = eval_child
    #             action_target = action
    #             alpha = max(alpha, best_value)
    #             if beta <= alpha:
    #                 break
    #         elif (not goldToMove) and best_value > eval_child:
    #             best_value = eval_child
    #             action_target = action
    #             beta = min(beta, best_value)
    #             if beta <= alpha:
    #                 break
    #     return best_value, action_target

    # def negaMaxAlphaBeta(self, depth, gameState, stillPlay, goldToMove, alpha, beta):
    #     self.visitedNode += 1
    #     # print("gioca ancora in aI:",stillPlay)
    #     if depth == self.maxDepth or not stillPlay:
    #         return self.evaluationFunction(gameState, gameState.goldToMove), ""
    #     validMoves, captureMoves = gameState.getValidMoves()
    #     for move in captureMoves:
    #         validMoves.append(move)
    #     vMoves = len(validMoves)
    #     # possibleMoves = dict(zip(range(vMoves), validMoves))
    #     # key_of_validMoves = list(possibleMoves.keys())
    #     score = float('-inf')
    #     action_target = ""
    #     for action in validMoves:
    #         previousMove=gameState.goldToMove
    #         new_gameState = self.nextState(action, gameState)
    #         # print(new_gameState.goldToMove)
    #         # print("turn", action.pieceMoved, previousMove, new_gameState.goldToMove)
    #         if previousMove != new_gameState.goldToMove:
    #
    #             value, child = self.negaMaxAlphaBeta(depth + 1, new_gameState, new_gameState.stillPlay,
    #                                                         new_gameState.goldToMove, -beta, -alpha)
    #             value = value * -1
    #         else:
    #             value, child = self.negaMaxAlphaBeta(depth + 1, new_gameState, new_gameState.stillPlay,
    #                                                         new_gameState.goldToMove, alpha, beta)
    #             value = value * -1
    #         if value > 10000:
    #             gameState.stillPlay = False
    #         if value < -10000:
    #             gameState.stillPlay = False
    #         if value > score:
    #             score = value
    #             action_target = action
    #         if score > alpha: alpha = score
    #         if score >= beta: break
    #
    #     # print("ci arriva", action_target)
    #     # del new_gameState
    #     # print(action_target,action_child)
    #     return score, action_target
