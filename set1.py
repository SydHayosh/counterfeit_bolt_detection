import time
import board
import digitalio
import adafruit_mlx90393 as maglib  # Updated library
import pandas as pd 
from frameworkOperator.pins import UP, DWN, L, R, MID, inputPins, inputNames

def quickMean(vec):
    length = len(vec)
    if length == 0: return 0
    return sum(vec) / length

i2c = board.I2C()  # uses board.SCL and board.SDA

# --- INITIALIZE PINS ---
# Rocker buttons must be set as INPUT with PULL_UP
for pin in inputPins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP

# --- INITIALIZE SENSOR ---
# MLX90393 initialization
try: 
    sensor = maglib.MLX90393(i2c, gain=maglib.GAIN_1X)
except ValueError:
    sensor = maglib.MLX90393(i2c, gain=maglib.GAIN_1X, address=0x18)
    
testX, testY, testZ, testC = [], [], [], []
entryX, entryY, entryZ, entryC = [], [], [], []

print("Press MID to record ambient.")
while MID.value:
    time.sleep(0.1)

print('\n')
time.sleep(0.5)

# --- AMBIENT RECORDING ---
while MID.value:
    x, y, z = sensor.magnetic
    temp = sensor.temperature
    
    displayOut = [f'Recording Ambient... (Press MID stop)',
    f'X:    {x:.2f} μT',
    f'Y:    {y:.2f} μT',
    f'Z:    {z:.2f} μT',
    f'Temp: {temp:.2f} °C',
    ]
    
    print('\n'.join(displayOut), flush=True)
    print(f'\033[{len(displayOut)}A', end='', flush=True)
    
    testX.append(x)
    testY.append(y)
    testZ.append(z)
    testC.append(temp)

entryX.append(quickMean(testX))
entryY.append(quickMean(testY))
entryZ.append(quickMean(testZ))
entryC.append(quickMean(testC))

# Reset lists for next recording
testX, testY, testZ, testC = [], [], [], []

time.sleep(0.5)

displayOut = ['Press MID to record bolt data.          ',
'Push R to end and output to .xlsx.',
'                                   ',
'                                   ',]

print('\n'.join(displayOut), flush=True)
print(f'\033[{len(displayOut)}A', end='', flush=True)

print('\n\n')
timeInit = time.monotonic()

# --- BOLT RECORDING ---
while R.value:
    x, y, z = sensor.magnetic
    temp = sensor.temperature
    
    displayOut = [f'Insert sample...                         ',
    f'Runtime: {time.monotonic() - timeInit:.3f}s',
    f'X:    {x:.3f} μT',
    f'Y:    {y:.3f} μT',
    f'Z:    {z:.3f} μT',
    f'Temp: {temp:.2f} °C',
    ]

    print('\n'.join(displayOut), flush=True)
    print(f'\033[{len(displayOut)}A', end='', flush=True)

    if not MID.value:
        time.sleep(0.5)
        # Clear lists for the new sample
        testX, testY, testZ, testC = [], [], [], []
                
        while MID.value:
            x, y, z = sensor.magnetic
            temp = sensor.temperature
            
            displayOut = [f'Recording... (Press MID stop recording)',
            f'Runtime: {time.monotonic() - timeInit:.3f}s',
            f'X:    {x:.3f} μT',
            f'Y:    {y:.3f} μT',
            f'Z:    {z:.3f} μT',
            f'Temp: {temp:.2f} °C',
            ]
            
            print('\n'.join(displayOut), flush=True)
            print(f'\033[{len(displayOut)}A', end='', flush=True)
            
            testX.append(x)
            testY.append(y)
            testZ.append(z)
            testC.append(temp)
        
        entryX.append(quickMean(testX))
        entryY.append(quickMean(testY))
        entryZ.append(quickMean(testZ))
        entryC.append(quickMean(testC))
    
    time.sleep(0.1)

# --- EXPORT ---
print("\n\n\n\n===================")
boltName = input("Bolt Name: ")
print("Generating Excel File...")

df = pd.DataFrame({
    'X Output (μT)': entryX,
    'Y Output (μT)': entryY,
    'Z Output (μT)': entryZ,
    'Temperature (°C)': entryC
})

timestamp = time.strftime('%Y%m%d_%H_%M_%S', time.localtime())
df.to_excel(f"{boltName}_{timestamp}.xlsx", index=False, sheet_name='Magnetometer Readings')

print(f"{boltName} Dataset created.")
