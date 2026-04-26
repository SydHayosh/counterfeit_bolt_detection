import time
import board
import busio
import digitalio
import adafruit_mlx90393 as maglib

import numpy as np
import csv
from frameworkOperator.pins import UP, DWN, L, R, MID, inputPins, inputNames, debounce

i2c = busio.I2C
sensor = maglib.MLX930393(i2c, address = 0x18)

def quickMean(vec):
    length = len(vec)
    sum = 0
    i = 0
    while (i < len(vec)):
        sum += vec[i]
        i += 1
    
    mean = sum/length
    return mean

def magRead(timer)

    testX,testY,testZ,testT = []
    testTime = time.monotonic() + timer
    
    while (time.monotonic() <= testTime):
        x, y, z = sensor.magnetic
        try:
            temp = sensor.temperature
        except:
            temp = 0
        testX.append(x)
        testY.append(y)
        testZ.append(z)
        testT.append(temp)

    meanX = np.mean(testX)
    meanY = np.mean(testY)
    meanZ = np.mean(testZ)
    meanC = np.mean(testC)

    magResult = [meanX, meanY, meanZ, meanC]
    
    return magResult

i2c = board.I2C()  # uses board.SCL and board.SDA

testX = []
testY = []
testZ = []
testC = []
    
try: 
    sensor = maglib.MLX90393(i2c)
except ValueError:
    sensor = maglib.MLX90393(i2c, address=0x18)
	
ambient = magRead(sensor, 3)

time.sleep(0.5)

displayOut = ['Insert bolt, then press MID.          ',
'					',
'                   ',
'                   ',]

print('\n'.join(displayOut), flush=True)
print(f'\033[{len(displayOut)}A', end='', flush=True)

print('\n\n')

while MID.value:
	time.sleep(0.1)

timeInit = time.monotonic()

while (time.monotonic() < timeInit + 5):
    
	x, y, z = sensor.magnetic
	temp = sensor.temperature
	
	displayOut = [f'Insert sample...                         ',
	f'Runtime: {time.monotonic() - timeInit:.3f}s',
	f'X:    {x:.3f} μT',
	f'Y:    {y:.3f} μT',
	f'Z:    {z:.3f} μT',
	f'Temp: {temp:.3f} °C',
	]
	
	print('\n'.join(displayOut), flush=True)
	print(f'\033[{len(displayOut)}A', end='', flush=True)
	
	testX.append(x)
	testY.append(y)
	testZ.append(z)
	testC.append(temp)
	
	sampleX = quickMean(testX) - ambX
	sampleY = quickMean(testY) - ambY
	sampleZ = quickMean(testZ) - ambZ
	sampleC = quickMean(testC)

sampleTrial = [sampleX, sampleY, sampleZ]

print("Writing to sample.csv")

with open('sample.csv', 'w') as csvfile:
	csv_writer = csv.writer(csvfile)
	csv_writer.writerow(sampleTrial)

print("Data written to sample.csv")
