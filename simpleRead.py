import smbus2
import time

ADDRESS = 0x18
bus = smbus2.SMBus(1)

while True:
    # Start measurement
    bus.write_byte(ADDRESS, 0x3F)
    time.sleep(0.05)

    # Read data
    data = bus.read_i2c_block_data(ADDRESS, 0x00, 7)

    # Combine bytes
    x = (data[1] << 8) | data[2]
    y = (data[3] << 8) | data[4]
    z = (data[5] << 8) | data[6]

    # Convert to signed
    if x > 32767: x -= 65536
    if y > 32767: y -= 65536
    if z > 32767: z -= 65536

    # Print live values
    print(f"X: {x}  Y: {y}  Z: {z}")

    time.sleep(0.5)