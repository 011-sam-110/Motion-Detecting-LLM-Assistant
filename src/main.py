#from src import speechToText
import json
import logging
import subprocess
import threading
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

# Config
LLM_LIFETIME = 60 * 2


def timer_():
    global stop_llm

    for i in range(LLM_LIFETIME):
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
    response = llm.sendMessage(str(messageHistory))
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


    messageHistory.append("""SYSTEM: Someone has
                          entered the room. Who
                          are they? What are they
                          doing here? Who the fuck
                          do you they think they are?""")

    response = newllm.sendMessage(str(messageHistory))
    messageHistory.append(f"AGENT:{response}")

    textToSpeech.run(response)
          
    while stop_llm is False:
        print("beginning to listen")
        userResponse = listen()
        if userResponse is not None:
            logging.debug(f"User response: {userResponse}")

            messageHistory.append(f'USER:{userResponse}')
            response = newllm.sendMessage(str(messageHistory)) #send to llm
            messageHistory.append(response)

            print(response) #print llm response
            textToSpeech.run(response) #speak llm response
        
        else:
            logging.debug("returned none")
    time.sleep(1)


    logging.debug("LLM lifetimer ended")
        

while True:
    run()