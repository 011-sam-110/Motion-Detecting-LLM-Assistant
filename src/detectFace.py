import cv2
import logging


def detect_face():
    print("started")

#   Logger
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    CAMERA = 1
    webcam = cv2.VideoCapture(CAMERA)

    trained_face_data = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        success, frame = webcam.read()
#          gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
#          find face
        face_coordinates = trained_face_data.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5)
#          Face found
        if len(face_coordinates) > 0:
            for (x, y, w, h) in face_coordinates:
                cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 5)
            return True

detect_face()
#        cv2.imshow(f'', gray)
#        if cv2.waitKey(1) == ord('q'):
#            break
#
