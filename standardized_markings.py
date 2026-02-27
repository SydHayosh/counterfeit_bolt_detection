import cv2 as cv

img = cv.imread('Photos/ideal_bolt.jpg')

cv.imshow('Ideal Bolt', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

canny = cv.Canny(img, 125, 175)
cv.imshow('Canny Edges', canny)

contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} countours(s) found!')

cv.waitKey(0)
