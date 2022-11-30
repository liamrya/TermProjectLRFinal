from characters import *
from cmu_112_graphics import *
import random

def appStarted(app):
    #ALL SPRITES FROM https://www.pngkey.com/detail/u2q8i1u2o0e6t4u2_imagenes-con-transparencia-para-que-la-puedan-descargar/ 
    spritestrip = app.loadImage('img/mainsprite.png')
    app.sprites = spritestrip
    app.gameOver = False
    app.cFloor = 157
    #background
    app.width = 1800
    app.height = 200
    app.tileSize = 17
    app.terrain = []
    skyLoad = app.sprites.crop((800,520,840,570))
    app.sky = app.scaleImage(skyLoad, .5)
    floorLoad = app.sprites.crop((235,130,275,180))
    app.floor = app.scaleImage(floorLoad, .5)
    brickLoad = app.sprites.crop((110,25,150,75))
    app.brick = app.scaleImage(brickLoad, .5)
    powerLoad = app.sprites.crop((195,90,225,130))
    app.power = app.scaleImage(powerLoad, .55)
    app.back = app.loadImage('img/backgroundMADE.png')
    #MARIO APP ITEMS
    mario_load = spritestrip.crop((10, 895, 60, 940))
    app.standingMario = app.scaleImage(mario_load, .66)
    #taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    app.runningRight = []
    app.runningLeft = []
    for i in range(3):
        sprite = spritestrip.crop((165+i*40, 895, 200+i*40, 940))
        spriteScale = app.scaleImage(sprite, .66)
        app.runningRight.append(spriteScale)
        spriteScaleTransposed = spriteScale.transpose(Image.FLIP_LEFT_RIGHT)
        app.runningLeft.append(spriteScaleTransposed)
    jMLoad = spritestrip.crop((180, 935, 240, 970))
    app.jumpingMario = app.scaleImage(jMLoad, .66)
    app.spriteCounter = 0
    app.currentMario = app.standingMario
    app.scrollX = 0
    app.isStart = True
    app.isJumping = False
    app.isFalling = False
    app.isRunning = False
    app.marioLocation = [200,120]
    app.current = app.marioLocation[1]

    #GOOMBA APP ITEMS
    app.goomba_load = spritestrip.crop((100, 1318, 160, 1350))
    app.goombaX = 80
    app.goombaMove = False
    app.goomba = app.scaleImage(app.goomba_load, .66)
    app.goombaLocations = []

    #MAPLOCATIONS
    app.barrierLocations = []
    app.gapLocations = []
    app.powerLocations = []
    app.barriersDict = {}
    app.gapDict = {}
    app.powerDict = {}
    loadTerrain(app)
    createGoombas(app)
    
def getCellBounds(app, L):
    if L == app.barrierLocations:
        x = app.barriersDict
    if L == app.gapLocations:
        x = app.gapDict
    if L == app.powerLocations:
        x = app.powerDict
    for i in range(len(L)):
        x[L[i]] = [17*(L[i][1]) - app.scrollX, 17*L[i][0], 17*(L[i][1]+1) - app.scrollX, 17*(L[i][0]+1)]

#generating terrain
def loadTerrain(app):
    board = []
    backupBoard = []
    for x in range(int((app.height)/app.tileSize)+1):
        board.append([])
        backupBoard.append([])
        for y in range(int(1800/app.tileSize)):
            if x>9:
                board[x].append('floor')
                backupBoard[x].append('floor')
            else:
                board[x].append('sky')
                backupBoard[x].append('sky')
     
    board = loadTerrainSolver(board, 9, 20)
    if board != None:
        app.terrain = board
    else:
        app.terrain = backupBoard
    for i in range(len(app.terrain)):
        for j in range(len(app.terrain[0])):
            if app.terrain[i][j] == 'brick':
                app.barrierLocations.append((i, j))
            if app.terrain[i][j] == 'power':
                app.powerLocations.append((i, j))
            if app.terrain[i][j] == 'skyDraw':
                app.gapLocations.append((i, j))

def loadTerrainSolver(board, curRow, curCol):
    cols = len(board[0])
    if curCol == 90:
        return board
    for i in range(cols-curCol):
        newCol = curCol + i
        if isLegal(board, curRow, newCol):
            if random.randint(0,8) == 5:
                board[curRow][newCol] = 'brick'
                board[curRow-1][newCol] = 'brick'
                result = loadTerrainSolver(board, curRow, newCol+1)
                if result != None:
                    return result
                board[curRow][newCol] = 'sky'
                board[curRow-1][newCol] = 'sky'
        if isLegalAir(board, curRow, newCol):
            if random.randint(0,6) == 2:
                x = random.randint(1,3)
                y = random.randint(1,3)
                board[curRow-3][newCol-1] = 'brick'
                board[curRow-3][newCol-2] = 'brick'
                board[curRow-3][newCol-3] = 'brick'
                if random.randint(0,1) == 1:
                    board[curRow-3][newCol-x] = 'power'
                if random.randint(0,2) == 1:
                    board[curRow-6][newCol-y] = 'brick'
                if random.randint(0,3) == 1:
                    board[10][newCol] = 'skyDraw'
                    board[10][newCol-1] = 'skyDraw'
                    board[10][newCol-2] = 'skyDraw'
                    board[11][newCol] = 'skyDraw'
                    board[11][newCol-1] = 'skyDraw'
                    board[11][newCol-2] = 'skyDraw'
                result = loadTerrainSolver(board, curRow, newCol+1)
                if result != None:
                    return result
                board[curRow-3][newCol] = 'sky'
                board[curRow-3][newCol-1] = 'sky'
                board[curRow-3][newCol-2] = 'sky'
    return None

def isLegal(board, curRow, curCol):
    if board[curRow][curCol-1] == 'brick' or board[curRow][curCol-2] == 'brick':
        return False
    return True

def isLegalAir(board, curRow, newCol):
    if board[curRow][newCol] == 'sky' and board[curRow][newCol-1] == 'sky' and board[curRow][newCol-2] == 'sky' and board[curRow][newCol-3] == 'sky':
        return True
    return False
    

#creating MOBS
#goombas
def createGoombas(app):
    count = 0
    for i in range(len(app.terrain[0])):
        if app.terrain[9][i] == 'sky':
            count += 1
        elif count > 5:
            app.goombaLocations.append(i*17)
            count = 0
        else:
            count = 0
    
        
            

def keyPressed(app, event):
    if (event.key == 'Left'):
        if app.scrollX > 2:
            app.scrollX -= 2
            app.currentMario = app.runningLeft
            app.isRunning = True
    if (event.key == 'Right'):
        app.currentMario = app.runningRight
        app.isRunning = True
        app.scrollX += 2
    if (event.key == 'r'):
        runApp(width=600, height=200)
    if (event.key == 'Up' and app.isJumping == False and app.isFalling == False):
        app.isJumping = True
        app.isFalling = False

def keyReleased(app, event):
    if (event.key == 'Right'):
        app.isRunning = False
    if (event.key == 'Left'):
        app.isRunning = False

#taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def timerFired(app):
    getCellBounds(app, app.barrierLocations)
    getCellBounds(app, app.gapLocations)
    getCellBounds(app, app.powerLocations)
    print(app.powerDict)
    print(app.barriersDict)
    print(app.gapDict)
    
    app.spriteCounter = (1+app.spriteCounter) % len(app.runningRight)
    if app.goombaX > 80:
        app.goombaMove = False
    if app.goombaX < 17:
        app.goombaMove = True
    if app.goombaMove == True:
        app.goombaX += 3
    if app.goombaMove == False:
        app.goombaX -= 3

    #initial drop
    if app.isStart == True:
        app.marioLocation[1] += 4.5
    if app.marioLocation[1] >= app.cFloor:
        app.isStart = False
    #jumping
    if app.isJumping == True:
        app.currentMario = app.jumpingMario
        if app.marioLocation[1] < app.cFloor-27:
            app.marioLocation[1] -= 10
        elif app.marioLocation[1] < app.cFloor-12:
            app.marioLocation[1] -= 13
        elif app.marioLocation[1] < app.cFloor+7:
            app.marioLocation[1] -= 16
        if app.marioLocation[1] <= app.cFloor-77:
            app.isJumping = False
            app.isFalling = True
    #gravity
    if app.marioLocation[1] <= app.cFloor:
        app.marioLocation[1] += 1

    #falling
    if app.isFalling == True:
        app.cFloor = 157
        if app.currentMario != app.jumpingMario:
                app.currentMario = app.jumpingMario
        if app.marioLocation[1] <= app.cFloor-27:
            app.marioLocation[1] += 6
        elif app.marioLocation[1] <= app.cFloor-22:
            app.marioLocation[1] += 8
        elif app.marioLocation[1] <= app.cFloor:
            app.marioLocation[1] += 9
            if app.marioLocation[1] >= app.cFloor-2:
                app.isFalling = False
        
    if app.isRunning != True and app.isFalling != True and app.isJumping != True:
        app.currentMario = app.standingMario

    #collisions
    for location in app.goombaLocations:
        locationNow = location-app.scrollX-app.goombaX
        if locationNow > 186 and locationNow < 214 and (app.currentMario == app.standingMario or 
        app.currentMario == app.runningRight or app.currentMario == app.runningLeft): 
            app.gameOver = True


def drawBack(app, canvas):
    canvas.create_image(300-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))
    canvas.create_image(900-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))
    canvas.create_image(1500-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))


def drawBackground(app, canvas):
    for i in range(len(app.terrain)):
        for j in range(len(app.terrain[i])):
            if app.terrain[i][j] == 'brick':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.brick))
            if app.terrain[i][j] == 'power':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.power))
            if app.terrain[i][j] == 'skyDraw':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.sky))
def drawMario(app, canvas):
    if app.currentMario == app.standingMario:
        canvas.create_image(200,app.marioLocation[1],image=ImageTk.PhotoImage(app.currentMario))
    if app.currentMario == app.runningRight:
        sprite = app.runningRight[app.spriteCounter]
        canvas.create_image(200,app.marioLocation[1], image=ImageTk.PhotoImage(sprite))
    if app.currentMario == app.runningLeft:
        sprite = app.runningLeft[app.spriteCounter]
        canvas.create_image(200,app.marioLocation[1], image=ImageTk.PhotoImage(sprite))
    if app.currentMario == app.jumpingMario:
        canvas.create_image(200, app.marioLocation[1], image=ImageTk.PhotoImage(app.jumpingMario))

def drawGoomba(app, canvas):
    for i in range(len(app.goombaLocations)):
        canvas.create_image(app.goombaLocations[i]-app.goombaX-app.scrollX,160,image=ImageTk.PhotoImage(app.goomba))

def drawGameOver(app, canvas):
    canvas.create_rectangle(0,0,600,200, fill='Black')
    canvas.create_text(300,100,text='Game Over', fill = 'White')

def redrawAll(app, canvas):
    drawBack(app, canvas)
    drawBackground(app, canvas)
    drawMario(app, canvas)
    drawGoomba(app, canvas)
    if app.gameOver == True:
        drawGameOver(app, canvas)
def playMario():
    runApp(width=600, height=200)
playMario()