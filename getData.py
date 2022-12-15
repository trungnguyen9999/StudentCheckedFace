import cv2 as cv
import numpy as np
import sqlite3 as sql
import os
import time

def insertOrUpdate(id, mssv, name):
    conn = sql.connect("data_face.db")
    query = "SELECT * FROM sinhvien where id = " + str(id)
    cursor = conn.execute(query)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist == 0):
        query = "INSERT INTO sinhvien (id, mssv, name) VALUES (" + str(id) + ", '" + str(mssv) + "', '" + str(name) + "')"
    else:
        query = "UPDATE sinhvien SET name = '" + str(name) + "', mssv = '" + str(mssv) + "' WHERE id = " + str(id)
    conn.execute(query)
    conn.commit()
    conn.close()

#Test ket noi db thanh cong    
#insertOrUpdate("DC1896N722", "Nguyen Trung Nguyen")

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv.VideoCapture(0)

index = 0

#Insert to db
# mssv = input("Nhập vào mã số sinh viên: ")
# name = input("Nhập họ tên sinh viên: ")   
# id = mssv.split('N')[1]
# insertOrUpdate(id, mssv, name)

while(True):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 225), 2)
        # if not os.path.exists('dataset/' + str(mssv) + '.' + str(id)):
        #     os.makedirs('dataset/' + str(mssv) + '.' + str(id))
            
        
        index += 1
        # cv.imwrite('dataset/' + str(mssv) + '.' + str(id) + '/student_'+ str(mssv) + '.' + str(index) + '.jpg', gray[y: y+h, x: x+w])
    cv.imshow("DETECTING FACE", frame)
    if(cv.waitKey(1) & 0xFF == ord('q')):
        break
    
    if(index >= 100):
        break
    #time.sleep(0.1)
cap.release()
cv.destroyAllWindows()
