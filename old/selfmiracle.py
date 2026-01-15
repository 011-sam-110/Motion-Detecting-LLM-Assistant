import cv2
import numpy as np
import threading
from src import test
import pyttsx3
import time
from collections import deque
#from src import speechToText

from queue import Queue

speech_queue = Queue()

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # speed
engine.setProperty('volume', 1.0)  # volume 0-1
motionDetected = False

# Configuration
TRIGGER_THRESHOLD = 1  
WINDOW_SECONDS = 1      

# State
input_boolean = False       
motionDetected = False      
trigger_times = deque()    


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

        
        face_coordinates = trained_face_data.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)
        
        found_face = len(face_coordinates) > 0
        for (x, y, w, h) in face_coordinates:
            cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 5)
            


        cv2.imshow(f'{found_face}', gray)
        if cv2.waitKey(1) == ord('q'):
            break

# Main monitoring loop
def monitorLoop():
    global motionDetected
    while True:
        input_boolean = found_face
        current_time = time.time()

        if input_boolean:
            trigger_times.append(current_time)

        # Remove timestamps older than WINDOW_SECONDS
        while trigger_times and current_time - trigger_times[0] > WINDOW_SECONDS:
            trigger_times.popleft()

        # Check if the threshold has been reached
        if len(trigger_times) >= TRIGGER_THRESHOLD:
            motionDetected = True
        else:
            motionDetected = False

        time.sleep(0.05)  # Adjust polling rate as needed

current_text = None
old_text = None

#def getS2T():
#    global current_text
#    while True:
#        current_text = speechToText.run()


    
def tts_worker():
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    while True:
        text = speech_queue.get()
        if text is None:
            print("exited loop", flush=True)
            break
        engine.say(text)
        engine.runAndWait()
        print("i spoke", flush=True)
        speech_queue.task_done()
        

def speak(text):
    speech_queue.put(text)



threading.Thread(target=detect_face).start()
threading.Thread(target=monitorLoop).start()
#threading.Thread(target=getS2T).start()
threading.Thread(target=tts_worker, daemon=False).start()



last_response = None

while True:
    if motionDetected:
        print("motion detected")
        response = test.sendMessage(
            "someone is moving around, what are they doing? better be leaving."
        )

        if response != last_response:
            print(response)
            speak(response)
            last_response = response

    elif current_text != old_text and current_text is not None:
        response = test.sendMessage(current_text)
        print(f"you said {current_text}")
        speak(response)
        print(response)
        old_text = current_text
        last_response = response

    time.sleep(0.1)