#from src import speechToText
import json
import threading
import time
from datetime import datetime
from email import message
from queue import Queue

import cv2
from colorama import Fore, Style, init

import describeSetting
import newllm
import textToSpeech
from detectFace import detect_face
from speechToText import runSpeechToText

# Initialize colorama (important on Windows)
init(autoreset=True)

#logs
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
    with open("C:\\Users\\sampo\\OneDrive\\Desktop\\Python projects\\Motion Detection AI\\src\config.json") as file:
        config = json.load(file)
        for setting in settings:
            returnedSettings.append(config[setting])

    return returnedSettings

log("Gathering LLM lifetime from config")
LLM_LIFETIME = getConfigSettings(["LLM_LIFETIME"])
log("Gathered LLM lifetime from config", "success")

def take_photo(filename="src/photo.jpg", camera_index=0):
    log(f"Opening camera, index {camera_index}", "info", "take_photo")
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
    log(f"Photo successfully saved as {filename}", "success", "take_photo")
    return filename

def timer_():
    log("LLM lifetime timer started", "success", "timer")
    global stop_llm

    for i in range(LLM_LIFETIME[0]):
        time.sleep(1)

    stop_llm = True


def listen():
    log("Running text to speech", "info", "listen")
    q = Queue()
    t = threading.Thread(target=runSpeechToText, args=(q,))  
    t.start()
    t.join()  

    result = q.get()
    log(f"Returning result: {result}", "Success", "listen")
    return result

messageHistory = []
def cleanMessage(message):
    messageHistory.append(f"USER:{message}")
    response = newllm.sendMessage(str(messageHistory))
    return response


def run():
    global stop_llm
    stop_llm = False
    
    detect_face()
    

#   Set lifetimer
    threading.Thread(target=timer_).start()


    messageHistory.append("""SYSTEM: motion detected""")

    response = newllm.sendMessage(str(messageHistory))
    response = newllm.sendMessage(str(messageHistory))
    messageHistory.append(f"AGENT:{response}")

    textToSpeech.run(response)

    no_response_count = 0
    last_response_count = 0      
    while stop_llm is False:
        userResponse = listen()
        if userResponse is not None:

            messageHistory.append(f'USER:{userResponse}')
            response = newllm.sendMessage(str(messageHistory)) #send to llm
            response = newllm.sendMessage(str(messageHistory)) #send to llm
            messageHistory.append(response)

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

                
                last_response_count = no_response_count
            
    time.sleep(1)


    
        

while True:
    log("Starting program", "info", "start")
    run()
