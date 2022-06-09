import pygame, sys
import math
import pygame3D as py3D

class playerObject:
    def __init__(self):
        hitbox = py3D.cuboid(0, 0, 0, 10, 10, 10, "player")
        line1 = py3D.cuboid(0, 0, 0, 5, 0, 0, "player")
        eye1 = py3D.cuboid(0, 0, 0, 2, 2, 0, "player")
        eye2 = py3D.cuboid(0, 0, 0, 2, 2, 0, "player")
    def setPose(self, x, y, z):
        self.hitbox.updatePose(x, y, z)
        self.line1.updatePose(x, y-2, z-5)
        self.eye1.updatePose(x-2, y+2, z-5)
        self.eye2.updatePose(x+2, y+2, z-5)
