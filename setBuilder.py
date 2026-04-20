import time
import board
import busio
import digitalio
import adafruit_mlx90393 as maglib

import numpy as np
import pandas as pd 

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

UP = digitalio.DigitalInOut(board.D6)#5
DWN = digitalio.DigitalInOut(board.D5)#6
L = digitalio.DigitalInOut(board.D13)#12
R = digitalio.DigitalInOut(board.D12)#13
MID = digitalio.DigitalInOut(board.D19)#19

inputPins = [UP, DWN, L, R, MID]
inputNames = ['UP', 'DWN', 'L', 'R', 'MID']

testX = []
testY = []
testZ = []

entryX = []
entryY = []
entryZ = []

for pin in inputPins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP

#Sensors output milliTeslas. No gain (Gain = 1)

#Makes sure chip isnt busy
while not i2c.try_lock():
    pass
try:
    i2c.writeto(0x18, bytes([0x80])) #EX (reset) command
    time.sleep(0.1)
finally:
    i2c.unlock() 
    
try: 
    sensor = maglib.MLX90393(i2c, gain=maglib.GAIN_1X)
except ValueError:
    sensor = maglib.MLX90393(i2c, gain=maglib.GAIN_1X, address=0x18)
    
print("Press MID to record ambient.")

while MID.value:
    time.sleep(0)

print('\n')
time.sleep(0.5)

while MID.value:
    x, y, z = sensor.magnetic
    
    displayOut = [f'Recording... (Press MID stop recording)',
    f'X:    {x:.3f} μT',
    f'Y:    {y:.3f} μT',
    f'Z:    {z:.3f} μT',
    ]
    
    print('\n'.join(displayOut), flush=True)
    print(f'\033[{len(displayOut)}A', end='', flush=True)
    
    testX.append(x)
    testY.append(y)
    testZ.append(z)

entryX.append(quickMean(testX))
entryY.append(quickMean(testY))
entryZ.append(quickMean(testZ))

entryX.append('')
entryY.append('')
entryZ.append('')

time.sleep(0.5)

displayOut = ['Press MID to record bolt data.          ',
'Push R to end and output to .xlsx.',
'                   ',
'                   ',]

print('\n'.join(displayOut), flush=True)
print(f'\033[{len(displayOut)}A', end='', flush=True)

print('\n\n')
timeInit = time.monotonic()

while R.value:
    
    x, y, z = sensor.magnetic
    
    displayOut = [f'Insert sample...                         ',
    f'Runtime: {time.monotonic() - timeInit:.3f}s',
    f'X:    {x:.3f} μT',
    f'Y:    {y:.3f} μT',
    f'Z:    {z:.3f} μT',
    ]

    print('\n'.join(displayOut), flush=True)
    print(f'\033[{len(displayOut)}A', end='', flush=True)

    if not MID.value:
        time.sleep(0.5)
                
        while MID.value:
            x, y, z = sensor.magnetic
            
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
        
        entryX.append(quickMean(testX))
        entryY.append(quickMean(testY))
        entryZ.append(quickMean(testZ))
    
    time.sleep(0.1)
    
    # Display the status field if an error occured, etc.
    if sensor.last_status > maglib.STATUS_OK:
        sensor.display_status()
print("\n\n\n\n===================")
boltName = input("Bolt Name: ")
print("Generating Excel File...")

df = pd.DataFrame({
    'X Output (μT)': entryX,
    'Y Output (μT)': entryY,
    'Z Output (μT)': entryZ
})

timestamp = time.strftime('%Y%m%d_%H_%M_%S', time.localtime())
df.to_excel(format(boltName) + "_" + timestamp + '.xlsx', index=False, sheet_name='Magnetometer Readings')

print("Dataset created.")

