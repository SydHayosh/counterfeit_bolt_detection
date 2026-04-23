import subprocess

def capture_photos():
    subprocess.run([
        "rpicam-still",
        "--camera", "0",
        "--autofocus-mode", "manual",
        "--lens-position", "20",
        "--immediate",
        "-o", "frameworkOIU/inputCV/bolt_head.jpg"
    ])

    subprocess.run([
        "rpicam-still",
        "--camera", "1",
        "--autofocus-mode", "manual",
        "--lens-position", "32",
        "--immediate",
        "-o", "frameworkOIU/inputCV/bolt_shaft.jpg"
    ])
