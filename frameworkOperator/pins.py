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
