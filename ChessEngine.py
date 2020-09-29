"""log of moves and info about the state of the game"""
import numpy as np


class GameState():
    def __init__(self):
        # "--" is used for empty spaces
        # sP stands for silver pawn and gP for gold pawn
        # gFS stands for gold flagship
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "sP", "sP", "sP", "sP", "sP", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "sP", "--", "--", "gP", "gP", "gP", "--", "--", "sP", "--"],
            ["--", "sP", "--", "gP", "--", "--", "--", "gP", "--", "sP", "--"],
            ["--", "sP", "--", "gP", "--", "gFS", "--", "gP", "--", "sP", "--"],
            ["--", "sP", "--", "gP", "--", "--", "--", "gP", "--", "sP", "--"],
            ["--", "sP", "--", "--", "gP", "gP", "gP", "--", "--", "sP", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "sP", "sP", "sP", "sP", "sP", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],

        ]
        self.whiteToMove = True
        self.moveLog = []
        self.turnCounter = 0
        self.secondMove = 0

    """take a move as a parameter and executes it"""

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # history and undo
        if move.pieceMoved[1] == 'F':
            self.secondMove += 1
        self.secondMove += 1
        if self.secondMove == 2:  # allows the double move to the small pawn
            self.whiteToMove = not self.whiteToMove
            self.turnCounter += 1
            self.secondMove = 0

    """undo previous move"""

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            # definire undo e change turn back if count==0
            if move.pieceMoved[1]=='F':
                self.secondMove = 0
                self.whiteToMove = not self.whiteToMove
            elif self.secondMove == 0:
                self.whiteToMove = not self.whiteToMove  # the turn back to the user
                self.turnCounter -= 1
                self.secondMove = 1
            elif self.secondMove == 1:
                self.secondMove = 0
            # TODO turn counter

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        # return self.getAllPossibleMoves()
        # oppMoves=self.getAllPossibleMoves() TODO check for checmate
        self.squareUnderAttack()
        return moves

    def getAllPossibleMoves(self):
        moves = []
        # if self.turnCounter==0:
        #     #decide to pass
        # else:
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns
                turn = self.board[r][c][0]
                if (turn == 'g' and self.whiteToMove) or (turn == 's' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        if self.secondMove == 1:
                            lastPiece = self.moveLog[-1]
                            if r != lastPiece.endRow or c != lastPiece.endCol:  # avoid 2-times moving of the same piece
                                self.getMoves(r, c, moves)
                        else:
                            self.getMoves(r, c, moves)
                    elif piece == 'F' and self.secondMove == 0:  # calculate Flagship moves only in the first step of
                        # the turn
                        self.getMoves(r, c, moves)
        return moves

    def squareUnderAttack(self):
        pass

    def getMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 10):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 10 and 0 <= endCol <= 10:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        break
                else:
                    break
        enemy = 's' if self.whiteToMove else 'g' #check who is the enemy
        # possible captures
        if self.secondMove == 0:  # it's possible to eat only in the first move of the turn
            for i in range(0, 2):
                newCol = c-1 if i == 0 else c+1  # c-1 -> left | c+1 -> right
                if newCol >= 0:
                    if r-1 >= 0:  # top
                        if self.board[r - 1][newCol][0] == enemy:
                            moves.append(Move((r, c), (r - 1, newCol), self.board))
                    if r+1 <= 10:  # bottom
                        if self.board[r + 1][newCol][0] == enemy:
                            moves.append(Move((r, c), (r + 1, newCol), self.board))



class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 10, "2": 9, "3": 8, "4": 7, "5": 6, "6": 5, "7": 4, "8": 3, "9": 2, "10": 1, "11": 0}
    rowToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, statSq, endSq, board):
        self.startRow = int(statSq[0])
        self.startCol = int(statSq[1])
        self.endRow = int(endSq[0])
        self.endCol = int(endSq[1])
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 100000 + self.startCol * 1000 + self.endRow * 10 + self.endCol

    """
    Override equals method"""

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]
