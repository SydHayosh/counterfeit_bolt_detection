import cv2 as cv

img = cv.imread('Photos/rawtest.jpg')
imgCT = cv.imread('Photos/counterfeit_bolt_titanium.jpg')
imgCB = cv.imread('Photos/counterfeit_bolt_black.jpg')

if img is None:
    print("Image failed to load")
    exit()

if imgCT is None:
    print("Titanium image failed to load")
    exit()

if imgCB is None:
    print("Black image failed to load")
    exit()


cv.imshow('Ideal Bolt', img)
#cv.imwrite("Photos/output/Ideal Bolt.jpg", img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)
cv.imwrite("Photos/output/Gray.jpg", gray)

grayCT = cv.cvtColor(imgCT, cv.COLOR_BGR2GRAY)
cv.imwrite('Photos/output/Gray Counterfeit Titanium.jpg', grayCT)

grayCB = cv.cvtColor(imgCB, cv.COLOR_BGR2GRAY)
cv.imwrite('Photos/output/Gray Counterfeit Black.jpg', grayCB)

canny = cv.Canny(gray, 125, 175)
cv.imshow('Canny Edges', canny)
cv.imwrite("Photos/output/Canny Edges.jpg", canny)

cannyCT = cv.Canny(grayCT, 125, 175)
cv.imwrite("Photos/output/Canny Edges Counterfeit Titanium.jpg", cannyCT)

cannyCB = cv.Canny(grayCB, 125, 175)
cv.imwrite("Photos/output/Canny Edges Counterfeit Black.jpg", cannyCB)

contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} countours(s) found on the ideal bolt!')

contoursCT, hierarchies = cv.findContours(cannyCT, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contoursCT)} countours(s) found on the titanium bolt!')

contoursCB, hierarchies = cv.findContours(cannyCB, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contoursCB)} countours(s) found on the black bolt!')

cv.waitKey(0)
