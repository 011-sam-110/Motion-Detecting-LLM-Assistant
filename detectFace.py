import cv2
import json 
import logging
logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
# Config
JSON_PATH = 'detectionState.json'
CAMERA = 1

def updateJson(setting : bool):

    data = {"activated":setting}

    with open(JSON_PATH, 'w') as file:
        data = json.dump(data, file)

def detect_face():
    webcam = cv2.VideoCapture(CAMERA)

    trained_face_data = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        success, frame = webcam.read()

#       gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

#       find face
        face_coordinates = trained_face_data.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)

#       Face found
        if len(face_coordinates) > 0:
            logging.info("Face detected")

            for (x, y, w, h) in face_coordinates:
                cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 5)

            updateJson(True)
            logging.debug("Killing facial recognition")
            quit()
            return True
        else:
            updateJson(False)

logging.info("Facial detection starting")
detect_face()
#        cv2.imshow(f'', gray)
#        if cv2.waitKey(1) == ord('q'):
#            break
#
