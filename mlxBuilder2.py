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

def display(header, x, y, z, temp, runtime=None, countdown=None):
    lines = [header]
    if runtime is not None:
        lines.append(f'Runtime: {runtime:.3f}s')
    if countdown is not None:
        lines.append(f'Closing in: {countdown:.0f}s      ')
    lines += [
        f'X:    {x:.3f}     μT',
        f'Y:    {y:.3f}     μT',
        f'Z:    {z:.3f}     μT',
        f'Temp: {temp:.3f}      °C',
    ]
    print('\n'.join(lines), flush=True)
    print(f'\033[{len(lines)}A', end='', flush=True)

def clear_stuck_i2c():
    scl = digitalio.DigitalInOut(board.SCL)
    sda = digitalio.DigitalInOut(board.SDA)
    
    scl.direction = digitalio.Direction.OUTPUT
    sda.direction = digitalio.Direction.INPUT
    sda.pull = digitalio.Pull.UP
    
    if not sda.value:
        print("I2C bus stuck! Attempting to clear...")
        for _ in range(9):
            scl.value = False
            time.sleep(0.001)
            scl.value = True
            time.sleep(0.001)
        
        scl.deinit()
        sda.deinit()
        print("Bus cleared.")
    else:
        scl.deinit()
        sda.deinit()

def init_hardware():
    i2c = board.I2C()
    
    # Wait for I2C lock, send exit mode command to ensure sensor is idle
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(0x18, bytes([0x80]))  # EXIT mode command
        time.sleep(0.1)
    finally:
        i2c.unlock()
    
    sensor = maglib.MLX90393(i2c, address=0x18)
    return i2c, sensor

def main(sensor):
    testX, testY, testZ, testC = [], [], [], []
    entryX, entryY, entryZ, entryC = [], [], [], []
    i2c = busio.I2C(board.SCL, board.SDA)
try:
    i2c.unlock() # Force an unlock in case it was stuck
except:
    pass
    print("Press MID to record ambient.")

    # Button debounce, only moves to next stage once button is pressed then unpressed
    while True:
        if not MID.value:
            while not MID.value:
                pass
            break

    while True:
        
        x, y, z = sensor.magnetic
        temp = sensor.temperature
        
        display('Recording... (Press MID to stop recording)', x, y, z, temp)
        
        testX.append(x)
        testY.append(y)
        testZ.append(z)
        testC.append(temp)
        
        if not MID.value:
            while not MID.value:
                pass
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
        
        while not R.value:
            display('Holding R...                         ', x, y, z, temp, countdown=(timer + 3) - time.monotonic())
            if time.monotonic() >= timer + 3:
                runTest = False
                break
                
        display('Insert sample...                         ', x, y, z, temp, runtime=time.monotonic() - timeInit)

        if not MID.value:
            while not MID.value:
                pass
                    
            while True:
                x, y, z = sensor.magnetic
                temp = sensor.temperature
                
                display('Recording... (Press MID to stop recording)', x, y, z, temp, runtime=time.monotonic() - timeInit)
                
                testX.append(x)
                testY.append(y)
                testZ.append(z)
                testC.append(temp)
                if not MID.value:
                    while not MID.value:
                        pass
                    break
            
            entryX.append(quickMean(testX))
            entryY.append(quickMean(testY))
            entryZ.append(quickMean(testZ))
            entryC.append(quickMean(testC))
        
        time.sleep(0.1)
        
    print("\n\n\n\n\n===================")
    boltName = input("Bolt Name: ")
    print("Generating Excel File...")

    df = pd.DataFrame({
        'X Output (μT)': entryX,
        'Y Output (μT)': entryY,
        'Z Output (μT)': entryZ,
        'Temperature (C)': entryC,
    })

    timestamp = time.strftime('%Y%m%d_%H_%M_%S', time.localtime())
    df.to_excel("MLX_" + format(boltName) + "_" + timestamp + '.xlsx', index=False, sheet_name='MLX90393 Readings')

    print(format(boltName) + " Dataset created.")

if __name__ == "__main__":
    i2c, sensor = init_hardware()
    try:
        main(sensor)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt received — cleaning up...")
    finally:
        try:
            sensor._i2c.unlock()                # release the bus lock if held mid-read
        except Exception:
            pass
        i2c.deinit()                            # fully release the I2C bus
        print("I2C bus released.")
