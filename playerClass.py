import pygame, sys
import math
import pygame3D as py3D

class playerObject:
    def __init__(self):
        self.hitbox = py3D.cuboid(0, 0, 0, 10, 10, 10, "player")
        self.line1 = py3D.cuboid(0, 0, 0, 2, 0, 0, "player")
        self.line2 = py3D.cuboid(0, 0, 0, 1.5, 0, 0, "player")
        self.line3 = py3D.cuboid(0, 0, 0, 1.5, 0, 0, "player")
        self.line4 = py3D.cuboid(0, 0, 0, 1, 0, 0, "player")
        self.line5 = py3D.cuboid(0, 0, 0, 1, 0, 0, "player")
        self.eye1 = py3D.cuboid(0, 0, 0, 2, 2, 0, "player")
        self.eye2 = py3D.cuboid(0, 0, 0, 2, 2, 0, "player")
    def setPose(self, x, y, z):
        self.hitbox.setPose(x, y, z)
        self.line1.setPose(x, y-3, z-5)
        self.line2.setPose(x-1.75, y-2.8, z-5)
        self.line3.setPose(x+1.75, y-2.8, z-5)
        self.line4.setPose(x-2.5, y-2.55, z-5)
        self.line5.setPose(x+2.5, y-2.55, z-5)
        self.eye1.setPose(x-2, y+2, z-5)
        self.eye2.setPose(x+2, y+2, z-5)
