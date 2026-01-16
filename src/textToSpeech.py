
import os
from openai import OpenAI
import simpleaudio as sa
import vlc
import time
import re
<<<<<<< HEAD
import json

def getConfigSettings(settings : list):
    """"""
    returnedSettings = []
    with open("config.json") as file:
        config = json.load(file)
        for setting in settings:
            returnedSettings.append(config[setting])

    return returnedSettings
=======
>>>>>>> e7fdc7d830628fdaff9933a47fd6885a027529de

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

def run(text_to_speak):
    if type(text_to_speak) == str:
<<<<<<< HEAD
    
        client = OpenAI()  # The client now picks up the key from the environment
        speech_file_path = "speech.wav"
=======
        os.environ["OPENAI_API_KEY"] = ""
    
        client = OpenAI()  # The client now picks up the key from the environment
        speech_file_path = "C:\\Users\\sampo\\Downloads\\OpenCV Things\\src\\speech.wav"
>>>>>>> e7fdc7d830628fdaff9933a47fd6885a027529de
    
        instructions, clean_text = split_stage_direction(text_to_speak)
        print(f'INSTRUCT: {instructions} {clean_text}')
    
    
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=clean_text,
            instructions=instructions
        ) as response:
            response.stream_to_file(speech_file_path)
    
        player = vlc.MediaPlayer(str(speech_file_path))
        player.play()
        while player.get_state() != vlc.State.Ended:
            time.sleep(0.1)

#run("*angry* get out of here")
