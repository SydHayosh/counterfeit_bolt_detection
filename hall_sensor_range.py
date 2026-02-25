import numpy as np

class Bolt:
    numBoltTypes = 0
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

    def set_range(self, a):
        #TODO check that there are enough values
        arr = np.array(self.samples) #converts list to array

        self.avg = np.mean(arr)
        self.stdDev = np.std(arr, ddof=1)

        self.min = self.avg - self.stdDev * a
        self.max = self.avg + self.stdDev * a

    def in_range(self, b):
        #TODO make sure set_range has been called first
        if self.max is None or self.min is None:
            return
        return self.min <= b <= self.max
        
#functions
def display_menu():
    print("Main menu")
    print("1. Add bolt")
    print("2. Test sample")

#variables
difBoltTypes = []
acceptedStdDev = 3

while True:
    display_menu()
    userInput = input()

    match userInput:
        case "f":
            break
        case "1":
            if input("is this bolt ideal? (y/n) : ") == "y":
                difBoltTypes.append(Bolt(True))
            else:
                difBoltTypes.append(Bolt())
            
            while True:
                # Relies on user entering the correct values.
                # In the final product the hardware will eliminate error.
                value = input("Enter test value (press c if done)")
                if value == "c":
                    if len(difBoltTypes[Bolt.numBoltTypes - 1].samples) < 2:
                        print("You need at least two samples per bolt type.")
                    else:
                        difBoltTypes[Bolt.numBoltTypes - 1].set_range(acceptedStdDev)
                        break
                else:
                    difBoltTypes[Bolt.numBoltTypes - 1].add_sample(float(value))
        case _:
            print("Invalid option")
            

print("\n--- " + difBoltTypes[0].name + " ---")
print("Sample data: " + f"{difBoltTypes[0].samples}")
print("Average: " + f"{difBoltTypes[0].avg}")
print("Standard Deviation: " + f"{difBoltTypes[0].stdDev}")
print("Minimum: " + f"{difBoltTypes[0].min}")
print("Maximum: " + f"{difBoltTypes[0].max}")

