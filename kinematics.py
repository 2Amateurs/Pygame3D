import pygame
from timer import timer
from keyHandler import keyHandlerClass
import math
import pygame3D as py3D

class kinematicsClass:
    def __init__(self):
        self.dKey = keyHandlerClass(pygame.K_d)
        self.aKey = keyHandlerClass(pygame.K_a)
        self.wKey = keyHandlerClass(pygame.K_w)
        self.sKey = keyHandlerClass(pygame.K_s)
        self.rightKey = keyHandlerClass(pygame.K_RIGHT)
        self.leftKey = keyHandlerClass(pygame.K_LEFT)
        self.upKey = keyHandlerClass(pygame.K_UP)
        self.downKey = keyHandlerClass(pygame.K_DOWN)
        self.yTimer = timer()
        self.fallVel = 0
        self.jumpVel = 0
        self.xVel = 0
        self.vectoredXVel = 5
        self.yVel = 5
        self.zVel = 0
        self.vectoredZVel = 5
        self.pitchVel = 0
        self.yawVel = 0
        self.playerX = 0
        self.playerY = 50
        self.playerZ = 0
        self.onGround = False
    def getXDisplacement(self):
        pressed = pygame.key.get_pressed()
        self.xVel = 100*self.dKey.getActiveTime(pressed)-100*self.aKey.getActiveTime(pressed)
        return self.xVel
    def getYDisplacement(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and self.onGround:
            self.jumpVel = 700
        self.fallVel += self.yTimer.elapsedTime()*-3000
        self.yVel = self.yTimer.elapsedTime()*(self.fallVel + self.jumpVel) 
        self.yTimer.reset()
        return self.yVel
    def getZDisplacement(self):
        pressed = pygame.key.get_pressed()
        self.zVel = 100*self.wKey.getActiveTime(pressed)-100*self.sKey.getActiveTime(pressed)
        return self.zVel
    def getPitchDisplacement(self):
        pressed = pygame.key.get_pressed()
        self.pitchVel = 2*self.upKey.getActiveTime(pressed)-3*self.downKey.getActiveTime(pressed)
        return self.pitchVel
    def getYawDisplacement(self):
        pressed = pygame.key.get_pressed()
        self.yawVel = 2*self.leftKey.getActiveTime(pressed)-3*self.rightKey.getActiveTime(pressed)
        return self.yawVel
    def vectorXZ(self, yaw):
        self.vectoredXVel = round(self.xVel * math.cos(yaw) + self.zVel * math.cos(yaw+1.5708), 5)
        self.vectoredZVel = round(self.xVel * math.sin(yaw) + self.zVel * math.sin(yaw+1.5708), 5)
    def collide(self, player):
        self.playerX += self.vectoredXVel
        player.setPose(self.playerX, self.playerY, self.playerZ)
        if py3D.touching(player.hitbox):
            while py3D.touching(player.hitbox):
                self.playerX += -0.01*self.vectoredXVel/abs(self.vectoredXVel)
                player.setPose(self.playerX, self.playerY, self.playerZ)
            self.dKey.reset()
            self.aKey.reset()
            self.wKey.reset()
            self.sKey.reset()   
        self.playerY += self.yVel
        player.setPose(self.playerX, self.playerY, self.playerZ)
        self.onGround = False
        if py3D.touching(player.hitbox):
            while py3D.touching(player.hitbox):
                self.playerY += -0.01*self.yVel/abs(self.yVel)
                player.setPose(self.playerX, self.playerY, self.playerZ)
            if self.yVel < 0:
                self.onGround = True
            self.fallVel = 0
            self.jumpVel = 0
            self.yTimer.reset()
        self.playerZ += self.vectoredZVel
        player.setPose(self.playerX, self.playerY, self.playerZ)
        if py3D.touching(player.hitbox):
            while py3D.touching(player.hitbox):
                self.playerZ += -0.01*self.vectoredZVel/abs(self.vectoredZVel)
                player.setPose(self.playerX, self.playerY, self.playerZ)
            self.dKey.reset()
            self.aKey.reset()
            self.wKey.reset()
            self.sKey.reset()
    def reset(self):
        self.dKey.reset()
        self.aKey.reset()
        self.wKey.reset()
        self.sKey.reset()
        self.rightKey.reset()
        self.leftKey.reset()
        self.upKey.reset()
        self.downKey.reset()
        self.yTimer.reset()
