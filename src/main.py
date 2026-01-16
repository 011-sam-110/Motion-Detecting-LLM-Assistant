#from src import speechToText
from email import message
import json
import logging
import logging
import subprocess
import threading
import time
from queue import Queue
#import llm
import newllm
import textToSpeech
from detectFace import detect_face
import time
from queue import Queue
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
LLM_LIFETIME = 60 * 2
def getConfigSettings(settings : list):
    """"""
    returnedSettings = []
    with open("config.json") as file:
        config = json.load(file)
        for setting in settings:
            print(setting)
            returnedSettings.append(config[setting])

    return returnedSettings

LLM_LIFETIME = getConfigSettings(["LLM_LIFETIME"])

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
                messageHistory.append("SYSTEM: user is ignoring you")
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
