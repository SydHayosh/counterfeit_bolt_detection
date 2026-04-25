import board
import busio
import time

i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass

try:
    # The 'RR' (Read Register) command for the MLX90393 is 0x40
    # Let's try to read Register 0x00 (Memory area)
    # Command format: [0x40, RegisterAddress << 2]
    # For Register 0, that is [0x40, 0x00]
    
    print("Attempting raw register read...")
    i2c.writeto(0x18, bytes([0x40, 0x00]))
    
    result = bytearray(3) # Status byte + 2 bytes of data
    i2c.readfrom_into(0x18, result)
    
    print(f"Raw Response: {result.hex()}")
    # A healthy response starts with a status byte where the last bit is usually 0
    
finally:
    i2c.unlock()
