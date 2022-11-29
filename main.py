from characters import *
from cmu_112_graphics import *
import random

def appStarted(app):
    app.timerDelay = 10
    spritestrip = app.loadImage('img/mainsprite.png')
    app.sprites = spritestrip
    app.gameOver = False
    #background
    app.width = 3000
    app.height = 200
    app.tileSize = 17
    app.terrain = []
    app.sky = app.sprites.crop((800,520,840,560))
    brickLoad = app.sprites.crop((110,25,150,65))
    app.brick = app.scaleImage(brickLoad, .5)
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
    app.isJumping = False
    app.isFalling = True
    app.isRunning = False
    app.marioLocation = [200,120]
    app.current = app.marioLocation[1]

    #GOOMBA APP ITEMS
    app.goomba_load = spritestrip.crop((100, 1318, 160, 1350))
    app.goomba = app.scaleImage(app.goomba_load, .66)
    app.goombaX = 0
    app.goombaAutoCount = 7
    app.goombaLocations = []
    app.gStart = 300
    for i in range(app.goombaAutoCount):
        app.goombaLocations.append(app.gStart*(i+1))
    loadTerrain(app)

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
    if (event.key == 'Up'):
        app.isJumping = True
        app.isFalling = False

def keyReleased(app, event):
    if (event.key == 'Right'):
        app.isRunning = False
    if (event.key == 'Left'):
        app.isRunning = False

#taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def timerFired(app):
    app.spriteCounter = (1+app.spriteCounter) % len(app.runningRight)
    if app.goombaX > 75:
        app.goombaMove = False
    if app.goombaX == 0:
        app.goombaMove = True
    if app.goombaMove == True:
        app.goombaX += 1
    if app.goombaMove == False:
        app.goombaX -= 1

    #gravity
    if app.marioLocation[1] <= 157:
        app.marioLocation[1] += 2
    #falling
    if app.marioLocation[1] <= 157 and app.isFalling == True:
        if app.currentMario != app.jumpingMario:
            app.currentMario = app.jumpingMario
        app.marioLocation[1] += 8
        if app.marioLocation[1] >= 155:
            app.isFalling = False
    #jumping
    if app.isJumping == True:
        if app.currentMario != app.jumpingMario:
            app.currentMario = app.jumpingMario
        app.marioLocation[1] -= 10
        if app.marioLocation[1] <= app.current-40:
            app.isJumping = False
            app.isFalling = True
    if app.isRunning != True and app.isFalling != True and app.isJumping != True:
        app.currentMario = app.standingMario

    #collisions
    for location in app.goombaLocations:
        locationNow = location-app.scrollX+app.goombaX
        if locationNow > 186 and locationNow < 214 and (app.currentMario == app.standingMario or 
        app.currentMario == app.runningRight or app.currentMario == app.runningLeft): 
            app.gameOver = True

#generating terrain
def loadTerrain(app):
    for x in range(int((app.height)/app.tileSize)+1):
        app.terrain.append([])
        for y in range(int(app.width/app.tileSize)):
            if x>9:
                app.terrain[x].append('brick')
            else:
                app.terrain[x].append('sky')
def loadTerrainSolver(app):
    rows, cols = len(app.terrain), len(app.terrain[0])

def isLegal(app):
    pass

def drawBackground(app, canvas):
    for i in range(len(app.terrain)):
        for j in range(len(app.terrain[i])):
            if app.terrain[i][j] == 'sky':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i,image=ImageTk.PhotoImage(app.sky))
            if app.terrain[i][j] == 'brick':
                canvas.create_image(10+app.tileSize*j-app.scrollX, 10+app.tileSize*i, image=ImageTk.PhotoImage(app.brick))

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
    for i in range(app.goombaAutoCount):
        canvas.create_image((app.gStart*(i+1))-app.scrollX+app.goombaX,160,image=ImageTk.PhotoImage(app.goomba))

def drawGameOver(app, canvas):
    canvas.create_rectangle(0,0,600,200, fill='Black')
    canvas.create_text(300,100,text='Game Over', fill = 'White')

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawMario(app, canvas)
    drawGoomba(app, canvas)
    if app.gameOver == True:
        drawGameOver(app, canvas)
def playMario():
    runApp(width=600, height=200)
playMario()