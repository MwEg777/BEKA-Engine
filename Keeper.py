import pygame
from pygame import mixer
from BekaEngine import *
import random
from OpenGL.GLUT import *
from PowerUps_TestField import generatePowerUp, checkCollectibles
import numpy
import os,time



mouse_x = 0
mouse_y = 0

poopy = GameObject()
poopy.setName("Poopy Butthole")
poopysprite = SpriteRenderer(poopy)
poopycol = Collider(poopy, "circle", 0.15)

rick = GameObject()
rick.setName("Rick")
ricksprite = SpriteRenderer(rick)
rickcol = Collider(rick, "circle")

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
creditsButton = UI()
exitButton = UI()

#   --------------
#   Sound files

owe = None
sadowe = None
choose = None
die = None
hitobstacle = None
hover = None
bgm = None

#   --------------


bgy = 0


def init():
    #   PlayScene Stuff

    # ------------------------------------------------------------------------------------------------------

    # glutSetCursor(GLUT_CURSOR_NONE) # Enable when game development ends.
    global owe
    global sadowe
    global choose
    global die
    global hitobstacle
    global hover
    global bgm
    glClearColor(1, 1, 1, 0.5)
    glMatrixMode(GL_MODELVIEW)

    mixer.init(frequency=44100)
    owe = mixer.Sound("ohwe.wav")
    sadowe = mixer.Sound("sadowe.wav")
    choose = mixer.Sound("choose.wav")
    die = mixer.Sound("die.wav")
    hitobstacle = mixer.Sound("hover.wav")
    bgm = mixer.Sound("bgmusic.wav")
    bgm.play(100)
    bgm.set_volume(0.5)
    # Sound Importing Functions.


    global gameImages
    gameImages = GameImages(
        ["bg.png", "SpriteSheet.png", "Font1.png", "Obstacles.png", "menuBG.png"])  # Only one instance is needed!

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
    playButton.gameObject.move([1.05, 0.3, 1], 1, 1, False)
    playButton.gameObject.setScale([3, 3, 1])
    playButton.hoverColor = playButton.normalColor
    playButton.pressedColor = playButton.normalColor
    playButton.setOnClick(playButtonFunc)

    # Credits Button

    creditsButton.Create("button")
    creditsButton.gameObject.move([1.05, 0, 1], 1, 1, False)
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
    if mouseYToWorld < 0.3:
        rick.move([mouseXToWorld, mouseYToWorld, rick.getPos()[2]], 0.1, 0.05)  # Pos, SpeedX, SpeedY
    else:
        rick.move([mouseXToWorld, 0.3, rick.getPos()[2]], 0.1, 0.05)  # Pos, SpeedX, SpeedY


def playButtonFunc():
    global scene
    global choose
    choose.play()
    scene = "Play"


def creditsButtonFunc():
    global scene
    global choose
    choose.play()
    scene = "Menu2"


def exitButtonFunc():
    global choose
    choose.play()
    exit(0)


def MotionFunc(x, y):  # Moving Mouse While Holding Button
    global mouse_x
    global mouse_y
    mouse_x = x
    mouse_y = y


def MouseMotion(button, state, x, y):  # Triggers with both MouseClick Down or Up
    # print("State changed! state now is", state)
    global scene
    for ui in UIs:
        if ui.type == "button":
            ui.state = state
    if state == 0:
        if scene is "Menu2":
            scene = "Menu"
        elif scene is "Score":
            exit(0)


def arrow_key(key, x, y):
    pass


def keyboard(key, x, y):
    # if key == b"d":
    #   poopyrb.AddForce(0.005, [1, 0])
    # elif key == b"a":
    #   poopyrb.AddForce(0.005, [-1, 0])
    # elif key == b"w":
    #   poopyrb.AddForce(0.01, [0, 1])
    # elif key == b"s":
    #   poopyrb.AddForce(0.005, [0, -1])
    if key == b"f":
        poopysprite.FlipX()
    if key == b"g":
        poopysprite.FlipY()  # Mouse and Keyboard Functions


def generateObstacle():
    global obstaclesSprites
    global obstacles
    toGenerate = random.choice([0, 1])
    if toGenerate is 0:
        toGenerateScale = random.choice([1, 2, 3])

    elif toGenerate is 1:
        toGenerateScale = random.choice([4, 5, 6])
    toGeneratePosX = random.uniform(-2.5, 2.5)
    obstacle = GameObject()
    obstacleSprite = SpriteRenderer(obstacle)
    obstacleRigidBody = RigidBody(obstacle)
    if toGenerate is 0:

        if toGenerateScale == 1:
            obstacleCollider = Collider(obstacle, "circle", 0.06)
            obstacle.setName("Circle Obstacle")
        elif toGenerateScale == 2:
            obstacleCollider = Collider(obstacle, "circle", 0.08)
            obstacle.setName("Circle Obstacle")
        elif toGenerateScale == 3:
            obstacleCollider = Collider(obstacle, "circle", 0.2)
            obstacle.setName("Circle Obstacle")


    elif toGenerate is 1:
        obstacleCollider = Collider(obstacle, "box")
        count = 0
        for element in obstacles:
            if element[2] is "box":
                count += 1
        name = "Bar Obstacle " + str(count)
        obstacle.setName(name)
    obstacleRigidBody.useGravity = True
    obstacleRigidBody.gravityScale = 0.7
    obstacle.Instantiate()
    obstacle.setScale([toGenerateScale, toGenerateScale, 1])
    obstacle.move([toGeneratePosX, 1.2, 1], 1, 1, False)
    obstacles.append(
        [obstacleSprite, obstacleRigidBody, obstacleCollider.type, toGenerate, toGeneratePosX, toGenerateScale])
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
    # Need to provide an array for each element
    # 1/type whether box or circle or etc
    # 2/X position
    # 3/Scale of X and Y in order


obstacleDelay = 0
obstacleInterval = 2

scoreDelay = 0
scoreInterval = 1

score = 0

alive = True

poopystate = 0
scorecolor = [1, 1, 1, 1]
scoresize = 1

idkdelay = 0
idkinterval = 2
numshit = 500


def Update():
    global scene
    #scene = "Score"
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
        global scoreDelay
        global scoreInterval
        global bgy
        global score
        global alive
        global rickcol
        global sound
        global poopystate
        global scorecolor
        global scoresize
        global idkdelay
        global idkinterval
        global numshit
        global bgm
        glClear(GL_COLOR_BUFFER_BIT)
        bgy += 0.0025
        if bgy >= 1:
            bgy = 0

        obstacleDelay += 1
        if (obstacleDelay / 25).is_integer() and (obstacleDelay / 25) > obstacleInterval:
            generateObstacle()
            print("Generated one obstacle!")
        if alive:
            scoreDelay += 1
            if (scoreDelay / 30).is_integer() and (scoreDelay / 30) > scoreInterval:
                score += 1
                pass

        idkdelay += 1
        if (idkdelay / numshit).is_integer() and (idkdelay / numshit) > idkinterval:
            if poopystate == 1:
                poopystate = 0
                scorecolor = [1, 1, 1, 1]
                scoresize = 1
                numshit = 500
            else:
                poopystate = 1
                scorecolor = [0, 1, 0, 1]
                scoresize = 2
                owe.play()
                numshit = 60

        gameImages.curImage(1)  # Load Gradient initial Background, and apply the following effects.
        backGroundSprite.DrawSprite(0, 1, 0 + bgy, 1 + bgy, 0.3)  # x1, x2, y1, y2, aspect ratio
        # backgroundColorChanger()
        # backGroundSprite.setColor(bgColor)

        gameImages.curImage(2)  # SpritesSHEET
        ricksprite.DrawSprite(0.1025, 0.203, 0.89625, 0.99875, 1.0)

        # ----
        if poopystate == 0:
            poopysprite.DrawSprite(0.0, 0.1025, 0.89625, 1.0, 1)
        elif poopystate == 1:
            poopysprite.DrawSprite(0.0, 0.10375, 0.79375, 0.89625, 1)
            # ----



            # ------------------------------------Powerups Generation Part--------------------------------------------------
            # a = generatePowerUp(0, 1)
            # if a is not None:
            # pass
            # print("a:", a)   # you can add parameters: (time rate for generation = 10, score rate for generation = 0)
            # checkCollectibles()

        # ------------------------------------------------------------------------------------------------------------------

        # ------------------------------------Obstacle Processing Part--------------------------------------------------
        gameImages.curImage(4)
        for obstacle in obstacles:  # For each obstacle in the obstacles array
            if obstacle[2] == "circle":  # if obstacle generated type is Circle
                obstacle[0].DrawSprite(0.3975, 0.48625, 0.885, 0.97375, 1.0)  # Draw the circle part of the sprite sheet
            elif obstacle[2] == "box":  # if obstacle generated type is Box
                obstacle[0].DrawSprite(0.0275, 0.22875, 0.95375, 0.97375, 10.0625)  # Draw box part of the sprite sheet
            obstacle[1].simulate()  # simulate object's rigid body physics
            if obstacle[0].gameObject.getPos()[1] <= -4:  # If object is completely out of screen Y coordinates:
                obstacles.remove(obstacle)
                #obstacle[1].gravityScale = -0.7
            if not obstacle[0].gameObject.Collider.collidable:
                disappear(obstacle)
                #pass
        # ------------------------------------------------------------------------------------------------------------------

        rickcol.checkCollision()
        print("rick is collided with", rickcol.collidedWith)


        poopycol.checkCollision()
        for element in poopycol.collidedWith:
            if element[0] is not rick:
                alive = False
                scene = "Score"
                sadowe.play()
                bgm.stop()
                die.play()
        for element in rickcol.collidedWith:
            if element[0].RigidBody is not None:
                element[0].RigidBody.newPos[1] = element[0].RigidBody.newPos[1] + 2
                element[0].RigidBody.AddForce(0.015, [0, 1])
                if element[0].Collider.type == "circle":
                    #score += 10
                    hitobstacle.play()
                elif element[0].Collider.type == "box":
                    #score += 10
                    hitobstacle.play()
                if rick.getPos()[0] > element[0].getPos()[0]:
                    element[0].RigidBody.AddTorque(random.uniform(0.01, 0.03))
                else:
                    element[0].RigidBody.AddTorque(-random.uniform(0.01, 0.03))
                rickcol.collidedWith.remove(element)

        gameImages.curImage(3)  # Fonts
        drawText(str(score), [0, 0.7, 0], scoresize, scorecolor)
        #poopy.RotateObject(360,0.1)
        glFlush()

    elif scene == "Menu":
        glClear(GL_COLOR_BUFFER_BIT)

        gameImages.curImage(5)
        menuBackGroundSprite.DrawSprite(0, 1, 0, 1, 1)  # x1, x2, y1, y2, aspect ratio
        gameImages.curImage(2)
        # Play button

        if playButton.Hovering and not playButton.Holding:
            playButton.DrawUI(mouse_x, mouse_y, 0.20375, 0.28875, 0.912, 0.955, 2.0606060606060606)
        elif playButton.Holding and playButton.Hovering:
            playButton.DrawUI(mouse_x, mouse_y, 0.20375, 0.28875, 0.87125, 0.9125, 2.0606060606060606)
        else:
            playButton.DrawUI(mouse_x, mouse_y, 0.20375, 0.28875, 0.955, 0.99875, 2.0606060606060606)

        # Credits button

        if creditsButton.Hovering and not creditsButton.Holding:
            creditsButton.DrawUI(mouse_x, mouse_y, 0.46875, 0.605, 0.875, 0.915, 3.40625)
        elif creditsButton.Holding and creditsButton.Hovering:
            creditsButton.DrawUI(mouse_x, mouse_y, 0.46875, 0.605, 0.91625, 0.95625, 3.40625)
        else:
            creditsButton.DrawUI(mouse_x, mouse_y, 0.46875, 0.605, 0.96, 0.99875, 3.40625)

        # Exit button

        if exitButton.Hovering and not exitButton.Holding:
            exitButton.DrawUI(mouse_x, mouse_y, 0.61125, 0.7075, 0.875, 0.915, 2.40625)
        elif exitButton.Holding and exitButton.Hovering:
            exitButton.DrawUI(mouse_x, mouse_y, 0.61125, 0.7075, 0.91625, 0.95625, 2.40625)
        else:
            exitButton.DrawUI(mouse_x, mouse_y, 0.61125, 0.7075, 0.96, 0.99875, 2.40625)

        glFlush()

    elif scene == "Menu2":
        glClear(GL_COLOR_BUFFER_BIT)

        gameImages.curImage(5)
        menuBackGroundSprite.DrawSprite(0, 1, 0, 1, 1)  # x1, x2, y1, y2, aspect ratio
        gameImages.curImage(3)

        drawText("KARIM SALAH", [0.75, 0.4, 0], 0.3, [0.2, 0.2, 1, 1])
        drawText("OMAR EL LEBOUDY", [0.625, 0.3, 0], 0.3, [1, 0.2, 0.2, 1])
        drawText("BOLA FAHMI", [0.775, 0.2, 0], 0.3, [0.3, 0.2, 0.7, 1])
        drawText("AHMED REDA", [0.775, 0.1, 0], 0.3, [0.2, 0.4, 1, 1])
        drawText("KAREEM ALLAM", [0.7, 0, 0], 0.3, [0.1, 0.5, 0.5, 1])
        drawText("AHMED SHEHA", [0.75, -0.1, 0], 0.3, [0, 0.6, 0.6, 1])
        drawText("ABDO SHEHAB", [0.75, -0.2, 0], 0.3, [0.9, 1, 1, 1])
        drawText("HAGAR METWALLI", [0.70, -0.3, 0], 0.3, [0.5, 0.8, 1, 1])
        drawText("ALAA SAID", [0.775, -0.4, 0], 0.3, [0.6, 0.9, 0, 0.4])
        drawText("NEHAL DAHRAWY", [0.72, -0.5, 0], 0.3, [0.7, 1, 0, 1])

        glFlush()

    elif scene == "Score":
        glClear(GL_COLOR_BUFFER_BIT)
        gameImages.curImage(1)  # Load Gradient initial Background, and apply the following effects.
        backGroundSprite.DrawSprite(0, 1, 0, 1, 0.3)  # x1, x2, y1, y2, aspect ratio
        gameImages.curImage(3)
        drawText("Score", [-0.4, 0.2, 0], 1)
        drawText(str(score), [0, -0.2, 0], 1)
        glFlush()


def disappear(obstacle):
        obstacle[0].setColor(
            [1, (obstacle[0].color[1] - 0.02), (obstacle[0].color[2] - 0.02), (obstacle[0].color[3] - 0.02)])