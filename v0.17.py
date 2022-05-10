import pygame, sys
from pygame.locals import *
from pygame import mixer
import math
import random 
import time
import enum
import pygame3D as py3D
from pygame3D import objectTypes as types

 
# Initialize program
pygame.init()
py3D.renderData.setFOV(80)
py3D.renderData.setScreenSize(900, 600)
py3D.renderData.setViewbox(600)

player = py3D.cuboid(0, 0, 0, 10, 10, 10, "player")
cuboid1 = py3D.cuboid(0, 50, 0, 10, 10, 10, "terrain")
cuboid2 = py3D.cuboid(0, 0, 50, 10, 10, 10, "terrain")
cuboid3 = py3D.cuboid(50, 0, 0, 10, 10, 10, "terrain")
cuboid4 = py3D.cuboid(0, 50, 50, 10, 10, 10, "terrain")
cuboid5 = py3D.cuboid(100, 0, 0, 100, 10, 10, "terrain")
 
# Assign FPS a value
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Setting up color objects
GREEN = (78, 154, 78)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (94, 251, 255)
MULTI_1 = (0, 0, 0)
MULTI_2 = (0, 0, 0)

#defining game variables

class debounce:
    def __init__(self): #Python constructors are a little annoying.  I prefer good old Java
        self.lastValue = False
        self.currentValue = False
    def update(self, button):
        if self.lastValue == False and button == True: 
            self.currentValue = True
        else:
            self.currentValue = False
        self.lastValue = button

toggledCam = True
camMult = 1
debouncedC = debounce()

camX = 0
camY = 10
camZ = 0


pressed = pygame.key.get_pressed()
py3D.renderData.update(0,0,0,0,0)

playerX = 0;
playerY = 0;
playerZ = -100;

playerWidth = 10
playerHeight = 10
playerDepth = 10

contact = False
ground = False

pitch = 0
yaw = 0

class State(enum.Enum):
    setup = 1
    collideX = 2
    collideY = 3
    collideZ = 4
    display = 5
    render = 6
    
state = State.setup

pointX = []
pointY = []


xVel = -5
yVel = -5
zVel = -5
pitchVel = 0
yawVel  = 0

vectoredVel = [0, 0]

# setting up display
screen = pygame.display.set_mode((900, 600))


# Beginning Game Loop
while True:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_d]:
        xVel += 0.2
    if pressed[pygame.K_a]:
        xVel -= 0.2
    if pressed[pygame.K_w]:
        zVel += 0.2
    if pressed[pygame.K_s]:
        zVel -= 0.2
    if pressed[pygame.K_q]:
        yVel -= 0.5
    if pressed[pygame.K_e]:
        yVel += 0.5
    if pressed[pygame.K_SPACE] and ground:
        ground = False
        yVel = 12
    if pressed[pygame.K_RIGHT]:
        yawVel -= 0.007 * camMult
    if pressed[pygame.K_LEFT]:
        yawVel += 0.007 * camMult
    if pressed[pygame.K_UP]:
        pitchVel += 0.007 * camMult
    if pressed[pygame.K_DOWN]:
        pitchVel -= 0.007 * camMult
        
    if abs(xVel) > 4:
        xVel = 2*xVel/abs(xVel)
    if abs(yVel) > 4:
        yVel = 2*yVel/abs(yVel)
    if abs(zVel) > 4:
        zVel = 2*zVel/abs(zVel)

    xVel *= 0.8
    yVel *= 0.8
    zVel *= 0.9
    yawVel *= 0.8
    pitchVel *= 0.8

    vectoredVel[0] = round(xVel * math.cos(yaw) + zVel * math.cos(yaw+1.5708), 5)
    vectoredVel[1] = round(xVel * math.sin(yaw) + zVel * math.sin(yaw+1.5708), 5)

    py3D.renderData.update(camX, camY, camZ, pitch, yaw)
 
    playerX += vectoredVel[0]
    playerY += yVel
    playerZ += vectoredVel[1]
    
    yaw += yawVel
    pitch += pitchVel

    debouncedC.update(pressed[pygame.K_c])
        
    screen.fill(WHITE)
    py3D.renderData.update(playerX+100*math.cos(pitch)*math.cos(yaw-1.5708), playerY+100*-math.sin(pitch), playerZ+100*math.cos(pitch)*math.sin(yaw-1.5708), pitch, yaw)
    player.setPose(playerX, playerY, playerZ)
    py3D.displayObjects(color=BLACK, objectType=(types.player, types.terrain))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
    FramePerSec.tick(FPS)
