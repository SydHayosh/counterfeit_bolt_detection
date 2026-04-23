import subprocess

def capture_photos():
    subprocess.run([
        "rpicam-still",
        "--camera", "0",
        "-o", "frameworkOIU/inputCV/bolt_head.jpg"
    ])

    subprocess.run([
        "rpicam-still",
        "--camera", "1",
        "-o", "frameworkOIU/inputCV/bolt_shaft.jpg"
    ])
