import time
from copy import deepcopy
import GameState
import random



class AI():
    def __init__(self, maxDepth, moveOrdering):

        self.timeRequired = 0
        self.ControlGold = True
        self.maxDepth = maxDepth
        self.visitedNode = 0
        self.table = [[[random.randint(1, 2 ** 64 - 1) for i in range(3)] for j in range(11)] for k in
                      range(11)]  # initialize a table with random values for the 3 different pieces
        self.TT = dict({})
        self.moveOrdering = moveOrdering

    def evaluationFunction(self, gameState, goldToMove):
        """Evaluate the state to decide the most convenient move"""
        evalValue = 0

        #get flag position
        fR, fC = gameState.flagShipPosition
        killScore = 0

        #flagship killed
        if gameState.flagShip == 0:
            killScore = -1000 if goldToMove else -1500
        evalValue += killScore

        #check if flag can escape
        if fR == 0: evalValue += 500
        if fR == 10: evalValue += 500
        if fC == 0: evalValue += 500
        if fC == 10: evalValue += 500

        #check if flag is under attacck
        directions = ((-1, -1), (1, 1), (1,-1), (-1, 1))
        for d in directions:
            row = fR + d[0]
            col = fC + d[1]
            if 0 <= row <= 10 and 0 <= col <= 10:
                if gameState.board[row][col] == "sP": evalValue = 500
        evalValue += 10 * gameState.goldFleet - 6 * gameState.silverFleet
        # print(evalValue)

        # flagship under attacck
        return evalValue

    def RandomAI(self, depth, validMoves, captureMoves):
        gameState = GameState.GameState()
        if len(captureMoves) != 0 and gameState.secondMove == 0:
            move = random.choice(captureMoves)
            return move
        else:
            return random.choice(validMoves)

    def nextAiMove(self, state):
        start_time = time.time()
        """get the next AI move"""
        self.visitedNode = 0
        print(">>AI calculating next move<<")
        gameState = deepcopy(state)
        score, move = self.miniMaxAlphaBeta(self.maxDepth, gameState, gameState.stillPlay, gameState.goldToMove,
                                                         float('-inf'), float('inf'))
        print("Evaluation with score:",score,"visited node:", self.visitedNode)
        timeSpent = time.time() - start_time
        self.timeRequired += timeSpent
        self.timeRequired = round(self.timeRequired, 2) #round to xx.xx seconds
        print(">>Ai spent %s s <<" % (round(timeSpent, 2)))
        return move

    def nextState(self, move, gameState):
        """return the new fake state after executing the test move"""
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
        hashKey = self.calculateHash(gameState)
        oldA = alpha  # save previous alpha
        oldB = beta
        self.visitedNode += 1
        n = self.retrieve(hashKey)  # check if it's a already seen state, -1 if not found
        if n != -1:
            if n[0] >= depth:
                if n[3] == "eX":
                    return n[1], n[2]
                elif n[3] == "lB":
                    alpha = max(alpha, n[1])
                elif n[3] == "uB":
                    beta = min(beta, n[1])
                if alpha >= beta:
                    return n[1], n[2]
        #leaf node
        if depth == 0 or not stillPlay:
            return self.evaluationFunction(gameState, gameState.goldToMove),""

        #getMoves for new state
        allMoves, captureMoves = gameState.getValidMoves()
        for move in captureMoves:
            allMoves.append(move)
        # random.shuffle(allMoves)

        #move ordering
        if self.moveOrdering:
            scoreList = []
            for action in allMoves:
                order_state = self.nextState(action, gameState)
                score = self.evaluationFunction(order_state, order_state.goldToMove)
                scoreList.append(score)
            sortedMoves = list(zip(scoreList, allMoves))
            if goldToMove:
                sortedMoves.sort(key=lambda mv: mv[0], reverse=True)
            else:
                sortedMoves.sort(key=lambda mv: mv[0], reverse=False)
            allMoves = [move for _, move in sortedMoves] #removes the score


        best_value = float('-inf') if goldToMove else float('inf')
        action_target = ""

        #Minimax
        for action in allMoves:
            new_gameState = self.nextState(action, gameState)
            eval_child, action_child = self.miniMaxAlphaBeta(depth - 1, new_gameState, new_gameState.stillPlay,
                                                             new_gameState.goldToMove, alpha, beta)

            #alpha-beta
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


        #TT storage
        if best_value <= oldA:
            flag = "uB"
        elif best_value >= oldB:
            flag = "lB"
        else:
            flag = "eX"
        hashKey = self.calculateHash(gameState)
        info = (depth, best_value, action_target, flag)
        self.store(hashKey, info)
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
        """check in the TT if the state already exists"""
        n = self.TT.get(hashKey)
        if n is not None:
            # print("exist hash stored")
            return n
        return -1

    def store(self, hashKey, info):
        """store the state inside the TT"""
        self.TT.setdefault(hashKey, info)

    """negaMax implementation"""
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
    #     # del new_gameState
    #     # print(action_target,action_child)
    #     return score, action_target
