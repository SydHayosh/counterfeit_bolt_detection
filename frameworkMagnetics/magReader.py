import time
import board
import busio
import smbus2
import adafruit_mlx90393 as maglib
import numpy as np

def magRead(timer):
    testX,testY,testZ,testC = [], [], [], []
    testTime = time.monotonic() + timer
    sensor.reset()
    while (time.monotonic() <= testTime):
        x, y, z = sensor.magnetic
        try:
            temp = sensor.temperature
        except:
            temp = 0
        testX.append(x)
        testY.append(y)
        testZ.append(z)
        testC.append(temp)

    meanX = np.mean(testX)
    meanY = np.mean(testY)
    meanZ = np.mean(testZ)
    meanC = np.mean(testC)

    magResult = [meanX, meanY, meanZ, meanC]
    reset_mlx(address=0x18)
    return magResult

i2c = board.I2C()
sensor = maglib.MLX90393(i2c)

