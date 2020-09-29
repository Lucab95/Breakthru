"""log of moves and info about the state of the game"""
import numpy as np



class GameState():
    def __init__(self):
        #"--" is used for empty spaces
        #sP stands for silver pawn and gP for gold pawn
        #gFS stands for gold flagship
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
        self.turncounter = 0

    """take a move as a parameter and executes it"""
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #history and undo
        self.whiteToMove = not self.whiteToMove

    """undo previous move"""
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #gives the turn back to the user
            #TODO turn counter

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        # return self.getAllPossibleMoves()
        # oppMoves=self.getAllPossibleMoves() TODO check for checmate
        self.squareUnderAttack()
        return moves


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of columns
                turn = self.board[r][c][0]
                if (turn == 'g' and self.whiteToMove) or( turn=='s' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r,c,moves)
                    else:
                        self.getFlagMoves(r,c,moves)
        return moves

    def squareUnderAttack(self):
        pass

    def getPawnMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0,1))
        for d in directions:
            for i in range(1,10):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <=endRow <=10 and 0 <= endCol <=10:
                    endPiece = self.board[endRow][endCol]
                    if endPiece =="--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    else:
                        break
                else:
                    break

    def getFlagMoves(self, r, c, moves):
        pass


class Move():

    #maps keys to values
    #key : value

    ranksToRows = {"1": 10, "2": 9, "3": 8, "4": 7, "5": 6, "6": 5, "7": 4, "8": 3, "9": 2, "10": 1, "11": 0}
    rowToRanks  = {v: k for k,v in ranksToRows.items()}
    filesToCols = { "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__ (self, statSq, endSq, board):
        self.startRow = int(statSq[0])
        self.startCol = int(statSq[1])
        self.endRow = int(endSq[0])
        self.endCol = int(endSq[1])
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow *100000 + self.startCol*1000 + self.endRow*10 + self.endCol

    """
    Override equals method"""
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    def getNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]