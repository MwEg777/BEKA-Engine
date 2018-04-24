#  Replace "Keeper" with game file name. Ex: if your game file is called MyGame.Py, Write MyGame instead of Keeper

from \
    Keeper \
    import *
from OpenGL.GLUT import *

# Setup Variables
screenwidth = 800
screenheight = 800
gameTitle = b"BEKA Engine"


def Timer(v):
    Update()
    glutTimerFunc(time_interval, Timer, 1)


def main():
    glutInit()                                  # Initialize Glut Features

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)    # Initialize Window Options
    glutInitWindowSize(screenwidth, screenheight)
    glutCreateWindow(gameTitle)

    glutPassiveMotionFunc(PassiveMotionFunc)    # Mouse Functions Enable
    glutMotionFunc(MotionFunc)                  # Mouse Functions Enable
    glutMouseFunc(MouseMotion)                  # Mouse Functions Enable

    glutKeyboardFunc(keyboard)                  # Keyboard Functions Enable
    glutSpecialFunc(arrow_key)                  # Keyboard Functions Enable

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # Blend
    glEnable(GL_BLEND)

    init()                                      # First fn in Keeper.py which imports sprites and instantiate objects

    glutTimerFunc(time_interval, Timer, 1)  # Loop Along
    glutDisplayFunc(Update)
    glutMainLoop()


main()
