from imutils import contours
import cv2 as cv

img = cv.imread('Photos/bolt_shaft ideal.jpg')

if img is None:
    print("Image failed to load")
    exit()

lowerThresh = 50 # ideal(50), oxide(10)
upperThresh = 50 # 

# Wide box to find the bolt
x1 = 2200
x2 = 2850
y1 = 1000
y2 = 1800

# preview = img.copy()
# cv.rectangle(preview, (x1,y1),(x2,y2), (0,255,0), 5) #(x1,y1),(x2,y2) measured from the top left
# cv.imshow("Wide scan for bolt", preview)

img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# img_gray = cv.GaussianBlur(img_gray, (101, 101), 0) # kernal needs to be an odd number

canny = img_gray.copy()*0
canny[y1:y2, x1:x2] = cv.Canny(img_gray.copy()[y1:y2, x1:x2], lowerThresh, upperThresh)
canny = cv.dilate(canny, None, iterations=10) # ideal(5), oxide(3)
canny = cv.erode(canny, None, iterations=4)

print(f'\n There are {len(canny)} canny edges')
cv.imshow('entire image canny', canny)

contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

boltPhoto = img.copy()
for c in contours:
    area = cv.contourArea(c)

    if 20000 < area : # ideal(500), oxide(800)
        print(area)
        cv.drawContours(boltPhoto, [c], -1, (0, 255, 0), 2)

cv.imshow('entire image contours', canny)
# ## the whole bolt
# x1 = 2000
# x2 = 3000
# y1 = 1250
# y2 = 1500

# ## just the threads
# x1 = 2010
# x2 = 3000
# y1 = 1300
# y2 = 1400

# # focuses on the lower edge
# x1 = 2200
# x2 = 2900
# y1 = 1480
# y2 = 1510

# focuses on the upper edge
x1 = 2200
x2 = 2900
y1 = 1240 #1240
y2 = 1255 #1255



print(img.shape)
roi = img[y1:y2, x1:x2] #Region of Interest image[y1:y2, x1:x2]
#cv.imshow('ROI', roi)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (7, 7), 0) # kernal needs to be an odd number

preview = img.copy()
cv.rectangle(preview, (x1,y1),(x2,y2), (0,255,0), 5) #(x1,y1),(x2,y2) measured from the top left
cv.imshow("ROI Location", preview)

canny = gray.copy()*0
canny[y1:y2, x1:x2] = cv.Canny(gray.copy()[y1:y2, x1:x2], lowerThresh, lowerThresh)
cv.imshow('Canny Edges', canny)
cv.imwrite("Photos/output/Canny Edges Shaft.jpg", canny)

canny = cv.dilate(canny, None, iterations=6) # ideal(5), oxide(3)
canny = cv.erode(canny, None, iterations=1)


contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

Contours = img.copy()
cv.drawContours(Contours, contours, -1, (0,255,0), 2) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
cv.imwrite("Photos/output/Contours 50.jpg", Contours)
cv.imshow('Contours', Contours)

idealBoltPhoto = img.copy()
upThreads = []

for contour in contours:
    area = cv.contourArea(contour)

    if 10 < area : # ideal(500), oxide(800)
        print(area)
        upThreads.append(contour)
        cv.drawContours(idealBoltPhoto, [contour], -1, (0, 255, 0), 2)

# focuses on the lower edge
x1 = 2200
x2 = 2900
y1 = 1480
y2 = 1510

preview = img.copy()
cv.rectangle(preview, (x1,y1),(x2,y2), (0,255,0), 5) #(x1,y1),(x2,y2) measured from the top left
cv.imshow("ROI Location", preview)

cannyLow = gray.copy()*0
cannyLow[y1:y2, x1:x2] = cv.Canny(gray.copy()[y1:y2, x1:x2], lowerThresh, lowerThresh)
cv.imshow('Canny Edges', cannyLow)
cv.imwrite("Photos/output/Canny Edges Shaft.jpg", cannyLow)

cannyLow = cv.dilate(cannyLow, None, iterations=6) # ideal(5), oxide(3)
cannyLow = cv.erode(cannyLow, None, iterations=1)


lowContours, hierarchies = cv.findContours(cannyLow, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

Contours = img.copy()
cv.drawContours(Contours, lowContours, -1, (0,255,0), 2) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
cv.imwrite("Photos/output/Contours 50.jpg", Contours)
cv.imshow('Contours', Contours)

lowThreads = []

for contour in lowContours:
    area = cv.contourArea(contour)

    if 10 < area : # ideal(500), oxide(800)
        print(area)
        lowThreads.append(contour)
        cv.drawContours(idealBoltPhoto, [contour], -1, (0, 255, 0), 2)
            
#cv.drawContours(idealBoltPhoto, contours, -1, (0,255,0), 10) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
cv.imshow('Contours', idealBoltPhoto)
cv.imwrite("Photos/output/Contours on the Ideal Bolt.jpg", idealBoltPhoto)

print(f'\n There are {len(lowThreads)} threads in the image') # Should be 24 when looking at just the threads


cv.waitKey(0)