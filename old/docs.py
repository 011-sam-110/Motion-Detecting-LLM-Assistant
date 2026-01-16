from charset_normalizer import detect
import cv2
import numpy as np
import threading
from src import test
import pyautogui
import pyttsx3
import time

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # speed
engine.setProperty('volume', 1.0)  # volume 0-1

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.runAndWait()

found_face = True

def detect_face():
    global webcam, found_face
    webcam = cv2.VideoCapture(1)

    trained_face_data = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        success, frame = webcam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        found_face = False
        face_coordinates = trained_face_data.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=4)

        for (x, y, w, h) in face_coordinates:
            cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 5)
            found_face = True


        cv2.imshow('frame', gray)
        if cv2.waitKey(1) == ord('q'):
            break


threading.Thread(target=detect_face).start()

while True:
    time.sleep(.5)
    if found_face:
        response = test.sendMessage("Someone has entered the room")
        engine.say(response)
        print("said response")
        

