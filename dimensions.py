from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2 as cv

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-w", "--width", type=float, required=True, help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (7, 7), 0)

edged = cv.Canny(gray, 50, 100)
edged = cv.dilate(edged, None, iterations=1)
edged = cv.erode(edged, None, iterations=1)

cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

for c in cnts:
    if cv.contourArea(c) < 100:
        continue

    orig = image.copy()
    box = cv.minAreaRect(c)
    box = cv.boxPoints(box)
    box = np.array(box, dtype="int")

    box = perspective.order_points(box)
    cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

    for (x, y) in box:
        cv.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)

    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

    cv.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    cv.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
    cv.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)

    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    if pixelsPerMetric is None:
        pixelsPerMetric = dB / args["width"]

    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric

    cv.putText(orig, "{:.1f}in".format(dimA), (int(tltrX - 15), int(tltrY - 10)), cv.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv.putText(orig, "{:.1f}in".format(dimB), (int(trbrX - 10), int(trbrY)), cv.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    cv.imshow("Image", orig)
    cv.waitKey(0)



# img = cv.imread('Photos/ideal_bolt.jpg')

# cv.imshow('Ideal Bolt', img)

# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('Gray', gray)

# canny = cv.Canny(img, 125, 175)
# cv.imshow('Canny Edges', canny)

# contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
# print(f'{len(contours)} countours(s) found!')

# cv.waitKey(0)
