import time

class timer:
    def __init__(self):
        self.startTimestamp = time.time()
    def elapsedTime(self):
        return time.time()-self.startTimestamp
    def reset(self):
        self.startTimestamp = time.time()
