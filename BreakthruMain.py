"""
handle user input and display the State
"""
import GameState
import pygame as p
# from tkinter import *
# from tkinter import messagebox
import AIMiniMax
import time
import sys
import os

WIDTH = HEIGHT = 512
DIMENSION = 11
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
MINMAX_DEPTH = 3


def loadImages():
    pieces = ["gP", "sP", "gFS"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""draw condition"""


# def staleMate(window):
#     messagebox.showinfo("Draw", "No possible moves")
#     window.deiconify()
#     window.destroy()
#     window.quit()
#     return True


def main():
    # if getattr(sys, 'frozen', False):
    #     os.chdir(sys._MEIPASS)
    p.init()  # Initializing library
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Initializing screen
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gameState = GameState.GameState()
    validMoves, captureMoves = gameState.getValidMoves()
    print(len(validMoves))
    moveMade = False  # flag for when we do a move
    print(gameState.board)
    loadImages()  # do it only once
    running = True
    sqSelected = ()  # tracks the last user's click (row,col)
    playerClicks = []  # track the clicks [(x,y),(x',y')]
    # initialize the AI
    AI = AIMiniMax.AI('g')
    AI2 = AIMiniMax.AI('g')
    AI2.ControlGold = False
    # messagebox part
    # window = Tk()
    # window.eval("tk::PlaceWindow %s center" % window.winfo_toplevel())
    # window.withdraw()
    monitor = True
    while running:
        drawGameState(screen, gameState, validMoves, captureMoves, sqSelected)
        if gameState.turnCounter !=0:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif not gameState.state:
                    return
                elif gameState.goldToMove and AI.ControlGold and monitor :
                    monitor = False
                    # #     # AI.evaluationFunction(validMoves,captureMoves)
                    move = AI.chooseMove(gameState, True)
                    # print("move: ", move)
                    print("AI1")
                    # move = AI.basicMiniMax(0, validMoves, captureMoves)
                    # print("moveee gold", gameState.goldToMove)
                    # #     print("Ai", gameState.secondMove, "movegold", gameState.goldToMove)
                    # #     # print(dict(map(reversed, enumerate(validMoves))))
                    # #     # print(dict(zip(range(len(validMoves)),validMoves)))
                    # #     # print(dict(captureMoves[i:i + 2] for i in range(0, len(captureMoves), 2)))
                    # #     gameState.makeMove(move, window)
                    # #     moveMade = True
                    # #     sqSelected = ()  # reset
                    # #     playerClicks = []
                    #     x, move = AI.chooseMove(validMoves, captureMoves, gameState, True)
                    gameState.makeMove(move)
                    moveMade = True
                    sqSelected = ()  # reset
                    playerClicks = []
                elif gameState.goldToMove == False and AI2.ControlGold == False and monitor:
                    monitor = False
                    print("\n aI2")
                    #     # AI.evaluationFunction(validMoves,captureMoves)
                    move = AI2.chooseMove(gameState, True)
                    # x, move = AI2.chooseMove(validMoves, captureMoves, gameState, True)
                    # move = AI.basicMiniMax(0, validMoves, captureMoves)
                    gameState.makeMove(move)
                    moveMade = True
                    sqSelected = ()  # reset
                    playerClicks = []
                elif e.type == p.MOUSEBUTTONDOWN and monitor and monitor:
                    location = p.mouse.get_pos()  # get x,y location of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    # print("clicked row", row, "col", col)
                    if sqSelected == (row, col):  # double click on the same one -> clear
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append first and second clicks
                    if len(playerClicks) == 2:  # 2nd click case
                        # print(gameState.secondMove)
                        move = GameState.Move(playerClicks[0], playerClicks[1], gameState.board)
                        if len(captureMoves) == 0 and len(validMoves) == 0:
                            # staleMate(window)
                            print("staleMate")
                        if move in validMoves:
                            gameState.makeMove(move)
                            moveMade = True
                            sqSelected = ()  # reset
                            playerClicks = []
                        elif move in captureMoves:
                            gameState.makeMove(move)
                            moveMade = True
                            sqSelected = ()  # reset
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]  # second click and avoid problem when i click black squares
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        gameState.undoMove()
                        moveMade = True

            if moveMade:  # calculate new moves only after a move was made
                validMoves, captureMoves = gameState.getValidMoves()
                monitor = True
                moveMade = False
        screen.fill(p.Color("black"))
        drawGameState(screen, gameState, validMoves, captureMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
        if gameState.turnCounter==0:
            p.time.wait(1500)
            gameState.turnCounter=1
    p.quit()


"""higlights selected and possible moves"""


def highlightSquares(screen, gameState, validMoves, sqSelected, color):
    if sqSelected != ():
        r, c, = sqSelected
        if gameState.board[r][c][0] == (
                'g' if gameState.goldToMove else 's'):  # selected Square is a piece that can be moves
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent 255 solid
            s.fill(p.Color('green'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highliht moves from that square
            s.fill(color)
            for move in validMoves:
                if move.startRow == r and move.startCol == c:  # all the moves that belong to the pawn in r,c
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


"""graphics for the game"""


def drawGameState(screen, gameState, validMoves, captureMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, gameState.board)  # draw pieces on top of squares
    highlightSquares(screen, gameState, validMoves, sqSelected, p.Color("yellow"))
    highlightSquares(screen, gameState, captureMoves, sqSelected, p.Color("red"))


"""draw squares on the board"""


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)


"""draw pieces on the board"""


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "-":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
