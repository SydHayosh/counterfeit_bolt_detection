from picamera2 import Picamera2
import time

camera = Picamera2()

camera_config = camera.create_still_configuration()
camera.configure(camera_config)

camera.start()
time.sleep(2)

image_path = "/home/pi/captured_image.jpg"
camera.capture_file(image_path)