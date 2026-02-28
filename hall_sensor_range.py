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

    # TODO replace range check and set by looking at how many standard deviations a value is away from the mean.
    def set_range(self, a):
        # Checking that there are enough values is currently preformed before calling this function
        arr = np.array(self.samples) #converts list to array

        self.avg = np.mean(arr)
        self.stdDev = np.std(arr, ddof=1)

        self.min = self.avg - self.stdDev * a
        self.max = self.avg + self.stdDev * a

    def in_range(self, b):
        # Code structure currently prevents in_range from being called before set_range
        if self.max is None or self.min is None: # TODO If range is always set before this function is called maybe delete this?
            return
        return self.min <= b <= self.max
        
# functions
def display_menu():
    print("Main menu")
    print("1. Add bolt")
    print("2. Test sample")

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
acceptedStdDev = 3

while True:
    display_menu()
    userInput = input()

    match userInput:
        case "f":
            break
        case "1":
            if input("is this bolt ideal? (y/n): ") == "y":
                difBoltTypes.append(Bolt(True))
            else:
                difBoltTypes.append(Bolt())
            
            while True:
                # Relies on user entering the correct values.
                # In the final product the hardware will eliminate this error.
                value = input("Enter test value (press f if done) ")
                if value == "f":
                    if len(difBoltTypes[-1].samples) < 2:
                        print("You need at least two samples per bolt type.")
                    else:
                        difBoltTypes[-1].set_range(acceptedStdDev)
                        break
                else:
                    difBoltTypes[-1].add_sample(float(value))
        case "2":
            if len(difBoltTypes) == 0:
                print("Sample data needs to be collected first")
            else:
                testSample = float(input("Enter test value: "))
                print("Pass: " + f"{difBoltTypes[-1].in_range(testSample)}")
                # TODO currently just looks if bolt is in range but does not check if the range it is in is ideal
        case _:
            print("Invalid option")
            

if len(difBoltTypes) > 0:
    print_bolt_values(0)

