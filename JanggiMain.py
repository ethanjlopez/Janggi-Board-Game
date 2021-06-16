"""
This is our main driver file. Responsible for handling user input and displaying the current GameState object.

"""
import pygame  as p
import JanggiEngine

HEIGHT = 704
WIDTH = 640
SQ_SIZE = 64
MAX_FPS = 15
IMAGES = {}


"""
Intialize a global dictionary of images. This will be called once in the main.
"""

def loadImages():
    pieces = ['RP', 'RC', 'RK', 'RR', 'RE', 'RH', 'RG', 'BP', 'BC', 'BK', 'BR', 'BE', 'BH', 'BG']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale((p.image.load("janggi_wooden/" + piece + ".svg")), (SQ_SIZE, SQ_SIZE))


"""
Main Driver. This will handle user input and updating graphics
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = JanggiEngine.JanggiGame()
    loadImages() #only once
    running = True
    sqSelected = () 
    playerClicks = [] # keeps track of player clicks (two tuples: [(6,4), (4,4)])
    moveLog = gs.get_move_log()
    while running:
        for e in p.event.get(): # go through these events 
            if e.type == p.QUIT:
                p.quit()
                running == False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = ((location[0]+30)//SQ_SIZE) - 1
                row = ((location[1]+30)//SQ_SIZE) - 1
                if sqSelected == (row,col): # if the user clicked the same square twice
                    sqSelected == () # deselect
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        animateBoard = gs.make_move(playerClicks[0], playerClicks[1])
                        if len(moveLog) != 0:
                            if animateBoard == True:
                                animateMove(moveLog[-1], screen, gs._board, clock)
                                animateBoard = False
                        gs.display()
                        sqSelected = ()
                        playerClicks = []
            #key handles
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when z is pressed
                    gs.undo_move()
                if e.key == p.K_r:
                    gs = JanggiEngine.JanggiGame()
                    sqSelected = ()
                    playerClicks = []
                    moveLog = gs.get_move_log()
                    animateBoard = False      
        drawGameState(screen, gs, gs.get_valid_moves(), sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip() # redraws the display
"""
Highlights square selected and moves for piece selected.
"""
def highlightSquares (screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs._board[r][c][0] == ('R' if gs.get_player_turn() == "RED" else 'B'): #sqSelected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('red'))
            screen.blit(s, (SQ_SIZE*c+30, SQ_SIZE*r+30))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move._startRow == r and move._startCol == c:
                    screen.blit(s, (move._endCol * SQ_SIZE + 30, move._endRow*SQ_SIZE + 30))

"""
Responsible for all graphics within the current game state.
"""

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #draw squares on the board
    # add in piece highlighting or move suggestions
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs._board)


"""
Draw the squares on the board.
"""
def drawBoard(screen):
    global colors
    for i in range(10):
        p.draw.rect(screen, "black", p.Rect(i*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.draw.rect(screen, "black", p.Rect(0*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.draw.rect(screen, "black", p.Rect(i*SQ_SIZE, 10*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.draw.rect(screen, "black", p.Rect(9*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    colors = [p.Color("#bf7c3d"), p.Color("#bf8d5e")]
    for r in range(1,10):
        for c in range(1, 9):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect((c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)))
            
    p.draw.line(screen, "black", (256,64), (384,192), width = 2)
    p.draw.line(screen, "black", (384, 64), (256,192), width = 2)
    p.draw.line(screen, "black", (256,640), (384,512), width = 2)
    p.draw.line(screen, "black", (384,640), (256,512), width = 2)

"""
Draw the pieces on the board using the current GameState.board
"""

def drawPieces(screen, board):
    for row in range(10):
        for col in range(9):
            piece = board[row][col]
            if piece != '--': # not an empty square
                screen.blit(IMAGES[piece], p.Rect(col*(SQ_SIZE) + 30, row *(SQ_SIZE) + 30, SQ_SIZE, SQ_SIZE))

    
"""
Animating a move
"""
def animateMove(move, screen, board, clock):
    global colors
    
    coords = [] #list of coords that the animation will move through
    dR = move._endRow - move._startRow
    dC = move._endCol - move._startCol
    framesPerSquare = 10  #frames to move on square
    frameCount = ((abs(dR) + abs(dC)) * framesPerSquare)
    for frame in range(frameCount + 1):
        r, c = (move._startRow + dR * frame/frameCount, move._startCol + dC  * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from it's ending square
        color = colors[(move._endRow + move._endCol) % 2]
        endSquare = p.Rect(move._endCol * SQ_SIZE+30, move._endRow * SQ_SIZE+30, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, "#4dcf36", endSquare)
        #draw captured piece onto rectangle
        if move._pieceCaptured != '--':
            screen.blit(IMAGES[move._pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move._pieceMoved], p.Rect(c*SQ_SIZE+30, r*SQ_SIZE+30, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()