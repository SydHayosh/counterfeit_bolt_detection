import board
import adafruit_mlx90393 as maglib

i2c = board.I2C()
sensor = maglib.MLX90393(i2c, 0x18)
sensor.reset()

print("Success")
