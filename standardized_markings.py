import numpy as np
import cv2 as cv

img = cv.imread('Photos/ideal_bolt_light_test.png')
imgCT = cv.imread('Photos/counterfeit_bolt_titanium.jpg')
imgCB = cv.imread('Photos/counterfeit_bolt_black.jpg')

# Canny edge thresholds
lowerThresh = 125
upperThresh = 175

if img is None:
    print("Image failed to load")
    exit()

if imgCT is None:
    print("Titanium image failed to load")
    exit()

if imgCB is None:
    print("Black image failed to load")
    exit()


#cv.imshow('Ideal Bolt', img)
#cv.imwrite("Photos/output/Ideal Bolt.jpg", img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)
cv.imwrite("Photos/output/Gray.jpg", gray)

grayCT = cv.cvtColor(imgCT, cv.COLOR_BGR2GRAY)
cv.imwrite('Photos/output/Gray Counterfeit Titanium.jpg', grayCT)

grayCB = cv.cvtColor(imgCB, cv.COLOR_BGR2GRAY)
cv.imwrite('Photos/output/Gray Counterfeit Black.jpg', grayCB)

# #gray = cv.GaussianBlur(gray, (7, 7), 0)
# blur = cv.medianBlur(grayCT,301) #number must be odd
# cimg = imgCT.copy()
 
# circles = cv.HoughCircles(blur,cv.HOUGH_GRADIENT,1,20,param1=50,param2=32,minRadius=210,maxRadius=300)

# if circles is not None: 
#     circles = np.uint16(np.around(circles))
#     for i in circles[0,:]:
#         # draw the outer circle
#         cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#         # draw the center of the circle
#         cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

# else:
#     print("No circles detected")
 
# cv.imshow('detected circles',cimg)
# cv.imwrite("Photos/output/detected circles.jpg",cimg)

canny = cv.Canny(gray, lowerThresh, upperThresh)
#canny = cv.dilate(canny, None, iterations=1)
#canny = cv.erode(canny, None, iterations=1)
cv.imshow('Canny Edges', canny)
cv.imwrite("Photos/output/Canny Edges.jpg", canny)

cannyCT = cv.Canny(grayCT, lowerThresh, upperThresh)
cv.imwrite("Photos/output/Canny Edges Counterfeit Titanium.jpg", cannyCT)

cannyCB = cv.Canny(grayCB, lowerThresh, upperThresh)
cv.imwrite("Photos/output/Canny Edges Counterfeit Black.jpg", cannyCB)

contours, hierarchies = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} countours(s) found on the ideal bolt!')
hierarchies = hierarchies[0]

contoursCT, hierarchiesCT = cv.findContours(cannyCT, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contoursCT)} countours(s) found on the titanium bolt!')

contoursCB, hierarchiesCB = cv.findContours(cannyCB, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contoursCB)} countours(s) found on the black bolt!')

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
