import board
import neopixel
import time

# Number of LEDs
NUM_PIXELS = 32
PIXEL_PIN = board.D18

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

TOP = (24, 32)
HEAD = (8, 24)
SHAFT = (0, 8)

# Use SPI (GPIO10 = MOSI)
pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=0.2,
    auto_write=False
)

def set_all(color):
    for i in range(NUM_PIXELS):
        pixels[i] = color
    pixels.show()
    
def setRegion(region, color):
    start, end = region

    for i in range(start, end):
        pixels[i] = color
    pixels.show()

def ledCheck():
    try:
        for i in range(3):
            print("Red")
            set_all(RED)
            time.sleep(1)
            
            print("Green")
            set_all(GREEN)
            time.sleep(1)
            
            print("Blue")
            set_all(BLUE)
            time.sleep(1)
            
            print("Off")
            set_all(OFF)
            time.sleep(1)
            
    except KeyboardInterrupt:
        set_all(OFF)

ledCheck()