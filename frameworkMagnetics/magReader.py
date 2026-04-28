import time
import board
import busio
import smbus2
import adafruit_mlx90393 as maglib
import numpy as np

def reset_mlx(address=0x18, bus_num=1):
    bus = smbus2.SMBus(bus_num)
    try:
        bus.write_byte(address, 0xF0)  # Exit mode
        time.sleep(0.01)
        bus.write_byte(address, 0xF1)  # Reset
        time.sleep(0.05)               # MLX boot time
    except OSError:
        pass
    finally:
        bus.close()

def magRead(timer):

    testX,testY,testZ,testC = [], [], [], []
    testTime = time.monotonic() + timer
    reset_mlx(0x18)
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
    
    return magResult

i2c = busio.I2C(board.SCL, board.SDA)
sensor = maglib.MLX90393(i2c, address=0x18)


