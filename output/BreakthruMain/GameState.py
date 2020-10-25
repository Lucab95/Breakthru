"""log of moves and info about the state of the game"""
import random
import pygame
from Move import Move
DEBUG = True


class GameState:
    def __init__(self):
        # "-" is used for empty spaces
        # sP stands for silver pawn and gP for gold pawn
        # gFS stands for gold flagship
        # self.board = np.array([
        #     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        #     ["-", "-", "-", "sP", "sP", "sP", "sP", "sP", "-", "-", "-"],
        #     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        #     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        #     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        #     ["-", "-", "-", "-", "-", "gFS", "-", "-", "-", "-", "-"],
        #     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        #     ["-", "-", "-", "-", "-", "-", "-", "gP", "gP", "-", "-"],
        #     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        #     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        #     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        #     ]
        # )
        self.board = ([
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "sP", "sP", "sP", "sP", "sP", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "sP", "-", "-", "gP", "gP", "gP", "-", "-", "sP", "-"],
            ["-", "sP", "-", "gP", "-", "-", "-", "gP", "-", "sP", "-"],
            ["-", "sP", "-", "gP", "-", "gFS", "-", "gP", "-", "sP", "-"],
            ["-", "sP", "-", "gP", "-", "-", "-", "gP", "-", "sP", "-"],
            ["-", "sP", "-", "-", "gP", "gP", "gP", "-", "-", "sP", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "sP", "sP", "sP", "sP", "sP", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
            ]
        )
        self.letters = (["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"])
        self.numbers = (["11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"])
        self.goldToMove = True
        self.moveLog = []
        self.turnCounter = 0
        self.secondMove = 0
        self.pieceCaptured = []
        self.silverFleet = 20
        self.goldFleet = 12
        self.flagShip = 1
        self.flagShipWinningMoves = []
        self.history = []
        self.flagShipPosition = (5,5)
        # TODO decide the state using a function and check evaluation not in move
        self.stillPlay = True  # used to define the gameState True -> game False-> end game
        self.win = "Gold"
        self.DEBUG = True

    """take a move as a parameter and executes it, include capture option"""

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "-"
        turn = 'Gold' if self.goldToMove else 'Silver'
        eR=move.endRow
        eC=move.endCol
        if move.pieceMoved == 'gFS':
            self.flagShipPosition = (eR, eC)
            if (eR == 0 or eR == 10) or (eC == 10 or eC == 0) :
                self.win = "Flag escaped, Gold"
                print("escaped")
                self.stillPlay = False
                print("Gold escaped")
        if self.DEBUG:
            if move.pieceCaptured == "-":
                print(move.pieceMoved, move.getNotation() + "  " + str(self.secondMove), self.goldToMove)
                self.history.append(turn + " move: " + move.pieceMoved + " " + move.getNotation())
                if move.pieceMoved == 'gFS':
                    if (move.endCol == 10 or move.endCol == 0) or (move.endRow == 0 or move.endRow == 10):
                        self.win = "Flag escaped, Gold"
                        print("escaped")
                        self.stillPlay = False
                        print("Gold escaped")
            else:
                print(move.pieceMoved, move.getNotation() + "  " + str(self.secondMove), self.goldToMove, "captured",
                      move.pieceCaptured)
                self.history.append(
                    turn + " captured " + move.pieceCaptured + " move: " + move.pieceMoved + " " + move.getNotation())
        self.moveCost(move)

        #text for endGame and endGame condition
        if self.silverFleet == 0:
            self.stillPlay = False;
            self.win = "Gold"
        if self.flagShip == 0:
            self.stillPlay = False
            self.win = "Flag captured, Silver"

        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # history and undo
        if self.secondMove == 2:
            self.changeTurn()


    def moveCost(self, move):
        if move.pieceCaptured != "-":
            self.secondMove = 2
            self.pieceCaptured.append(move.pieceCaptured)
            if move.pieceCaptured == 'gFS':
                self.flagShip = 0
            elif move.pieceCaptured[0] == 'g':
                self.goldFleet -= 1
            else:
                self.silverFleet -= 1
        elif move.pieceMoved[1] == "F":
            self.secondMove = 2
        else:
            self.secondMove += 1

    def changeTurn(self):
        """gives the turn to the other player and add a turn to the counter"""
        self.goldToMove = not self.goldToMove
        self.turnCounter += 1
        self.secondMove = 0

    """undo previous move"""

    def undoMove(self):  # fixme RIVEDERE
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            if move.pieceMoved[1] == 'F':
                self.secondMove = 0
                self.goldToMove = not self.goldToMove
            elif self.secondMove == 0:
                self.goldToMove = not self.goldToMove  # gives the turn back to the user
                self.turnCounter -= 1
                self.secondMove = 1
            elif self.secondMove == 1:
                self.secondMove = 0

    def getValidMoves(self):
        moves, capture = self.getAllPossibleMoves()
        return moves, capture

    def getAllPossibleMoves(self):
        moves = []
        capture = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[0])):  # number of columns
                turn = self.board[r][c][0]
                if (turn == 'g' and self.goldToMove) or (turn == 's' and not self.goldToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        if self.secondMove == 1:
                            lastPiece = self.moveLog[-1]
                            if r != lastPiece.endRow or c != lastPiece.endCol:  # avoid 2-times moving of the same piece
                                self.getMoves(r, c, moves)
                        else:
                            self.getMoves(r, c, moves)
                            self.getCaptureMoves(r, c, capture)
                    elif piece == 'F' and self.secondMove == 0:  # calculate Flagship moves only in the first part of the turn

                        diffmo = self.getMoves(r, c, moves)
                        diffca = self.getCaptureMoves(r, c, capture)

        return moves, capture


    def getMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        before = len(moves)
        for d in directions:
            for i in range(1, 11):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 10 and 0 <= endCol <= 10:
                    endPiece = self.board[endRow][endCol]

                    if endPiece == "-":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        break
                else:
                    break
        return len(moves) - before

    def getCaptureMoves(self, r, c, capture):
        before = len(capture)
        enemy = 's' if self.goldToMove else 'g'  # check who is the enemy
        # possible captures
        if self.secondMove == 0:  # it's possible to eat only in the first move of the turn
            for i in range(0, 2):
                newCol = c - 1 if i == 0 else c + 1  # c-1 -> left | c+1 -> right
                if 0 <= newCol <= 10:
                    if r - 1 >= 0:  # top
                        if self.board[r - 1][newCol][0] == enemy:
                            capture.append(Move((r, c), (r - 1, newCol), self.board))
                    if r + 1 <= 10:  # bottom
                        if self.board[r + 1][newCol][0] == enemy:
                            capture.append(Move((r, c), (r + 1, newCol), self.board))
        return len(capture) - before
