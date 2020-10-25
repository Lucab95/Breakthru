"""
handle user input and display the State
"""
from pygame import font

import GameState
import pygame as p
import AIModel
from Move import Move
import sys

WIDTH = HEIGHT = 512
INFOWIDTH = 400
DIMENSION = 11
SQ_SIZE = HEIGHT // DIMENSION
LABEL = SQ_SIZE
MAX_FPS = 15
IMAGES = {}
maxDepth = 3
moveOrdering = False



def main():
    p.init()
    screen = p.display.set_mode((WIDTH + LABEL + INFOWIDTH, HEIGHT + LABEL))  # Initializing screen
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gameState = GameState.GameState()
    validMoves, captureMoves = gameState.getValidMoves()


    moveMade = False  # flag used to calculate the next move
    print(gameState.board)
    loadImages()
    running = True
    runningMenu = True
    clickedSQ = ()  # tracks the last user's click (row,col)
    playerClicks = []  # track the clicks [(x,y),(x',y')]

    # initialize the AI Object
    AI = AIModel.AI(maxDepth,moveOrdering)
    AI.ControlGold = 0
    AITurn = True

    while runningMenu:
        pos = drawMenu(screen)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # get x,y location of mouse
                if pos[0].collidepoint(location):
                    AI.ControlGold = 0
                    runningMenu = False
                elif pos[1].collidepoint(location):
                    AI.ControlGold = 1
                    runningMenu =False
                elif pos[2].collidepoint(location):
                    AI.ControlGold = 2
                    runningMenu =False
        screen.fill(p.Color("black"))
        drawMenu(screen)
        clock.tick(MAX_FPS)
        p.display.flip()


    while running:
        requiredTime = AI.timeRequired
        drawGameState(screen, gameState, validMoves, captureMoves, clickedSQ, requiredTime)
        if gameState.stillPlay:
            if gameState.turnCounter != 0:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif gameState.goldToMove and AI.ControlGold == 1 and AITurn:
                        AITurn = False
                        move = AI.nextAiMove(gameState)
                        if move != "":
                            gameState.makeMove(move)
                        drawGameState(screen, gameState, validMoves, captureMoves, clickedSQ, requiredTime)
                        moveMade = True
                        clickedSQ = ()  # reset
                        playerClicks = []
                    elif not gameState.goldToMove and AI.ControlGold == 2 and AITurn:
                        AITurn = False
                        move = AI.nextAiMove(gameState)
                        if move != "":
                            gameState.makeMove(move)
                        drawGameState(screen, gameState, validMoves, captureMoves, clickedSQ, requiredTime)
                        moveMade = True
                        clickedSQ = ()  # reset
                        playerClicks = []
                    elif e.type == p.MOUSEBUTTONDOWN and AITurn:
                        location = p.mouse.get_pos()  # get x,y location of mouse
                        col = (location[0] - LABEL) // SQ_SIZE
                        row = (location[1] - LABEL) // SQ_SIZE

                        if col > 10 or row > 10: #avoid problem when clicking outside of the board
                            clickedSQ = ()
                            playerClicks = []
                            break

                        if clickedSQ == (row, col):  # double click on the same one -> clear
                            clickedSQ = ()
                            playerClicks = []
                        else:
                            clickedSQ = (row, col)
                            playerClicks.append(clickedSQ)  # append first and second clicks

                        if len(playerClicks) == 2:  # 2nd click case
                            move = Move(playerClicks[0], playerClicks[1], gameState.board)
                            if len(captureMoves) == 0 and len(validMoves) == 0:
                                print("staleMate")
                            if move in validMoves:
                                gameState.makeMove(move)
                                moveMade = True
                                clickedSQ = ()  # reset
                                playerClicks = []
                            elif move in captureMoves:
                                gameState.makeMove(move)
                                moveMade = True
                                clickedSQ = ()  # reset
                                playerClicks = []
                            else:
                                playerClicks = [clickedSQ]  # second click and avoid problem when i click black squares

                    #perform the undo of the move
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_z:
                            gameState.undoMove()
                            moveMade = True

                if moveMade:  # calculate new moves only after a move was made
                    validMoves, captureMoves = gameState.getValidMoves()
                    AITurn = True #used to align
                    moveMade = False
            screen.fill(p.Color("black"))
            drawGameState(screen, gameState, validMoves, captureMoves, clickedSQ, requiredTime)
            clock.tick(MAX_FPS)
            p.display.flip()
            if gameState.turnCounter == 0:
                # p.time.wait(1500)
                gameState.turnCounter = 1
        else:
            font = p.font.SysFont("calibri", 32)
            text = font.render(gameState.win + " player won", True, p.Color("red"), p.Color("black"))
            textRect = text.get_rect()
            textRect.center = ((WIDTH + LABEL + INFOWIDTH) / 2, HEIGHT / 2)
            drawGameState(screen, gameState, validMoves, captureMoves, clickedSQ, requiredTime)
            screen.blit(text, textRect)
            # print("done")
            p.display.flip()
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
    p.quit()




def drawMenu(screen):
    center = p.display.get_surface().get_size()[0]/2 -LABEL*2
    font = p.font.SysFont("rockwellgrassettocorsivo", 40)
    text = font.render("BreakThru", True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (WIDTH-25, SQ_SIZE*1)
    screen.blit(text, textRect)
    font = p.font.SysFont("rockwellgrassettocorsivo", 20)
    pos1 = p.draw.rect(screen, p.Color("white"), p.Rect(center, (2 * SQ_SIZE), 200, 75), 2)
    text = font.render("Player vs Player", True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (pos1[0]+100, pos1[1]+35)
    screen.blit(text, textRect)
    pos2 = p.draw.rect(screen, p.Color("white"), p.Rect(center, (5 * SQ_SIZE), 200, 75), 2)
    text = font.render("AI vs Player", True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (pos2[0]+100, pos2[1]+35)
    screen.blit(text, textRect)
    pos3 = p.draw.rect(screen, p.Color("white"), p.Rect(center, (8 * SQ_SIZE), 200, 75), 2)
    text = font.render("Player vs AI", True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (pos3[0]+100, pos3[1]+35)
    screen.blit(text, textRect)
    return pos1,pos2,pos3




def drawGameState(screen, gameState, validMoves, captureMoves, sqSelected, time):
    """graphics for the game"""
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, gameState.board, gameState.letters, gameState.numbers)  # draw pieces on top of squares
    drawHistory(screen, gameState.goldToMove, gameState.history, time)
    highlightSquares(screen, gameState, validMoves, sqSelected, p.Color("yellow"))
    highlightSquares(screen, gameState, captureMoves, sqSelected, p.Color("red"))



def drawBoard(screen):
    """draw squares on the board"""

    color = p.Color("white")
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            p.draw.rect(screen, color, p.Rect((c * SQ_SIZE) + LABEL, (r * SQ_SIZE) + LABEL, SQ_SIZE, SQ_SIZE), 2)
    p.draw.rect(screen, color, p.Rect((WIDTH + LABEL + 50, SQ_SIZE + LABEL, 300, 512 - SQ_SIZE * 2)))


"""draw pieces on the board"""
def drawPieces(screen, board, letters, numbers):
    """draw letters on board"""

    font = p.font.SysFont("rockwellgrassettocorsivo", 28)
    half = SQ_SIZE / 2
    for r in range(1, DIMENSION + 1):
        text = font.render(letters[r - 1], True, p.Color("blue"), p.Color("black"))
        textRect = text.get_rect()
        textRect.center = (r * SQ_SIZE + half, half)
        screen.blit(text, textRect)
        text = font.render(numbers[r - 1], True, p.Color("blue"), p.Color("black"))
        textRect = text.get_rect()
        textRect.center = (half, r * SQ_SIZE + half)
        screen.blit(text, textRect)

    """draw pieces/sprites on board"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "-":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE + LABEL, r * SQ_SIZE + LABEL, SQ_SIZE, SQ_SIZE))


def drawHistory(screen, turn, history, time):
    """draw the last 12 moves on the right label"""

    font = p.font.SysFont("rockwellgrassettocorsivo", 15)
    turn = 'Gold' if turn else 'Silver'
    text = font.render("TURN: " + str(turn), True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (WIDTH + LABEL + 50, SQ_SIZE / 2 * 3)
    screen.blit(text, textRect)
    text = font.render("AI time spent: " + str(time), True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (WIDTH + LABEL * 3 + INFOWIDTH / 2, SQ_SIZE / 2 * 3)
    screen.blit(text, textRect)

    #if there is history, print it
    if len(history) != 0:
        for i in range(len(history)):
            text = font.render(history[len(history) - i - 1], True, p.Color("black"), p.Color("white"))
            textRect = text.get_rect()
            textRect.center = (WIDTH + LABEL + INFOWIDTH / 2, 512 - (i + 1) * 30)
            screen.blit(text, textRect)
            if i > 11:
                break

def loadImages():
    pieces = ["gP", "sP", "gFS"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gameState, moves, sqSelected, color):
    """higlights selected piece possible moves"""
    if sqSelected != ():
        r, c, = sqSelected
        if gameState.board[r][c][0] == (
                'g' if gameState.goldToMove else 's'):  # selected Square is a piece that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('green'))
            screen.blit(s, (c * SQ_SIZE + LABEL, r * SQ_SIZE + LABEL))
            s.fill(color)
            for move in moves:
                if move.startRow == r and move.startCol == c:  # all the moves that belong to the pawn in r,c
                    screen.blit(s, (move.endCol * SQ_SIZE + LABEL, move.endRow * SQ_SIZE + LABEL))

if __name__ == "__main__":
    main()
