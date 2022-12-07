from cmu_112_graphics import *
import random

def appStarted(app):
    #ALL SPRITES FROM https://www.pngkey.com/detail/u2q8i1u2o0e6t4u2_imagenes-con-transparencia-para-que-la-puedan-descargar/ 
    spritestrip = app.loadImage('img/mainsprite.png')
    app.sprites = spritestrip
    app.gameOver, app.win, app.gravity, app.gap = False, False, True, False
    app.hold, app.cFloor, app.currentX, app.fell = 160, 160, 0, 0

    #background
    app.width, app.height, app.tileSize = 1800, 200, 17
    app.terrain = []
    skyLoad = app.sprites.crop((800,520,840,570))
    app.sky = app.scaleImage(skyLoad, .5)
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
    app.runningRight, app.runningLeft, app.tallRunningRight = [], [], []
    app.tallRunningLeft, app.starRunningRight, app.starRunningLeft = [], [], []
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
    app.spriteCounter, app.scrollX, app.startTrack = 0, 0, -2000,
    app.currentMario = app.standingMario
    app.isStart, app.isJumping, app.isFalling = True, False, False
    app.isRunning, app.isTall, app.isStar = False, False, False
    app.marioLocation, app.marioBounds = [200,120], [189,110,202,130]
    app.current = app.marioLocation[1]
    
    #POWER UP ITEMS
    mushLoad = app.sprites.crop((360,25,388,75))
    app.mushroom = app.scaleImage(mushLoad, .5)
    app.mushroomLocations = []
    starLoad = app.sprites.crop((360,160,390,210))
    app.star = app.scaleImage(starLoad, .5)
    app.starLocations = []
    app.startTimer = 2000

    #GOOMBA APP ITEMS
    app.goomba_load = spritestrip.crop((100, 1318, 160, 1350))
    app.goombaX = 80
    app.goombaMove = False
    app.goomba = app.scaleImage(app.goomba_load, .66)
    app.goombaLocations = []

    #HAMMER BRO APP ITEMS
    app.hammerBrosRight, app.hammerBrosLeft, app.hammerBrosLocation = [], [], []
    app.currentHammers = app.hammerBrosRight
    app.hammerMove = False
    app.hammerX, app.addX = 0, 0
    for i in range(3):
        hammerBro_load = spritestrip.crop((750 + i*60,1160,800 + i*60,1215))
        hammerBro = app.scaleImage(hammerBro_load, .5)
        hammerBroTransposed = hammerBro.transpose(Image.FLIP_LEFT_RIGHT)
        app.hammerBrosRight.append(hammerBro)
        app.hammerBrosLeft.append(hammerBroTransposed)

    #HAMMER APP ITEMS
    app.hammer, app.hammerLocation = [], []
    hammer1_load = spritestrip.crop((930,1190,959,1210))
    hammer1 = app.scaleImage(hammer1_load, .5)
    hammer2_load = spritestrip.crop((959,1181,969,1210))
    hammer2 = app.scaleImage(hammer2_load, .5)
    hammer3_load = spritestrip.crop((975,1190,1009,1210))
    hammer3 = app.scaleImage(hammer3_load, .5)
    hammer4_load = spritestrip.crop((1010,1181,1030,1210))
    hammer4 = app.scaleImage(hammer4_load, .5)
    app.hammer.append(hammer1)
    app.hammer.append(hammer2)
    app.hammer.append(hammer3)
    app.hammer.append(hammer4)
    app.spriteCounterH, app.count = 0, 1
    app.currentMarioX, app.currentMarioY = 0, 0
    app.currentHLocX, app.currentHLocY = 0,0

    #MAPLOCATIONS
    app.barrierLocations, app.gapLocations, app.powerLocations = [], [], []
    app.barriersList, app.gapList, app.powerList = [], [], []

    #COLLISION HELP
    app.blockR, app.blockL = False, False
    loadTerrain(app)
    createGoombas(app)
    createHammerBros(app)

#getting cell bounds for the map objects
def getCellBounds(app):
    for i in range(len(app.barrierLocations)):
        x, L = app.barriersList, app.barrierLocations
        x.append([17*(L[i][1]), 17*L[i][0], 17*(L[i][1]+1), 17*(L[i][0]+1)])
    for i in range(len(app.gapLocations)):
        x, L = app.gapList, app.gapLocations
        x.append([17*(L[i][1]), 17*L[i][0], 17*(L[i][1]+1), 17*(L[i][0]+1)])
    for i in range(len(app.powerLocations)):
        x, x2, L = app.barriersList, app.powerList, app.powerLocations
        x.append([17*(L[i][1]), 17*L[i][0], 17*(L[i][1]+1), 17*(L[i][0]+1)])
        x2.append([17*(L[i][1]), 17*L[i][0], 17*(L[i][1]+1), 17*(L[i][0]+1)])

#generating terrain
def loadTerrain(app):
    board, backupBoard = [], []
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
#recursive function
def loadTerrainSolver(board, curRow, curCol):
    cols = len(board[0])
    if curCol == 100:
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
                x, y = random.randint(1,3), random.randint(1,3)
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
#checking move legality
def isLegal(board, curRow, curCol):
    if board[curRow][curCol-1] == 'brick' or board[curRow][curCol-2] == 'brick':
        return False
    return True

def isLegalAir(board, curRow, newCol):
    if board[curRow][newCol] == 'sky' and board[curRow][newCol-1] == 'sky' and board[
        curRow][newCol-2] == 'sky' and board[curRow][newCol-3] == 'sky':
        return True
    return False
    

#creating enemies
#hammer bros
def createHammerBros(app):
    count = 0
    for i in range(len(app.terrain[0])):
        if app.terrain[6][i] == 'power':
            count += 1
        if count == 2:
            if app.terrain[6][i-1] != 'power' and app.terrain[6][i-1] != 'brick':
                app.addX = 17
            elif app.terrain[6][i-2] != 'power' and app.terrain[6][i-2] != 'brick':
                app.addX = 0
            elif app.terrain[6][i-2] == 'power' or app.terrain[6][i-2] == 'brick':
                app.addX = -17
            app.hammerBrosLocation.append(i*17+8.5+app.addX)
            count = 0
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

#checking collision with barriers
def barrierCollision(app):
    for i in range(len(app.barriersList)):
            inRange, inXRange, inRangeL, inXRangeL = False, False, False, False
            for j in range(app.barriersList[i][1], app.barriersList[i][3]):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.barriersList[i][0]-app.scrollX, app.barriersList[i][2]-app.scrollX):
                    if app.marioBounds[2] + 5 == k:
                        inXRange = True
            if inRange == True and inXRange == True:
                app.blockR = True
            if app.isJumping == True or app.isFalling == True and app.marioBounds[3] < 137:
                app.blockR = False
            if app.currentMario == app.runningLeft or app.currentMario == app.tallStandingMario:
                    app.blockR = False
            for j in range(app.barriersList[i][1], app.barriersList[i][3]):
                if int(app.marioBounds[3]) - 10 == j:
                    inRangeL = True
            if inRangeL==True:
                for k in range(app.barriersList[i][0]-app.scrollX, app.barriersList[i][2]-app.scrollX):
                    if app.marioBounds[0] - 5 == k:
                        inXRangeL = True
            if inRangeL == True and inXRangeL == True:
                app.blockL = True
            if app.isJumping == True or app.isFalling == True and app.marioBounds[3] < 137:
                app.blockL = False
            if app.currentMario == app.runningRight or app.currentMario == app.tallRunningRight:
                app.blockL = False
#standing on top and hitting head on bricks and power blocks
def standCollision(app):
    for i in range(len(app.barriersList)):
            inRange, inXRange = False, False
            for j in range(app.barriersList[i][1]-17, app.barriersList[i][3]-17):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.barriersList[i][0]-app.scrollX, app.barriersList[i][2]-app.scrollX):
                    if k in range(app.marioBounds[0], app.marioBounds[2]):
                        inXRange = True    
            if inRange == True and inXRange == True and app.marioBounds[3] < 140:
                app.isJumping, app.isFalling, app.gravity = False, False, True
                app.cFloor = app.barriersList[i][1] - 10
                app.currentX = app.scrollX
            if app.scrollX > app.currentX+8 or app.scrollX < app.currentX-8:
                app.cFloor = 160
                app.isFalling, app.gravity = True, True
                app.currentX = app.scrollX
    for i in range(len(app.barriersList)):
            inRange, inXRange = False, False
            for j in range(app.barriersList[i][1]+17, app.barriersList[i][3]+17):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.barriersList[i][0]-app.scrollX, app.barriersList[i][2]-app.scrollX):
                    if k in range(app.marioBounds[0], app.marioBounds[2]):
                        inXRange = True    
            if inRange == True and inXRange == True and app.isJumping == True:
                app.isJumping, app.isFalling = False, True
                if app.barriersList[i] in app.powerList:
                    app.powerList.remove(app.barriersList[i])
                    choose = random.randint(0, 2)
                    if choose == 0 or choose == 1:
                        app.mushroomLocations.append([app.barriersList[i][0], app.barriersList[i][1]-17
                        , app.barriersList[i][2], app.barriersList[i][1]])
                    if choose == 2:
                        app.starLocations.append([app.barriersList[i][0], app.barriersList[i][1]-17
                        , app.barriersList[i][2], app.barriersList[i][1]])
#checking if mario/goomba fall into gaps
def gapCollision(app):
    #MARIO
    for i in range(len(app.gapList)):
            inRange, inXRange = False, False
            for j in range(app.gapList[i][1]-17, app.gapList[i][3]-17):
                if int(app.marioBounds[3]) - 10 == j:
                    inRange = True
            if inRange==True:
                for k in range(app.gapList[i][0]-app.scrollX, app.gapList[i][2]-app.scrollX):
                    if app.marioBounds[2] - 10 == k:
                        inXRange = True    
            if inRange == True and inXRange == True:
                app.isFalling, app.gap = False, True
                app.fell = 2000
    #GOOMBA
    for i in range(len(app.gapList)):
            inRange, inXRange = False, False
            for j in range(app.gapList[i][0]-app.scrollX, app.gapList[i][2]-app.scrollX):
                for k in range(len(app.goombaLocations)):
                    if app.goombaLocations[k] - app.scrollX- app.goombaX == j:
                        app.goombaLocations[k] = -200
#mario colliding with mushrooms
def mushroomCollision(app):
    for i in range(len(app.mushroomLocations)):
            inRange, inXRange = False, False
            for j in range(app.mushroomLocations[i][1], app.mushroomLocations[i][3]):
                for k in range(int(app.marioBounds[1]),int(app.marioBounds[3])):
                    if k == j:
                        inRange = True
            if inRange==True:
                for k in range(app.mushroomLocations[i][0]-app.scrollX, app.mushroomLocations[i][2]-app.scrollX):
                    for j in range(app.marioBounds[0], app.marioBounds[2]):
                        if j == k:
                            inXRange = True
            if inRange == True and inXRange == True:
                app.isTall, app.isStar = True, False
                app.currentMario = app.tallStandingMario
                app.mushroomLocations.pop(i)
                break
#mario colliding with stars
def starCollision(app):
    for i in range(len(app.starLocations)):
            inRange, inXRange = False, False
            for j in range(app.starLocations[i][1], app.starLocations[i][3]):
                for k in range(int(app.marioBounds[1]),int(app.marioBounds[3])):
                    if k == j:
                        inRange = True
            if inRange==True:
                for k in range(app.starLocations[i][0]-app.scrollX, app.starLocations[i][2]-app.scrollX):
                    for j in range(app.marioBounds[0], app.marioBounds[2]):
                        if k == j:
                            inXRange = True
            if inRange == True and inXRange == True:
                app.isTall, app.isStar = False, True
                app.currentMario = app.starStandingMario
                app.starLocations.pop(i)
                app.startTimer = app.scrollX
                break
#hammers hitting mario
def hammerCollision(app):
    if app.hammerLocation != []:
        if int(app.hammerLocation[0][0]) in range(app.marioBounds[0]-2, app.marioBounds[2]+2):
            if int(app.hammerLocation[0][1]) in range(int(app.marioBounds[1])-2, int(app.marioBounds[3])+2):
                if app.isStar == True:
                    pass
                elif app.isTall == True:
                    app.isTall = False
                    app.currentMario = app.standingMario
                    app.hammerLocation = []
                    app.count = 1
                else:
                    app.gameOver = True
            app.hammerLocation = []
            app.count = 1

#hammerbros hitting mario
def hammerBroCollision(app):
    for i in range(len(app.hammerBrosLocation)):
        if app.isStar == True:
            locationNow = app.hammerBrosLocation[i]-app.scrollX+app.hammerX
            if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[3] < 119 and app.marioBounds[3] > 90: 
                app.hammerBrosLocation[i] = -200
        elif app.isTall == False:
            locationNow = app.hammerBrosLocation[i]-app.scrollX+app.hammerX
            if locationNow > app.marioBounds[0]-5 and locationNow < app.marioBounds[2]+5 and app.marioBounds[3] < 119 and app.marioBounds[3] > 80: 
                app.gameOver = True
        elif app.isTall == True:
            locationNow = app.hammerBrosLocation[i]-app.scrollX+app.hammerX
            if locationNow > app.marioBounds[0]-5 and locationNow < app.marioBounds[2]+5 and app.marioBounds[3] < 119 and app.marioBounds[3] > 90: 
                app.gameOver = True

#goombas hitting mario
def goombaCollision(app):
    for i in range(len(app.goombaLocations)):
        if app.isStar == True:
            locationNow = app.goombaLocations[i]-app.scrollX-app.goombaX
            if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[1] > 115: 
                app.goombaLocations[i] = -200
        elif app.isTall == False:
            locationNow = app.goombaLocations[i]-app.scrollX-app.goombaX
            if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[3] < 153 and app.marioBounds[3] > 145 and app.isFalling == True:
                app.goombaLocations[i] = -200
            if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[3] < 170 and app.marioBounds[3] > 153: 
                app.gameOver = True
        elif app.isTall == True:
            locationNow = app.goombaLocations[i]-app.scrollX-app.goombaX
            if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[3] < 153 and app.marioBounds[3] > 145 and app.isFalling == True:
                app.goombaLocations[i] = -200
            if locationNow > app.marioBounds[0] and locationNow < app.marioBounds[2] and app.marioBounds[3] < 170 and app.marioBounds[3] > 153: 
                app.isTall = False
                app.currentMario = app.standingMario
                app.goombaLocations[i] = -200

def keyPressed(app, event):
    if app.win == False:
        if (event.key == 'Left' or event.key =='a'):
            if app.scrollX > 2:
                if app.blockL == False:
                    app.scrollX -= 2
                app.currentMario = app.runningLeft
                if app.isTall == True:
                    app.currentMario = app.tallRunningLeft
                if app.isStar == True:
                    app.currentMario = app.starRunningLeft
                app.isRunning = True
        if (event.key == 'Right' or event.key == 'd'):
            app.currentMario = app.runningRight
            if app.isTall == True:
                app.currentMario = app.tallRunningRight
            if app.isStar == True:
                app.currentMario = app.starRunningRight    
            app.isRunning = True
            if app.blockR == False:
                app.scrollX += 2
        if ((event.key == 'Up' or event.key == 'w') and app.isJumping == False and app.isFalling == False):
            app.isJumping, app.isFalling, app.gravity = True, False, True
    if (event.key == 'p'):
        app.isTall, app.isStar = False, True
        app.currentMario = app.starStandingMario
        app.startTimer = app.scrollX
    if (event.key == 'o'):
        app.isTall, app.isStar = True, False
        app.currentMario = app.tallStandingMario
    if (event.key == 'r'):
        runApp(width=600, height=200)
def keyReleased(app, event):
    if (event.key == 'Right' or event.key == 'd'):
        app.isRunning = False
    if (event.key == 'Left' or event.key == 'a'):
        app.isRunning = False

#taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def timerFired(app):
    app.spriteCounter = (1+app.spriteCounter) % len(app.runningRight)
    app.spriteCounterH = (1+app.spriteCounterH) % len(app.hammer)

    #goomba movement
    if app.goombaX > 80:
        app.goombaMove = False
    if app.goombaX < 17:
        app.goombaMove = True
    if app.goombaMove == True:
        app.goombaX += 3
    if app.goombaMove == False:
        app.goombaX -= 3
    
    #hammer bro movement
    if app.hammerX == 15:
        app.hammerMove = False
    if app.hammerX == -15:
        app.hammerMove = True
    if app.hammerMove == True:
        app.hammerX += 3
        app.currentHammers = app.hammerBrosLeft
    if app.hammerMove == False:
        app.hammerX -= 3
        app.currentHammers= app.hammerBrosRight

    #hammer movement
    for i in range(len(app.hammerBrosLocation)):
        if app.count == 1 and (app.marioLocation[0]-(app.hammerBrosLocation[i]-app.scrollX+app.hammerX)) < -100 and (
            (app.marioLocation[0]-(app.hammerBrosLocation[i]-app.scrollX+app.hammerX)) > -200):
            app.hammerLocation.append([app.hammerBrosLocation[i]-app.scrollX+app.hammerX, 90])
            app.count = 0
            app.currentMarioX, app.currentMarioY = app.marioLocation[0], app.marioLocation[1]
            app.currentHLocX, app.currentHLocY = app.hammerLocation[0][0], app.hammerLocation[0][1]
    for i in range(len(app.hammerLocation)):
        app.hammerLocation[i][0] = app.hammerLocation[i][0] - (app.currentHLocX - app.currentMarioX)/10
        app.hammerLocation[i][1] = app.hammerLocation[i][1] - (app.currentHLocY - app.currentMarioY)/10
        

    #initial drop
    if app.isStart == True:
        app.marioLocation[1] += 4.5
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
        elif app.marioLocation[1] < app.cFloor-12:
            app.marioLocation[1] -= 13
        elif app.marioLocation[1] < app.cFloor+7:
            app.marioLocation[1] -= 16
        if app.marioLocation[1] <= app.cFloor-77:
            app.isJumping = False
            app.isFalling = True
    #gravity
    if app.gravity == True:
        if app.marioLocation[1] < app.cFloor:
            app.marioLocation[1] += .5
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
        elif app.marioLocation[1] <= app.cFloor-22:
            app.marioLocation[1] += 8
        elif app.marioLocation[1] < app.cFloor-10:
            app.marioLocation[1] += 9
        elif app.marioLocation[1] < app.cFloor-2:
            app.marioLocation[1] += 4
            if app.marioLocation[1] >= app.cFloor-.5:
                app.isFalling = False
    #setting marios location
    app.marioBounds[1] = app.marioLocation[1]-10
    app.marioBounds[3] = app.marioLocation[1]+10    

    #setting marios state
    if app.isRunning != True and app.isFalling != True and app.isJumping != True and app.isTall != True:
        app.currentMario = app.standingMario

    if app.isTall == True and app.isRunning != True and app.isFalling != True and app.isJumping != True:
        app.currentMario = app.tallStandingMario
    
    if app.isStar == True and app.isRunning != True and app.isFalling != True and app.isJumping != True:
        app.currentMario = app.starStandingMario
    
    #running all function
    if app.isStar == False:
        barrierCollision(app)
    hammerBroCollision(app)
    goombaCollision(app)
    standCollision(app)
    mushroomCollision(app)
    starCollision(app)
    gapCollision(app)
    hammerCollision(app)

    #ending star mode
    if app.scrollX - app.startTimer > 400:
        app.startTimer = 3000
        app.isStar, app.isTall = False, True
        app.currentMario = app.tallStandingMario

    #win condition
    if app.marioBounds[2] + app.scrollX > 1380:
        app.win = True
    
#drawing image background
def drawBack(app, canvas):
    canvas.create_image(300-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))
    canvas.create_image(900-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))
    canvas.create_image(1500-app.scrollX, 100, image=ImageTk.PhotoImage(app.back))

#drawing objects in background
def drawBackground(app, canvas):
    for i in range(len(app.terrain)):
        for j in range(0+int(app.scrollX/17), len(app.terrain[i])-70+int(app.scrollX/17)):
            if app.terrain[i][j] == 'brick':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.brick))
            if app.terrain[i][j] == 'power':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.power))
            if app.terrain[i][j] == 'skyDraw':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.sky))

#drawing mario
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

#drawing powerups
def drawPowerups(app, canvas):
    for i in range(len(app.mushroomLocations)):
        canvas.create_image(app.mushroomLocations[i][0]-app.scrollX+8.5, app.mushroomLocations[i][1]+8.5, image=ImageTk.PhotoImage(app.mushroom))
    for i in range(len(app.starLocations)):
        canvas.create_image(app.starLocations[i][0]-app.scrollX+8.5, app.starLocations[i][1]+8.5, image=ImageTk.PhotoImage(app.star))

#drawing enemies
def drawEnemies(app, canvas):
    for i in range(len(app.goombaLocations)):
        if app.goombaLocations[i] in range(0+app.scrollX, 600+app.scrollX):
            canvas.create_image(app.goombaLocations[i]-app.goombaX-app.scrollX,160,image=ImageTk.PhotoImage(app.goomba))
    for i in range(len(app.hammerBrosLocation)):
        if int(app.hammerBrosLocation[i]) in range(0+app.scrollX, 600+app.scrollX):
            sprite = app.currentHammers[app.spriteCounter]
            canvas.create_image(app.hammerBrosLocation[i]-app.scrollX+app.hammerX,90, image=ImageTk.PhotoImage(sprite))
        for j in range(len(app.hammerLocation)):
            spriteH = app.hammer[app.spriteCounterH]
            canvas.create_image(app.hammerLocation[0][0], app.hammerLocation[0][1], image=ImageTk.PhotoImage(spriteH))
    
#drawing game over screen
def drawGameOver(app, canvas):
    canvas.create_rectangle(0,0,600,200, fill='Black')
    canvas.create_text(300,100,text='Game Over', fill = 'White')

#drawing win screen
def drawWin(app, canvas):
    canvas.create_rectangle(0,0,600,200, fill='White')
    canvas.create_text(300,100,text='You win!', fill = 'Black')


def redrawAll(app, canvas):
    drawBack(app, canvas)
    drawBackground(app, canvas)
    drawMario(app, canvas)
    drawEnemies(app, canvas)
    drawPowerups(app, canvas)
    if app.gameOver == True:
        drawGameOver(app, canvas)
    if app.win == True:
        drawWin(app, canvas)
def playMario():
    runApp(width=600, height=200)
playMario()