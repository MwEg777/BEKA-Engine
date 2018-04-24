from Keeper import time_interval
from random import randint
# Every one second, 100 frames will pass, the game is on 100 FPS
'''
Ways of generating a powerup:
    1. Conventional Timer (done)
    2. A flag from the score system (Call for a special reward) with a CODE to choose from available powerups. (done)
    3. Other Rewards (to be decided later by the team)
Types of powerups: *TBListed* (done, check text file "what each does")
What a powerup does: the file RETURNS a FLAG with a certain CODE to be handled by the engine or the game itself.
'''
currentScore = 0                    # !!!!!!!!DUMY SCORE - DELETE when score system is done
currentTime = 0                     # Essential for PowerUp generation calculations
everyFrame = time_interval/1000     # Essential for PowerUp generation calculations
collectedPowerUps = [0, 0, 0]       # To Be Used generatePowerUps function

def stopwatch():
    # Generates a number every second (in relevance to game frame refresh rate) - the time is not accurate.
    global currentTime
    global everyFrame

    currentTime += everyFrame
    currentTime = round(currentTime, 2)

    if currentTime.is_integer():
        return int(currentTime)
    else:
        return 0.1  # just for discrimination


def dummyScoreCounter():
    global currentScore  # DUMY SCORE - DELETE WHEN SCORE SYSTEM IS DONE
    currentScore += 1


def checkForTime(n=5):    # n = obstacle generation rate in seconds, remember: game seconds != real life seconds
    currentSecond = stopwatch()
    if currentSecond != 0.1:
        if currentSecond % n == 0:
            return True
        else:
            return False


def checkForScore(scoreTrigger):
    global currentScore
    dummyScoreCounter()
    if (currentScore / scoreTrigger).is_integer():
        return True
    else:
        return False


def generatePowerUp(t=10, s=0):  # Switches
    """ Switches: if t > 0 then it will check the time, if s is not 0 it will check the score
        both can be activated at once. """
    # ----------Switches Logic-------------
    if (t > 0) and (s != 0):
        currentCheck = checkForScore(s) or checkForTime(t)
    elif t > 0:
        currentCheck = checkForTime(t)
    elif s != 0:
        currentCheck = checkForScore(s)
    else:
        currentCheck = False
    # -------------------------------------

    generate = False
    if currentCheck is True:
        print("💃💃💃💃💃💃💃💃💃💃💃💃💃💃 powerup successfully generated 💃💃💃💃💃💃💃💃💃💃💃💃💃💃💃💃💃💃")
        generate = True
    else:
        generate = False

    global collectedPowerUps
    listOfPowerUps = ["NeutrinoBomb", "Laser Gun", "Kalaxian Crystal", "Yummy Yum's"]
    if generate:
        chosenPowerup = randint(0, 3)               # Choose one of the four powerups
        if chosenPowerup == 0:                      # If Neutrino Bomb was chosen: check for collectibles
            if collectedPowerUps == [1, 1, 1]:      # All collectibles where collected and NeutrinoBomb is available
                chosenPowerup = randint(1, 3)       # to player, now choose from the rest powerups
                return chosenPowerup                # ("Laser Gun", "Kalaxian Crystal", "Yummy Yum's")
            elif collectedPowerUps == [0, 0, 0]:    # If collectibles where still not collected, generate one.
                chosenPowerup = 4
                collectedPowerUps = [1, 0, 0]       # Now I've collected one
                return chosenPowerup
            elif collectedPowerUps == [1, 0, 0]:
                chosenPowerup = 5
                collectedPowerUps = [1, 1, 0]       # Now I've collected two
                return chosenPowerup
            elif collectedPowerUps == [1, 1, 0]:
                chosenPowerup = 6
                collectedPowerUps = [1, 1, 1]       # Now I've collected all of them, go to comment line 83-85
                return chosenPowerup
        else:
            return chosenPowerup
    else:
        return False


def checkCollectibles():    # Hookup with sprites
    print(collectedPowerUps)


def checkIfCollected(someColliderFunction, generatePowerUp):
    pass
    # Add the action of the power up here
    # Help Needed.
