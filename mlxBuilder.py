import time
import board
import digitalio
import adafruit_mlx90393 as maglib

import numpy as np
import pandas as pd 
from frameworkOperator.pins import UP, DWN, L, R, MID, inputPins, inputNames, debounce
import frameworkOperator.pins

i2c = board.I2C()

try:
    i2c.unlock() # Force an unlock in case it was stuck
except:
    i2c.deinit()

testX = []
testY = []
testZ = []
testC = []

entryX = []
entryY = []
entryZ = []
entryC = []

ambX = []
ambY = []
ambZ = []
ambC = []

try:
    sensor = maglib.MLX90393(i2c)
    print("Press MID to record ambient.")
    
    #Button debounce, only moves to next stage once button is pressed then unpressed
    while True:
        if not MID.value:
            debounce(MID)
            break
    
    while True:
        
        x, y, z = sensor.magnetic
        temp = sensor.temperature
        
        displayOut = [f'Recording... (Press MID stop recording)',
        f'X:    {x:.3f} μT',
        f'Y:    {y:.3f} μT',
        f'Z:    {z:.3f} μT',
        f'Temp: {temp:.3f}      °C',
        ]
        
        print('\n'.join(displayOut), flush=True)
        print(f'\033[{len(displayOut)}A', end='', flush=True)
        
        testX.append(x)
        testY.append(y)
        testZ.append(z)
        testC.append(temp)
        
        if not MID.value:
            debounce(MID)
            break
    
    ambX = np.mean(testX)
    ambY = np.mean(testY)
    ambZ = np.mean(testZ)
    ambC = np.mean(testC)

    testX.clear()
    testY.clear()
    testZ.clear()
    testC.clear()
    
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
        x, y, z = sensor.magnetic
        temp = sensor.temperature
                
        displayOut = [f'Insert sample...                         ',
        f'Runtime: {time.monotonic() - timeInit:.3f}s',
        f'X:    {x:.3f} μT',
        f'Y:    {y:.3f} μT',
        f'Z:    {z:.3f} μT',
        f'Temp: {temp:.3f}      °C',
        ]
        
    
        print('\n'.join(displayOut), flush=True)
        print(f'\033[{len(displayOut)}A', end='', flush=True)
        
        while not R.value:
        
            displayOut = [f'Holding R...                         ',
            f'Closing in: {(timer + 3) - time.monotonic():.0f}s      ',
            f'X:    {x:.3f} μT  ',
            f'Y:    {y:.3f} μT  ',
            f'Z:    {z:.3f} μT  ',
            f'Temp: {temp:.3f}  °C',
            ]
            print('\n'.join(displayOut), flush=True)
            print(f'\033[{len(displayOut)}A', end='', flush=True)
            if time.monotonic() >= timer + 3:
                runTest = False
                break
                
        if not MID.value:
            while not MID.value:
                pass
                    
            while True:
                x, y, z = sensor.magnetic
                temp = sensor.temperature
                
                displayOut = [f'Recording... (Press MID stop recording)',
                f'Runtime: {time.monotonic() - timeInit:.3f}s',
                f'X:    {x:.3f} μT      ',
                f'Y:    {y:.3f} μT      ',
                f'Z:    {z:.3f} μT      ',
                f'Temp: {temp:.3f}  °C',
                ]
                
                print('\n'.join(displayOut), flush=True)
                print(f'\033[{len(displayOut)}A', end='', flush=True)
                
                testX.append(x)
                testY.append(y)
                testZ.append(z)
                testC.append(temp)
                if not MID.value:
                    while not MID.value:
                        pass
                    break
            
            entryX.append(np.mean(testX))
            entryY.append(np.mean(testY))
            entryZ.append(np.mean(testZ))
            entryC.append(np.mean(testC))

            testX.clear()
            testY.clear()
            testZ.clear()
            testC.clear()
        
        time.sleep(0.1)

finally:
    try:
        i2c.unlock()
    except:
        pass      
    i2c.deinit()

print("\n\n\n\n\n=====================")

boltName = input("Enter Boltname: ")

# Subtract ambient from each entry
adjX = [v - 0 for v in entryX]
adjY = [v - 0 for v in entryY]
adjZ = [v - 0 for v in entryZ]
adjC = [v - 0 for v in entryC]

n = len(adjX)
bolt_cols = {f'Bolt{i+1}': [adjX[i], adjY[i], adjZ[i], adjC[i]] for i in range(n)}

df = pd.DataFrame({
    'Axis':   ['X', 'Y', 'Z', 'Temp'],
    'Mean':   [np.mean(adjX), np.mean(adjY), np.mean(adjZ), np.mean(adjC)],
    'StdDev': [np.std(adjX),  np.std(adjY),  np.std(adjZ),  np.std(adjC)],
    **bolt_cols
})

timestamp = time.strftime('%Y%m%d_%H_%M_%S', time.localtime())
df.to_excel(format(boltName) + "_" + timestamp + '.xlsx', index=False, sheet_name='Readings')

print(format(boltName) + " Dataset created.")

