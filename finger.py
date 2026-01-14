import numpy as np
import cv2 as cv


cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")


while True:
#   Read frame from camera
    ret, frame = cap.read()

#   If the frame is read correctly, ret is true
    if not ret:
        print("Can't receive frame")
        break
    
#   Colour frame operations
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    if cv.waitKey():
        break

cap.release()
cv.destroyAllWindows()