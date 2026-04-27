import numpy as np
import cv2 as cv

# ROI parameters
center = (2205,1635) # true center is (2304,1296)
radius = 165

lowerThresh = 50
upperThresh = 50

def standMarkCheck():
    img = cv.imread('frameworkOIU/inputCV/bolt_head.jpg') # 18 seems to be in more focus

    if img is None:
        print("Image failed to load")
        exit()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray=cv.bitwise_not(gray)

    preview = img.copy()
    cv.circle(preview, center, radius, (255,0,0), 3)

    # Create circular mask
    mask = np.zeros_like(gray, dtype=np.uint8)
    cv.circle(mask, center, radius, 255, -1)

    # Edge detection ONLY in ROI
    cannyCircle = cv.Canny(gray, lowerThresh, upperThresh)
    cannyCircle = cv.bitwise_and(cannyCircle, cannyCircle, mask=mask)
    cannyCircle = cv.dilate(cannyCircle, None, iterations=2)
    cannyCircle = cv.erode(cannyCircle, None, iterations=1)

    contours, hierarchy = cv.findContours(cannyCircle, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    idealBoltPhoto = img.copy()
    markings = []

    for contour in contours:
        area = cv.contourArea(contour)

        if area > 2000:  # large = center hole
            cv.drawContours(cannyCircle, [contour], -1, 0, -1)  # erase it

    cannyCircle = cv.dilate(cannyCircle, None, iterations=5)
    cannyCircle = cv.erode(cannyCircle, None, iterations=5)

    contours, hierarchy = cv.findContours(cannyCircle, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv.contourArea(contour)

        if 500 < area:
            print(area)
            markings.append(contour)
            cv.drawContours(idealBoltPhoto, [contour], -1, (0, 255, 0), 10)
            cv.drawContours(preview, [contour], -1, (0, 255, 0), 10)

    cv.imwrite("frameworkOperator/dataOut/Contours on the Ideal Bolt Head.jpg", idealBoltPhoto)

    print(f'\n There are {len(markings)} standardized markings')

    cv.imwrite("frameworkOperator/dataOut/ROI Preview with marks.jpg", preview)
    return len(markings) > 2
