import numpy as np
#import pandas as pd

class Bolt:
    numBoltTypes = 0
    # x, y, z
    def __init__(self, ideal = False):
        Bolt.numBoltTypes += 1
        self.name = "Sample type " + str(Bolt.numBoltTypes)
        self.ideal = ideal
        self.avg = None
        self.stdDev = None
        self.min = None
        self.max = None
        self.samples = []

    def add_sample(self, s):
        self.samples.append(s)

    def set_range(self, numStd):
        # Checking that there are enough values is currently preformed before calling this function
        arr = np.array(self.samples) #converts list to array

        self.avg = np.mean(arr)
        self.stdDev = np.std(arr, ddof=1)

        self.min = self.avg - self.stdDev * numStd
        self.max = self.avg + self.stdDev * numStd

    # Checks that bolt value is within an acceptable number of standard deviations
    def in_range(self, b):
        # Code structure currently prevents in_range from being called before set_range
        if self.max is None or self.min is None:
            return
        return self.min <= b <= self.max
        
# functions
def print_bolt_values(i):
    print("\n--- " + difBoltTypes[i].name + " ---")
    print("Ideal: " + f"{difBoltTypes[i].ideal}")
    print("Sample data: " + f"{difBoltTypes[i].samples}")
    print("Average: " + f"{difBoltTypes[i].avg}")
    print("Standard Deviation: " + f"{difBoltTypes[i].stdDev}")
    print("Minimum: " + f"{difBoltTypes[i].min}")
    print("Maximum: " + f"{difBoltTypes[i].max}")

# variables
difBoltTypes = []
acceptedNumOfStdDev = 3

idealBolt = None

#setup_read_dataset(file_path, column_name, num_std=acceptedNumOfStdDev)
def setup_read_dataset():
    # Example dataset (replace with Excel later)
    global idealBolt
    idealBolt = Bolt(ideal=True)
    data = [10.1, 9.9, 10.0, 10.2, 9.8]

    for d in data:
        idealBolt.add_sample(d)

    idealBolt.set_range(num_std)

testSample = 10.15 

#z first x then y
def mag_test(test_value):
    if idealBolt.in_range(test_value):
        print("Magnetic test passed")
    else:
        print("Magnetic test failed")
    return idealBolt.in_range(test_value)

            
