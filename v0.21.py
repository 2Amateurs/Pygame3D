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
floor = py3D.cuboid(0, -25, 0, 500, 50, 500, "terrain")
jumpMeasurer = py3D.cuboid(0, 75, -50, 10, 10, 10, "terrain")
player = playerObject()

for i in range(50):
    randomObjs.append(py3D.cuboid(randint(-300, 300), randint(-300, 300), randint(-300, 300), randint(0, 100), randint(0, 100), randint(0, 100), "terrain"))

# Setting up color objects
GREEN = (78, 154, 78)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (94, 251, 255)

#defining game variables
loops = 0
text_surface = my_font.render(str(loops), False, (0, 0, 0))

camX = 0
camY = 10
camZ = 0

falling = False

pressed = pygame.key.get_pressed()
kinematics = kinematicsClass()
py3D.renderData.update(0,0,0,0,0)

playerX = 0;
playerY = 50;
playerZ = 0;

pitch = 0
yaw = 0

pitchVel = 0
yawVel  = 0
timer = timer()

# setting up display
screen = pygame.display.set_mode((900, 600))

def displayAll():
    global loops
    global text_surface
    screen.fill(WHITE)
    py3D.renderData.update(kinematics.playerX+100*math.cos(pitch)*math.cos(yaw-1.5708), kinematics.playerY+100*-math.sin(pitch), kinematics.playerZ+100*math.cos(pitch)*math.sin(yaw-1.5708), pitch, yaw)
    py3D.displayObjects(color=BLACK, objectType=(types.player, types.terrain))
    pygame.draw.rect(screen, WHITE, [0, 0, 100, 50])
    if timer.elapsedTime() > 1:
        timer.reset()
        text_surface = my_font.render(str(loops) + " fps", False, (0, 0, 0))
        loops = 0
    screen.blit(text_surface, (0,0))
    pygame.display.update()
def checkForExit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

#play music!!!
#mixer.init()
#mixer.music.load("./Music/elevator.wav")
#mixer.music.set_volume(0.7)
#mixer.music.play()

# Beginning Game Loop
while True:
    xVel = kinematics.getXDisplacement()
    zVel = kinematics.getZDisplacement()
    yVel = kinematics.getYDisplacement()
    
    kinematics.vectorXZ(yaw)
    kinematics.collide(player)

    yawVel = kinematics.getYawDisplacement()
    pitchVel = kinematics.getPitchDisplacement()

    yaw += yawVel
    pitch += pitchVel
    loops+=1
    displayAll()
    checkForExit()
