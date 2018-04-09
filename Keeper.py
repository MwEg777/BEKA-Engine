import pygame
from pygame import mixer
from BekaEngine import *
import random
from OpenGL.GLUT import *
import time
x = 0
time_interval = 10  # try  1000 msec

screenwidth = 800
screenheight = 800

rotation = 0
poopy = GameObject()
poopy.setName("Poopy Butthole")
rick = GameObject()
rick.setName("Rick")
poopysprite = SpriteRenderer(poopy)
ricksprite = SpriteRenderer(rick)
backGround = GameObject()
backGround.setName("Background")
backGroundSprite = SpriteRenderer(backGround)
gameImages = None
def init():
    global modelViewMatrix
    #glutSetCursor(GLUT_CURSOR_NONE)
    glClearColor(1, 1, 1, 0.5)
    glMatrixMode(GL_MODELVIEW)
    mixer.init(frequency=48000)
    sound = mixer.Sound("ohwe.wav")
    sound.play()
    global gameImages
    gameImages = GameImages(2)
    gameImages.addImage("BG.png")
    gameImages.addImage("pb.png")



    gameImages.curImage(0)
    backGround.Instantiate([0,0,0],[1,1,1],0)
    backGround.setScale([20, 20, 1])

    gameImages.curImage(0)

    poopy.Instantiate([0, -0.5, 0], [1, 1, 1],0)
    poopy.setScale([1,1,1])
    rick.Instantiate([0,0.5,0],[1,1,1],0)
    rick.setScale([3,3,1])




    
pboffsetx = 0.9
pboffsety = 1.5
pbwidth = 0.2 #CharachterWidth
pbheight = 0.4
pbposx = 0
pbposy = -0.6
keeperwidth = 0.5
keeperheight = 0.4
keeperoffsetx = 0.9
keeperoffsety = 0.9

bgColor = [0.1,0.1,0.1,1]
bgChanger = [0,0,0,0,0,0]
def draw():
    global pboffsetx
    global pboffsety
    global x
    global pbwidth
    global pbheight
    global pbposx
    global pbposy
    global keeperoffsetx
    global keeperoffsety
    global keeperwidth
    global keeperheight
    global rotation
    global poopy
    global poopysprite
    global rick
    global ricksprite
    global bgColor
    global gameImages

    glClear(GL_COLOR_BUFFER_BIT)
    gameImages.curImage(0)
    backGroundSprite.DrawSprite(0, 1, 1, 0, 1)
    backgroundColorChanger()
    backGroundSprite.setColor(bgColor)
    gameImages.curImage(1)
    ricksprite.DrawSprite(0.0478515625, 0.126953125, 0.99365234375, 0.91455078125, 1)
    poopysprite.DrawSprite(0, 0.0317, 0.908203125, 1, 0.34574468085106382978723404255319)


    glFlush()
    #print("Rick position is: " ,rick.getPos())


    x += 0.01


mouse_x = 0
mouse_y = 0

redChange = 0
greenChange = 0
blueChange = 0
redTarget = 0
greenTarget = 0
blueTarget = 0
redCurrent = 0
greenCurrent = 0
blueCurrent = 0
redFlag = True
greenFlag = True
blueFlag = True
def backgroundColorChanger():
    global redChange
    global greenChange
    global blueChange
    global redTarget
    global greenTarget
    global blueTarget
    global redCurrent
    global greenCurrent
    global blueCurrent
    global bgColor
    global redFlag
    global greenFlag
    global blueFlag

    if redFlag:
        redChange = random.uniform(0.0001,0.001)
        redTarget = random.uniform(0,1)
        if redTarget < redCurrent:
            redChange *= -1
        redFlag = False
    redCurrent += redChange
    if (redChange < 0 and redCurrent <= redTarget) or (redChange > 0 and redCurrent >= redTarget):
        redFlag = True

    if greenFlag:
        greenChange = random.uniform(0.0001,0.001)
        greenTarget = random.uniform(0, 1)
        if greenTarget < greenCurrent:
            greenChange *= -1
        greenFlag = False
    greenCurrent += greenChange
    if (greenChange < 0 and greenCurrent <= greenTarget) or (greenChange > 0 and greenCurrent >= greenTarget):
        greenFlag = True

    if blueFlag:
        blueChange = random.uniform(0.0001,0.001)
        blueTarget = random.uniform(0, 1)
        if blueTarget < blueCurrent:
            blueChange *= -1
        blueFlag = False
    blueCurrent += blueChange
    if (blueChange < 0 and blueCurrent <= blueTarget) or (blueChange > 0 and blueCurrent >= blueTarget):
        blueFlag = True

    bgColor = [bgColor[0] + redChange, bgColor[1] + greenChange, bgColor[2] + blueChange, 1]


def PassiveMotionFunc(x, y):  # Moving Mouse Without Holding Button
    global mouse_x
    global mouse_y
    global screenwidth
    global screenheight
    mouse_x = x
    mouse_y = y
    rick.move([((mouse_x - (glutGet(GLUT_WINDOW_WIDTH) / 2)) / (glutGet(GLUT_WINDOW_WIDTH) / 4)),
               (((glutGet(GLUT_WINDOW_HEIGHT) / 2) - mouse_y) / (glutGet(GLUT_WINDOW_HEIGHT) / 2))
                  ,rick.getPos()[2]],0.05,0.05)


def MotionFunc(x,y):  # Moving Mouse While Holding Button
    pass


def MouseMotion(button,state,x,y):  # Triggers with both MouseClick Down or Up
    pass


curwidth = 0.1
curheight = 0
def arrow_key(key, x, y):
    global curwidth
    global curheight

    if key == 100:  # left

        if (curwidth > 0):
            curwidth -=0.01
        poopysprite.setDensity(curwidth)
        print("I clicked left, curwidth now is: ", curwidth)

    elif key == 102:  # right

        if (curwidth < 1):
            curwidth += 0.01
        poopysprite.setDensity(curwidth)
        print("I clicked right, curwidth now is: ", curwidth)

    elif key == 103: # down

        if (curheight > 0):
            curheight -=0.01
        poopysprite.setHeight(curheight)
        print("I clicked down, curheight now is: ", curheight)

    elif key == 101:  # up

        if (curheight < 1):
            curheight += 0.01
        poopysprite.setHeight(curheight)
        print("I clicked up, curheight now is: ", curheight)

curPosx = 0
curPosy = 0
def keyboard(key, x, y):
    global curPosx
    global curPosy
    if key == b"d":
        poopy.move([1.5,poopy.getPos()[1],0],0.1,0.1,False)
    elif key == b"a":
        poopy.move([-0.4, poopy.getPos()[1], 0], 0.1, 0.1,True)
    elif key == b"w":
        poopy.move([poopy.getPos()[0], 0.4, 0], 0.1, 0.1,False)
    elif key == b"s":
        poopy.move([poopy.getPos()[0], -0.4, 0], 0.1, 0.1,True)
    if key == b"f":
        poopysprite.FlipX()
    if key == b"g":
        poopysprite.FlipY()
    if key== b"r":
        if poopy.angle == 45:
            poopy.RotateObject(0,1)
        else:
            poopy.RotateObject(45, 1)
        if rick.angle == 45:
            rick.RotateObject(0,1)
        else:
            rick.RotateObject(45, 1)
    #if key== b"m":
        #poopy.targetPosition = [1,0,0]

