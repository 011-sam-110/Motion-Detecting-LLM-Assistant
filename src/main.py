#from src import speechToText
import json
import subprocess
import logging
import time
import threading
import pyttsx3
import llm
from speechToText import runSpeechToText
from queue import Queue






logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')




# Config
JSON_PATH = 'C:\\Users\\sampo\\Downloads\\OpenCV Things\\detectFace.py'
LLM_LIFETIME = 60 * 5

audio_lock = threading.Lock()
engine = pyttsx3.init()
engine.setProperty('rate', 200)  # speed
engine.setProperty('volume', 1.0)  # volume 0-1

def timer_():
    global stop_llm

    for i in range(LLM_LIFETIME):
        time.sleep(1)

    stop_llm = True


def readJson():
    time.sleep(.5)
    try:
        with open(JSON_PATH) as file:
            data = json.load(file)
            return data["activated"]
    except Exception as e:
        return False


def updateJson(setting: bool):

    data = {"activated": setting}

    with open(JSON_PATH, 'w') as file:
        json.dump(data, file)


# Kill face detection
def killFaceDetection():
    global detectFace

    detectFace.terminate()
    detectFace.wait()
    detectFace = None

def startFaceDetection():
    global detectFace

    # Start face detection
    detectFace = subprocess.Popen(["Python", "detectFace.py"])

    while True:
        if readJson() == True:
            killFaceDetection()
            updateJson(False)
            break

def speak(text):
    with audio_lock:
        engine.say(text)
        engine.runAndWait()

def listen():
    with audio_lock:
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
    response = llm.sendMessage(str(messageHistory))
    print(response)
    return response


def run():
    global stop_llm
    stop_llm = False

    startFaceDetection()
    logging.debug("face detection finished")
    print("face detection finished")

#   Set lifetimer
    threading.Thread(target=timer_).start()
    logging.debug("LLM lifetimer started")


    messageHistory.append("""SYSTEM: Someone has
                          entered the room. Who
                          are they? What are they
                          doing here? Who the fuck
                          do you they think they are?""")

    response = llm.sendMessage(str(messageHistory))
    messageHistory.append(f"AGENT:{response}")

    print(response)
          
    while stop_llm is not False:

        userResponse = listen()
        if userResponse is not None:
            logging.debug(f"User response: {userResponse}")

            messageHistory.append(f'USER:{userResponse}')
            response = llm.sendMessage(str(messageHistory)) #send to llm
            messageHistory.append(response)

            print(response) #print llm response
            speak(response) #speak llm response
        else:
            logging.debug("returned none")
    time.sleep(1)


    logging.debug("LLM lifetimer ended")
        
run()