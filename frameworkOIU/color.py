import cv2 as cv
import numpy as np

# ---- PARAMETERS ----
IMAGE_PATH = 'frameworkOIU/inputCV/bolt_head.jpg'

# If you already know the center:
CENTER_X = 2205
CENTER_Y = 1635

# Radius of sampling area (in pixels)
SAMPLE_RADIUS = 10
OUTPUT_DEBUG = 'frameworkOperator/dataOut/Color Sample.jpg'

def get_center_color(img, cx, cy, r):
    # Create a circular mask
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv.circle(mask, (cx, cy), r, 255, -1)

    # Extract pixels inside the circle
    pixels = img[mask == 255]

    # Compute average color (BGR)
    avg_color = np.mean(pixels, axis=0)

    return avg_color


def colorCheck():
    img = cv.imread(IMAGE_PATH)

    if img is None:
        print("Error: Image not found")
        return

    avg_bgr = get_center_color(img, CENTER_X, CENTER_Y, SAMPLE_RADIUS)

    b, g, r = avg_bgr
    print(f"Average BGR color: ({b:.1f}, {g:.1f}, {r:.1f})")
    print(f"Average RGB color: ({r:.1f}, {g:.1f}, {b:.1f})")

    if(r > 100 and g > 100 and b > 100):
        return "silver"
    elif(b > r and r > g):
        return "black"
    elif(r > b and b > g):
        return "gold"
    else:
        return "unknown"

    # # Optional: visualize sampling area
    # display = img.copy()
    # cv.circle(display, (CENTER_X, CENTER_Y), SAMPLE_RADIUS, (0, 255, 0), 2)
    # cv.imwrite(OUTPUT_DEBUG, display)

