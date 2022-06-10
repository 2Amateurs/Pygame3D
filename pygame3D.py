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
    def __init__(self, x, y, z, parent): 
        self.x = x
        self.y = y
        self.z = z
        self.xRelative = 0
        self.yRelative = 0
        self.zRelative = 0
        self.rotationValues = [0, 0, 0, 0] #1: x 2: z 3: z 4: y
        self.myParent = parent
        self.myParent.pointRegistry.append(self)
        self.myIndex = len(self.myParent.pointRegistry)-1
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
        self.rotationValues[0] = self.xRelative*math.cos(-yaw) - self.zRelative*math.sin(-yaw)
        self.rotationValues[1] = self.xRelative*math.sin(-yaw) + self.zRelative*math.cos(-yaw)
        self.rotationValues[2] = self.rotationValues[1]*math.cos(-pitch) - self.yRelative*math.sin(-pitch)
        self.rotationValues[3]  = self.rotationValues[1]*math.sin(-pitch) + self.yRelative*math.cos(-pitch)
        self.xRelative = self.rotationValues[0]
        self.yRelative = self.rotationValues[3]
        self.zRelative = self.rotationValues[2]
        return self
    def projectTo2D(self):
        self.xProjected = (renderData.screenWidth/2 + (renderData.viewbox*self.xRelative)/((self.zRelative)*renderData.FOVconst))
        self.yProjected = (renderData.screenHeight/2 - (renderData.viewbox*self.yRelative)/((self.zRelative)*renderData.FOVconst))
        if self.zRelative < 0:
            self.xProjected = None
class cuboidRegistry:
    def __init__(self):
        self.registry = []
        self.touchingID = 0
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
        self.pointRegistry = []
        self.point1 = point(0, 0, 0, self)#passes the self parameter so each point can easily access the parent object
        self.point2 = point(0, 0, 0, self)
        self.point3 = point(0, 0, 0, self)
        self.point4 = point(0, 0, 0, self)
        self.point5 = point(0, 0, 0, self)
        self.point6 = point(0, 0, 0, self)
        self.point7 = point(0, 0, 0, self)
        self.point8 = point(0, 0, 0, self)
        self.setPoints()
        self.objectType = objectType
        cuboidRegistry.registry.append(self)
    def setPose(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.setPoints()
    def setupDisplay(self):
        for item in self.pointRegistry:
            item.update().rotateAroundCam(renderData.pitch, renderData.yaw).projectTo2D()
    def drawLine(self, x1, y1, x2, y2, color):
        if not((x1 == None) or (x2 == None)):
            pygame.draw.line(renderData.screen, color, (x1, y1), (x2, y2), 3)
    def display(self, color):
        self.drawLine(self.point1.xProjected, self.point1.yProjected, self.point2.xProjected, self.point2.yProjected, color)
        self.drawLine(self.point2.xProjected, self.point2.yProjected, self.point3.xProjected, self.point3.yProjected, color)
        self.drawLine(self.point3.xProjected, self.point3.yProjected, self.point4.xProjected, self.point4.yProjected, color)
        self.drawLine(self.point4.xProjected, self.point4.yProjected, self.point1.xProjected, self.point1.yProjected, color)
        self.drawLine(self.point5.xProjected, self.point5.yProjected, self.point6.xProjected, self.point6.yProjected, color)
        self.drawLine(self.point6.xProjected, self.point6.yProjected, self.point7.xProjected, self.point7.yProjected, color)
        self.drawLine(self.point7.xProjected, self.point7.yProjected, self.point8.xProjected, self.point8.yProjected, color)
        self.drawLine(self.point8.xProjected, self.point8.yProjected, self.point5.xProjected, self.point5.yProjected, color)
        self.drawLine(self.point1.xProjected, self.point1.yProjected, self.point5.xProjected, self.point5.yProjected, color)
        self.drawLine(self.point2.xProjected, self.point2.yProjected, self.point6.xProjected, self.point6.yProjected, color)
        self.drawLine(self.point3.xProjected, self.point3.yProjected, self.point7.xProjected, self.point7.yProjected, color)
        self.drawLine(self.point4.xProjected, self.point4.yProjected, self.point8.xProjected, self.point8.yProjected, color)
    def contact(self, objectX, objectY, objectZ, objectWidth, objectHeight, objectDepth):
        return (objectX + objectWidth/2 > self.x-self.width/2) and (objectX - objectWidth/2 < self.x+self.width/2) and (objectY + objectHeight/2 > self.y-self.height/2) and (objectY - objectHeight/2 < self.y+self.height/2) and (objectZ + objectDepth/2 > self.z-self.depth/2) and (objectZ - objectDepth/2 < self.z+self.depth/2)
def touching(hitbox):
    touching = False
    i = 0
    for item in cuboidRegistry.registry:
        if item.contact(hitbox.x, hitbox.y, hitbox.z, hitbox.width, hitbox.height, hitbox.depth) and not (item.objectType == 'player' or item is hitbox):
            touching = True
            cuboidRegistry.touchingID = i
        i+=1
    return touching
def displayObjects(color, objectType):
    for item in cuboidRegistry.registry:
        item.setupDisplay()
        item.display(color)
