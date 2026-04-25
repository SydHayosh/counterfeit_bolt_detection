import time
from smbus2 import SMBus

# I2C address for MLX90393
ADDR = 0x18
bus = SMBus(1)

def read_magnetic_data():
    try:
        # 1. Start Measurement (Z, Y, X axes) - Command 0x3E
        # This tells the sensor to take a reading right now
        bus.write_byte(ADDR, 0x3E) 
        time.sleep(0.1) # Wait for conversion

        # 2. Read Measurement - Command 0x4E
        bus.write_byte(ADDR, 0x4E)
        
        # We expect 7 bytes: Status + (2 bytes per axis x 3)
        data = bus.read_i2c_block_data(ADDR, 0, 7)
        
        status = data[0]
        # Combine high and low bytes for X, Y, and Z
        x = (data[1] << 8) | data[2]
        y = (data[3] << 8) | data[4]
        z = (data[5] << 8) | data[6]

        # Handle two's complement for negative values
        def to_signed(val):
            return val if val < 32768 else val - 65536

        print(f"Status: {hex(status)} | X: {to_signed(x)} | Y: {to_signed(y)} | Z: {to_signed(z)}")

    except Exception as e:
        print(f"Error: {e}")

while True:
    read_magnetic_data()
    time.sleep(0.5)