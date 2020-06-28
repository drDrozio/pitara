# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:15:23 2020

@author: Ishan SS
"""

import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

path='Resources/shapes.png'
img=cv2.imread(path)
imgContour=img.copy()

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        print()
        print(area)
        if area>500:
            cv2.drawContours(imgContour,cnt,-1,(0,0,0),3)
            perimeter=cv2.arcLength(cnt,True)
            print(perimeter)
            approx=cv2.approxPolyDP(cnt,0.02*perimeter,True)
            print(len(approx))
            objCorners=len(approx)
            x,y,w,h=cv2.boundingRect(approx)
            if objCorners==3:
                objType="Tri"
            elif objCorners==4:
                aspRatio=w/float(h)
                if aspRatio>0.95 and aspRatio<1.05:
                    objType="Square"
                else:
                    objType="Rect"
            elif objCorners==5:
                objType="Pent"
            elif objCorners==6:
                objType="Hex"
            elif objCorners==10:
                objType="Star"
            else:
                objType="Poly"
            
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour,objType,(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,255),2)
            print()
            
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur=cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny=cv2.Canny(imgBlur,50,50)
getContours(imgCanny)
imgBlank=np.zeros_like(img)
imgStack=stackImages(0.6,([img,imgGray,imgBlur],[imgCanny,imgContour,imgBlank]))
cv2.imshow("Output",imgStack)
cv2.waitKey(0)