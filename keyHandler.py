import pygame
from timer import timer

class keyHandlerClass:
    def __init__(self, myKey):
        self.myTimer = timer()
        self.amActive = False
        self.activeTime = 0
        self.pressed = pygame.key.get_pressed()
        self.myKey = myKey
        self.condition = False
    def setCondition(self, condition):
        self.condition = condition
    def getActiveTime(self, pressed): #to be called whenever the kinematics module updates
        if pressed[self.myKey]:
            elapsedTime = self.myTimer.elapsedTime()
        else:
            elapsedTime = 0
        self.myTimer.reset()
        return elapsedTime
    def reset(self):
        self.myTimer.reset()


        
