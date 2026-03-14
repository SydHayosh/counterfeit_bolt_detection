import cv2 as cv

img = cv.imread('Photos/ppt_ex_head.jpg')
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


#cv.imshow('Ideal Bolt', img)
#cv.imwrite("Photos/output/Ideal Bolt.jpg", img)

# preview = img.copy()
# cv.rectangle(preview, (2380,1550), (2880,2050), (0,255,0), 5) #(x1,y1),(x2,y2) measured from the top left
# cv.imshow("ROI Location", preview)

print(img.shape)
roi = img[1550:2050, 2380:2880] #Region of Interest image[y1:y2, x1:x2]
#cv.imshow('ROI', roi)
# TODO look into HoughCircles()
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#cv.imshow('Gray', gray)
cv.imwrite("Photos/output/Gray.jpg", gray)

# grayCT = cv.cvtColor(imgCT, cv.COLOR_BGR2GRAY)
# cv.imwrite('Photos/output/Gray Counterfeit Titanium.jpg', grayCT)

# grayCB = cv.cvtColor(imgCB, cv.COLOR_BGR2GRAY)
# cv.imwrite('Photos/output/Gray Counterfeit Black.jpg', grayCB)
cannyMin50 = gray.copy()*0
cannyMin50[1550:2050, 2380:2880] = cv.Canny(gray.copy()[1550:2050, 2380:2880], 50, 70)
#cv.imshow('Canny Edges', cannyMin50)
cv.imwrite("Photos/output/Canny Edges 50.jpg", cannyMin50)

cannyMin100 = cv.Canny(gray.copy(), 100, 175)
cv.imwrite("Photos/output/Canny Edges 100.jpg", cannyMin100)

cannyMin125 = cv.Canny(gray.copy(), 125, 175)
cv.imwrite("Photos/output/Canny Edges 125.jpg", cannyMin125)

# TODO compare all canny edges on the same photo
contours, hierarchies = cv.findContours(cannyMin50, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours)} contours(s) found when the lower threshold is 50!')

Contours50 = img.copy()
cv.drawContours(Contours50, contours, -1, (0,255,0), 10) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
cv.imwrite("Photos/output/Contours 50.jpg", Contours50)

contoursCT, hierarchies = cv.findContours(cannyMin100, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contoursCT)} contours(s) found when the lower threshold is 100!')

contoursCB, hierarchies = cv.findContours(cannyMin125, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contoursCB)} contours(s) found when the lower threshold is 125!')

grayWithContours125 = gray.copy()
cv.drawContours(grayWithContours125, contoursCB, -1, (0,255,0), 4)
cv.imwrite("Photos/output/Contours 125.jpg", grayWithContours125)

# cv.waitKey(0) #needed because of imshow
# cv.destroyAllWindows()

