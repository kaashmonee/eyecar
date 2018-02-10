import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

center = 0
while(1):
    _, frame = cap.read()
    height, width, channels = frame.shape
    frame[0:height - 30, 0:width] = [255, 255, 255]
    
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    retval, threshold = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
    #gaus = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 2)
    count = 0;
    i = 0
    for r in range(width):
        for c in range(height):
            if str(threshold[r:r+1, c:c+1]) == '0':
                count+=1
            elif count > 0:
                center = i % width  - (count / 2)
                break
            i+=1
            
            
    
    cv2.rectangle(frame, (center, 0), (center+1, height), (0, 255, 0), 2)
    #for a in contours:
    #    cv2.drawContours(frame, [a], 0, (0,255,0), 3)
    #cnt = contours[0]
    #cv2.drawContours(frame, [cnt], 0, (0,255,0), 3)
    #lower_black = np.array([0,0,0])
    #upper_black = np.array([155,155,155])
    
    #mask = cv2.inRange(hsv, lower_black, upper_black)
    #res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('gaus', gaus)
    cv2.imshow('threshold', threshold)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
