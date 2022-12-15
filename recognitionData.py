
import profile
import cv2 as cv
import numpy as np
import os
import sqlite3 as sql
from PIL import Image

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingdata.yml')

def getProfile(id):
    conn = sql.connect('data_face.db')
    query = "SELECT * FROM sinhvien WHERE id = " + str(id)
    cursor = conn.execute(query)
    profile = None
    for r in cursor:
        profile = r
    conn.close()
    return profile

cap = cv.VideoCapture(0)
while (True):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 225), 2)
        roi_gray = gray[y:y+h, x:x+w]
        id, confidence = recognizer.predict(roi_gray)
        if confidence < 40:
            profile = getProfile(id)
            if profile != None:
                cv.putText(frame, "" + str(profile[1]), (x+10, y+h+30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv.putText(frame, "Unknown", (x+10, y+h+30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv.imshow('My Face' ,frame)
    if (cv.waitKey(1) == ord ('q')):
        break

cap.release()
cv.destroyAllWindows()