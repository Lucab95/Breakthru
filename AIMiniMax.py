import time
from copy import deepcopy

import GameState
import random
from tkinter import *
import gc
from tkinter import messagebox

MAXDEPTH = 3


class AI():
    def __init__(self, player_turn):

        self.timeRequired = 0
        self.ControlGold = True
        self.maxDepth = MAXDEPTH
        self.player_turn = player_turn
        self.node_expanded = 0

    def evaluationFunction(self, gameState, goldToMove):
        """Evaluate the state to decide the most convenient move"""
        # basiceval = 5 * gameState.goldFleet + 20 * gameState.flagShip - 4 * gameState.silverFleet + 50*winMoves
        # if winMoves!=0:
        #
        #     # print("win")
        #     return  10000000
        # print (gameState.flagShipPosition)
        # if r ==0 or r ==10 or c==0 or c==10:
        #     return 10000000
        #     print("win")
        # last = gameState.moveLog[-1]
        # print(last.pieceMoved)
        win = 0
        fR, fC = gameState.flagShipPosition
        # if last.pieceMoved == "gFS":
        #     print("gfs", last.endRow, last.endCol)
        #     if last.endRow == 0 or last.endRow ==10 or last.endCol==0 or last.endCol ==10:
        #         print("win")
        #         # gameState.stillPlay=False;
        #         win= 10000000
        if gameState.flagShip == 0:
            win = -10000000
        elif fR == 0 or fR == 10 or fC == 0 or fC == 10:
            print("win")
            # gameState.stillPlay=False;
            win = 10000000
        evalValue = 5 * gameState.goldFleet - 3 * gameState.silverFleet + win
        # print(evalValue)
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

    def chooseMove(self, state):
        # def chooseMove(self, validMoves, captureMoves, gameState, play):
        gc.collect()
        """try to predict a move using minmax algorithm"""
        self.node_expanded = 0

        start_time = time.time()

        print("AI is thinking")
        # eval_score, selected_Action = self.miniMax(0, validMoves, captureMoves, gameState, play, True)
        # eval_score, selected_Action = self.miniMax(0, gameState, play, gameState.goldToMove)

        gameState = deepcopy(state)
        print("end? :", gameState.stillPlay)
        eval_score, selectedMove = self.miniMaxAlphaBeta(0, gameState, gameState.stillPlay, gameState.goldToMove,
                                                         float('-inf'), float('inf'))
        # print("mossaa", validMoves[selected_Action])
        print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.node_expanded))
        timeSpent = time.time() - start_time
        self.timeRequired += timeSpent
        self.timeRequired = round(self.timeRequired, 3)
        print("--- %s seconds ---" % (timeSpent))
        return (selectedMove)

    def nextState(self, move, gameState):
        """return the new state after executing the move"""
        # window = Tk()
        # window.eval("tk::PlaceWindow %s center" % window.winfo_toplevel())
        # window.withdraw()
        # if move.pieceMoved == "gFS":
        #     print(move.pieceMoved)
        nextGameState = deepcopy(gameState)
        nextGameState.DEBUG = False
        nextGameState.makeMove(move)
        return nextGameState

    # def miniMax(self, depth, state, play, goldToMove):  # , validMoves, captureMoves*/, ):
    #     gameState = deepcopy(state)
    #     validMoves, captureMoves = gameState.getValidMoves()
    #     vMoves = len(validMoves)
    #     cMoves = len(captureMoves)
    #     if depth == self.maxDepth or not play:
    #         return self.evaluationFunction(validMoves, state, gameState.goldToMove), ""
    #
    #     self.node_expanded += 1
    #     # possible_action = AIElements.get_possible_action(state)
    #     # validMoves and captureMoves in my case
    #     vMoves = dict(zip(range(vMoves), validMoves))
    #     cMoves = dict(zip(range(cMoves), captureMoves))  # TODO togliere mosse sovrascr-> cambiare nella funzione che genera le mosse
    #     possibleMoves = {**vMoves, **cMoves}
    #     # print(len(cMoves),len(vMoves),len(possibleMoves))
    #     # possibleCapture = dict(captureMoves[i:i + 2] for i in range(0, len(captureMoves), 2))
    #     key_of_validMoves = list(possibleMoves.keys())
    #     random.shuffle(key_of_validMoves)  # randomness
    #     best_value = float('-inf') if goldToMove else float('inf')
    #     action_target = ""
    #     for action in key_of_validMoves:
    #         new_gameState = self.nextState(possibleMoves[action], gameState)
    #         # print(new_gameState.goldToMove)
    #         eval_child, action_child = self.miniMax(depth + 1, new_gameState, play,new_gameState.goldToMove)
    #         if goldToMove and best_value < eval_child:
    #             best_value = eval_child
    #             action_target = action
    #         elif (not goldToMove) and best_value > eval_child:
    #             best_value = eval_child
    #             action_target = action
    #     # print("ci arriva", action_target)
    #     # del new_gameState
    #     return best_value, possibleMoves[action_target]
    #
    #     # evalscore,  move = self.minMax(0,)
    #     # prima funz
    #
    #     # best_value = float('-inf') if is_max_turn else float('inf')

    def miniMaxAlphaBeta(self, depth, state, stillPlay, goldToMove, alpha, beta):
        gameState = state
        # for move in validMoves:
        #     if move.pieceMoved == "gFS":
        #         print(move.getNotation())
        # vMoves = len(validMoves)
        # cMoves = len(captureMoves)
        # winMoves = gameState.getSpecificalMoves(gameState.flagShipPosition[0], gameState.flagShipPosition[1])
        # if not stillPlay:

        self.node_expanded += 1
        # print("gioca ancora in aI:",stillPlay)
        if depth == self.maxDepth or not stillPlay:
            return self.evaluationFunction(gameState, gameState.goldToMove), ""
        validMoves, captureMoves = gameState.getValidMoves()
        for move in captureMoves:
            validMoves.append(move)
        vMoves = len(validMoves)
        possibleMoves = dict(zip(range(vMoves), validMoves))
        # print(vMoves)
        # cMoves = dict(zip(range(cMoves),
        #                   captureMoves))  # TODO togliere mosse sovrascr-> cambiare nella funzione che genera le mosse
        # print(len(possibleMoves), len(cMoves))
        # possibleMoves.update(cMoves)
        # print(len(cMoves),len(vMoves),len(possibleMoves))
        # possibleCapture = dict(captureMoves[i:i + 2] for i in range(0, len(captureMoves), 2))
        key_of_validMoves = list(possibleMoves.keys())
        random.shuffle(key_of_validMoves)  # randomness
        best_value = float('-inf') if goldToMove else float('inf')
        action_target = ""
        for action in key_of_validMoves:
            # for i,k in enumerate(validMoves):
            # print(i,k)
            new_gameState = self.nextState(possibleMoves[action], gameState)
            # print(new_gameState.goldToMove)
            # print(depth, goldToMove)
            eval_child, action_child = self.miniMaxAlphaBeta(depth + 1, new_gameState, new_gameState.stillPlay,
                                                             new_gameState.goldToMove, alpha, beta)
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
        return best_value, possibleMoves[action_target]

    # def negaMaxAlphaBeta(self, depth, state, play, goldToMove, alpha, beta):
    #     gameState = deepcopy(state)
    #     validMoves, captureMoves = gameState.getValidMoves()
    #     vMoves = len(validMoves)
    #     cMoves = len(captureMoves)
    #     if depth == self.maxDepth or not play:
    #         return self.evaluationFunction(validMoves, state, gameState.goldToMove), ""
    #
    #     self.node_expanded += 1
    #     # possible_action = AIElements.get_possible_action(state)
    #     # validMoves and captureMoves in my case
    #     vMoves = dict(zip(range(vMoves), validMoves))
    #     cMoves = dict(zip(range(cMoves),
    #                       captureMoves))  # TODO togliere mosse sovrascr-> cambiare nella funzione che genera le mosse
    #     possibleMoves = {**vMoves, **cMoves}
    #     # print(len(cMoves),len(vMoves),len(possibleMoves))
    #     # possibleCapture = dict(captureMoves[i:i + 2] for i in range(0, len(captureMoves), 2))
    #     key_of_validMoves = list(possibleMoves.keys())
    #     random.shuffle(key_of_validMoves)  # randomness
    #     best_value = float('-inf') if goldToMove else float('inf')
    #     action_target = ""
    #     for action in key_of_validMoves:
    #         new_gameState = self.nextState(possibleMoves[action], gameState)
    #         # print(new_gameState.goldToMove)
    #         eval_child, action_child = self.miniMaxAlphaBeta(depth + 1, new_gameState, play,
    #                                                          new_gameState.goldToMove, alpha, beta)
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
    #     # print("ci arriva", action_target)
    #     # del new_gameState
    #     return best_value, possibleMoves[action_target]
