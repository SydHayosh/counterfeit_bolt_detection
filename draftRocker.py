import board
import time
import digitalio
import numpy as np

UP = digitalio.DigitalInOut(board.D6)#5
DWN = digitalio.DigitalInOut(board.D5)#6
L = digitalio.DigitalInOut(board.D13)#12
R = digitalio.DigitalInOut(board.D12)#13
MID = digitalio.DigitalInOut(board.D19)#19

inputPins = [UP, DWN, L, R, MID]
inputNames = ['UP', 'DWN', 'L', 'R', 'MID']

for pin in inputPins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP

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