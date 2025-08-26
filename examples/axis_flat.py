# flippy.py - Flippy (Othello/Reversi) with Minecraft integration
# Python 3.x, pygame-ce, mc_remote

import random, sys, pygame, copy, time
from pygame.locals import *
from mc_remote.minecraft import Minecraft
from param_mc_remote import PLAYER_ORIGIN, block, ADRS_MCR, PORT_MCR

# ------------------ Minecraft setup ------------------
mc = Minecraft.create(address=ADRS_MCR, port=PORT_MCR)

MC_X = 2000  # 原点X
MC_Y = 100   # 原点Y
MC_Z = 2000  # 原点Z

MC_WHITE_BLOCK = block.CHERRY_LOG
MC_BLACK_BLOCK = block.OAK_LOG

# ------------------ Flippy parameters ------------------
FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
SPACESIZE = 50
BOARDWIDTH = 8
BOARDHEIGHT = 8
WHITE_TILE = 'WHITE_TILE'
BLACK_TILE = 'BLACK_TILE'
EMPTY_SPACE = 'EMPTY_SPACE'
HINT_TILE = 'HINT_TILE'
ANIMATIONSPEED = 25

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 50, 255)
BROWN = (174, 94, 0)
TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN

# ------------------ Main function ------------------
def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE
    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Flippy')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    # Load images
    boardImage = pygame.image.load('flippyboard.png')
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH*SPACESIZE, BOARDHEIGHT*SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)
    BGIMAGE = pygame.image.load('flippybackground.png')
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    while True:
        if runGame() == False:
            break

# ------------------ Game loop ------------------
def runGame():
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    showHints = False
    turn = random.choice(['computer','player'])
    drawBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()

    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH-8, 10)
    hintsSurf = FONT.render('Hints', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (WINDOWWIDTH-8, 40)

    while True:
        if turn == 'player':
            if getValidMoves(mainBoard, playerTile) == []:
                break
            movexy = None
            while movexy == None:
                boardToDraw = getBoardWithValidMoves(mainBoard, playerTile) if showHints else mainBoard
                checkForQuit()
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint((mousex, mousey)):
                            return True
                        elif hintsRect.collidepoint((mousex, mousey)):
                            showHints = not showHints
                        movexy = getSpaceClicked(mousex, mousey)
                        if movexy != None and not isValidMove(mainBoard, playerTile, movexy[0], movexy[1]):
                            movexy = None
                drawBoard(boardToDraw)
                drawInfo(boardToDraw, playerTile, computerTile, turn)
                DISPLAYSURF.blit(newGameSurf,newGameRect)
                DISPLAYSURF.blit(hintsSurf,hintsRect)
                MAINCLOCK.tick(FPS)
                pygame.display.update()

            makeMove(mainBoard, playerTile, movexy[0], movexy[1], True)
            if getValidMoves(mainBoard, computerTile) != []:
                turn = 'computer'
        else:
            if getValidMoves(mainBoard, computerTile) == []:
                break
            drawBoard(mainBoard)
            drawInfo(mainBoard, playerTile, computerTile, turn)
            DISPLAYSURF.blit(newGameSurf,newGameRect)
            DISPLAYSURF.blit(hintsSurf,hintsRect)
            pauseUntil = time.time() + random.randint(5,15)*0.1
            while time.time() < pauseUntil:
                pygame.display.update()
            x,y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y, True)
            if getValidMoves(mainBoard, playerTile) != []:
                turn = 'player'

    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    if scores[playerTile] > scores[computerTile]:
        text = f'You beat the computer by {scores[playerTile]-scores[computerTile]} points!'
    elif scores[playerTile] < scores[computerTile]:
        text = f'You lost. Computer beat you by {scores[computerTile]-scores[playerTile]} points.'
    else:
        text = 'The game was a tie!'

    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2))
    DISPLAYSURF.blit(textSurf, textRect)

    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)+50)

    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH/2)-60,int(WINDOWHEIGHT/2)+90)
    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH/2)+60,int(WINDOWHEIGHT/2)+90)

    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint((mousex,mousey)):
                    return True
                elif noRect.collidepoint((mousex,mousey)):
                    return False
        DISPLAYSURF.blit(textSurf,textRect)
        DISPLAYSURF.blit(text2Surf,text2Rect)
        DISPLAYSURF.blit(yesSurf,yesRect)
        DISPLAYSURF.blit(noSurf,noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

# ------------------ Minecraft integration ------------------
def setBlockInMinecraft(boardX, boardY, tile):
    mcX = MC_X + boardX
    mcY = MC_Y
    mcZ = MC_Z + boardY
    if tile == WHITE_TILE:
        mcBlock = MC_WHITE_BLOCK
    elif tile == BLACK_TILE:
        mcBlock = MC_BLACK_BLOCK
    else:
        return
    mc.setBlock(mcX, mcY, mcZ, mcBlock)
    print(f"Placed {mcBlock} at ({mcX},{mcY},{mcZ})")

def makeMove(board, tile, xstart, ystart, realMove=False):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))
        setBlockInMinecraft(xstart, ystart, tile)
        for x, y in tilesToFlip:
            setBlockInMinecraft(x, y, tile)
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def resetBoard(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            board[x][y] = EMPTY_SPACE
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[4][4] = WHITE_TILE
    setBlockInMinecraft(3,3,WHITE_TILE)
    setBlockInMinecraft(3,4,BLACK_TILE)
    setBlockInMinecraft(4,3,BLACK_TILE)
    setBlockInMinecraft(4,4,WHITE_TILE)

# ------------------ Flippy helper functions ------------------
def translateBoardToPixelCoord(x, y):
    return XMARGIN + x*SPACESIZE + int(SPACESIZE/2), YMARGIN + y*SPACESIZE + int(SPACESIZE/2)

def animateTileChange(tilesToFlip, tileColor, additionalTile):
    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE/2)-4)
    pygame.display.update()
    for rgbValues in range(0, 255, int(ANIMATIONSPEED*2.55)):
        if rgbValues > 255:
            rgbValues = 255
        if tileColor == WHITE_TILE:
            color = (rgbValues,rgbValues,rgbValues)
        else:
            color = (255-rgbValues,255-rgbValues,255-rgbValues)
        for x,y in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(x,y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx,centery), int(SPACESIZE/2)-4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()

def drawBoard(board):
    DISPLAYSURF.blit(BGIMAGE,BGIMAGE.get_rect())
    for x in range(BOARDWIDTH+1):
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (XMARGIN+x*SPACESIZE,YMARGIN), (XMARGIN+x*SPACESIZE,YMARGIN+BOARDHEIGHT*SPACESIZE))
    for y in range(BOARDHEIGHT+1):
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (XMARGIN,YMARGIN+y*SPACESIZE), (XMARGIN+BOARDWIDTH*SPACESIZE,YMARGIN+y*SPACESIZE))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x,y)
            if board[x][y]==WHITE_TILE:
                pygame.draw.circle(DISPLAYSURF,WHITE,(centerx,centery),int(SPACESIZE/2)-4)
            elif board[x][y]==BLACK_TILE:
                pygame.draw.circle(DISPLAYSURF,BLACK,(centerx,centery),int(SPACESIZE/2)-4)
            elif board[x][y]==HINT_TILE:
                pygame.draw.rect(DISPLAYSURF,HINTCOLOR,(centerx-4,centery-4,8,8))

def getSpaceClicked(mousex, mousey):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if XMARGIN + x*SPACESIZE < mousex < XMARGIN + (x+1)*SPACESIZE and \
               YMARGIN + y*SPACESIZE < mousey < YMARGIN + (y+1)*SPACESIZE:
                return (x,y)
    return None

def drawInfo(board, playerTile, computerTile, turn):
    scores = getScoreOfBoard(board)
    scoreSurf = FONT.render(f"Player Score: {scores[playerTile]}  Computer Score: {scores[computerTile]}  {turn.title()}'s Turn", True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10,WINDOWHEIGHT-5)
    DISPLAYSURF.blit(scoreSurf,scoreRect)

def getNewBoard():
    return [[EMPTY_SPACE]*BOARDHEIGHT for _ in range(BOARDWIDTH)]

def isOnBoard(x,y):
    return 0<=x<BOARDWIDTH and 0<=y<BOARDHEIGHT

def isValidMove(board,tile,xstart,ystart):
    if not isOnBoard(xstart,ystart) or board[xstart][ystart]!=EMPTY_SPACE:
        return False
    board[xstart][ystart]=tile
    otherTile = BLACK_TILE if tile==WHITE_TILE else WHITE_TILE
    tilesToFlip=[]
    for xdir,ydir in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x,y=xstart+ xdir, ystart+ ydir
        if isOnBoard(x,y) and board[x][y]==otherTile:
            while True:
                x+=xdir
                y+=ydir
                if not isOnBoard(x,y):
                    break
                if board[x][y]==EMPTY_SPACE:
                    break
                if board[x][y]==tile:
                    while True:
                        x-=xdir
                        y-=ydir
                        if x==xstart and y==ystart:
                            break
                        tilesToFlip.append((x,y))
                    break
    board[xstart][ystart]=EMPTY_SPACE
    return tilesToFlip if len(tilesToFlip)>0 else False

def getBoardWithValidMoves(board,tile):
    dupeBoard=copy.deepcopy(board)
    for x,y in getValidMoves(dupeBoard,tile):
        dupeBoard[x][y]=HINT_TILE
    return dupeBoard

def getValidMoves(board,tile):
    valid=[]
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if isValidMove(board,tile,x,y)!=False:
                valid.append((x,y))
    return valid

def getScoreOfBoard(board):
    whiteScore=sum(1 for x in range(BOARDWIDTH) for y in range(BOARDHEIGHT) if board[x][y]==WHITE_TILE)
    blackScore=sum(1 for x in range(BOARDWIDTH) for y in range(BOARDHEIGHT) if board[x][y]==BLACK_TILE)
    return {WHITE_TILE:whiteScore,BLACK_TILE:blackScore}

def enterPlayerTile():
    textSurf = FONT.render('Do you want to be white or black?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center=(WINDOWWIDTH//2, WINDOWHEIGHT//2)
    xSurf = BIGFONT.render('White', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center=(WINDOWWIDTH//2-60, WINDOWHEIGHT//2+40)
    oSurf = BIGFONT.render('Black', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center=(WINDOWWIDTH//2+60, WINDOWHEIGHT//2+40)
    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONUP:
                mx,my=event.pos
                if xRect.collidepoint((mx,my)):
                    return [WHITE_TILE,BLACK_TILE]
                elif oRect.collidepoint((mx,my)):
                    return [BLACK_TILE,WHITE_TILE]
        DISPLAYSURF.blit(textSurf,textRect)
        DISPLAYSURF.blit(xSurf,xRect)
        DISPLAYSURF.blit(oSurf,oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

def isOnCorner(x,y):
    return (x==0 and y==0) or (x==0 and y==BOARDHEIGHT-1) or (x==BOARDWIDTH-1 and y==0) or (x==BOARDWIDTH-1 and y==BOARDHEIGHT-1)

def getComputerMove(board, computerTile):
    possibleMoves=getValidMoves(board,computerTile)
    random.shuffle(possibleMoves)
    for x,y in possibleMoves:
        if isOnCorner(x,y):
            return [x,y]
    bestScore=-1
    bestMove=None
    for x,y in possibleMoves:
        dupeBoard=copy.deepcopy(board)
        makeMove(dupeBoard,computerTile,x,y)
        score=getScoreOfBoard(dupeBoard)[computerTile]
        if score>bestScore:
            bestScore=score
            bestMove=[x,y]
    return bestMove

def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)):
        if event.type==QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
            pygame.quit()
            sys.exit()

# ------------------ Main ------------------
if __name__=='__main__':
    main()
