from timer import timer
import time

class tick:
    def __init__(self):
        self.timer = timer()
        self.fps = 60 #estimating what the fps will be without tick regulation
        self.targetFPS = 60
        self.sleepTime = 0
        self.counter = 1
        self.averageFPS = 0
    def update(self): #to be called once every game loop
        self.counter += 1
        self.fps = 1/self.timer.elapsedTime()
        self.timer.reset()
        self.averageFPS = ((self.counter-1)*(self.averageFPS) + self.fps)/self.counter
        if self.targetFPS < self.averageFPS:
            self.sleepTime = (1/self.targetFPS)-(1/self.averageFPS)
            time.sleep(self.sleepTime)
        

    
    

