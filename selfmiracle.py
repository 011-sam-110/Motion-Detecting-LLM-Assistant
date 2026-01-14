import cv2
import numpy as np

webcam = cv2.VideoCapture(1)

trained_face_data = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    success, frame = webcam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_coordinates = trained_face_data.detectMultiScale(gray, 1.3, 2)

    for (x, y, w, h) in face_coordinates:
        cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 5)
        print("face found")

    
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()

"""
to DO;
take screenshot of the face
discord webhook
AI
"""