
import json
import random
from datetime import datetime

import cv2
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Logs
def log(message: str, level: str = "INFO", function_name: str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    colors = {
        "INFO": Fore.CYAN,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "DEBUG": Fore.MAGENTA,
    }

    color = colors.get(level.upper(), Fore.WHITE)
    level = level.upper()

    print(f"{Fore.WHITE}[{timestamp}] "
          f"{color}[{level}]  [@{function_name}] "
          f"{Style.RESET_ALL}{message}")
    
# Config
def getConfigSettings(settings : list):
    """"""
    returnedSettings = []
    with open("C:\\Users\\sampo\\OneDrive\\Desktop\\Python projects\\Motion Detection AI\\src\\config.json") as file:
        config = json.load(file)
        for setting in settings:
            returnedSettings.append(config[setting])

    return returnedSettings

def detect_face():
    log("Running facial detection script", "info", "detect_face.py")

#   CAMERA CONFIG
    if getConfigSettings(["MULTIPLE_CAMERAS"]):
        cameraDigits = []
        COMBINED_CAMERA_DIGITS = getConfigSettings(["CAMERA_DIGITS"])
        for each in COMBINED_CAMERA_DIGITS:
            cameraDigits.append(each)
        CAMERA = random.choice(cameraDigits[0])
        CAMERA = int(CAMERA)
    else:
#       Type validation
        CAMERA = getConfigSettings(["CAMERA_DIGITS"])
        if type(CAMERA) is not int:
            CAMERA = 0 
    
    mycodelies = 1
    webcam = cv2.VideoCapture(mycodelies, cv2.CAP_DSHOW)
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
            log("Face detected, script terminating", "success", "DetectFace.py")
            return True


#        cv2.imshow(f'', gray)
#        if cv2.waitKey(1) == ord('q'):
#            break


