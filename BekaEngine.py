
from OpenGL.GL import *
import math
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import pygame
from pygame import mixer

GameObjects = list()
UIs = list()
class GameObject:


    def __init__(self):
        self.name = "GameObject"
        self.initialPosition = [0, 0, 0]
        self.position = [0, 0, 0]  # GameObject's Position
        self.scale = [0, 0, 0]  # GameObject's Scale
        self.angle = 0  # GameObject's Z rotation ( 2D rotation )
        self.targetAngle = 0  # The angle to which the GameObject is willing to rotate
        self.targetPosition = [0, 0, 0]  # The position which the GameObject is willing to reach
        self.initialTranslationStepX = 1  # Maximum translation speed in X axis
        self.initialTranslationStepY = 1  # Maximum translation speed in Y axis
        self.translationStepX = 0.01  # Current translation speed in X axis
        self.translationStepY = 0.01  # Current translation speed in Y axis
        self.smoothDamping = True
        self.rotationStep = 0
        self.initialRotationStep = 0
        self.RigidBody = None
        global GameObjects
        GameObjects.append(self)

    def setPos(self, positionArray):  # A function used to set GameObject's position. Usually internally used
        self.position = positionArray

    def move(self, TargetArray,StepX,StepY,SmoothDamping = True):  # A function used to move GameObject to a certain location
        # Usage :
        # TargetArray is a 3-element array including the target X,Y,Z position to which you want to move your GameObject
        # StepX is the maximum movement speed in X axis in case of SmoothDamping
        # StepY is the maximum movement speed in Y axis in case of SmoothDamping

        self.initialTranslationStepX = StepX
        self.initialTranslationStepY = StepY
        self.translationStepX = StepX
        self.translationStepY = StepY
        self.targetPosition = TargetArray
        self.smoothDamping = SmoothDamping

    def setName(self,Name):
        self.name = Name

    def getPos(self):
        return self.position


    def setScale(self, scaleArray):
        self.scale = scaleArray
        glScale(self.scale[0],self.scale[1],self.scale[2])

    def getScale(self):
        return self.scale

    def RotateObject(self,TargetAngle,Step):
        self.targetAngle = TargetAngle
        self.rotationStep = Step
        if not self.targetAngle == 360:
            if not (self.angle <= self.targetAngle + 1  and  self.angle > self.targetAngle - 1):
                self.angle += self.rotationStep
        else:
            self.angle += self.rotationStep
            if self.angle >= 360:
                self.angle -= 360


    def getAngle(self):
        return self.angle

    def Destroy(self):
        del self

    def loadInitialPosition(self):
        glTranslate(self.initialPosition[0], self.initialPosition[1] * 2,self.initialPosition[2])

    def Instantiate(self, positionArray = [0,0,0], scaleArray = [1,1,1],Angle = 0):

        self.scale = scaleArray
        glScale(scaleArray[0],scaleArray[1],scaleArray[2])
        self.angle = Angle

        if self.RigidBody is not None:
            self.RigidBody.newPos =  [ positionArray[0] * 2,positionArray[1] * 2,positionArray[2] ]
        self.setPos(positionArray)
        self.initialPosition = positionArray
        self.targetPosition = [self.getPos()[0], self.getPos()[1], self.getPos()[2]]
        self.loadInitialPosition()


class GameImages:


    def __init__(self,imageNames):
        self.currentImage = 0
        self.imageCount = 0
        for imageName in imageNames:
            self.imageCount += 1
        print("images: ", self.imageCount)
        self.images = glGenTextures(self.imageCount)
        i = 0
        for imageName in imageNames:
            imgload = pygame.image.load(imageName)
            img = pygame.image.tostring(imgload, "RGBA", 1)
            width = imgload.get_width()
            height = imgload.get_height()
            glBindTexture(GL_TEXTURE_2D, self.images[i])  # Set this image in images array
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
            i += 1
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.images[0])

    def curImage(self,CurrentImage = 1):
        self.currentImage = CurrentImage
        glBindTexture(GL_TEXTURE_2D, self.images[self.currentImage - 1])

    def getImagecount(self):
        return self.imageCount


class SpriteRenderer:


    def __init__(self, gObject):
        self.gameObject = gObject
        self.texCoordX1 = 0
        self.texCoordX2 = 0
        self.texCoordY1 = 0
        self.texCoordY2 = 0
        self.color = [1, 1, 1, 1]
        self.flipX = False
        self.flipY = False
        self.density = 0.1
        self.height = 0
        self.startTime = 0
        self.interval = 0.1
        self.WidthToHeight = 0
        self.currentVelocity = 0
        self.rotang = 0

    def setColor(self,newColor):
        self.color = newColor

    def setDensity(self,newDensity):
        self.density = newDensity

    def setHeight(self,newHeight):
        self.height = newHeight
    def setWidthToHeight(self,newWidthToHeight):
        self.WidthToHeight = newWidthToHeight

    def FlipX(self):
        if self.flipX:
            self.flipX = False
        else:
            self.flipX = True

    def FlipY(self):
        if self.flipY:
            self.flipY = False
        else:
            self.flipY = True


    #Draws Sprite every frame. Sprite is determined using 4 Coordinates from the main sprite sheet.
    def DrawSprite(self, TextureCoordX1 = 0, TextureCoordX2 = 0, TextureCoordY1 = 0, TextureCoordY2 = 0, WidthToHeightRatio = 1):
        global currentVelocity
        curGameObject = self.gameObject
        self.rotang += 1
        self.gameObject.loadInitialPosition()
        #print("self of SpriteRenderer DrawSprite is: ", self)
        self.texCoordX1 = TextureCoordX1
        self.texCoordX2 = TextureCoordX2
        self.texCoordY1 = TextureCoordY1
        self.texCoordY2 = TextureCoordY2
        deltaTexCoordX = self.texCoordX2 - self.texCoordX1
        self.setWidthToHeight(WidthToHeightRatio)
        self.height = self.density / self.WidthToHeight
        #if math.fabs( self.gameObject.targetPosition[1] - self.gameObject.position[1] ) <= 0.05:
         #   self.gameObject.translationStepY = 0


        # Y Movement

        if (self.gameObject.targetPosition[1] * 0.5) > self.gameObject.position[1]:
            addition = self.SmoothDamp(self.gameObject.getPos()[1],self.gameObject.targetPosition[1],1,self.gameObject.initialTranslationStepY)
            self.gameObject.setPos([(self.gameObject.getPos()[0]) ,
                                    ((self.gameObject.getPos()[1])+ addition),
                                   self.gameObject.getPos()[2]])
        elif (self.gameObject.targetPosition[1] * 0.5) < self.gameObject.position[1]:
            addition = self.SmoothDamp(self.gameObject.getPos()[1], self.gameObject.targetPosition[1], 1,
                                       self.gameObject.initialTranslationStepY)

            self.gameObject.setPos([(self.gameObject.getPos()[0]),
                                    ((self.gameObject.getPos()[1]) - addition),
                                   self.gameObject.getPos()[2]])


        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])



        # X Movement

        glLoadIdentity()

        if (self.gameObject.targetPosition[0] * 0.5) > self.gameObject.position[0]:
            addition = self.SmoothDamp(self.gameObject.getPos()[0],self.gameObject.targetPosition[0], 1,
                                       self.gameObject.initialTranslationStepX)

            self.gameObject.setPos([(self.gameObject.getPos()[0] + addition),
                                   self.gameObject.getPos()[1],
                                   self.gameObject.getPos()[2]])

        elif (self.gameObject.targetPosition[0] * 0.5) < self.gameObject.position[0]:
            addition = self.SmoothDamp(self.gameObject.getPos()[0], self.gameObject.targetPosition[0], 1,
                                       self.gameObject.initialTranslationStepX)

            self.gameObject.setPos([(self.gameObject.getPos()[0] - addition),
                                   self.gameObject.getPos()[1],
                                   self.gameObject.getPos()[2]])

        glTranslatef(self.gameObject.getPos()[0], self.gameObject.getPos()[1] * 2, 0)

        self.gameObject.RotateObject(self.gameObject.targetAngle,self.gameObject.rotationStep)

        glRotatef(self.gameObject.angle, 0, 0, 1)

        if self.gameObject.angle >= 360:
            self.gameObject.angle -= 360
        elif self.gameObject.angle <0:
            self.gameObject.angle += 360



        glBegin(GL_QUADS)
        glTexCoord(self.texCoordX2 if self.flipX else self.texCoordX1, self.texCoordY2 if self.flipY else self.texCoordY1)
        glVertex(((-self.density / 2) * self.gameObject.getScale()[0]),(-self.height / 2) * self.gameObject.getScale()[1], 1 * self.gameObject.getScale()[2])

        glTexCoord(self.texCoordX1 if self.flipX else self.texCoordX2, self.texCoordY2 if self.flipY else self.texCoordY1)
        glVertex(((self.density / 2) * self.gameObject.getScale()[0]),(-self.height / 2) * self.gameObject.getScale()[1], 1 * self.gameObject.getScale()[2])

        glTexCoord(self.texCoordX1 if self.flipX else self.texCoordX2, self.texCoordY1 if self.flipY else self.texCoordY2)
        glVertex(((self.density / 2) * self.gameObject.getScale()[0]),(self.height / 2) * self.gameObject.getScale()[1], 1 * self.gameObject.getScale()[2])

        glTexCoord(self.texCoordX2 if self.flipX else self.texCoordX1, self.texCoordY1 if self.flipY else self.texCoordY2)
        glVertex(((-self.density / 2) * self.gameObject.getScale()[0]),+(self.height / 2) * self.gameObject.getScale()[1], 1 * self.gameObject.getScale()[2])

        glEnd()


    def SmoothDamp(self, current, target, smoothTime, maxVelocity):
        # maxVelocity is 0.001
        # current is 0
        # target is 0.001
        # current is current X position of player
        # target is target X position that I want to reach
        # curVelocity is the current body velocity [ current step ]
        # smoothTime is a value that when increased, it takes more time to reach the target
        # for example : current = 0 , target = 1 , curVelocity = step = 0.2 , smoothTime = 0.1
        # where : y is Speed ( step ) or curVelocity
        #                where : x is current distance
        #                where : maxSpeed is maximum step, defined by initialStep
        #                where : smoothTime should slow down the whole process
        realtarget = 0.5 * target
        # target is now 0.0005
        distance = current - realtarget
        # distance is now -0.0005
        if self.gameObject.smoothDamping:

            self.currentVelocity = math.pow(math.fabs(distance), (0.7 * math.e))
            if self.currentVelocity > maxVelocity:
                self.currentVelocity = maxVelocity
        else:
            if math.fabs(distance) > maxVelocity: # first term is 0.0005 , second term is 0.0005
                #print("Condition occured! math.fabs(distance) > maxVelocity/2")
                self.currentVelocity = maxVelocity
            else:
                #print("Condition NOT occured! math.fabs(distance) > maxVelocity/2")
                self.currentVelocity = math.fabs(distance)


        #print("Current:", current, ", Target: ", realtarget)
        return self.currentVelocity
        # an if statement to prevent y from exceeding maxSpeed
        # x^4e


class BoxCollider:

    def __init__(self, gObject):
        self.gameObject = gObject


class RigidBody:


    def __init__(self, gObject):
        self.gameObject = gObject
        self.gameObject.RigidBody = self
        self.appliedForcesInfo = [] # Elements : 0/Force, 1/DirectionX , 2/DirectionY, 3/initialVelocityX, 4/initialVelocityY, 5/initialTimeX, 6/initialTimeY, 7/resultVelocityX, 8/resultVelocityY, 9/ToBeRemoved
        self.gravityAcceleration = 9.8
        self.gravityScale = 1
        self.useGravity = False
        self.angularDrag = 0.01
        self.linearDrag = 0.5
        self.mass = 1
        self.actvelocity = [0, 0]
        self.freezeRotation = False
        self.newPos = [0,0,0]
        self.timeY = 0
        self.lastForcey = 0
        self.underTorque = False
    def getVelocity(self):
        return self.actvelocity

    def setMass(self,Mass):
        self.mass = Mass

    def AddForceAtPosition(self,Force = 1.0,ForcePoint = [0,0], Direction = [1,0], Test = [1,0]):
        # Wait for collision to be implemented
        # This function will cause both Force and Torque

        # ------------------------------------- Torque part -------------------------------------
        #                              Torque will be calculated using:
        # Torque = Force * r * sin(theta)
        # Force = Force
        # r = distance between body center and force point
        # Force point varies from -1 to 1 , where 0 is the body center
        r = math.sqrt(math.pow((self.gameObject.getPos()[0] - ForcePoint[0]), 2) + math.pow((self.gameObject.getPos()[1] - ForcePoint[1]), 2))        #Unline after test
        # sin(theta) = angle between Force direction and axis of rotation
        # to calculate theta:
        #   1/Calculate the Axis of rotation vector, as follows:
        #       new vector = ( X * cos ( alpha ) + y * sin ( alpha ) , -X * sin alpha + y * cos ( alpha ) )
        #       Where X     --> X of first vector ( equals 1 )
        #       Where Y     --> Y of first vector ( equals 0 )
        #       Where alpha --> Angle between two vectors ( self.gameObject.GetAngle() )
        newVect = [ 1 * math.cos(math.radians(self.gameObject.getAngle())), -1 * math.sin(math.radians(self.gameObject.getAngle())) ]        #Unline after test
        #   2/Use this equation after obtaining new vector ( newVect ) to get the angle between both vectors
        print("Vector of body rotation: ", newVect)
        theta = math.acos( ( ( Direction[0] *  newVect[0] ) + ( Direction[1] * newVect[1] ) ) /  ( ( math.sqrt(( math.pow(Direction[0],2) + math.pow(Direction[1],2) )) )*( ( math.sqrt(( math.pow(newVect[0],2) + math.pow(newVect[1],2) )) ) ) ) )        #Unline after test
        #   3/Torque equals Force * r * sin theta
        # Test purpose : r = Test[0] and theta = Test[1]
        #r = Test[0]
        #theta = Test[1]
        torque = Force * r * math.sin(math.radians(theta))
        print("Torque = ", torque, ", math.sin(theta) = ", math.sin(math.radians(theta)), ", Theta = ", theta)

        self.AddTorque(torque)

        # --------------------------------------------------------------------------------------

        # ------------------------------------- Force part -------------------------------------




        self.AddForce(Force, Direction)

        # --------------------------------------------------------------------------------------



    def AddForce(self,Force = 1.0,Direction = [1,0]):
        print("Force Added To: ", self.gameObject.name)
        self.actvelocity[0] += Force * Direction[0] * self.mass
        self.actvelocity[1] += Force * Direction[1] * self.mass
        #print("Forces list of" , self.gameObject.name ,"before append:", len(self.appliedForcesInfo))
        self.appliedForcesInfo.append(
            [Force, Direction[0], Direction[1], self.actvelocity[0], self.actvelocity[1], 0, 0, 0, 0, False])
        #print("Forces list of", self.gameObject.name, "after append:", len(self.appliedForcesInfo))

    def AddTorque(self,Force = 1.0):
        self.gameObject.RotateObject(360, self.gameObject.rotationStep + (Force * 100))
        self.underTorque = True



    def simulate(self):
        glLoadIdentity()
        self.timeY += 0.011
        #print("RotationStep is: ", self.gameObject.rotationStep)
        """if self.gameObject.rotationStep > 0:
            print("Decreasing")
            self.gameObject.rotationStep -= self.angularDrag"""

        # ----------------------------------------Horizontal Force-------------------------------------------------

        if self.actvelocity[0] <= 0.0001 and self.actvelocity[0] > -0.0001:
            self.actvelocity[0] = 0

        for force in self.appliedForcesInfo:
            force[5] += 0.01
            force[7] = (force[3] * math.pow(math.e,
                                                                  (-self.linearDrag * force[5]) / self.mass))

            if (force[7] < 0.0001 and force[7] > -0.0001):    # Detect if specific force effect is over
                force[9] = True    # Remove specific ended force from forces array
                force[7] = 0

            self.actvelocity[0] = force[7]   # Apply the effect of this force to the velocity of X


        self.newPos[0] += self.actvelocity[0]

        # -------------------------------------------------------------------------------------------------------

        # -----------------------------Vertical Force ( Including Gravity )--------------------------------------
        if self.actvelocity[1] <= 0.0001 and self.actvelocity[1] > -0.0001:
            if not self.useGravity:
                self.actvelocity[1] = 0
        if self.timeY > 5.5:
            self.timeY = 5.5
        for force in self.appliedForcesInfo:
            force[6] += 0.01
            force[8] = (force[4] * math.pow(math.e,
                                                                  (-self.linearDrag * force[6]) / self.mass))
            if (force[7] < 0.0001 and force[7] > -0.0001) and (force[8] < 0.0001 and force[8] > -0.0001) and force[9]:  # Detect if specific force effect is over
                self.appliedForcesInfo.remove(force)    # Remove specific ended force from forces array

            self.actvelocity[1] = force[8]
            self.lastForcey = force[8]

        self.actvelocity[1] = self.lastForcey + ((self.gravityScale if self.useGravity else 0) * self.gravityAcceleration * -0.001 *  self.timeY)

        self.newPos[1] += self.actvelocity[1]

        if not self.useGravity:
            self.timeY = 0
        if self.timeY > 5.5:
            self.timeY = 5.5

        # -------------------------------------------------------------------------------------------------------

        # -----------------------------------------Air Resistance------------------------------------------------

        if math.fabs(self.actvelocity[1]) > 0.054:
            if self.actvelocity[1] > 0:
                self.actvelocity[1] = 0.054
            else:
                self.actvelocity[1] = -0.054

        # -------------------------------------------------------------------------------------------------------

        if self.gameObject.rotationStep > 0 and self.underTorque:
            self.gameObject.rotationStep -= self.angularDrag
        else:
            self.underTorque = False
        #if self.gameObject.name == "Bar":
            #print("Name: ", self.gameObject.name, ", newPos: ", self.newPos, ", curPos: ", self.gameObject.getPos(), ", TargetPos: ", self.gameObject.targetPosition)
        self.gameObject.move([self.newPos[0], self.newPos[1],self.gameObject.getPos()[2]],math.fabs(self.actvelocity[0]),math.fabs(self.actvelocity[1]),False)



class UI:

    def __init__(self):
        self.gameObject = GameObject()
        self.spriteRenderer = SpriteRenderer(self.gameObject)
        self.type = "button" #Types : "button" , "text"
        self.HoldingMouse = False
        self.Hovering = False
        self.state = 1
        self.normalColor = [1,1,1,1]
        self.hoverColor = [0.75,0.75,0.75,1]
        self.pressedColor = [0.25,0.25,0.5,1]
        self.Holding = False
        self.onClickFunction = None
        self.char = "A"
        UIs.append(self)
        self.x = 0
        self.y = 0
    def Create(self, Type = "button", Letter = 'A'):
        if Type is "button":
            self.type = "button"
            self.gameObject.Instantiate([0,0,0],[5,5,1],0)
            self.gameObject.smoothDamping = False
            self.gameObject.setScale([5,5,1])
        elif Type is "char":
            self.type = "char"
            self.gameObject.Instantiate([0,0,0])
            self.gameObject.smoothDamping = False
            self.char = Letter
    def DrawUI(self, mouseX = 0, mouseY = 0, TextureCoordX1 = 0, TextureCoordX2 = 0, TextureCoordY1 = 0, TextureCoordY2 = 0, WidthToHeightRatio = 1):

        arrayToDraw = []
        mouseYToWorld = (((glutGet(GLUT_WINDOW_HEIGHT) / 2) - mouseY) / (glutGet(GLUT_WINDOW_HEIGHT) / 2)) / 2
        mouseXToWorld = ((mouseX - (glutGet(GLUT_WINDOW_WIDTH) / 2)) / (glutGet(GLUT_WINDOW_WIDTH) / 4))

        #print ("if", mouseYToWorld, "<",( self.gameObject.getPos()[1] + ((-self.spriteRenderer.height / 2) * self.gameObject.getScale()[1])))

        if mouseYToWorld > ( self.gameObject.getPos()[1] + ((-self.spriteRenderer.height / 2) * self.gameObject.getScale()[1]))\
                and mouseYToWorld < ( self.gameObject.getPos()[1] + ((self.spriteRenderer.height / 2) * self.gameObject.getScale()[1]))\
                and mouseXToWorld > ( self.gameObject.getPos()[0] +((-self.spriteRenderer.density) * self.gameObject.getScale()[0]))\
                and mouseXToWorld < ( self.gameObject.getPos()[0] +((self.spriteRenderer.density) * self.gameObject.getScale()[0])):

            self.Hovering = True
        else:
            self.Hovering = False

        if self.type is "button":
            arrayToDraw = [TextureCoordX1, TextureCoordX2, TextureCoordY1, TextureCoordY2, WidthToHeightRatio]
            if self.Hovering:
                if self.state == 0:
                    self.spriteRenderer.setColor(self.pressedColor)
                    self.Holding = True
                else:
                    self.spriteRenderer.setColor(self.hoverColor)
                    if self.Holding:
                        self.onClick(self.onClickFunction)
                        self.Holding = False
            else:
                self.spriteRenderer.setColor(self.normalColor)
        elif self.type is "char":
            charArray = charToSpriteDetails(self.char)
            arrayToDraw = [charArray[0], charArray[1], charArray[2], charArray[3],
                                           charArray[4]]
        self.spriteRenderer.DrawSprite(arrayToDraw[0], arrayToDraw[1], arrayToDraw[2], arrayToDraw[3],
                                       arrayToDraw[4])
    def onClick(self,fun):
        fun()
    def setOnClick(self,fun):
        self.onClickFunction = fun

def charToSpriteDetails(char):
    return {
        'a': 1,
        'b': 2,
        'A': [0.223,0.298,0.575,0.695,0.625],
        'B': [0.53, 0.615, 0.578, 0.695, 0.625],
        'C': [0.243, 0.342, 0.221, 0.324, 0.625],
        'D': [0.213, 0.301, 0.449, 0.565, 0.625],
        'E': [0.387, 0.477, 0.448, 0.565, 0.625],
        'F': [0.118, 0.207, 0.451, 0.565, 0.625],
        'G': [0.556, 0.662, 0.452, 0.565, 0.625],
        'H': [0.303, 0.382, 0.572, 0.695, 0.625],
        'I': [0.745, 0.821, 0.451, 0.565, 0.625],
        'J': [0.142, 0.236, 0.218, 0.323, 0.625],
        'K': [0.778, 0.872, 0.575, 0.695, 0.625],
        'L': [0.666, 0.741, 0.451, 0.565, 0.625],
        'M': [0.002, 0.116, 0.447, 0.563, 0.625],
        'N': [0.713, 0.810, 0.334, 0.441, 0.625],
        'O': [0.350, 0.463, 0.332, 0.441, 0.625],
        'P': [0.467, 0.540, 0.334, 0.442, 0.625],
        'Q': [0.877, 0.982, 0.577, 0.695, 0.625],
        'R': [0.278, 0.345, 0.332, 0.441, 0.625],
        'S': [0.093, 0.176, 0.328, 0.442, 0.625],
        'T': [0.545, 0.638, 0.333, 0.439, 0.625],
        'U': [0.002, 0.090, 0.329, 0.441, 0.625],
        'V': [0.697, 0.773, 0.576, 0.695, 0.625],
        'W': [0.826, 0.946, 0.451, 0.563, 0.625],
        'X': [0.180, 0.273, 0.329, 0.441, 0.625],
        'Y': [0.132, 0.216, 0.573, 0.695, 0.625],
        'Z': [0.038, 0.137, 0.217, 0.324, 0.625]

    }.get(char,9)

def drawText(text = "ABABAABBBAAAAAA", textPosition = [0,0,0], textSize = 1):
    textX = 0
    for char in list(text):
        c = UI()
        c.Create("char",char)
        c.gameObject.move([textPosition[0] + textX,textPosition[1],textPosition[2]], 1, 1, False)
        c.gameObject.setScale([textSize,textSize,1])
        c.DrawUI()
        textX += c.spriteRenderer.density * 2 * textSize

def drawChar(char = "A", charPosition = [0,0,0], charSize = 1):
    c = UI()
    c.Create("char",char)
    c.gameObject.move([charPosition[0],charPosition[1],charPosition[2]], 1, 1, False)
    c.gameObject.setScale([charSize,charSize,1])
    c.DrawUI()