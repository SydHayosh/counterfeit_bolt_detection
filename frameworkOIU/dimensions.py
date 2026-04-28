from imutils import contours
import numpy as np
import cv2 as cv

def countThreads():
    IMAGE_PATH = 'frameworkOIU/inputCV/bolt_shaft.jpg'
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
    def detect_threads(img, bolt_bbox):
        x, y, w, h = bolt_bbox

        BAND_HEIGHT = 20
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

        def extract_thread_contours(roi, y_offset, x_offset):
            edges = cv.Canny(roi, 30, 100)
            edges = cv.dilate(edges, None, iterations=2)
            edges = cv.erode(edges, None, iterations=1)

            contours, _ = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

            thread_contours = []

            for c in contours:
                area = cv.contourArea(c)

                if 10 < area:
                    c = c + np.array([[x_offset, y_offset]])
                    thread_contours.append(c)

            return thread_contours


        top_threads = extract_thread_contours(top_band, top_y1, x1)
        bottom_threads = extract_thread_contours(bottom_band, bot_y1, x1)

        return top_threads, bottom_threads


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
    top_threads, bottom_threads = detect_threads(img, bolt_bbox)

    for t in top_threads:
        cv.drawContours(output, [t], -1, (0, 0, 255), 2)

    for t in bottom_threads:
        cv.drawContours(output, [t], -1, (0, 0, 255), 2)

    print(f"{len(top_threads)} threads on top and {len(bottom_threads)} threads on the bottom")

    cv.imwrite("frameworkOperator/dataOut/Thread count.jpg", output)

