from BekaEngine import *
from OpenGL.GLUT import *
backGround = GameObject()
backGround.setName("Background")
backGroundSprite = SpriteRenderer(backGround)
gameImages = None

screenheight = 800
screenwidth = 800

def init():

    global modelViewMatrix
    glClearColor(1, 1, 1, 0.5)
    glMatrixMode(GL_MODELVIEW)
    global gameImages
    gameImages = GameImages(["SM3.PNG","SM.PNG"])
    backGround.Instantiate([0,0,0],[1,1,1],0)
    backGround.setScale([20, 20, 1])


recx1 = 0
recy1 = 0
recx2 = 0
recy2 = 0
drawRectangle = False
mouseDown = False
drawing = False
firstClick = False
x1 = 0
x2 = 0
y1 = 0
y2 = 0
def MouseMotion(button,state,x,y): #Triggers with both MouseClick Down or Up
    global recx1
    global recx2
    global recy1
    global recy2
    global mouseDown
    global drawing
    global firstClick
    global y1, y2 , x1 , x2
    print("Button: ",button, ", state: ", state, ", x: ", x, ", y: " ,y)
    if state == 0:
        firstClick = True
        mouseDown = True
        recx1 = ((x - (glutGet(GLUT_WINDOW_WIDTH) / 2)) / (glutGet(GLUT_WINDOW_WIDTH) / 2))
        recy1 = ((glutGet(GLUT_WINDOW_HEIGHT) / 2) - y) / (glutGet(GLUT_WINDOW_HEIGHT) / 2)
        x1 = x
        y1 = y
    elif state == 1:
        mouseDown = False
        x2 = x
        y2 = y
        ratio = (math.fabs(x1 - x2) / math.fabs(y1 - y2))
        #print("X1: ", x1 / glutGet(GLUT_WINDOW_WIDTH), ", X2: ", x2 / glutGet(GLUT_WINDOW_WIDTH), ", Y1: ", 1 - (y1  / (glutGet(GLUT_WINDOW_HEIGHT))),
        #      ", Y2: ",  1 - (y2  / (glutGet(GLUT_WINDOW_HEIGHT))), ", WidthToHeightRatio: ", ratio)

        print("[", x1 / glutGet(GLUT_WINDOW_WIDTH),",",x2 / glutGet(GLUT_WINDOW_WIDTH),",", 1 - (y1  / (glutGet(GLUT_WINDOW_HEIGHT))),",",  1 - (y2  / (glutGet(GLUT_WINDOW_HEIGHT))),",",ratio,"]")


def MotionFunc(x,y):  # Mouse While Holding Button
    global mouseDown
    global recy1
    global recy2
    global recx1
    global recx2
    global drawing
    if mouseDown:
        recy2 = ((glutGet(GLUT_WINDOW_HEIGHT) / 2) - y) / (glutGet(GLUT_WINDOW_HEIGHT) / 2)
        recx2 = ((x - (glutGet(GLUT_WINDOW_WIDTH) / 2)) / (glutGet(GLUT_WINDOW_WIDTH) / 2))


def PassiveMotionFunc(x,y):  # Moving Mouse Without Holding Button
    global recx1
    global recy1
    global drawing




def draw():
    global recx1
    global recx2
    global recy1
    global recy2
    global mouseDown
    global firstClick
    glClear(GL_COLOR_BUFFER_BIT)
    backGroundSprite.DrawSprite(0, 1, 0, 1, 1)
    glColor(0.2, 0.2, 0.5,1)
    glScale(1, 1, 1)

    if firstClick:

        glLoadIdentity()

        glBegin(GL_LINE_LOOP)

        glColor3d(0.5, 0.50, 0.2)
        glVertex(recx1, recy1)
        glVertex(recx2, recy1)
        glVertex(recx2, recy2)
        glVertex(recx1, recy2)
        glEnd()
    glFlush()

def arrow_key(key, x, y):
    pass

def keyboard(key):
    pass






