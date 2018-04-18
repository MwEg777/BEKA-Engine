
from OpenGL.GL import *
import math
from OpenGL.GLU import *
import time
import pygame
from pygame import mixer

class GameObject:
    name = "GameObject"
    initialPosition = [0, 0, 0]
    position = [0, 0, 0]  # GameObject's Position
    scale = [0, 0, 0]  # GameObject's Scale
    angle = 0  # GameObject's Z rotation ( 2D rotation )
    targetAngle = 0  # The angle to which the GameObject is willing to rotate
    targetPosition = [0,0,0]  # The position which the GameObject is willing to reach
    initialTranslationStepX = 0.01  # Maximum translation speed in X axis
    initialTranslationStepY = 0.01  # Maximum translation speed in Y axis
    translationStepX = 0.01  # Current translation speed in X axis
    translationStepY = 0.01  # Current translation speed in Y axis
    smoothDamping = True
    rotationStep = 0
    initialRotationStep = 0
    def __init__(self):
        pass

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

    def Del(self):
        del self

    def loadInitialPosition(self):
        glTranslate(self.initialPosition[0], self.initialPosition[1],self.initialPosition[2])

    def Instantiate(self, positionArray = [0,0,0], scaleArray = [1,1,1],Angle = 0):
        self.position = positionArray
        self.scale = scaleArray
        glScale(scaleArray[0],scaleArray[1],scaleArray[2])
        self.angle = Angle
        self.targetPosition = self.position
        self.initialPosition = self.position


class GameImages:

    currentImage = 0
    imageCount = 0
    def __init__(self,imagesCount = 1):
        self.images = glGenTextures(imagesCount)
        glBindTexture(GL_TEXTURE_2D, self.images[0])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)


    def addImage(self,imageName):
        glGenTextures(self.imageCount)
        imgload = pygame.image.load(imageName)
        img = pygame.image.tostring(imgload, "RGBA", 1)
        width = imgload.get_width()
        height = imgload.get_height()
        glBindTexture(GL_TEXTURE_2D, self.images[self.imageCount - 1])  # Set this image in images array
        glBindTexture(GL_TEXTURE_2D, self.images[self.currentImage])  # Retrieve last loaded image
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        glEnable(GL_TEXTURE_2D)

    def curImage(self,CurrentImage = 1):
        self.currentImage = CurrentImage
        glBindTexture(GL_TEXTURE_2D, self.images[self.currentImage - 1])

    def getImagecount(self):
        return self.imageCount


class SpriteRenderer:
    gameObject = None
    texCoordX1 = 0
    texCoordX2 = 0
    texCoordY1 = 0
    texCoordY2 = 0
    color = [1, 1, 1, 1]
    flipX = False
    flipY = False
    density = 0.1
    height = 0
    startTime = 0
    interval = 0.1
    WidthToHeight = 0

    def __init__(self, gObject):
        self.gameObject = gObject


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

    rotang = 0
    #Draws Sprite every frame. Sprite is determined using 4 Coordinates from the main sprite sheet.
    def DrawSprite(self, TextureCoordX1 = 0, TextureCoordX2 = 0, TextureCoordY1 = 0, TextureCoordY2 = 0, WidthToHeightRatio = 1):
        global currentVelocity
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

    currentVelocity = 0
    def SmoothDamp(self, current, target, smoothTime, maxVelocity):
        global currentVelocity
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


            currentVelocity = math.pow(math.fabs(distance), (0.7 * math.e))
            if currentVelocity > maxVelocity:
                currentVelocity = maxVelocity
        else:
            if math.fabs(distance) > maxVelocity/4: # first term is 0.0005 , second term is 0.0005
                #print("Condition occured! math.fabs(distance) > maxVelocity/2")
                currentVelocity = maxVelocity
            else:
                #print("Condition NOT occured! math.fabs(distance) > maxVelocity/2")
                currentVelocity = 0

        #print("Current:", current, ", Target: ", realtarget)
        return currentVelocity
        # an if statement to prevent y from exceeding maxSpeed
        # x^4e


class BoxCollider:
    gameObject = None

    def __init__(self, gObject):
        self.gameObject = gObject


class RigidBody:
    gameObject = None
    gravityAcceleration = 9.8
    gravityScale = 1
    useGravity = False
    angularDrag = 0.01
    linearDrag = 0.05
    mass = 1
    actvelocity = [0,0]
    freezeRotation = False
    newPos = [0,0,0]
    timeY = 0
    lastForcey = 0
    underTorque = False
    appliedForcesInfo = [] # Elements : 0/Force, 1/DirectionX , 2/DirectionY, 3/initialVelocityX, 4/initialVelocityY, 5/initialTimeX, 6/initialTimeY, 7/resultVelocityX, 8/resultVelocityY, 9/ToBeRemoved
    def __init__(self, gObject):
        self.gameObject = gObject

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
        # r = math.sqrt(math.pow((self.gameObject.GetPos[0] - ForcePoint[0]), 2) + math.pow((self.gameObject.GetPos[1] - ForcePoint[1]), 2))        #Unline after test
        # sin(theta) = angle between Force direction and axis of rotation
        # to calculate theta:
        #   1/Calculate the Axis of rotation vector, as follows:
        #       new vector = ( X * cos ( alpha ) + y * sin ( alpha ) , -X * sin alpha + y * cos ( alpha ) )
        #       Where X     --> X of first vector ( equals 1 )
        #       Where Y     --> Y of first vector ( equals 0 )
        #       Where alpha --> Angle between two vectors ( self.gameObject.GetAngle() )
        # newVect = [ 1 * math.cos(self.gameObject.getAngle()), -1 * math.sin(self.gameObject.getAngle()) ]        #Unline after test
        #   2/Use this equation after obtaining new vector ( newVect ) to get the angle between both vectors
        # theta = math.acos( ( ( Direction[0] *  newVect[0] ) + ( Direction[1] * newVect[1] ) ) /  ( ( math.sqrt(( math.pow(Direction[0],2) + math.pow(Direction[1],2) )) )*( ( math.sqrt(( math.pow(newVect[0],2) + math.pow(newVect[1],2) )) ) ) ) )        #Unline after test
        #   3/Torque equals Force * r * sin theta
        # Test purpose : r = Test[0] and theta = Test[1]
        r = Test[0]
        theta = Test[1]
        torque = Force * r * math.sin(math.radians(theta))
        print("Torque = ", torque, ", math.sin(theta) = ", math.sin(math.radians(theta)), ", Theta = ", theta)

        self.AddTorque(torque)

        # --------------------------------------------------------------------------------------



    def AddForce(self,Force = 1.0,Direction = [1,0]):

        print("velocity[0] before: ", self.actvelocity[0])
        self.actvelocity[0] += Force * Direction[0] * self.mass
        self.actvelocity[1] += Force * Direction[1] * self.mass
        self.appliedForcesInfo.append(
            [Force, Direction[0], Direction[1], self.actvelocity[0], self.actvelocity[1], 0, 0, 0, 0, False])

        print("velocity[0] after: ", self.actvelocity[0])

        #Make an array containing forces DONE
        #Determine when a force effect is over by checking the equation of it when it's near zero DONE
        #constantly check that then remove it from forces array DONE
        #make a for loop to add the effect of each force DONE
        print("Forces list length is now: ", len(self.appliedForcesInfo))

    def AddTorque(self,Force = 1.0):
        self.gameObject.RotateObject(360, self.gameObject.rotationStep + Force)
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

        self.gameObject.move([self.newPos[0], self.newPos[1],self.gameObject.getPos()[2]],math.fabs(self.actvelocity[0]),math.fabs(self.actvelocity[1]),False)



