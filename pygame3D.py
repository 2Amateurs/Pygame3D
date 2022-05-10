import math
import pygame
import enum
import numpy as np

class renderData:
    def __init__(self):
        self.camX = 0
        self.camY = 0
        self.camZ = 0
        self.pitch = 0
        self.yaw = 0
        self.screenWidth = 0
        self.screenHeight = 0
        self.screen = 0
        self.viewbox = 0
        self.FOVconst = 0
    print('Pygame3D module initialized.')
    def setFOV(self, FOV):
        self.FOVconst = math.tan(math.radians(FOV/2))
    def setScreenSize(self, width, height):
        self.screenWidth = width
        self.screenHeight = height
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
    def setViewbox(self, viewbox):
        self.viewbox = viewbox
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
    def update(self, camX, camY, camZ, pitch, yaw):
        self.camX = camX
        self.camY = camY
        self.camZ = camZ
        self.pitch = pitch
        self.yaw = yaw
renderData = renderData()
class objectTypes(enum.Enum):
    player = 1
    terrain = 2
    enemy = 3
class point:
    def __init__(self, x, y, z): 
        self.x = x
        self.y = y
        self.z = z
        self.xRelative = 0
        self.yRelative = 0
        self.zRelative = 0
        self.yPitchVector = 0
        self.zPitchVector = 0
        self.yawHypotenuse = 0
        self.adjacent = 0
        self.xProjected = 0
        self.yProjected = 0
        self.thetaPitch = 0
        self.thetaYaw = 0
    def update(self):
       self.xRelative = self.x-renderData.camX
       self.yRelative = self.y-renderData.camY
       self.zRelative = self.z-renderData.camZ
       return self
    def setPose(self, newX, newY, newZ):
        self.x = newX
        self.y = newY
        self.z = newZ
    def mult(self, value):
        if value == 0:
            return 1
        else:
            return value/abs(value)
    def rotateAroundCam(self, pitch, yaw):
        self.yPitchVector = self.yRelative * math.cos(pitch)
        self.zPitchVector = self.yRelative * math.sin(pitch)
        self.yawHypotenuse = math.sqrt((self.xRelative**2)+(self.zRelative**2)) * self.mult(self.zRelative)
        if self.zRelative == 0:
            self.thetaYaw = 1.5708
        else:
            self.thetaYaw = math.atan(self.xRelative/self.zRelative) + yaw
        self.adjacent = self.yawHypotenuse * math.cos(self.thetaYaw)
        self.thetaPitch = pitch + 1.5708
        self.xRelative = self.yawHypotenuse * math.sin(self.thetaYaw+0.002*self.xRelative)
        self.yRelative = self.adjacent * math.cos(self.thetaPitch+0.001*self.zRelative+0.1*pitch) + self.yPitchVector
        self.zRelative = self.adjacent * math.sin(self.thetaPitch+0.001*self.yRelative+0.1*yaw) + self.zPitchVector
        return self
    def projectTo2D(self):
        if self.zRelative <= 1:#A temporary solution that I need to fix
            self.xProjected = 0#None
            self.yProjected = 0#None
        else:
            self.xProjected = renderData.screenWidth/2 + (renderData.viewbox*self.xRelative)/((self.zRelative+1)*renderData.FOVconst)
            self.yProjected = renderData.screenHeight/2 - (renderData.viewbox*self.yRelative)/((self.zRelative+1)*renderData.FOVconst)
class cuboidRegistry:
    def __init__(self):
        self.registry = []
cuboidRegistry = cuboidRegistry()
class cuboid:
    def setPoints(self):
        self.point1.setPose(self.x-self.width/2, self.y-self.height/2, self.z-self.depth/2)
        self.point2.setPose(self.x-self.width/2, self.y+self.height/2, self.z-self.depth/2)
        self.point3.setPose(self.x+self.width/2, self.y+self.height/2, self.z-self.depth/2)
        self.point4.setPose(self.x+self.width/2, self.y-self.height/2, self.z-self.depth/2)
        self.point5.setPose(self.x-self.width/2, self.y-self.height/2, self.z+self.depth/2)
        self.point6.setPose(self.x-self.width/2, self.y+self.height/2, self.z+self.depth/2)
        self.point7.setPose(self.x+self.width/2, self.y+self.height/2, self.z+self.depth/2)
        self.point8.setPose(self.x+self.width/2, self.y-self.height/2, self.z+self.depth/2)
    def __init__(self, x, y, z, width, height, depth, objectType):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.point1 = point(0, 0, 0)
        self.point2 = point(0, 0, 0)
        self.point3 = point(0, 0, 0)
        self.point4 = point(0, 0, 0)
        self.point5 = point(0, 0, 0)
        self.point6 = point(0, 0, 0)
        self.point7 = point(0, 0, 0)
        self.point8 = point(0, 0, 0)
        self.setPoints()
        self.objectType = objectType
        cuboidRegistry.registry.append(self)
    def setPose(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.setPoints()
    def display(self, color):
        self.point1.update().rotateAroundCam(renderData.pitch, renderData.yaw,).projectTo2D()
        self.point2.update().rotateAroundCam(renderData.pitch, renderData.yaw,).projectTo2D()
        self.point3.update().rotateAroundCam(renderData.pitch, renderData.yaw,).projectTo2D()
        self.point4.update().rotateAroundCam(renderData.pitch, renderData.yaw,).projectTo2D()
        self.point5.update().rotateAroundCam(renderData.pitch, renderData.yaw,).projectTo2D()
        self.point6.update().rotateAroundCam(renderData.pitch, renderData.yaw,).projectTo2D()
        self.point7.update().rotateAroundCam(renderData.pitch, renderData.yaw,).projectTo2D()
        self.point8.update().rotateAroundCam(renderData.pitch, renderData.yaw,).projectTo2D()
        pygame.draw.line(renderData.screen, color, (self.point1.xProjected, self.point1.yProjected), (self.point2.xProjected, self.point2.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point2.xProjected, self.point2.yProjected), (self.point3.xProjected, self.point3.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point3.xProjected, self.point3.yProjected), (self.point4.xProjected, self.point4.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point4.xProjected, self.point4.yProjected), (self.point1.xProjected, self.point1.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point5.xProjected, self.point5.yProjected), (self.point6.xProjected, self.point6.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point6.xProjected, self.point6.yProjected), (self.point7.xProjected, self.point7.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point7.xProjected, self.point7.yProjected), (self.point8.xProjected, self.point8.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point8.xProjected, self.point8.yProjected), (self.point5.xProjected, self.point5.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point1.xProjected, self.point1.yProjected), (self.point5.xProjected, self.point5.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point2.xProjected, self.point2.yProjected), (self.point6.xProjected, self.point6.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point3.xProjected, self.point3.yProjected), (self.point7.xProjected, self.point7.yProjected), 3)
        pygame.draw.line(renderData.screen, color, (self.point4.xProjected, self.point4.yProjected), (self.point8.xProjected, self.point8.yProjected), 3)
    def contact(self, objectX, objectY, objectZ, objectWidth, objectHeight, objectDepth):
        return (objectX + objectWidth/2 > self.x-self.width/2) and (objectX - objectWidth/2 < self.x+self.width/2) and (objectY + objectHeight/2 > self.y-self.height/2) and (objectY - objectHeight/2 < self.y+self.height/2) and (objectZ + objectDepth/2 > self.z-self.depth/2) and (objectZ - objectDepth/2 < self.z+self.depth/2)
def displayObjects(color, objectType):
    for item in cuboidRegistry.registry:
        item.display(color)
