#from src import speechToText
import json
import logging
import subprocess
import threading
import time
from email import message
from queue import Queue
import describeSetting
import cv2

#import llm
#import llm
import newllm
import textToSpeech
from detectFace import detect_face
from speechToText import runSpeechToText

# Logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Config
def getConfigSettings(settings : list):
    """"""
    returnedSettings = []
    with open("C:\\Users\\sampo\\OneDrive\\Desktop\\Python projects\\Motion Detection AI\\src\config.json") as file:
        config = json.load(file)
        for setting in settings:
            print(setting)
            returnedSettings.append(config[setting])

    return returnedSettings

LLM_LIFETIME = getConfigSettings(["LLM_LIFETIME"])

def take_photo(filename="src/photo.jpg", camera_index=0):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # CAP_DSHOW = faster on Windows

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")

    # Warm up camera very briefly (improves exposure)
    time.sleep(0.1)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("Failed to capture image")

    cv2.imwrite(filename, frame)
    return filename

def timer_():
    
    global stop_llm

    for i in range(LLM_LIFETIME[0]):
        time.sleep(1)

    stop_llm = True


def listen():
    q = Queue()
    t = threading.Thread(target=runSpeechToText, args=(q,))  
    t.start()
    t.join()  

    result = q.get()
    print(result)
    return result

messageHistory = []
def cleanMessage(message):
    messageHistory.append(f"USER:{message}")
    response = newllm.sendMessage(str(messageHistory))
    print(response)
    return response


def run():
    global stop_llm
    stop_llm = False
    print("starting face detection")
    detect_face()
    logging.debug("face detection finished")
    print("face detection finished")

#   Set lifetimer
    threading.Thread(target=timer_).start()
    logging.debug("LLM lifetimer started")


    messageHistory.append("""SYSTEM: motion detected""")

    response = newllm.sendMessage(str(messageHistory))
    response = newllm.sendMessage(str(messageHistory))
    messageHistory.append(f"AGENT:{response}")

    textToSpeech.run(response)

    no_response_count = 0
    last_response_count = 0      
    while stop_llm is False:
        print("beginning to listen")
        userResponse = listen()
        if userResponse is not None:
            logging.debug(f"User response: {userResponse}")

            messageHistory.append(f'USER:{userResponse}')
            response = newllm.sendMessage(str(messageHistory)) #send to llm
            response = newllm.sendMessage(str(messageHistory)) #send to llm
            messageHistory.append(response)

            print(response) #print llm response
            textToSpeech.run(response) #speak llm response
        
        elif userResponse is None:
            no_response_count = no_response_count + 1
            if no_response_count - last_response_count > 1:
                photoname = take_photo()
                room_description = describeSetting.describe_setting(photoname)
                messageHistory.append(f"SYSTEM: the user is ignoring you. Description of room: {room_description}")
                response = newllm.sendMessage(str(messageHistory))
                textToSpeech.run(response)
                messageHistory.append(response)

                logging.debug("Sent inactivity report to LLM")
                last_response_count = no_response_count
            logging.debug("returned none")
    time.sleep(1)


    logging.debug("LLM lifetimer ended")
        

while True:
    run()
