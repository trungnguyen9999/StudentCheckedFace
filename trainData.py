import cv2 as cv
import numpy as np
import os
from PIL import Image

recognizer = cv.face.LBPHFaceRecognizer_create()
path = 'dataset'

def getImageWithMssv(path):
    sinhVienPaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    for sinhVienPath in sinhVienPaths:
        print(sinhVienPath)
        imagePaths = [os.path.join(sinhVienPath, f) for f in os.listdir(sinhVienPath)]
        print(imagePaths)
        
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            
            faces.append(faceNp)
            ids.append(int(sinhVienPath.split('\\')[1].split('.')[1]))
            cv.imshow('Training...', faceNp)
            cv.waitKey(10)
    return faces, ids
        
_faces, _ids = getImageWithMssv(path)
recognizer.train(_faces, np.array(_ids))

if not os.path.exists('recognizer'):
    os.makedirs('recognizer')
    
recognizer.save('recognizer/trainingdata.yml')
cv.destroyAllWindows()