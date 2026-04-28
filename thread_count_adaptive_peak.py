import cv2 as cv
import numpy as np

IMAGE_PATH = 'Photos/bolt_shaft copy.jpg'
lowerThresh = 30
upperThresh = 50 

# -----------------------------
# STAGE 1: DETECT BOLT
# -----------------------------
def detect_bolt(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9, 9), 0)

    edges = cv.Canny(blur, 30, 100)
    edges = cv.dilate(edges, None, iterations=3)
    edges = cv.erode(edges, None, iterations=2)

    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    bolt_contour = None
    max_area = 0

    for c in contours:
        area = cv.contourArea(c)
        if area > max_area:
            max_area = area
            bolt_contour = c

    if bolt_contour is None:
        return None

    x, y, w, h = cv.boundingRect(bolt_contour)


    return (x, y, w, h), bolt_contour


# -----------------------------
# STAGE 2: DETECT THREADS
# -----------------------------
def compute_projection(roi):
    edges = cv.Canny(roi, 30, 100)  # better than raw grayscale
    projection = np.mean(edges, axis=0)

    # normalize
    if np.max(projection) > 0:
        projection = projection / np.max(projection)

    return projection


def smooth_signal(signal, ksize=25):
    kernel = np.ones(ksize) / ksize
    return np.convolve(signal, kernel, mode='same')


def find_peaks(signal, min_distance=15, threshold=0.3):
    peaks = []
    last_peak = -min_distance

    for i in range(1, len(signal)-1):
        if signal[i] > signal[i-1] and signal[i] > signal[i+1]:
            if signal[i] > threshold:
                if i - last_peak >= min_distance:
                    peaks.append(i)
                    last_peak = i
                else:
                    # keep stronger peak if too close
                    if signal[i] > signal[peaks[-1]]:
                        peaks[-1] = i
                        last_peak = i

    return peaks

def detect_threads(img, bolt_bbox):
    x, y, w, h = bolt_bbox

    BAND_HEIGHT = 30
    MARGIN = 10

    if h < (2 * BAND_HEIGHT + 2 * MARGIN):
        print("Bolt too small for thread detection")
        return []
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7, 7), 0)

    # Define ROIs RELATIVE to bolt
    top_y1 = int(y)
    top_y2 = top_y1 + BAND_HEIGHT

    bot_y2 = int(y + h)
    bot_y1 = bot_y2 - BAND_HEIGHT

    x1 = int(x)
    x2 = int(x + w)

    top_band = blur[top_y1:top_y2, x1:x2]
    bottom_band = blur[bot_y1:bot_y2, x1:x2]

    debug = img.copy()

    cv.rectangle(debug, (x1, top_y1), (x2, top_y2), (255, 0, 0), 2)
    cv.rectangle(debug, (x1, bot_y1), (x2, bot_y2), (0, 0, 255), 2)

    def detect_peaks_in_band(roi, y_offset, x_offset, debug_img):
        projection = compute_projection(roi)
        smoothed = smooth_signal(projection)

        peaks = find_peaks(smoothed)

        # draw peaks
        for px in peaks:
            cv.line(
                debug_img,
                (x_offset + px, y_offset),
                (x_offset + px, y_offset + roi.shape[0]),
                (0, 0, 255),
                1
            )

        return peaks

    top_peaks = detect_peaks_in_band(top_band, top_y1, x1, debug)
    bottom_peaks = detect_peaks_in_band(bottom_band, bot_y1, x1, debug)

    cv.imshow("Thread Bands", debug)

    return top_peaks, bottom_peaks


# -----------------------------
# MAIN
# -----------------------------
img = cv.imread(IMAGE_PATH)

if img is None:
    print("Image failed to load")
    exit()

# Stage 1: Bolt detection
result = detect_bolt(img)

if result is None:
    print("Bolt not found")
    exit()

(bolt_bbox, bolt_contour) = result
x, y, w, h = bolt_bbox

output = img.copy()
cv.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 3)

# Stage 2: Thread detection
top_peaks, bottom_peaks = detect_threads(img, bolt_bbox)

print(f"{len(top_peaks)} threads on top")
print(f"{len(bottom_peaks)} threads on bottom")

cv.imshow("Result", output)
cv.waitKey(0)
cv.destroyAllWindows()
