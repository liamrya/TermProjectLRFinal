from characters import *
from cmu_112_graphics import *
def appStarted(app):
    spritestrip = app.loadImage('img/mainsprite.png')
    app.gameOver = False

    #MARIO APP ITEMS
    app.mario_load = spritestrip.crop((10, 895, 60, 940))
    app.standingMario = app.scaleImage(app.mario_load, .66)
    #taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    app.runningRight = []
    app.runningLeft = []
    for i in range(3):
        sprite = spritestrip.crop((165+i*40, 895, 200+i*40, 940))
        spriteScale = app.scaleImage(sprite, .66)
        app.runningRight.append(spriteScale)
    for i in range(3):
        sprite = spritestrip.crop((165+i*40, 895, 200+i*40, 940))
        spriteScale = app.scaleImage(sprite, .66)
        spriteScaleTransposed = spriteScale.transpose(Image.FLIP_LEFT_RIGHT)
        app.runningLeft.append(spriteScaleTransposed)
    app.spriteCounter = 0
    app.currentMario = app.standingMario
    app.scrollX = 0
    app.isJumping = False
    app.isFalling = False

    #GOOMBA APP ITEMS
    app.goomba_load = spritestrip.crop((100, 1318, 160, 1350))
    app.goomba = app.scaleImage(app.goomba_load, .66)
    app.goombaX = 0
    app.goombaAutoCount = 7
    app.goombaLocations = []
    for i in range(app.goombaAutoCount):
        app.goombaLocations.append(300*(i+1))

def keyPressed(app, event):
    if (event.key == 'Left'):
        if app.scrollX > 3:
            app.scrollX -= 3
            app.currentMario = app.runningLeft
    if (event.key == 'Right'):
        app.currentMario = app.runningRight
        app.scrollX += 3
    if (event.key == 'r'):
        runApp(width=600, height=200)
    if (event.key == 'Up'):
        pass

def keyReleased(app, event):
    if (event.key == 'Right'):
        app.currentMario = app.standingMario
    if (event.key == 'Left'):
        app.currentMario = app.standingMario

#taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def timerFired(app):
    app.spriteCounter = (1+app.spriteCounter) % len(app.runningRight)
    if app.goombaX > 75:
        app.goombaMove = False
    if app.goombaX == 0:
        app.goombaMove = True
    if app.goombaMove == True:
        app.goombaX += 2
    if app.goombaMove == False:
        app.goombaX -= 2

    #collisions
    for location in app.goombaLocations:
        locationNow = location-app.scrollX+app.goombaX
        if locationNow > 196 and locationNow < 204 and app.currentMario == app.standingMario:
            app.gameOver = True
        if locationNow > 186 and locationNow < 214 and app.currentMario == app.runningRight:
            app.gameOver = True
        if locationNow > 186 and locationNow < 214 and app.currentMario == app.runningLeft:
            app.gameOver = True
def drawBackground(app, canvas):
    canvas.create_image(1670-app.scrollX,200, image=ImageTk.PhotoImage(Image.open('img/background.png')))

def drawMario(app, canvas):
    if app.currentMario == app.standingMario:
        canvas.create_image(200,160,image=ImageTk.PhotoImage(app.currentMario))
    if app.currentMario == app.runningRight:
        sprite = app.runningRight[app.spriteCounter]
        canvas.create_image(200, 160, image=ImageTk.PhotoImage(sprite))
    if app.currentMario == app.runningLeft:
        sprite = app.runningLeft[app.spriteCounter]
        canvas.create_image(200,160, image=ImageTk.PhotoImage(sprite))

def drawGoomba(app, canvas):
    for i in range(app.goombaAutoCount):
        canvas.create_image((300*(i+1))-app.scrollX+app.goombaX,160,image=ImageTk.PhotoImage(app.goomba))

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