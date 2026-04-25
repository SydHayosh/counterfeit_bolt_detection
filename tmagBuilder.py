import time
import board
import busio
import digitalio
import adafruit_tmag5273 as maglib

import numpy as np
import pandas as pd 
from frameworkOperator.pins import UP, DWN, L, R, MID, inputPins, inputNames, debounce
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

# for pin in inputPins:
    # pin.direction = digitalio.Direction.INPUT
    # pin.pull = digitalio.Pull.UP

#Sensors output milliTeslas. No gain (Gain = 1)

#Makes sure chip isnt busy
# while not i2c.try_lock():
    # pass
# try:
    # i2c.writeto(0x18, bytes([0x80])) #EX (reset) command
    # time.sleep(0.1)
# finally:
#    i2c.unlock() 
    
try: 
    sensor = maglib.TMAG5273(i2c)
except ValueError:
    sensor = maglib.TMAG5273(i2c, address=0x18)
    
print("Press MID to record ambient.")

while True:
    if not MID.value:
        debounce(MID)
        break

print('==========================')
time.sleep(0.1)

while True:
    x, y, z = sensor.magnetic
    temp = sensor.temperature
    
    displayOut = [f'Recording... (Press MID stop recording)',
    f'X:    {x:.2f} μT  ',
    f'Y:    {y:.2f} μT  ',
    f'Z:    {z:.2f} μT  ',
    f'Temp: {temp:.2f} °C   ',
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

entryX.append(quickMean(testX))
entryY.append(quickMean(testY))
entryZ.append(quickMean(testZ))
entryC.append(quickMean(testC))

entryX.append('')
entryY.append('')
entryZ.append('')
entryC.append('')

time.sleep(0.5)

displayOut = ['Press MID to record bolt data.          ',
'Push R to end and output to .xlsx.',
'========================',
'                   ',]

print('\n'.join(displayOut), flush=True)
print(f'\033[{len(displayOut)}A', end='', flush=True)

print('\n')
print('========================')
timeInit = time.monotonic()
runTest = True

while runTest:
    
    x, y, z = sensor.magnetic
    temp = sensor.temperature
     
    displayOut = [f'Insert sample...                         ',
    f'Runtime: {format(time.monotonic() - timeInit)}s',
    f'X:    {x:.3f}     μT  ',
    f'Y:    {y:.3f}     μT  ',
    f'Z:    {z:.3f}     μT  ',
    f'Temp: {temp:.3f}      °C  ',
    ]

    print('\n'.join(displayOut), flush=True)
    print(f'\033[{len(displayOut)}A', end='', flush=True)
    
    timer = time.monotonic()
    while not R.value:
        
        displayOut = [f'Holding R...                         ',
        f'Closing in: {(timer + 3) - time.monotonic():.1}s      ',
        f'X:    {x:.3f}     μT',
        f'Y:    {y:.3f}     μT',
        f'Z:    {z:.3f}     μT',
        f'Temp: {temp:.3f}      °C',
        ]
    
        print('\n'.join(displayOut), flush=True)
        print(f'\033[{len(displayOut)}A', end='', flush=True)
        
        if time.monotonic() >= timer + 3:
            runTest = False
            break
       
    if not MID.value:
        debounce(MID)
                
        while True:
            x, y, z = sensor.magnetic
            temp = sensor.temperature
            
            displayOut = [f'Recording... (Press MID stop recording)',
            f'Runtime: {time.monotonic() - timeInit:.3f}s',
            f'X:    {x:.3f}     μT  ',
            f'Y:    {y:.3f}     μT  ',
            f'Z:    {z:.3f}     μT  ',
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
        
        entryX.append(quickMean(testX))
        entryY.append(quickMean(testY))
        entryZ.append(quickMean(testZ))
        entryC.append(quickMean(testC))
    
    time.sleep(0.1)
    
    # Display the status field if an error occured, etc.
#    if sensor.last_status > maglib.STATUS_OK:
#        sensor.display_status()
print("\n\n\n\n\n=======================")
boltName = input("Bolt Name: ")
print("Generating Excel File...")

df = pd.DataFrame({
    'X Output (μT)': entryX,
    'Y Output (μT)': entryY,
    'Z Output (μT)': entryZ,
    'Temperature (°C)': entryC
})

timestamp = time.strftime('%Y%m%d_%H_%M_%S', time.localtime())
df.to_excel("TMAG_" + format(boltName) + "_" + timestamp + '.xlsx', index=False, sheet_name='TMAG5273 Readings')

print( format(boltName) + " Dataset created.")

