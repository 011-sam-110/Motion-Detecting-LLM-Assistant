
import json
import os
import re
import time
from datetime import datetime

import simpleaudio as sa
import vlc
from colorama import Fore, Style, init
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

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

def getConfigSettings(settings : list):
    """"""
    returnedSettings = []
    with open("config.json") as file:
        config = json.load(file)
        for setting in settings:
            returnedSettings.append(config[setting])

    return returnedSettings

def split_stage_direction(text: str):
    """
    Splits text into stage direction (inside *) and the spoken text.
    Returns a tuple: (stage_direction, spoken_text)
    """
    # Look for text between asterisks at the start
    match = re.match(r'^\*(.*?)\*\s*(.*)', text)
    if match:
        stage_direction = match.group(1).strip()
        spoken_text = match.group(2).strip()
        return stage_direction, spoken_text
    else:
        # No asterisks found, return None for stage direction
        return None, text.strip()

  # comma unpacks single element list



def run(text_to_speak):
    if type(text_to_speak) == str:
        
        
        client = OpenAI()  # The client now picks up the key from the environment
        speech_file_path = "speech.wav"
    
        given_instructions, clean_text = split_stage_direction(text_to_speak)
        log(f"{text_to_speak}", "AGENT", "TextToSpeech/run")
    
    
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="coral",
            input=clean_text,
            instructions=f"Speak in a {given_instructions} tone"
        ) as response:
            response.stream_to_file(speech_file_path)
    
        player = vlc.MediaPlayer(str(speech_file_path))
        player.play()
        while player.get_state() != vlc.State.Ended:
            time.sleep(0.1)

#run("*angry* get out of here")
