# speech_to_text.py
import speech_recognition as sr
import logging
from queue import Queue

# Logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class SpeechToText:
    def __init__(self, language='en-US'):
        """
        Initialize the speech recognizer and set the language.
        """
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen_from_mic(self, timeout=10, phrase_time_limit=10):
        """
        Capture audio from the microphone and convert it to text.
        
        :param timeout: Maximum time to wait for a phrase (in seconds)
        :param phrase_time_limit: Maximum duration of a phrase (in seconds)
        :return: Recognized text or None
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3) #issue
            print("Listening...")
            logging.debug("TTS active")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio, language=self.language)
                return text
            except sr.WaitTimeoutError:
                x = 1
            except sr.UnknownValueError:
                x=  1
            except sr.RequestError as e:
                x = 1
        return None

def runSpeechToText(q: Queue): #returns if anything is gathered
    stt = SpeechToText()
    print("at run speech to text")
    text = stt.listen_from_mic()
    if text:
        q.put(text)
    else:
        q.put(None)
