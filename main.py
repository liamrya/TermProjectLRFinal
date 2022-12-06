from characters import *
from cmu_112_graphics import *
import random

def appStarted(app):
    #ALL SPRITES FROM https://www.pngkey.com/detail/u2q8i1u2o0e6t4u2_imagenes-con-transparencia-para-que-la-puedan-descargar/ 
    spritestrip = app.loadImage('img/mainsprite.png')
    app.sprites = spritestrip
    app.gameOver = False
    app.win = False
    app.hold = 157
    app.cFloor = 157
    app.gravity = True
    app.currentX = 0
    app.gap = False
    app.fell = 0
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
    tallMario_load = spritestrip.crop((60, 980, 100, 1060))
    app.tallStandingMario = app.scaleImage(tallMario_load, .5)
    starMario_load = spritestrip.crop((880, 1390, 920, 1470))
    app.starStandingMario = app.scaleImage(starMario_load, .5)
    #taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    app.runningRight = []
    app.runningLeft = []
    app.tallRunningRight = []
    app.tallRunningLeft = []
    app.starRunningRight = []
    app.starRunningLeft = []
    for i in range(3):
        sprite = spritestrip.crop((165+i*40, 895, 200+i*40, 940))
        spriteScale = app.scaleImage(sprite, .66)
        app.runningRight.append(spriteScale)
        spriteScaleTransposed = spriteScale.transpose(Image.FLIP_LEFT_RIGHT)
        app.runningLeft.append(spriteScaleTransposed)
        spriteTall = spritestrip.crop((150 + i*45, 978, 200+i*40, 1057))
        spriteScaleTall = app.scaleImage(spriteTall, .5)
        spriteScaleTallTransposed = spriteScaleTall.transpose(Image.FLIP_LEFT_RIGHT)
        app.tallRunningRight.append(spriteScaleTall)
        app.tallRunningLeft.append(spriteScaleTallTransposed)
        spriteStar = spritestrip.crop((968 + i*45, 1397, 1023+i*40, 1464))
        spriteScaleStar = app.scaleImage(spriteStar, .5)
        spriteScaleStarTransposed = spriteScaleStar.transpose(Image.FLIP_LEFT_RIGHT)
        app.starRunningRight.append(spriteScaleStar)
        app.starRunningLeft.append(spriteScaleStarTransposed)
    jMLoad = spritestrip.crop((180, 935, 240, 970))
    app.jumpingMario = app.scaleImage(jMLoad, .66)
    tJMLoad = spritestrip.crop((280, 975, 345, 1050))
    app.tallJumpingMario = app.scaleImage(tJMLoad, .5)
    sJMLoad = spritestrip.crop((1108, 1394, 1168, 1457))
    app.starJumpingMario = app.scaleImage(sJMLoad, .5)
    app.spriteCounter = 0
    app.currentMario = app.standingMario
    app.scrollX = 0
    app.startTrack = -2000
    app.isStart = True
    app.isJumping = False
    app.isFalling = False
    app.isRunning = False
    app.isTall = False
    app.isStar = False
    app.marioLocation = [200,120]
    app.marioBounds = [187,110,207,130]
    app.current = app.marioLocation[1]
    
    #POWER UP ITEMS
    mushLoad = app.sprites.crop((360,25,388,75))
    app.mushroom = app.scaleImage(mushLoad, .5)
    app.mushroomLocations = []
    starLoad = app.sprites.crop((360,160,390,210))
    app.star = app.scaleImage(starLoad, .5)
    app.starLocations = []

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
    app.barriersDict = []
    app.gapDict = []
    app.powerList = []

    #COLLISION HELP
    app.blockR = False
    app.blockL = False
    loadTerrain(app)
    createGoombas(app)
    
def getCellBounds(app):
    for i in range(len(app.barrierLocations)):
        x = app.barriersDict
        L = app.barrierLocations
        x.append([17*(L[i][1]), 17*L[i][0], 17*(L[i][1]+1), 17*(L[i][0]+1)])
    for i in range(len(app.gapLocations)):
        x = app.gapDict
        L = app.gapLocations
        x.append([17*(L[i][1]), 17*L[i][0], 17*(L[i][1]+1), 17*(L[i][0]+1)])
    for i in range(len(app.powerLocations)):
        x = app.barriersDict
        x2 = app.powerList
        L = app.powerLocations
        x.append([17*(L[i][1]), 17*L[i][0], 17*(L[i][1]+1), 17*(L[i][0]+1)])
        x2.append([17*(L[i][1]), 17*L[i][0], 17*(L[i][1]+1), 17*(L[i][0]+1)])

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
     
    board = loadTerrainSolver(board, 9, 15)
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
    getCellBounds(app)

def loadTerrainSolver(board, curRow, curCol):
    cols = len(board[0])
    if curCol == 90:
        return board
    for i in range(cols-curCol):
        newCol = curCol + i
        if isLegal(board, curRow, newCol):
            if random.randint(0,10) == 5:
                board[curRow][newCol] = 'brick'
                board[curRow-1][newCol] = 'brick'
                result = loadTerrainSolver(board, curRow, newCol+1)
                if result != None:
                    return result
                board[curRow][newCol] = 'sky'
                board[curRow-1][newCol] = 'sky'
        if isLegalAir(board, curRow, newCol):
            if random.randint(0,4) == 2:
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
    return None

def isLegal(board, curRow, curCol):
    if board[curRow][curCol-1] == 'brick' or board[curRow][curCol-2] == 'brick':
        return False
    return True

def isLegalAir(board, curRow, newCol):
    if board[curRow][newCol] == 'sky' and board[curRow][newCol-1] == 'sky' and board[curRow][newCol-2] == 'sky' and board[curRow][newCol-3] == 'sky':
        return True
    return False
    

#creating enemies
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
    


def barrierCollision(app):
    for i in range(len(app.barriersDict)):
            inRange = False
            inXRange = False
            inRangeL = False
            inXRangeL = False
            for j in range(app.barriersDict[i][1], app.barriersDict[i][3]):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.barriersDict[i][0]-app.scrollX, app.barriersDict[i][2]-app.scrollX):
                    if app.marioBounds[2] + 5 == k:
                        inXRange = True
            if inRange == True and inXRange == True:
                app.blockR = True
            if app.isJumping == True or app.isFalling == True or app.currentMario == app.runningLeft or app.currentMario == app.tallStandingMario:
                app.blockR = False
            for j in range(app.barriersDict[i][1], app.barriersDict[i][3]):
                if int(app.marioBounds[3]) - 10 == j:
                    inRangeL = True
            if inRangeL==True:
                for k in range(app.barriersDict[i][0]-app.scrollX, app.barriersDict[i][2]-app.scrollX):
                    if app.marioBounds[0] - 5 == k:
                        inXRangeL = True
            if inRangeL == True and inXRangeL == True:
                app.blockL = True
            if app.isJumping == True or app.isFalling == True or app.currentMario == app.runningRight or app.currentMario == app.tallRunningRight:
                app.blockL = False
    
def standCollision(app):
    for i in range(len(app.barriersDict)):
            inRange = False
            inXRange = False
            for j in range(app.barriersDict[i][1]-17, app.barriersDict[i][3]-17):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.barriersDict[i][0]-app.scrollX, app.barriersDict[i][2]-app.scrollX):
                    if app.marioBounds[2] - 10 == k:
                        inXRange = True    
            if inRange == True and inXRange == True:
                app.isJumping = False
                app.isFalling = False
                app.cFloor = app.marioLocation[1]
                app.gravity = True
                app.currentX = app.scrollX
            if app.scrollX > app.currentX+8 or app.scrollX < app.currentX-8:
                app.cFloor = 160
                app.isFalling = True
                app.gravity = True
                app.currentX = app.scrollX
    for i in range(len(app.barriersDict)):
            inRange = False
            inXRange = False
            for j in range(app.barriersDict[i][1]+17, app.barriersDict[i][3]+17):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.barriersDict[i][0]-app.scrollX, app.barriersDict[i][2]-app.scrollX):
                    if app.marioBounds[2] - 10 == k:
                        inXRange = True    
            if inRange == True and inXRange == True and app.isJumping == True:
                app.isJumping = False
                app.isFalling = True
                if app.barriersDict[i] in app.powerList:
                    app.powerList.remove(app.barriersDict[i])
                    choose = random.randint(0, 3)
                    if choose == 0 or choose == 1:
                        app.mushroomLocations.append([app.barriersDict[i][0], app.barriersDict[i][1]-17, app.barriersDict[i][2], app.barriersDict[i][1]])
                    if choose == 2:
                        app.starLocations.append([app.barriersDict[i][0], app.barriersDict[i][1]-17, app.barriersDict[i][2], app.barriersDict[i][1]])
def gapCollision(app):
    #MARIO
    for i in range(len(app.gapDict)):
            inRange = False
            inXRange = False
            for j in range(app.gapDict[i][1]-17, app.gapDict[i][3]-17):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.gapDict[i][0]-app.scrollX, app.gapDict[i][2]-app.scrollX):
                    if app.marioBounds[2] - 10 == k:
                        inXRange = True    
            if inRange == True and inXRange == True:
                app.isFalling = False
                app.gap = True
                app.fell = 2000
    #GOOMBA
    for i in range(len(app.gapDict)):
            inRange = False
            inXRange = False
            for j in range(app.gapDict[i][0]-app.scrollX, app.gapDict[i][2]-app.scrollX):
                for k in range(len(app.goombaLocations)):
                    if app.goombaLocations[k] - app.scrollX- app.goombaX == j:
                        app.goombaLocations[k] = -200
    
def mushroomCollision(app):
    for i in range(len(app.mushroomLocations)):
            inRange = False
            inXRange = False
            for j in range(app.mushroomLocations[i][1], app.mushroomLocations[i][3]):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.mushroomLocations[i][0]-app.scrollX, app.mushroomLocations[i][2]-app.scrollX):
                    if app.marioBounds[2] - 10 == k:
                        inXRange = True
            if inRange == True and inXRange == True:
                app.isTall = True
                app.isStar = False
                app.currentMario = app.tallStandingMario
                app.mushroomLocations.pop(i)
def starCollision(app):
    for i in range(len(app.starLocations)):
            inRange = False
            inXRange = False
            for j in range(app.starLocations[i][1], app.starLocations[i][3]):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.starLocations[i][0]-app.scrollX, app.starLocations[i][2]-app.scrollX):
                    if app.marioBounds[2] - 10 == k:
                        inXRange = True
            if inRange == True and inXRange == True:
                app.isTall = False
                app.isStar = True
                app.currentMario = app.starStandingMario
                app.starLocations.pop(i)
                app.startTrack = app.scrollX
def keyPressed(app, event):
    if app.win == False:
        if (event.key == 'Left'):
            if app.scrollX > 2:
                if app.blockL == False:
                    app.scrollX -= 2
                app.currentMario = app.runningLeft
                if app.isTall == True:
                    app.currentMario = app.tallRunningLeft
                if app.isStar == True:
                    app.currentMario = app.starRunningLeft
                app.isRunning = True
        if (event.key == 'Right'):
            app.currentMario = app.runningRight
            if app.isTall == True:
                app.currentMario = app.tallRunningRight
            if app.isStar == True:
                app.currentMario = app.starRunningRight    
            app.isRunning = True
            if app.blockR == False:
                app.scrollX += 2
        if (event.key == 'Up' and app.isJumping == False and app.isFalling == False):
            app.isJumping = True
            app.isFalling = False
            app.gravity = True
    if (event.key == 'r'):
        runApp(width=600, height=200)
def keyReleased(app, event):
    if (event.key == 'Right'):
        app.isRunning = False
    if (event.key == 'Left'):
        app.isRunning = False

#taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def timerFired(app):
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
        app.marioBounds[1] = app.marioLocation[1]-10
        app.marioBounds[3] = app.marioLocation[1]+10
    if app.marioLocation[1] >= app.cFloor:
        app.isStart = False
    if app.marioLocation[1] == 157:
        app.isFalling = False
    if app.marioLocation[1] > 157:
        app.marioLocation[1] = app.cFloor
        app.isFalling = False
        app.isJumping = False
        
    #jumping
    if app.isJumping == True:
        if app.isTall == False:
            app.currentMario = app.jumpingMario
        elif app.isTall == True:
            app.currentMario = app.tallJumpingMario
        if app.isStar == True:
            app.currentMario = app.starJumpingMario
        if app.marioLocation[1] < app.cFloor-27:
            app.marioLocation[1] -= 10
            app.marioBounds[1] = app.marioLocation[1]-10
            app.marioBounds[3] = app.marioLocation[1]+10
        elif app.marioLocation[1] < app.cFloor-12:
            app.marioLocation[1] -= 13
            app.marioBounds[1] = app.marioLocation[1]-10
            app.marioBounds[3] = app.marioLocation[1]+10
        elif app.marioLocation[1] < app.cFloor+7:
            app.marioLocation[1] -= 16
            app.marioBounds[1] = app.marioLocation[1]-10
            app.marioBounds[3] = app.marioLocation[1]+10
        if app.marioLocation[1] <= app.cFloor-77:
            app.isJumping = False
            app.isFalling = True
    #gravity
    if app.gravity == True:
        if app.marioLocation[1] < app.cFloor:
            app.marioLocation[1] += .5
            app.marioBounds[1] = app.marioLocation[1]-10
            app.marioBounds[3] = app.marioLocation[1]+10
    #gap
    if app.gap == True:
        for i in range(100):
            if app.marioLocation[1] < app.fell:
                app.marioLocation[1] += 5
    if int(app.marioLocation[1]) > 200:
        app.gameOver = True     
    
    if app.gap == False:
        if app.marioLocation[1] > 157:
            app.cFloor = 157
            app.marioLocation[1] = app.cFloor

    #falling
    if app.isFalling == True:
        if app.isTall == False:
            if app.currentMario != app.jumpingMario:
                    app.currentMario = app.jumpingMario
        elif app.isTall == True:
            if app.currentMario != app.tallJumpingMario:
                    app.currentMario = app.tallJumpingMario
        if app.isStar == True:
            if app.currentMario != app.starJumpingMario:
                app.currentMario = app.starJumpingMario
        if app.marioLocation[1] <= app.cFloor-27:
            app.marioLocation[1] += 6
            app.marioBounds[1] = app.marioLocation[1]-10
            app.marioBounds[3] = app.marioLocation[1]+10
        elif app.marioLocation[1] <= app.cFloor-22:
            app.marioLocation[1] += 8
            app.marioBounds[1] = app.marioLocation[1]-10
            app.marioBounds[3] = app.marioLocation[1]+10
        elif app.marioLocation[1] < app.cFloor-10:
            app.marioLocation[1] += 9
            app.marioBounds[1] = app.marioLocation[1]-10
            app.marioBounds[3] = app.marioLocation[1]+10
        elif app.marioLocation[1] < app.cFloor-2:
            app.marioLocation[1] += 4
            app.marioBounds[1] = app.marioLocation[1]-10
            app.marioBounds[3] = app.marioLocation[1]+10
            if app.marioLocation[1] >= app.cFloor-.5:
                app.isFalling = False
        
    if app.isRunning != True and app.isFalling != True and app.isJumping != True and app.isTall != True:
        app.currentMario = app.standingMario

    if app.isTall == True and app.isRunning != True and app.isFalling != True and app.isJumping != True:
        app.currentMario = app.tallStandingMario
    
    if app.isStar == True and app.isRunning != True and app.isFalling != True and app.isJumping != True:
        app.currentMario = app.starStandingMario
    
    
    #collisions
        #goomba collision
    if app.isStar == False:
        for i in range(len(app.goombaLocations)):
            if app.isTall == False:
                locationNow = app.goombaLocations[i]-app.scrollX-app.goombaX
                if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[1] < 130 and app.marioBounds[3] > 115:
                    app.goombaLocations[i] = -200
                if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[1] > 115: 
                    app.gameOver = True
            if app.isTall == True:
                locationNow = app.goombaLocations[i]-app.scrollX-app.goombaX
                if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[1] < 130 and app.marioBounds[3] > 115:
                    app.goombaLocations[i] = -200
                if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[1] > 115: 
                    app.isTall = False
                    app.currentMario = app.standingMario
                    app.goombaLocations[i] = -200
        #brick collision
    if app.isStar == False:
        barrierCollision(app)
    standCollision(app)
    mushroomCollision(app)
    starCollision(app)
    gapCollision(app)
    #win condition
    if app.marioBounds[2] + app.scrollX > 1380:
        app.win = True
    
    
def drawBack(app, canvas):
    canvas.create_image(300-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))
    canvas.create_image(900-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))
    canvas.create_image(1500-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))

def drawBackground(app, canvas):
    for i in range(len(app.terrain)):
        for j in range(0+int(app.scrollX/17), len(app.terrain[i])-70+int(app.scrollX/17)):
            if app.terrain[i][j] == 'brick':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.brick))
            if app.terrain[i][j] == 'power':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.power))
            if app.terrain[i][j] == 'skyDraw':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.sky))
def drawMario(app, canvas):
    if app.isStar == False:
        if app.isTall == False:
            if app.currentMario == app.runningRight:
                sprite = app.runningRight[app.spriteCounter]
                canvas.create_image(200,app.marioLocation[1], image=ImageTk.PhotoImage(sprite))
            elif app.currentMario == app.runningLeft:
                sprite = app.runningLeft[app.spriteCounter]
                canvas.create_image(200,app.marioLocation[1], image=ImageTk.PhotoImage(sprite))
            else:
                canvas.create_image(200,app.marioLocation[1],image=ImageTk.PhotoImage(app.currentMario))
        if app.isTall == True:
            if app.currentMario == app.tallRunningRight:
                sprite = app.tallRunningRight[app.spriteCounter]
                canvas.create_image(200,app.marioLocation[1], image=ImageTk.PhotoImage(sprite))
            elif app.currentMario == app.tallRunningLeft:
                sprite = app.tallRunningLeft[app.spriteCounter]
                canvas.create_image(200,app.marioLocation[1], image=ImageTk.PhotoImage(sprite))
            else:
                canvas.create_image(200,app.marioLocation[1],image=ImageTk.PhotoImage(app.currentMario))
    if app.isStar == True:
        if app.currentMario == app.starRunningRight:
                sprite = app.starRunningRight[app.spriteCounter]
                canvas.create_image(200,app.marioLocation[1], image=ImageTk.PhotoImage(sprite))
        elif app.currentMario == app.starRunningLeft:
                sprite = app.starRunningLeft[app.spriteCounter]
                canvas.create_image(200,app.marioLocation[1], image=ImageTk.PhotoImage(sprite))
        else:
            canvas.create_image(200,app.marioLocation[1],image=ImageTk.PhotoImage(app.currentMario))    

def drawPowerups(app, canvas):
    for i in range(len(app.mushroomLocations)):
        canvas.create_image(app.mushroomLocations[i][0]-app.scrollX+8.5, app.mushroomLocations[i][1]+8.5, image=ImageTk.PhotoImage(app.mushroom))
    for i in range(len(app.starLocations)):
        canvas.create_image(app.starLocations[i][0]-app.scrollX+8.5, app.starLocations[i][1]+8.5, image=ImageTk.PhotoImage(app.star))

def drawGoomba(app, canvas):
    for i in range(len(app.goombaLocations)):
        canvas.create_image(app.goombaLocations[i]-app.goombaX-app.scrollX,160,image=ImageTk.PhotoImage(app.goomba))

def drawGameOver(app, canvas):
    canvas.create_rectangle(0,0,600,200, fill='Black')
    canvas.create_text(300,100,text='Game Over', fill = 'White')

def drawWin(app, canvas):
    canvas.create_rectangle(0,0,600,200, fill='White')
    canvas.create_text(300,100,text='You win!', fill = 'Black')

def redrawAll(app, canvas):
    drawBack(app, canvas)
    drawBackground(app, canvas)
    drawMario(app, canvas)
    drawGoomba(app, canvas)
    drawPowerups(app, canvas)
    if app.gameOver == True:
        drawGameOver(app, canvas)
    if app.win == True:
        drawWin(app, canvas)
def playMario():
    runApp(width=600, height=200)
playMario()