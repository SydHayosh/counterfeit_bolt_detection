import board
import busio
import time
from adafruit_mlx90393 import MLX90393

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# 1. Manual Reset Trigger (The "Secret Shake")
# This sends a 'Reset' command (0x06) to the device address directly
while not i2c.try_lock():
    pass
try:
    i2c.writeto(0x18, bytes([0x06]))
    print("Reset command sent...")
    time.sleep(0.2) # Give it a moment to wake up
finally:
    i2c.unlock()

# 2. Now try the library initialization
try:
    sensor = MLX90393(i2c, address=0x18)
    print("Success! Sensor is ready.")
    print(f"Current gain setting: {sensor.gain}")
except Exception as e:
    print(f"Library still failing: {e}")