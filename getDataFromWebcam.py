from curses import window
import cv2 as cv
import numpy as np
from tkinter import *

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    for(x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 225), 2)
    cv.imshow("DETECTING FACE", frame)
    if(cv.waitKey(1) & 0xFF == ord('q')):
        break
cap.release()
cv.destroyAllWindows()
