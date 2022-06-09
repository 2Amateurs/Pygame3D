import pygame, sys
from pygame.locals import *
from pygame import mixer
import math
import random 
import time
import pygame3D as py3D
from pygame3D import objectTypes as types
from random import randint
from playerClass import playerObject
from kinematics import kinematicsClass
from timer import timer

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

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

#defining game variables

toggledCam = True
camMult = 1

loops = 0
text_surface = my_font.render(str(loops), False, (0, 0, 0))

camX = 0
camY = 10
camZ = 0

falling = False

pressed = pygame.key.get_pressed()
kinematicsThread = kinematicsClass()
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

xVel = 0.1
yVel = 0.1
zVel = 0.1
pitchVel = 0
yawVel  = 0
vectoredVel = [0, 0]
timer = timer()

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
        playerX -= 0.05*vectoredVel[0]/abs(vectoredVel[0])
        player.setPose(playerX, playerY, playerZ)
def correctY():
    global playerX
    global playerY
    global playerZ
    global yVel
    global ground
    while py3D.touching(player.hitbox):
        playerY -= 0.05*yVel/abs(yVel)
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
        playerZ -= 0.05*vectoredVel[1]/abs(vectoredVel[1])
        player.setPose(playerX, playerY, playerZ)
def displayAll():
    global loops
    global text_surface
    screen.fill(WHITE)
    py3D.renderData.update(playerX+100*math.cos(pitch)*math.cos(yaw-1.5708), playerY+100*-math.sin(pitch), playerZ+100*math.cos(pitch)*math.sin(yaw-1.5708), pitch, yaw)
    py3D.displayObjects(color=BLACK, objectType=(types.player, types.terrain))
    pygame.draw.rect(screen, WHITE, [0, 0, 100, 50])
    if timer.elapsedTime() > 1:
        timer.reset()
        text_surface = my_font.render(str(loops) + " fps", False, (0, 0, 0))
        loops = 0
    screen.blit(text_surface, (0,0))
    pygame.display.update()
def tick():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
# Beginning Game Loop
while True:
    xVel = kinematicsThread.getXDisplacement()
    zVel = kinematicsThread.getZDisplacement()
    yVel = kinematicsThread.getYDisplacement()

    yawVel = kinematicsThread.getYawDisplacement()
    pitchVel = kinematicsThread.getPitchDisplacement()  

    vectoredVel[0] = round(xVel * math.cos(yaw) + zVel * math.cos(yaw+1.5708), 5)
    vectoredVel[1] = round(xVel * math.sin(yaw) + zVel * math.sin(yaw+1.5708), 5)

    py3D.renderData.update(camX, camY, camZ, pitch, yaw)
 
    playerX += round(vectoredVel[0], 2)
    player.setPose(playerX, playerY, playerZ)
    if py3D.touching(player.hitbox):
        correctX()
    playerY += round(yVel, 1)
    if playerY < -200:
        if not falling:
            i = 0
        i+=0.1
        falling = True
        yawVel = 0.01*math.sin(i) + 0.01*i
        pitchVel = 0.01*math.sin(i) + 0.01*i
    if playerY < -3750:
        yawVel = 0
        if playerZ == 0:
            yaw = 1.5708
        else:
            yaw = math.atan((playerX)/(playerZ))
        if math.sqrt(playerX**2+playerZ**2) == 0:
            pitch = 1.5708
        else:
            pitch = -math.atan((playerY-50)/math.sqrt(playerX**2+playerZ**2))
        rectWidth = 0
        while rectWidth < 900:
            rectWidth += (905-rectWidth)/100
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
        while abs(0-yaw) > 0.01:
            yaw += (0-yaw)/85
            pitch += (0-pitch)/85
            displayAll()
            tick()
        kinematicsThread.reset()
        yVel = 0
        yawVel = 0
        pitchVel = 0
        falling = False
    player.setPose(playerX, playerY, playerZ)
    if py3D.touching(player.hitbox):
        correctY()
    playerZ += round(vectoredVel[1], 2)
    player.setPose(playerX, playerY, playerZ)
    if py3D.touching(player.hitbox):
        correctZ()

    player.setPose(playerX, playerY, playerZ)    
    yaw += yawVel
    pitch += pitchVel
    loops+=1
    displayAll()
    tick()
