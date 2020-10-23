"""
handle user input and display the State
"""
from pygame import font

import GameState
import pygame as p
import AIMiniMax

WIDTH = HEIGHT = 512
INFOWIDTH = 400
DIMENSION = 11
SQ_SIZE = HEIGHT // DIMENSION
LABEL = SQ_SIZE
MAX_FPS = 15
IMAGES = {}
MINMAX_DEPTH = 2


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
    screen = p.display.set_mode((WIDTH + LABEL + INFOWIDTH, HEIGHT + LABEL))  # Initializing screen
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gameState = GameState.GameState()
    validMoves, captureMoves = gameState.getValidMoves()

    # print(len(validMoves))
    moveMade = False  # flag for when we do a move
    print(gameState.board)
    loadImages()  # do it only once
    running = True
    sqSelected = ()  # tracks the last user's click (row,col)
    playerClicks = []  # track the clicks [(x,y),(x',y')]
    # initialize the AI
    AI = AIMiniMax.AI('g')
    AI.ControlGold = True
    AI2 = AIMiniMax.AI('g')
    AI2.ControlGold = False

    # messagebox part
    # window = Tk()
    # window.eval("tk::PlaceWindow %s center" % window.winfo_toplevel())
    # window.withdraw()
    monitor = True
    while running:
        requiredTime = AI.timeRequired
        drawGameState(screen, gameState, validMoves, captureMoves, sqSelected, requiredTime)
        if gameState.stillPlay:
            if gameState.turnCounter != 0:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False

                    elif gameState.goldToMove and AI.ControlGold and monitor:
                        monitor = False
                        move = AI.chooseMove(gameState)
                        print("GoldAI")
                        if move != "":
                            gameState.makeMove(move)
                        drawGameState(screen, gameState, validMoves, captureMoves, sqSelected, requiredTime)
                        moveMade = True
                        sqSelected = ()  # reset
                        playerClicks = []
                    # elif not gameState.goldToMove and not AI2.ControlGold and monitor:
                    #     monitor = False
                    #     print("\n Silver AI")
                    #     #     # AI.evaluationFunction(validMoves,captureMoves)
                    #     move = AI2.chooseMove(gameState)
                    #     # x, move = AI2.chooseMove(validMoves, captureMoves, gameState, True)
                    #     # move = AI.basicMiniMax(0, validMoves, captureMoves)
                    #     gameState.makeMove(move)
                    #     drawGameState(screen, gameState, validMoves, captureMoves, sqSelected, requiredTime)
                    #     moveMade = True
                    #     sqSelected = ()  # reset
                    #     playerClicks = []
                    elif e.type == p.MOUSEBUTTONDOWN and monitor:
                        location = p.mouse.get_pos()  # get x,y location of mouse
                        col = (location[0] - LABEL) // SQ_SIZE
                        row = (location[1] - LABEL) // SQ_SIZE
                        if col > 10 or row > 10:
                            sqSelected = ()
                            playerClicks = []
                            break
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
            drawGameState(screen, gameState, validMoves, captureMoves, sqSelected, requiredTime)
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
            drawGameState(screen, gameState, validMoves, captureMoves, sqSelected, requiredTime)
            screen.blit(text, textRect)
            # print("done")
            p.display.flip()
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
    p.quit()


"""higlights selected and possible moves"""


def highlightSquares(screen, gameState, moves, sqSelected, color):
    if sqSelected != ():
        r, c, = sqSelected
        if gameState.board[r][c][0] == (
                'g' if gameState.goldToMove else 's'):  # selected Square is a piece that can be moves
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent 255 solid
            s.fill(p.Color('green'))
            screen.blit(s, (c * SQ_SIZE + LABEL, r * SQ_SIZE + LABEL))
            # highliht moves from that square
            s.fill(color)
            for move in moves:
                if move.startRow == r and move.startCol == c:  # all the moves that belong to the pawn in r,c
                    screen.blit(s, (move.endCol * SQ_SIZE + LABEL, move.endRow * SQ_SIZE + LABEL))


"""graphics for the game"""


def drawGameState(screen, gameState, validMoves, captureMoves, sqSelected, time):
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, gameState.board, gameState.letters, gameState.numbers)  # draw pieces on top of squares
    drawHistory(screen, gameState.goldToMove, gameState.history, time)
    highlightSquares(screen, gameState, validMoves, sqSelected, p.Color("yellow"))
    highlightSquares(screen, gameState, captureMoves, sqSelected, p.Color("red"))


"""draw squares on the board"""


def drawBoard(screen):
    # colors = [p.Color("white"), p.Color("grey")]
    # for r in range(0, DIMENSION + 1):
    #     p.draw.rect(screen, p.Color("grey"), p.Rect(0, (r * SQ_SIZE), SQ_SIZE, SQ_SIZE), 2)
    #     # screen.blit(s, (0,r * SQ_SIZE))
    #     if r != 0:
    #         p.draw.rect(screen, p.Color("grey"), p.Rect((r * SQ_SIZE), 0, SQ_SIZE, SQ_SIZE), 2)
    #         # screen.blit(s, (r * SQ_SIZE, 0))

    color = p.Color("white")
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect((c * SQ_SIZE) + LABEL, (r * SQ_SIZE) + LABEL, SQ_SIZE, SQ_SIZE), 2)
    p.draw.rect(screen, color, p.Rect((WIDTH + LABEL + 50, SQ_SIZE + LABEL, 300, 512 - SQ_SIZE * 2)))


"""draw pieces on the board"""


def drawPieces(screen, board, letters, numbers):
    """draw letters"""
    # print(p.font.get_fonts())
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
        # screen.blit(text, p.Rect(r*SQ_SIZE,0, SQ_SIZE, SQ_SIZE))

        # screen.blit(text, p.Rect(5,r+1, SQ_SIZE, SQ_SIZE))
    "draw pieces"
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "-":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE + LABEL, r * SQ_SIZE + LABEL, SQ_SIZE, SQ_SIZE))


def drawHistory(screen, turn, history, time):
    # print(history[-9:])
    font = p.font.SysFont("rockwellgrassettocorsivo", 15)
    # if len(history)>13 and len(history)!=0:
    #     for i in range(1,13):
    #         text = font.render(history[len(history) - i-1], True, p.Color("black"), p.Color("white"))
    #         textRect = text.get_rect()
    #         textRect.center = (WIDTH + LABEL + 200, i * 30 + 105)
    #         screen.blit(text, textRect)
    turn = 'Gold' if turn else 'Silver'
    text = font.render("TURN: " + str(turn), True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (WIDTH + LABEL + 50, SQ_SIZE / 2 * 3)
    screen.blit(text, textRect)

    text = font.render("AI time spent: " + str(time), True, p.Color("blue"))
    textRect = text.get_rect()
    textRect.center = (WIDTH + LABEL * 3 + INFOWIDTH / 2, SQ_SIZE / 2 * 3)
    screen.blit(text, textRect)

    if len(history) != 0:
        for i in range(len(history)):
            text = font.render(history[len(history) - i - 1], True, p.Color("black"), p.Color("white"))
            textRect = text.get_rect()
            textRect.center = (WIDTH + LABEL + INFOWIDTH / 2, 512 - (i + 1) * 30)
            screen.blit(text, textRect)
            if i > 11:
                break


if __name__ == "__main__":
    main()
