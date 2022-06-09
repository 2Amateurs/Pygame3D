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
jumpMeasurer = py3D.cuboid(0, 75, -50, 10, 10, 10, "terrain")
player = playerObject()

#for i in range(50):
 #   randomObjs.append(py3D.cuboid(randint(-300, 300), randint(-300, 300), randint(-300, 300), randint(0, 100), randint(0, 100), randint(0, 100), "terrain"))

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
    py3D.renderData.update(kinematicsThread.playerX+100*math.cos(pitch)*math.cos(yaw-1.5708), kinematicsThread.playerY+100*-math.sin(pitch), kinematicsThread.playerZ+100*math.cos(pitch)*math.sin(yaw-1.5708), pitch, yaw)
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
    
    kinematicsThread.vectorXZ(yaw)
    kinematicsThread.collide(player)

    yawVel = kinematicsThread.getYawDisplacement()
    pitchVel = kinematicsThread.getPitchDisplacement()  

    yaw += yawVel
    pitch += pitchVel
    loops+=1
    displayAll()
    tick()
