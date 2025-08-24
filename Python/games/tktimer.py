import time

class Timer:
    start_time: int
    length: int

    def __init__(self, length):
        self.start_time = time.time()
        self.length = length
    
    def finished(self):
        return time.time() >= self.start_time + self.length