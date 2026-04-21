import numpy as np
import cv2 as cv

img = cv.imread('Photos/CBDS_Pics/ideal-pos20.jpg')

# ROI parameters
center = (2205,1635) # true center is (2304,1296)
radius = 170

lowerThresh = 40
upperThresh = 50

if img is None:
    print("Image failed to load")
    exit()


gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#gray = cv.GaussianBlur(gray, (7, 7), 0)

#cv.imshow('Ideal Bolt', img)
#cv.imwrite("Photos/output/Ideal Bolt.jpg", img)

preview = img.copy()
cv.circle(preview, center, radius, (0,255,0), 3)
cv.imshow("ROI Preview", preview)

# Create circular mask
mask = np.zeros_like(gray, dtype=np.uint8)
cv.circle(mask, center, radius, 255, -1)

# Apply mask
maskedGray = cv.bitwise_and(gray, gray, mask=mask)

# Edge detection ONLY in ROI
cannyCircle = cv.Canny(maskedGray, lowerThresh, upperThresh)
cannyCircle = cv.dilate(cannyCircle, None, iterations=1)
cannyCircle = cv.erode(cannyCircle, None, iterations=1)

cv.imshow("Edges in Circular ROI", cannyCircle)

# Use THIS for contours (not full image!)
#contours, hierarchies = cv.findContours(cannyCircle, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
contours, hierarchy = cv.findContours(cannyCircle, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


# blur = cv.medianBlur(grayCT,301) #number must be odd
# cimg = imgCT.copy()


idealBoltPhoto = img.copy()
markings = []

for contour in contours:
    area = cv.contourArea(contour)

    if 120 < area < 130 or 107 < area < 109:
        print(area)
        markings.append(contour)
        cv.drawContours(idealBoltPhoto, [contour], -1, (0, 255, 0), 10)
        # if hierarchies[i][3] == -1:
        #     # outer contour
        #     cv.drawContours(idealBoltPhoto, contours, i, (0,255,0), 3)
        # else: #elif area < 1500:
        #     # inner contour
            
#cv.drawContours(idealBoltPhoto, contours, -1, (0,255,0), 10) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
cv.imshow('Contours', idealBoltPhoto)
cv.imwrite("Photos/output/Contours on the Ideal Bolt.jpg", idealBoltPhoto)

print(f'\n There are {len(markings)} standardized markings')


cv.waitKey(0)

