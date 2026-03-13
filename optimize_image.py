import cv2 as cv

img = cv.imread('Photos/rawtest.jpg')
#imgCT = cv.imread('Photos/counterfeit_bolt_titanium.jpg')
#imgCB = cv.imread('Photos/counterfeit_bolt_black.jpg')

if img is None:
    print("Image failed to load")
    exit()

# if imgCT is None:
#     print("Titanium image failed to load")
#     exit()

# if imgCB is None:
#     print("Black image failed to load")
#     exit()


cv.imshow('Ideal Bolt', img)
#cv.imwrite("Photos/output/Ideal Bolt.jpg", img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)
cv.imwrite("Photos/output/Gray.jpg", gray)

# grayCT = cv.cvtColor(imgCT, cv.COLOR_BGR2GRAY)
# cv.imwrite('Photos/output/Gray Counterfeit Titanium.jpg', grayCT)

# grayCB = cv.cvtColor(imgCB, cv.COLOR_BGR2GRAY)
# cv.imwrite('Photos/output/Gray Counterfeit Black.jpg', grayCB)

cannyMin50 = cv.Canny(gray.copy(), 50, 175)
cv.imshow('Canny Edges', cannyMin50)
cv.imwrite("Photos/output/Canny Edges 50.jpg", cannyMin50)

cannyMin100 = cv.Canny(gray.copy(), 100, 175)
cv.imwrite("Photos/output/Canny Edges 100.jpg", cannyMin100)

cannyMin125 = cv.Canny(gray.copy(), 125, 175)
cv.imwrite("Photos/output/Canny Edges 125.jpg", cannyMin125)

contours, hierarchies = cv.findContours(cannyMin50, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} countours(s) found when the lower threshold is 50!')

contoursCT, hierarchies = cv.findContours(cannyMin100, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contoursCT)} countours(s) found when the lower threshold is 100!')

contoursCB, hierarchies = cv.findContours(cannyMin125, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contoursCB)} countours(s) found when the lower threshold is 125!')

cv.waitKey(0)

