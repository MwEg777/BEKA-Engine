import pygame
from pygame import mixer
from BekaEngine import *
import random
from OpenGL.GLUT import *
import numpy
import time


time_interval = 10  # try  1000 msec
mouse_x = 0
mouse_y = 0

screenwidth = 800
screenheight = 800


button1 = UI()  # UI Class has GameObject Properties plus additional ones, such as (hover detection)

poopy = GameObject()
poopy.setName("Poopy Butthole")
poopysprite = SpriteRenderer(poopy)
poopyrb = RigidBody(poopy)

rick = GameObject()
rick.setName("Rick")
ricksprite = SpriteRenderer(rick)

backGround = GameObject()
backGround.setName("Background")
backGroundSprite = SpriteRenderer(backGround)

gameImages = None


def init():
    # glutSetCursor(GLUT_CURSOR_NONE) # Enable when game development ends.

    glClearColor(1, 1, 1, 0.5)
    glMatrixMode(GL_MODELVIEW)

    mixer.init(frequency=48000)
    sound = mixer.Sound("ohwe.wav")
    # sound.play()  # Sound Importing Functions.

    global gameImages
    gameImages = GameImages(["bg.png", "pb.png", "Font1.png"])  # Only one instance is needed!

    backGround.Instantiate([0, 0, 0], [20, 20, 1], 0)  # Position, Scale, Rotation

    poopy.Instantiate([0, 0, 0], [1, 1, 1], 0)
    poopy.smoothDamping = False
    rick.Instantiate()  # Depends on mouse movement, no need to enter parameters.
    rick.setScale([3,3,1])

    button1.Create("button")
    button1.gameObject.move([0,0.25,0],1,1,False)
    button1.setOnClick(buttonTest)  # What the button does - calls the function.

redChange = 0
greenChange = 0
blueChange = 0#--
redTarget = 0
greenTarget = 0
blueTarget = 0#--
redCurrent = 0
greenCurrent = 0
blueCurrent = 0#--
redFlag = True
greenFlag = True
blueFlag = True
bgColor = [0.1,0.1,0.1,1]   # Colors Initialization for the next function vvv (Expand)
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
        redChange = random.uniform(0.0001,0.001)  # Generates a "speed" for which the color changes.
        redTarget = random.uniform(0,1)           # Generates a degree of the color: RED
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


def PassiveMotionFunc(x, y):
    global mouse_x
    global mouse_y

    mouseYToWorld = (((glutGet(GLUT_WINDOW_HEIGHT) / 2) - y) / (glutGet(GLUT_WINDOW_HEIGHT) / 2))
    mouseXToWorld = ((x - (glutGet(GLUT_WINDOW_WIDTH) / 2)) / (glutGet(GLUT_WINDOW_WIDTH) / 4))

    mouse_x = x
    mouse_y = y
    rick.move([ mouseXToWorld, mouseYToWorld, rick.getPos()[2]],0.05,0.05)  # Pos, SpeedX, SpeedY


def buttonTest():
    print("Just clicked my button!")

def MotionFunc(x,y):  # Moving Mouse While Holding Button
    global mouse_x
    global mouse_y
    mouse_x = x
    mouse_y = y


def MouseMotion(button,state,x,y):  # Triggers with both MouseClick Down or Up
    print("State changed! state now is", state)
    for ui in UIs:
        if ui.type == "button":
            ui.state = state


def arrow_key(key, x, y):
    pass


def keyboard(key, x, y):
    if key == b"d":
        poopyrb.AddForce(0.005,[1,0])
    elif key == b"a":
        poopyrb.AddForce(0.005, [-1, 0])
    elif key == b"w":
        poopyrb.AddForce(0.01, [0, 1])
    elif key == b"s":
        poopyrb.AddForce(0.005, [0, -1])
    if key == b"f":
        poopysprite.FlipX()
    if key == b"g":
        poopysprite.FlipY() # Mouse and Keyboard Functions

def Update():
    global rotation
    global poopy
    global barsprite
    global poopysprite
    global rick
    global ricksprite
    global bgColor
    global gameImages
    glClear(GL_COLOR_BUFFER_BIT)

    gameImages.curImage(1)  # Load Gradient initial Background, and apply the following effects.
    backGroundSprite.DrawSprite(0, 1, 0, 1, 1)  # x1, x2, y1, y2, aspect ratio
    backgroundColorChanger()
    backGroundSprite.setColor(bgColor)

    gameImages.curImage(2) # SpritesSHEET
    ricksprite.DrawSprite(0.0478515625, 0.126953125, 0.99365234375, 0.91455078125, 1)
    poopysprite.DrawSprite(0, 0.0317, 0.908203125, 1, 0.34574468085106382978723404255319)
    poopyrb.simulate() # Simulate: Simulate physics for the rigid body every frame.

    gameImages.curImage(3) #Fonts
    drawText("abcdefghijklmnopqrstuvwxyz",[-1,0.5,0],0.5)
    drawText("AbCdEfGhIjKlMnOpQrStUvWxYz", [-1, 0.625, 0], 0.5,[0.5,0,0.5,1])   # (Text, Position, Size, Color)
    drawText("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [-1, 0.75, 0], 0.5,[0.5,0.5,0,1])
    drawText("WHAT IS YOUR NAME?", [-1, -0.25, 0], 0.5,[0,0.5,0.5,1])
    drawText("Score:9005", [-1.75, 0.9, 0], 0.5,[0,0.5,0.5,1])  #Score text

    gameImages.curImage(2)
    button1.DrawUI(mouse_x,mouse_y,0.1375,0.325,0.885,0.93375,3.8461538461538463)   # Mouse location for detection, x1, x2, y1, y2, aspect ratio

    glFlush()