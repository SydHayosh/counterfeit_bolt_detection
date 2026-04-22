from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2 as cv

img = cv.imread('Photos/CBDS_Pics/idealSide.jpg')

if img is None:
    print("Image failed to load")
    exit()

img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
inv_img=cv.bitwise_not(img_gray)
cv.imshow('image1.jpg',inv_img)

# ## the whole bolt
# x1 = 2000
# x2 = 3000
# y1 = 1250
# y2 = 1500

## just the threads
x1 = 2010
x2 = 3000
y1 = 1300
y2 = 1400

## focuses on the lower edge
# x1 = 2200
# x2 = 2900
# y1 = 1480
# y2 = 1500

lowerThresh = 50
upperThresh = 30

print(img.shape)
roi = img[y1:y2, x1:x2] #Region of Interest image[y1:y2, x1:x2]
#cv.imshow('ROI', roi)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (7, 7), 0)

# edged = cv.Canny(gray, 50, 100)
# edged = cv.dilate(edged, None, iterations=6)
# edged = cv.erode(edged, None, iterations=1)

# cnts = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

preview = img.copy()
cv.rectangle(preview, (x1,y1),(x2,y2), (0,255,0), 5) #(x1,y1),(x2,y2) measured from the top left
cv.imshow("ROI Location", preview)



#cv.imshow('Gray', gray)
cv.imwrite("Photos/output/Gray.jpg", gray)

canny = gray.copy()*0
canny[y1:y2, x1:x2] = cv.Canny(gray.copy()[y1:y2, x1:x2], lowerThresh, lowerThresh)
cv.imshow('Canny Edges', canny)
cv.imwrite("Photos/output/Canny Edges Shaft.jpg", canny)

canny = cv.dilate(canny, None, iterations=5)
canny = cv.erode(canny, None, iterations=1)


contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

Contours = img.copy()
cv.drawContours(Contours, contours, -1, (0,255,0), 2) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
cv.imwrite("Photos/output/Contours 50.jpg", Contours)
cv.imshow('Contours', Contours)

idealBoltPhoto = img.copy()
threads = []

for contour in contours:
    area = cv.contourArea(contour)

    if 500 < area :
        print(area)
        threads.append(contour)
        cv.drawContours(idealBoltPhoto, [contour], -1, (0, 255, 0), 2)
            
#cv.drawContours(idealBoltPhoto, contours, -1, (0,255,0), 10) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
cv.imshow('Contours', idealBoltPhoto)
cv.imwrite("Photos/output/Contours on the Ideal Bolt.jpg", idealBoltPhoto)

print(f'\n There are {len(threads)} threads in the image') # Should be 24 when looking at just the threads


cv.waitKey(0)