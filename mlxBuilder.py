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
        testC.append(temp)
    
    entryX.append(np.mean(testX))
    entryY.append(np.mean(testY))
    entryZ.append(np.mean(testZ))
    entryC.append(np.mean(testC))
    
    entryX.append('')
    entryY.append('')
    entryZ.append('')
    entryC.append('')
    
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
        timer = time.monotonic()
                
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
            f'Closing in: {(timer + 3) - time.monotonic():.0}s      ',
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
        
        time.sleep(0.1)

finally:
    try:
        i2c.unlock()
    except:
        pass      
    i2c.deinit()

print("\n\n\n\n\n=====================")
boltName = input("Bolt Name: ")
print("Generating Excel File...")

df = pd.DataFrame({
    'X Output (μT)': entryX,
    'Y Output (μT)': entryY,
    'Z Output (μT)': entryZ,
    'Temperature (C)': entryC,
})

timestamp = time.strftime('%Y%m%d_%H_%M_%S', time.localtime())
df.to_excel(format(boltName) + "_" + timestamp + '.xlsx', index=False, sheet_name='Readings')

print( format(boltName) + " Dataset created.")

