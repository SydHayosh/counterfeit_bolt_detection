import board
import time
import digitalio
import numpy as np

UP = digitalio.DigitalInOut(board.IO5)
DWN = digitalio.DigitalInOut(board.IO6)
L = digitalio.DigitalInOut(board.IO12)
R = digitalio.DigitalInOut(board.IO13)
MID = digitalio.DigitalInOut(board.IO19)

UP.direction = digitalio.Direction.INPUT
DWN.direction = digitalio.Direction.INPUT
L.direction = digitalio.Direction.INPUT
R.direction = digitalio.Direction.INPUT
MID.direction = digitalio.Direction.INPUT

inputPins = [UP, DWN, L, R, MID]
inputNames = ['UP', 'DWN', 'L', 'R', 'MID']

print("Press MID to begin test...")

while not MID.value:
    
    for i in range(len(inputPins)):
        if inputPins[i].value:
            print(inputNames[i])

    time.sleep(0.1)

print("Test Complete.")