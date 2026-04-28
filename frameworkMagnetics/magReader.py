import time
import board
import busio
import smbus2
import adafruit_mlx90393 as maglib
import numpy as np

def reset_mlx(address=0x18, bus_num=1):
    bus = smbus2.SMBus(bus_num)
    try:
        for attempt in range(5):
            try:
                bus.write_byte(address, 0xF0)   # Exit mode
            except OSError:
                time.sleep(0.1)
        time.sleep(0.01)
        # First reset attempt may fail — retry until it succeeds
        for attempt in range(5):
            try:
                bus.write_byte(address, 0xF1)
                break
            except OSError:
                time.sleep(0.02)
        time.sleep(0.1)  # MLX more time to fully boot
    finally:
        bus.close()
    time.sleep(0.1)  # Extra settle time before I2C bus reinit

def magRead(timer):
    testX,testY,testZ,testC = [], [], [], []
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
        testC.append(temp)

    meanX = np.mean(testX)
    meanY = np.mean(testY)
    meanZ = np.mean(testZ)
    meanC = np.mean(testC)

    magResult = [meanX, meanY, meanZ, meanC]
    reset_mlx(address=0x18)
    return magResult

reset_mlx(address=0x18)
i2c = busio.I2C()
sensor = maglib.MLX90393(i2c, address=0x18)

