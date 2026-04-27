import numpy as np
import pandas as pd
from .magReader import magRead

acceptedNumOfStdDev = 2

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
#setup_read_dataset(file_path, column_name, num_std=acceptedNumOfStdDev)

def getIdealData(num_std):
    idealBolt = pd.read_csv("./idealBolt.csv", index_col="Axis")
    xRaw = idealBolt.loc["X"].to_numpy()
    yRaw = idealBolt.loc["Y"].to_numpy()
    zRaw = idealBolt.loc["Z"].to_numpy()

    x = [ (xRaw[0] - num_std*xRaw[1]), (xRaw[0] + num_std*xRaw[1])]
    y = [ (yRaw[0] - num_std*yRaw[1]), (yRaw[0] + num_std*yRaw[1]) ]
    z = [ (zRaw[0] - num_std*zRaw[1]), (zRaw[0] + num_std*zRaw[1]) ]

    idealData = [x, y, z]
    return idealData

def magTest(idealData, ambient):
    passCriteria = [False, False, False]
    sample = magRead(3)
    #This code will check to see if the samples X, Y, and Z readings are good. 
    for i in range(len(passCriteria)):
        if (idealData[i][0] <= sample[i] <= idealData[i][1]):
            passCriteria[i] = True
        else:
            passCriteria[i] = False

    return (all(passCriteria))

