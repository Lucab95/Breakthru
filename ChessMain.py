"""
handle user input and display the State
"""
import ChessEngine
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 11
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["gP", "sP","gFS"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))






def main():
    p.init()  # Initializing library
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Initializing screen
    clock = p.time.Clock()
    # p.display.flip()
    screen.fill(p.Color("black"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag for when we do a move
    print(gs.board)
    loadImages()#do it only once
    running = True
    sqSelected = () #tracks the last user's click (row,col)
    playerClicks = [] #track the clicks [(x,y),(x',y')]



    while running:
        drawGameState(screen, gs,validMoves,sqSelected)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # get x,y location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                print("clicked row",row,"col",col)

                if sqSelected == (row, col):  # double click on the same one -> clear
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append first and second clicks
                if len(playerClicks)==2: #2nd click case
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #reset
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected] #second click and avoid problem when i click black squares
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade: #calculate new moves only after a move was made
            validMoves = gs.getValidMoves()
            moveMade = False
        screen.fill(p.Color("black"))
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()

"""higlights selected and possible moves"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c, = sqSelected
        if gs.board[r][c][0] == ('g' if gs.whiteToMove else 's'): #selected Square is a piece that can be moves
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #transparency value -> 0 transparent 255 solid
            s.fill(p.Color('green'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highliht moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:#all the moves that belong to the pawn in r,c
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

"""graphics for the game"""

def drawGameState(screen, gs,validMoves,sqSelected):
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board)#draw pieces on top of squares
    highlightSquares(screen, gs, validMoves, sqSelected)


"""draw squares on the board"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE),2)
1
"""draw pieces on the board"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                # print("pedina  " + )
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()