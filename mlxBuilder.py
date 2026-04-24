import time
import board
import busio
import digitalio
import adafruit_mlx90393 as maglib

import numpy as np
import pandas as pd 
from frameworkOperator.pins import UP, DWN, L, R, MID, inputPins, inputNames
import frameworkOperator.pins

def quickMean(vec):
    length = len(vec)
    sum = 0
    i = 0
    while (i < len(vec)):
        sum += vec[i]
        i += 1
    
    mean = sum/length

    return mean
i2c = board.I2C()  # uses board.SCL and board.SDA

testX = []
testY = []
testZ = []
testC = []

entryX = []
entryY = []
entryZ = []
entryC = []
    
try: 
    sensor = maglib.MLX90393(i2c)
except ValueError:
    sensor = maglib.MLX90393(i2c, address=0x18)
    
print("Press MID to record ambient.")

#Button debounce, only moves to next stage once button is pressed then unpressed
while True:
    if not MID.value:
        while not MID.value:
            pass
        break

while True:
    
    x, y, z = sensor.magnetic
    #temp = sensor.temperature
    
    displayOut = [f'Recording... (Press MID stop recording)',
    f'X:    {x:.2f} μT',
    f'Y:    {y:.2f} μT',
    f'Z:    {z:.2f} μT',
    ]
    
    print('\n'.join(displayOut), flush=True)
    print(f'\033[{len(displayOut)}A', end='', flush=True)
    
    testX.append(x)
    testY.append(y)
    testZ.append(z)
    
    if not MID.value:
        while not MID.value:
            pass
        break
    #testC.append(temp)

entryX.append(quickMean(testX))
entryY.append(quickMean(testY))
entryZ.append(quickMean(testZ))
#entryC.append(quickMean(testC))

entryX.append('')
entryY.append('')
entryZ.append('')
#entryC.append('')

time.sleep(0.5)

displayOut = ['Press MID to record bolt data.          ',
'Hold R for 3s to end and output to .xlsx.',
'                   ',
'                   ',]

print('\n'.join(displayOut), flush=True)
print(f'\033[{len(displayOut)}A', end='', flush=True)

print('\n')
timeInit = time.monotonic()

runTest = True

while runTest:
    
    timer = time.monotonic()
    
    while not R.value:
        if time.monotonic() >= timer + 3:
            runTest = False
            break
    x, y, z = sensor.magnetic
#    temp = sensor.temperature
    
    displayOut = [f'Insert sample...                         ',
    f'Runtime: {time.monotonic() - timeInit:.3f}s',
    f'X:    {x:.3f} μT',
    f'Y:    {y:.3f} μT',
    f'Z:    {z:.3f} μT',
    ]

    print('\n'.join(displayOut), flush=True)
    print(f'\033[{len(displayOut)}A', end='', flush=True)

    if not MID.value:
        while not MID.value:
            pass
                
        while True:
            x, y, z = sensor.magnetic
            #temp = sensor.temperature
            
            displayOut = [f'Recording... (Press MID stop recording)',
            f'Runtime: {time.monotonic() - timeInit:.3f}s',
            f'X:    {x:.3f} μT',
            f'Y:    {y:.3f} μT',
            f'Z:    {z:.3f} μT',
            ]
            
            print('\n'.join(displayOut), flush=True)
            print(f'\033[{len(displayOut)}A', end='', flush=True)
            
            testX.append(x)
            testY.append(y)
            testZ.append(z)
#            testC.append(temp)
            if not MID.value:
                while not MID.value:
                    pass
                break
        
        entryX.append(quickMean(testX))
        entryY.append(quickMean(testY))
        entryZ.append(quickMean(testZ))
#        entryC.append(quickMean(testC))
    
    time.sleep(0.1)
    
print("\n\n\n\n\n===================")
boltName = input("Bolt Name: ")
print("Generating Excel File...")

df = pd.DataFrame({
    'X Output (μT)': entryX,
    'Y Output (μT)': entryY,
    'Z Output (μT)': entryZ,
})

timestamp = time.strftime('%Y%m%d_%H_%M_%S', time.localtime())
df.to_excel("MLX_" + format(boltName) + "_" + timestamp + '.xlsx', index=False, sheet_name='MLX90393 Readings')

print( format(boltName) + " Dataset created.")

