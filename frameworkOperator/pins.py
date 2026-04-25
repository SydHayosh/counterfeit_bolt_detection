import digitalio, board, time

UP = digitalio.DigitalInOut(board.D6)
DWN = digitalio.DigitalInOut(board.D5)
L = digitalio.DigitalInOut(board.D13)
R = digitalio.DigitalInOut(board.D12)
MID = digitalio.DigitalInOut(board.D19)
inputPins = [UP, DWN, L, R, MID]
inputNames = ['UP', 'DWN', 'L', 'R', 'MID']

for pin in inputPins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP

def debounce(pin):
    while not pin.value:
        pass

def clear_stuck_i2c():
    # 1. Define the pins manually
    scl = digitalio.DigitalInOut(board.SCL)
    sda = digitalio.DigitalInOut(board.SDA)
    
    # 2. Set SCL to output, SDA to input (with pullup)
    scl.direction = digitalio.Direction.OUTPUT
    sda.direction = digitalio.Direction.INPUT
    sda.pull = digitalio.Pull.UP
    
    # 3. Check if SDA is low (stuck)
    if not sda.value:
        print("I2C bus stuck! Attempting to clear...")
        # 4. Toggle SCL 9 times to force the slave to finish its bit
        for _ in range(9):
            scl.value = False
            time.sleep(0.001)
            scl.value = True
            time.sleep(0.001)
        
        # 5. Clean up pins so the I2C library can use them again
        scl.deinit()
        sda.deinit()
        print("Bus cleared.")
    else:
        # If not stuck, just clean up
        scl.deinit()
        sda.deinit()
