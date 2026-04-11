# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from digitalio import DigitalInOut, Direction, Pull

# LED setup.
led = DigitalInOut(board.GPIO18)
led.direction = Direction.OUTPUT

switch = DigitalInOut(board.GPIO19)

switch.direction = Direction.INPUT
switch.pull = Pull.UP

print("LED Testing Start")
print("Press down on the rocker to turn on the LED")

while True:
    # We could also do "led.value = not switch.value"!
    if switch.value:
        led.value = False
    else:
        led.value = True

    time.sleep(0.01)  # debounce delay
