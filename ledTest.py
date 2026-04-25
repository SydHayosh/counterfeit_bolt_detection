import board
import neopixel
import time

# Number of LEDs
NUM_PIXELS = 32
PIXEL_PIN = board.D18

# Use SPI (GPIO10 = MOSI)
pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=0.5,
    auto_write=False
)

def set_all(color):
    for i in range(NUM_PIXELS):
        pixels[i] = color
    pixels.show()
    
def ledWhite():
    set_all((255, 255, 255))

def ledRed():
    set_all((255, 0, 0))

def ledGreen():
    set_all((0, 255, 0))

def setStrip(strip_num, color):
    leds_per_strip = 8
    start = strip_num * leds_per_strip
    end = start + leds_per_strip

    for i in range(start, end):
        pixels[i] = color
    pixels.show()

def ledCheck():
    try:
        for i in range(3):
            print("Red")
            set_all((255, 0, 0))
            time.sleep(1)
            
            print("Green")
            set_all((0, 255, 0))
            time.sleep(1)
            
            print("Blue")
            set_all((0, 0, 255))
            time.sleep(1)
            
            print("Off")
            set_all((0, 0, 0))
            time.sleep(1)
            
    except KeyboardInterrupt:
        set_all((0, 0, 0,))

ledCheck()