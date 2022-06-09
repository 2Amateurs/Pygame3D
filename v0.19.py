import pygame, sys
from pygame.locals import *
from pygame import mixer
import math
import random 
import time
import enum
import pygame3D as py3D
from pygame3D import objectTypes as types
from random import randint
from playerClass import playerObject
from tick import tick

# Initialize program
pygame.init()
py3D.renderData.setFOV(80)
py3D.renderData.setScreenSize(900, 600)
py3D.renderData.setViewbox(600)

randomObjs = []
floor = py3D.cuboid(0, 0, 0, 500, 0, 500, "terrain")
player = playerObject()

for i in range(50):
    randomObjs.append(py3D.cuboid(randint(-300, 300), randint(-300, 300), randint(-300, 300), randint(0, 100), randint(0, 100), randint(0, 100), "terrain"))

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

toggledCam = True
camMult = 1

camX = 0
camY = 10
camZ = 0

dying = False

pressed = pygame.key.get_pressed()
py3D.renderData.update(0,0,0,0,0)

playerX = 0;
playerY = 50;
playerZ = 0;

xVel = 0
yVel = 0
ZVel = 0

playerWidth = 10
playerHeight = 10
playerDepth = 10

contact = False
ground = False

pitch = 0
yaw = 0

tickRegulation = tick()

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

def correctX():
    global playerX
    global playerY
    global playerZ
    global xVel
    global yVel
    global zVel
    while py3D.touching(player.hitbox):
        playerX -= 0.1*vectoredVel[0]/abs(vectoredVel[0])
        player.setPose(playerX, playerY, playerZ)
    if pressed[pygame.K_SPACE]:
        vectoredVel[0] = -15*vectoredVel[0]/abs(vectoredVel[0])
        xVel = vectoredVel[0]
        yVel = 2
def correctY():
    global playerX
    global playerY
    global playerZ
    global yVel
    global ground
    while py3D.touching(player.hitbox):
        playerY -= 0.1*yVel/abs(yVel)
        player.setPose(playerX, playerY, playerZ)
    if yVel < 0:
        ground = True
    yVel = 0
def correctZ():
    global playerX
    global playerY
    global playerZ
    global xVel
    global yVel
    global zVel
    while py3D.touching(player.hitbox):
        playerZ -= 0.1*vectoredVel[1]/abs(vectoredVel[1])
        player.setPose(playerX, playerY, playerZ)
    if pressed[pygame.K_SPACE]:
        vectoredVel[1] = -15*vectoredVel[1]/abs(vectoredVel[1])
        zVel = vectoredVel[1]
        yVel = 2

def displayAll():
    screen.fill(WHITE)
    py3D.renderData.update(playerX+100*math.cos(pitch)*math.cos(yaw-1.5708), playerY+100*-math.sin(pitch), playerZ+100*math.cos(pitch)*math.sin(yaw-1.5708), pitch, yaw)
    py3D.displayObjects(color=BLACK, objectType=(types.player, types.terrain))
    pygame.display.update()
def tick():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
    #FramePerSec.tick(FPS)
# Beginning Game Loop
while True:
    pressed = pygame.key.get_pressed()
    if not dying:
        if pressed[pygame.K_d]:
            xVel += 0.2
        if pressed[pygame.K_a]:
            xVel -= 0.2
        if pressed[pygame.K_w]:
            zVel += 0.2
        if pressed[pygame.K_s]:
            zVel -= 0.2
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

        yawVel *= 0.8
        pitchVel *= 0.8
        
    xVel *= 0.8
    yVel -= 0.1
    zVel *= 0.9

    vectoredVel[0] = round(xVel * math.cos(yaw) + zVel * math.cos(yaw+1.5708), 5)
    vectoredVel[1] = round(xVel * math.sin(yaw) + zVel * math.sin(yaw+1.5708), 5)

    py3D.renderData.update(camX, camY, camZ, pitch, yaw)
 
    playerX += vectoredVel[0]
    player.setPose(playerX, playerY, playerZ)
    if py3D.touching(player.hitbox):
        correctX()
    playerY += yVel
    if playerY < -200:
        if not dying:
            i = 0
        i+=0.1
        dying = True
        yawVel = 0.01*math.sin(i) + 0.01*i
        pitchVel = 0.01*math.sin(i) + 0.01*i
    if playerY < -3750:
        yawVel = 0
        pitchVel = 0
        yaw = math.atan((playerX)/(playerZ))
        pitch = math.atan((playerY-50)/math.sqrt(playerX**2+playerZ**2)) #+ 1.5708
        rectWidth = 0
        while rectWidth < 900:
            rectWidth += (905-rectWidth)/20
            pygame.draw.rect(screen, BLACK, [0, 0, rectWidth, 600])
            pygame.display.update()
            tick()
        time.sleep(2)
        while abs(51-playerY) > 1.1:
            playerX += (0-playerX)/30
            playerY += (50-playerY)/30
            playerZ += (0-playerZ)/30
            player.setPose(playerX, playerY, playerZ)
            displayAll()
            tick()
        dying = False
    player.setPose(playerX, playerY, playerZ)
    if py3D.touching(player.hitbox):
        correctY()
    playerZ += vectoredVel[1]
    player.setPose(playerX, playerY, playerZ)
    if py3D.touching(player.hitbox):
        correctZ()

    player.setPose(playerX, playerY, playerZ)
    
    yaw += yawVel
    pitch += pitchVel
    displayAll()
    tickRegulation.update()
    tick()
