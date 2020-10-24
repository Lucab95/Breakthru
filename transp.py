import time
from copy import deepcopy
import numpy as np
import GameState
import random

MAXDEPTH = 3


class AI():
    def __init__(self, player_turn):

        self.timeRequired = 0
        self.ControlGold = True
        self.maxDepth = MAXDEPTH
        self.player_turn = player_turn
        self.visitedNode = 0
        self.table = [[[random.randint(1, 2 ** 64 - 1) for i in range(3)] for j in range(11)] for k in range(11)]
        self.TT = dict({})

    def evaluationFunction(self, gameState, goldToMove):
        """evalfunction to give a certain score to the state"""
        win = 0
        fR, fC = gameState.flagShipPosition
        if gameState.flagShip == 0:
            win = -10000000
        elif fR == 0 or fR == 10 or fC == 0 or fC == 10:
            print("win")
            # gameState.stillPlay=False;
            win = 10000000
        evalValue = 5 * gameState.goldFleet - 3 * gameState.silverFleet + win
        # print(evalValue)
        return evalValue

        # best_value = float('-inf') if is_max_turn else float('inf')

    def chooseMove(self, state):
        # def chooseMove(self, validMoves, captureMoves, gameState, play):
        """predict next move for the AI"""
        self.visitedNode = 0
        start_time = time.time()
        print("AI is calculating the next move")
        gameState = deepcopy(state)
        eval_score, selectedMove = self.miniMaxAlphaBeta(MAXDEPTH, gameState, gameState.stillPlay, gameState.goldToMove,
                                                         float('-inf'), float('inf'))
        # print(selectedMove)
        # print("mossaa", validMoves[selected_Action])
        print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.visitedNode))
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

    def miniMaxAlphaBeta(self, depth, gameState, stillPlay, goldToMove, alpha, beta):
        hashKey = self.calculateHash(gameState)
        olda = alpha  # save previous alpha
        self.visitedNode += 1
        # TT lookup
        """n[0]: depth, n[1] = best_value, n[2] = action_target, n[3] = flag"""
        n = self.retrieve(hashKey)  # check if it's a already seen state -1 if not found
        # print("lista",len(list(self.TT)))
        if n != -1:
            # print("repetition")
            if n[0] >= depth:
                if n[3] == "eX":
                    return n[1],n[2]
                elif n[3] == "lB":
                    alpha = max(alpha, n[1])
                elif n[3] == "uB":
                    beta = min(beta,n[1])
                if alpha >= beta:
                    return n[1],n[2]
        if depth == 0 or not stillPlay:  # leaf node!
            return self.evaluationFunction(gameState, gameState.goldToMove), ""
        validMoves, captureMoves = gameState.getValidMoves()
        #union of moves
        for move in captureMoves:
            validMoves.append(move)
        # random.shuffle(validMoves)
        best_value = float('-inf') if goldToMove else float('inf')
        action_target = ""
        for action in validMoves:
            new_gameState = self.nextState(action, gameState)
            eval_child, action_child = self.miniMaxAlphaBeta(depth - 1, new_gameState, new_gameState.stillPlay,
                                                             new_gameState.goldToMove, alpha, beta)
            # if eval_child > 10000:
            #     gameState.stillPlay = False
            # if eval_child < -10000:
            #     gameState.stillPlay = False
            if goldToMove and best_value <= eval_child:
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

        if best_value <= olda:
            flag = "uB"
        elif best_value>= beta:
            flag = "lB"
        else:
            flag = "eX"

        info = (depth,best_value,action_target, flag)
        self.store(hashKey,info)
        return best_value, action_target

    def calculateHash(self, gameState):
        """calculates the Zobrist hash for the current board"""
        board = gameState.board
        hash = 0
        for r in range(len(board)):  # number of rows
            for c in range(len(board[0])):  # number of columns
                piece = board[r][c]
                if piece != "-":
                    hash ^= self.table[r][c][self.calculateIndex(piece)]
        return hash

    def calculateIndex(self, piece):
        """calculate the index for every piece-> empty = -1, silver = 0, gold=1, flagShip = 2"""
        if piece == "sP":
            return 0
        elif piece == "gP":
            return 1
        else:
            return 2

    def retrieve(self, hashKey):
        n = self.TT.get(hashKey)
        if n is not None:
            # print("exist hash stored")
            return n
        return -1

    def store(self, hashKey, info ):
        # print(self.retrieve(hashKey))
        self.TT.setdefault(hashKey, info)

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
