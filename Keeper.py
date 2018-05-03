import pygame
from pygame import mixer
from BekaEngine import *
import random
from OpenGL.GLUT import *
from PowerUps_TestField import generatePowerUp, checkCollectibles
import numpy
import time

mouse_x = 0
mouse_y = 0

poopy = GameObject()
poopy.setName("Poopy Butthole")
poopysprite = SpriteRenderer(poopy)
poopycol = Collider(poopy,"circle", 0.15)

rick = GameObject()
rick.setName("Rick")
ricksprite = SpriteRenderer(rick)
rickcol = Collider(rick,"circle")

backGround = GameObject()
backGround.setName("Background")
backGroundSprite = SpriteRenderer(backGround)

gameImages = None

scene = "Menu"

#   Obstacles in order:
#   0: Long bar
#   1: Big Circle
obstaclesSprites = [
    [0.0275, 0.22875, 0.95375, 0.97375, 10.0625],
    [0.3975, 0.48625, 0.885, 0.97375, 1.0]
]
obstacles = list()

# ------------------------------------------------------------------------------------------------------

# MenuSceneStuff

menuBackGround = GameObject()
menuBackGround.setName("menuBackGround")
menuBackGroundSprite = SpriteRenderer(menuBackGround)

playButton = UI()
optionsButton = UI()
creditsButton = UI()
exitButton = UI()

bgy = 0
def init():

    #   PlayScene Stuff

    # ------------------------------------------------------------------------------------------------------

    # glutSetCursor(GLUT_CURSOR_NONE) # Enable when game development ends.

    glClearColor(1, 1, 1, 0.5)
    glMatrixMode(GL_MODELVIEW)

    mixer.init(frequency=48000)
    sound = mixer.Sound("ohwe.wav")
    # sound.play()  # Sound Importing Functions.

    global gameImages
    gameImages = GameImages(["bg.png", "SpriteSheet.png", "Font1.png", "Obstacles.png","menuBG.png"])  # Only one instance is needed!

    backGround.Instantiate([0, 0, 0], [20, 20, 1], 0)  # Position, Scale, Rotation

    poopy.Instantiate([0, -0.7, 0], [1, 1, 1], 0)
    poopy.setScale([3, 3, 1])
    poopy.smoothDamping = False

    rick.Instantiate()  # Depends on mouse movement, no need to enter parameters.
    rick.setScale([1.75, 1.75, 1])
    rickcol.radius = (rick.SpriteRenderer.density / 2) * rick.getScale()[0]

    # ------------------------------------------------------------------------------------------------------

    #   MenuScene Stuff

    # ------------------------------------------------------------------------------------------------------

    menuBackGround.Instantiate([0, 0, 0], [20, 20, 1], 0)

    # Play Button

    playButton.Create("button")
    playButton.gameObject.move([1.05,0.3,1],1,1,False)
    playButton.gameObject.setScale([3,3,1])
    playButton.hoverColor = playButton.normalColor
    playButton.pressedColor = playButton.normalColor
    playButton.setOnClick(playButtonFunc)

    # Options Button

    optionsButton.Create("button")
    optionsButton.gameObject.move([1.05, 0.1, 1], 1, 1, False)
    optionsButton.gameObject.setScale([5, 5, 1])
    optionsButton.hoverColor = optionsButton.normalColor
    optionsButton.pressedColor = optionsButton.normalColor
    optionsButton.setOnClick(optionsButtonFunc)

    # Credits Button

    creditsButton.Create("button")
    creditsButton.gameObject.move([1.05, -0.1, 1], 1, 1, False)
    creditsButton.gameObject.setScale([4, 4, 1])
    creditsButton.hoverColor = creditsButton.normalColor
    creditsButton.pressedColor = creditsButton.normalColor
    creditsButton.setOnClick(creditsButtonFunc)

    # Exit Button

    exitButton.Create("button")
    exitButton.gameObject.move([1.05, -0.3, 1], 1, 1, False)
    exitButton.gameObject.setScale([3, 3, 1])
    exitButton.hoverColor = exitButton.normalColor
    exitButton.pressedColor = exitButton.normalColor
    exitButton.setOnClick(exitButtonFunc)

    # ------------------------------------------------------------------------------------------------------


redChange = 0
greenChange = 0
blueChange = 0  # --
redTarget = 0
greenTarget = 0
blueTarget = 0  # --
redCurrent = 0
greenCurrent = 0
blueCurrent = 0  # --
redFlag = True
greenFlag = True
blueFlag = True
bgColor = [0.1, 0.1, 0.1, 1]  # Colors Initialization for the next function vvv (Expand)


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
        redChange = random.uniform(0.0001, 0.001)  # Generates a "speed" for which the color changes.
        redTarget = random.uniform(0, 1)  # Generates a degree of the color: RED
        if redTarget < redCurrent:
            redChange *= -1
        redFlag = False
    redCurrent += redChange
    if (redChange < 0 and redCurrent <= redTarget) or (redChange > 0 and redCurrent >= redTarget):
        redFlag = True

    if greenFlag:
        greenChange = random.uniform(0.0001, 0.001)
        greenTarget = random.uniform(0, 1)
        if greenTarget < greenCurrent:
            greenChange *= -1
        greenFlag = False
    greenCurrent += greenChange
    if (greenChange < 0 and greenCurrent <= greenTarget) or (greenChange > 0 and greenCurrent >= greenTarget):
        greenFlag = True

    if blueFlag:
        blueChange = random.uniform(0.0001, 0.001)
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
    rick.move([mouseXToWorld, mouseYToWorld, rick.getPos()[2]], 0.1, 0.05)  # Pos, SpeedX, SpeedY


def playButtonFunc():
    global scene
    scene = "Play"

def optionsButtonFunc():
    print("I pressed options")

def creditsButtonFunc():
    global scene
    scene = "Menu2"

def exitButtonFunc():
    exit(0)


def MotionFunc(x, y):  # Moving Mouse While Holding Button
    global mouse_x
    global mouse_y
    mouse_x = x
    mouse_y = y


def MouseMotion(button, state, x, y):  # Triggers with both MouseClick Down or Up
    #print("State changed! state now is", state)
    global scene
    for ui in UIs:
        if ui.type == "button":
            ui.state = state
    if state == 0 and scene is "Menu2":
        scene = "Menu"


def arrow_key(key, x, y):
    pass


def keyboard(key, x, y):
    #if key == b"d":
     #   poopyrb.AddForce(0.005, [1, 0])
    #elif key == b"a":
     #   poopyrb.AddForce(0.005, [-1, 0])
    #elif key == b"w":
     #   poopyrb.AddForce(0.01, [0, 1])
    #elif key == b"s":
     #   poopyrb.AddForce(0.005, [0, -1])
    if key == b"f":
        poopysprite.FlipX()
    if key == b"g":
        poopysprite.FlipY()  # Mouse and Keyboard Functions

def generateObstacle():
    global obstaclesSprites
    global obstacles
    obstacleInfo = None
    toGenerate = random.choice([0, 1])
    if toGenerate is 0:
        toGenerateScale = random.choice([1, 2, 3])
    elif toGenerate is 1:
        toGenerateScale = random.choice([4, 5, 6])
    toGeneratePosX = random.uniform(-2.5,2.5)
    obstacle = GameObject()
    obstacleSprite = SpriteRenderer(obstacle)
    obstacleRigidBody = RigidBody(obstacle)
    if toGenerate is 0:
        obstacleCollider = Collider(obstacle,"circle",0.1)
        obstacle.setName("Circle Obstacle")
    elif toGenerate is 1:
        obstacleCollider = Collider(obstacle, "box")
        obstacle.setName("Bar Obstacle")
    obstacleRigidBody.useGravity = True
    obstacleRigidBody.gravityScale = 0.65
    obstacle.Instantiate()
    obstacle.setScale([toGenerateScale,toGenerateScale,1])
    obstacle.move([toGeneratePosX, 1.2, 1], 1, 1, False)
    obstacles.append([obstacleSprite, obstacleRigidBody, obstacleCollider, toGenerate,toGeneratePosX,toGenerateScale])
    if toGeneratePosX >= 1:
        if toGenerate is 0 and toGenerateScale is not 1:
            obstacleRigidBody.AddForce(-0.005)
        else:
            obstacleRigidBody.AddForce(-0.01)
    if toGeneratePosX <= -1:
        if toGenerate is 0 and toGenerateScale is not 1:
            obstacleRigidBody.AddForce(0.005)
        else:
            obstacleRigidBody.AddForce(0.01)
    #Need to provide an array for each element
    #1/type whether box or circle or etc
    #2/X position
    #3/Scale of X and Y in order


obstacleDelay = 0
obstacleInterval = 2


def Update():
    global scene
    if scene == "Play":
        global rotation
        global poopy
        global barsprite
        global poopysprite
        global rick
        global ricksprite
        global bgColor
        global gameImages
        global obstacleDelay
        global obstacleInterval
        global bgy
        glClear(GL_COLOR_BUFFER_BIT)

        bgy += 0.0025
        if bgy >= 1:
            bgy = 0

        obstacleDelay += 1
        if (obstacleDelay / 60).is_integer() and (obstacleDelay / 60) > obstacleInterval:
            generateObstacle()
            print("Generated one obstacle!")

        gameImages.curImage(1)  # Load Gradient initial Background, and apply the following effects.
        backGroundSprite.DrawSprite(0, 1, 0 + bgy, 1 +bgy, 0.3)  # x1, x2, y1, y2, aspect ratio
        #backgroundColorChanger()
        #backGroundSprite.setColor(bgColor)

        gameImages.curImage(2)  # SpritesSHEET
        ricksprite.DrawSprite(0.1025 , 0.203 , 0.89625 , 0.99875 , 1.0)
        rickcol.checkCollision()
        # ----
        poopysprite.DrawSprite(0.0 , 0.1025 , 0.89625 , 1.0 , 1)
        # ----

        gameImages.curImage(3)  # Fonts
        drawText("Score: ", [-1.72, 0.9, 0], 0.5, [0.9, 0.2, 0.1, 1])   # (Text, Pos, Size, Color)


        gameImages.curImage(2)

        # ------------------------------------Powerups Generation Part--------------------------------------------------
        a = generatePowerUp(0, 1)
        if a is not None:
            pass
            # print("a:", a)   # you can add parameters: (time rate for generation = 10, score rate for generation = 0)
            checkCollectibles()

        # ------------------------------------------------------------------------------------------------------------------

        # ------------------------------------Obstacle Generation Part--------------------------------------------------
        gameImages.curImage(4)
        for obstacle in obstacles:  # For each obstacle in the obstacles array
            if obstacle[3] == 0:    # if obstacle generated type is Circle
                obstacle[0].DrawSprite(0.3975, 0.48625, 0.885, 0.97375, 1.0) # Draw the circle part of the sprite sheet
            elif obstacle[3] == 1:  # if obstacle generated type is Box
                obstacle[0].DrawSprite(0.0275, 0.22875, 0.95375, 0.97375, 10.0625)  # Draw box part of the sprite sheet
            obstacle[1].simulate()  # simulate object's rigid body physics
            if obstacle[0].gameObject.getPos()[1] <= -4: # If object is completely out of screen Y coordinates:
                obstacles.remove(obstacle)

        # ------------------------------------------------------------------------------------------------------------------

        print("Collision status: ", poopycol.checkCollision())

        for ob in obstacles:
            print(ob[2].checkCollision())

        glFlush()

    elif scene == "Menu":
        glClear(GL_COLOR_BUFFER_BIT)

        gameImages.curImage(5)
        menuBackGroundSprite.DrawSprite(0, 1, 0, 1, 1)  # x1, x2, y1, y2, aspect ratio
        gameImages.curImage(2)

        # Play button

        if playButton.Hovering and not playButton.Holding:
            playButton.DrawUI(mouse_x, mouse_y, 0.20375 , 0.28875 , 0.912 , 0.955 , 2.0606060606060606)
        elif playButton.Holding and playButton.Hovering:
            playButton.DrawUI(mouse_x, mouse_y, 0.20375 , 0.28875 , 0.87125 , 0.9125 , 2.0606060606060606)
        else:
            playButton.DrawUI(mouse_x,mouse_y,0.20375 , 0.28875 , 0.955 , 0.99875 , 2.0606060606060606)

        # Options button

        if optionsButton.Hovering and not optionsButton.Holding:
            optionsButton.DrawUI(mouse_x, mouse_y, 0.295 , 0.46375 , 0.87125 , 0.9125 , 4.354838709677419)
        elif optionsButton.Holding and optionsButton.Hovering:
            optionsButton.DrawUI(mouse_x, mouse_y, 0.295 , 0.46375 , 0.91625 , 0.955 , 4.354838709677419)
        else:
            optionsButton.DrawUI(mouse_x,mouse_y,0.295 , 0.46375 , 0.96 , 0.99875 , 4.354838709677419)

        # Credits button

        if creditsButton.Hovering and not creditsButton.Holding:
            creditsButton.DrawUI(mouse_x, mouse_y, 0.46875 , 0.605 , 0.875 , 0.915 , 3.40625)
        elif creditsButton.Holding and creditsButton.Hovering:
            creditsButton.DrawUI(mouse_x, mouse_y, 0.46875 , 0.605 , 0.91625 , 0.95625 , 3.40625)
        else:
            creditsButton.DrawUI(mouse_x,mouse_y, 0.46875 , 0.605 , 0.96 , 0.99875 , 3.40625)

        # Exit button

        if exitButton.Hovering and not exitButton.Holding:
            exitButton.DrawUI(mouse_x, mouse_y, 0.61125 , 0.7075 , 0.875 , 0.915 , 2.40625)
        elif exitButton.Holding and exitButton.Hovering:
            exitButton.DrawUI(mouse_x, mouse_y, 0.61125 , 0.7075 , 0.91625 , 0.95625 , 2.40625)
        else:
            exitButton.DrawUI(mouse_x,mouse_y,0.61125 , 0.7075 , 0.96 , 0.99875 , 2.40625)

        glFlush()

    elif scene == "Menu2":
        glClear(GL_COLOR_BUFFER_BIT)

        gameImages.curImage(5)
        menuBackGroundSprite.DrawSprite(0, 1, 0, 1, 1)  # x1, x2, y1, y2, aspect ratio
        gameImages.curImage(3)

        drawText("KARIM SALAH", [0.75,0.4,0],0.3,[0.2,0.2,1,1])
        drawText("OMAR EL LEBOUDY", [0.625, 0.3, 0], 0.3, [1, 0.2, 0.2, 1])
        drawText("BOLA FAHMI", [0.775, 0.2, 0], 0.3, [0, 0, 0, 1])
        drawText("AHMED REDA", [0.775, 0.1, 0], 0.3, [0, 0, 0, 1])
        drawText("KAREEM ALLAM", [0.7, 0, 0], 0.3, [0, 0, 0, 1])

        glFlush()