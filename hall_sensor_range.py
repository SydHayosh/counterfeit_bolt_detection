import numpy as np

class Bolt:
    def __init__(self, name):
        self.name = name
        self.avg = None
        self.stdDev = None
        self.min = None
        self.max = None
        self.samples = []

    def add_sample(self, s):
        self.samples.append(s)

    def set_range(self, a):
        #TODO check that there are enough values
        arr = np.array(self.samples)

        self.avg = np.mean(arr)
        self.stdDev = np.std(arr, ddof=1)

        self.min = self.avg - self.stdDev * a
        self.max = self.avg + self.stdDev * a

    def in_range(self, b):
        return self.min <= b <= self.max
        




