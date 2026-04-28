import time
import board
import busio
import adafruit_mlx90393 as maglib
import numpy as np

def magRead(timer):
    sensor.reset()
    testX,testY,testZ,testC = [], [], [], []
    testTime = time.monotonic() + timer
    
    while (time.monotonic() <= testTime):
        x, y, z = sensor.magnetic
        try:
            temp = sensor.temperature
        except Exception:
            temp = 0
        testX.append(x)
        testY.append(y)
        testZ.append(z)
        testC.append(temp)
        print("X: {x:.2f} | Y: {y:.2f} | Z: {z:.2f}")
        
        time.sleep(0.05)

    meanX = np.mean(testX)
    meanY = np.mean(testY)
    meanZ = np.mean(testZ)
    meanC = np.mean(testC)
	
    magResult = [meanX, meanY, meanZ, meanC]
    print(magResult)
    return magResult

i2c = board.I2C()

try:
    sensor = maglib.MLX90393(i2c, address=0x18, gain=maglib.GAIN_1X)
except Exception:
    sensor = maglib.MLX90393(i2c)

time.sleep(0.1)


