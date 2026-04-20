import numpy as np
import cv2 as cv

img = cv.imread('Photos/ideal_bolt_light_test.png')


# Canny edge thresholds
lowerThresh = 125
upperThresh = 175

if img is None:
    print("Image failed to load")
    exit()


#cv.imshow('Ideal Bolt', img)
#cv.imwrite("Photos/output/Ideal Bolt.jpg", img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)
cv.imwrite("Photos/output/Gray.jpg", gray)


# #gray = cv.GaussianBlur(gray, (7, 7), 0)
# blur = cv.medianBlur(grayCT,301) #number must be odd
# cimg = imgCT.copy()

canny = cv.Canny(gray, lowerThresh, upperThresh)
#canny = cv.dilate(canny, None, iterations=1)
#canny = cv.erode(canny, None, iterations=1)
cv.imshow('Canny Edges', canny)
cv.imwrite("Photos/output/Canny Edges.jpg", canny)


contours, hierarchies = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} countours(s) found on the ideal bolt!')
hierarchies = hierarchies[0]


markings = []

idealBoltPhoto = img.copy()
for i, contour in enumerate(contours):
    area = cv.contourArea(contour)

    if area > 50:
        if hierarchies[i][3] == -1:
            # outer contour
            cv.drawContours(idealBoltPhoto, contours, i, (0,255,0), 3)
        else: #elif area < 1500:
            # inner contour
            markings.append(contour)
            cv.drawContours(idealBoltPhoto, contours, i, (0,0,255), 3)
#cv.drawContours(idealBoltPhoto, contours, -1, (0,255,0), 10) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
cv.imshow('Contours', idealBoltPhoto)
cv.imwrite("Photos/output/Contours on the Ideal Bolt.jpg", idealBoltPhoto)

print(f'\n There are {len(markings)} standardized markings')


cv.waitKey(0)