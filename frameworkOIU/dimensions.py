from imutils import contours
import cv2 as cv

def countThreads():
    img = cv.imread('frameworkOIU/inputCV/bolt_shaft.jpg')

    if img is None:
        print("Image failed to load")
        exit()

    img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    inv_img=cv.bitwise_not(img_gray)

    # focuses on the upper edge
    x1 = 2200
    x2 = 2900
    y1 = 1240 #1240
    y2 = 1255 #1255

    lowerThresh = 50 # ideal(50), oxide(10)
    upperThresh = 30 # 

    print(img.shape)
    roi = img[y1:y2, x1:x2] #Region of Interest image[y1:y2, x1:x2]

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 0)

    preview = img.copy()
    cv.rectangle(preview, (x1,y1),(x2,y2), (0,255,0), 5) #(x1,y1),(x2,y2) measured from the top left

    canny = gray.copy()*0
    canny[y1:y2, x1:x2] = cv.Canny(gray.copy()[y1:y2, x1:x2], lowerThresh, lowerThresh)
    cv.imwrite("frameworkOperator/dataOut/Canny Edges Shaft.jpg", canny)

    canny = cv.dilate(canny, None, iterations=6) # ideal(5), oxide(3)
    canny = cv.erode(canny, None, iterations=1)


    contours, hierarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    Contours = img.copy()
    cv.drawContours(Contours, contours, -1, (0,255,0), 2) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
    cv.imwrite("frameworkOperator/dataOut/Contours 50.jpg", Contours)

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

    cannyLow = gray.copy()*0
    cannyLow[y1:y2, x1:x2] = cv.Canny(gray.copy()[y1:y2, x1:x2], lowerThresh, lowerThresh)
    cv.imwrite("frameworkOperator/dataOut/Canny Edges Shaft.jpg", cannyLow)

    cannyLow = cv.dilate(cannyLow, None, iterations=6) # ideal(5), oxide(3)
    cannyLow = cv.erode(cannyLow, None, iterations=1)

    lowContours, hierarchies = cv.findContours(cannyLow, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    Contours = img.copy()
    cv.drawContours(Contours, lowContours, -1, (0,255,0), 2) #cv.drawContours(image being drawn on, contours, which contours to draw? just use -1, color, line thickness)
    cv.imwrite("frameworkOperator/dataOut/Contours 50.jpg", Contours)

    lowThreads = []

    for contour in lowContours:
        area = cv.contourArea(contour)

        if 10 < area : # ideal(500), oxide(800)
            print(area)
            lowThreads.append(contour)
            cv.drawContours(idealBoltPhoto, [contour], -1, (0, 255, 0), 2)

    cv.imwrite("frameworkOperator/dataOut/Contours on the Ideal Bolt.jpg", idealBoltPhoto)

    print(f'\n There are {len(lowThreads)} threads in the image') # Should be 17 when looking at just the threads
    return len(lowThreads) == 17
