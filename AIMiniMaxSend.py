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
        self.table = [[[random.randint(1, 2 ** 64 - 1) for i in range(3)] for j in range(11)] for k in range(11)]#initialize a table with random values for the 3 different pieces
        self.TT = dict({})
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
        """try to predict a move using minmax algorithm"""
        self.visitedNode = 0

        start_time = time.time()
        # hashValue = self.calculateHash(state.board)
        # print(hashValue)

        print("AI is thinking")
        # eval_score, selected_Action = self.miniMax(0, validMoves, captureMoves, gameState, play, True)
        # eval_score, selected_Action = self.miniMax(0, gameState, play, gameState.goldToMove)
        gameState = deepcopy(state)
        # print("end? :", gameState.stillPlay)

        eval_score, selectedMove = self.miniMaxAlphaBeta(0, gameState, gameState.stillPlay, gameState.goldToMove,
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
    #     self.visitedNode += 1
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

    def miniMaxAlphaBeta(self, depth, gameState, stillPlay, goldToMove, alpha, beta):
        # gameState = state
        # for move in validMoves:
        #     if move.pieceMoved == "gFS":
        #         print(move.getNotation())
        # vMoves = len(validMoves)
        # cMoves = len(captureMoves)
        # winMoves = gameState.getSpecificalMoves(gameState.flagShipPosition[0], gameState.flagShipPosition[1])
        # if not stillPlay:
        # hash = self.calculateHash(gameState.board)
        # self.TT.setdefault(hash,[depth,alpha,beta])
        # print("value",self.TT.get(2))
        # print(list(self.TT))

        self.visitedNode += 1
        # print("gioca ancora in aI:",stillPlay)
        if depth == self.maxDepth or not stillPlay:
            return self.evaluationFunction(gameState, gameState.goldToMove), ""
        validMoves, captureMoves = gameState.getValidMoves()
        for move in captureMoves:
            validMoves.append(move)
        random.shuffle(validMoves)
        vMoves = len(validMoves)
        # possibleMoves = dict(zip(range(vMoves), validMoves))
        # print(vMoves)
        # cMoves = dict(zip(range(cMoves),
        #                   captureMoves))  # TODO togliere mosse sovrascr-> cambiare nella funzione che genera le mosse
        # print(len(possibleMoves), len(cMoves))
        # possibleMoves.update(cMoves)
        # print(len(cMoves),len(vMoves),len(possibleMoves))
        # possibleCapture = dict(captureMoves[i:i + 2] for i in range(0, len(captureMoves), 2))
        # key_of_validMoves = list(possibleMoves.keys())
        # random.shuffle(key_of_validMoves)  # randomness
        best_value = float('-inf') if goldToMove else float('inf')
        action_target = ""
        for action in validMoves:
            # for i,k in enumerate(validMoves):
            # print(i,k)
            new_gameState = self.nextState(action, gameState)
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
        return best_value, action_target

    # def miniMaxABIDD(self, depth, gameState, stillPlay, goldToMove, alpha, beta):
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

    # def zobristHashing(self, board):
    #     calculateHash(gameState.board)

    def calculateHash(self, board):
        """calculates the Zobrist hash for the current board"""
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
