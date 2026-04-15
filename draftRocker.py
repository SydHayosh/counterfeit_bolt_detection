import board
import time
import digitalio
import numpy as np

UP = digitalio.DigitalInOut(board.D6)
DWN = digitalio.DigitalInOut(board.D5)
L = digitalio.DigitalInOut(board.D13)
R = digitalio.DigitalInOut(board.D12)
MID = digitalio.DigitalInOut(board.D19)

UP.direction = digitalio.Direction.INPUT
DWN.direction = digitalio.Direction.INPUT
L.direction = digitalio.Direction.INPUT
R.direction = digitalio.Direction.INPUT
MID.direction = digitalio.Direction.INPUT

inputPins = [UP, DWN, L, R, MID]
inputNames = ['UP', 'DWN', 'L', 'R', 'MID']

#print("Press MID to begin test...")

#while not MID.value:
#    time.sleep(0.1)
    
#print("Press MID to end test...")
    
#while not MID.value:
#    for i in range(len(inputPins)):
#        print(inputNames[i] + ": " + str(inputPins[i].value))

#    time.sleep(1)

#print("Test Complete.")

lastState = [True] * len(inputPins)

while True:
    for i in range(len(inputPins)):
        currentState = inputPins[i].value
        
        if lastState[i] == True and currentState == False:
            print(f"{inputNames[i]} pressed")
            
        lastState[i] = currentState
        
    time.sleep(0.05)