
#  Replace "Keeper" with game file name. Ex: if your game file is called MyGame.Py, Write MyGame instead of Keeper

from \
    Keeper\
    import *
from OpenGL.GLUT import *


#from BekaEngine import *
x = 0
time_interval = 10  # try  1000 msec

screenwidth = 800
screenheight = 800
gameTitle = b"BEKA Engine"

def Timer(v):

    draw()

    glutTimerFunc(time_interval, Timer, 1)



def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(screenwidth , screenheight)
    glutCreateWindow(gameTitle)
    glutTimerFunc(time_interval, Timer, 1)
    glutDisplayFunc(draw)
    glutPassiveMotionFunc(PassiveMotionFunc)
    glutMotionFunc(MotionFunc)
    glutMouseFunc(MouseMotion)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(arrow_key)
    init()
    glutMainLoop()

main()
