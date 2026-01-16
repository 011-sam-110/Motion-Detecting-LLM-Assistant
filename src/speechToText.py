import speech_recognition as sr
from queue import Queue
from colorama import Fore, Style, init
from datetime import datetime

# Logs
def log(message: str, level: str = "INFO", function_name: str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    colors = {
        "INFO": Fore.CYAN,
        "SUCCESS": Fore.GREEN,
        "AGENT": Fore.YELLOW,
        "ERROR": Fore.RED,
        "DEBUG": Fore.MAGENTA,
    }

    color = colors.get(level.upper(), Fore.WHITE)
    level = level.upper()

    print(f"{Fore.WHITE}[{timestamp}] "
          f"{color}[{level}]  [@{function_name}] "
          f"{Style.RESET_ALL}{message}")


class SpeechToText:
    def __init__(self, language='en-US'):
        """
        Initialize the speech recognizer and set the language.
        """
        log("Speach To Text initialised", "Success", "SpeechToText")
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
            log("Listening for user...", "INFO", "SpeechToText/listen_from_mic")
            
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
    text = stt.listen_from_mic()
    if text:
        q.put(text)
    else:
        q.put(None)
