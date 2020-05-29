import cv2
import numpy as np

framewidth = 640
frameheight = 480

cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,150)

colors = [[0,129,140,6,255,255],
          [83,96,0,159,232,255]]

colorValue = [[0,0,255],       #BGR
              [255,0,0]]
myPoints =  []  ## [x , y , colorId ]


def findColor(img,colors,colorValue):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        #cv2.imshow(str(color[0]),mask)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,colorValue[count],cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count+=1
    return newPoints

def getContours(img):
    x,y,w,h=0,0,0,0
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if(area > 500):
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,colorValue):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, colorValue[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, colors, colorValue)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, colorValue)
    cv2.imshow("Result", imgResult)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break