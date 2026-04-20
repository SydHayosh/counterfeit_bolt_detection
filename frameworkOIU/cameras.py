from picamera2 import Picamera2
import time

SAVE_DIR = "frameworksOIU/inputCV"

camera_head = Picamera2(0)
camera_shaft = Picamera2(1)

cam_head_config = camera_head.create_still_configuration()
camera_head.configure(cam_head_config)

cam_shaft_config = camera_shaft.create_still_configuration()
camera_shaft.configure(cam_shaft_config)

def capture_photos():
    camera_head.start() # Maybe move start and stop to their own functions
    camera_shaft.start()

    time.sleep(2)

    image_path_head = SAVE_DIR + "/bolt_head.jpg"
    camera_head.capture_file(image_path_head)

    image_path_shaft = SAVE_DIR + "/bolt_shaft.jpg"
    camera_shaft.capture_file(image_path_shaft)

    camera_head.stop()
    camera_shaft.stop()