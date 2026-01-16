from datetime import datetime
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

def describe_setting(img_path : str):
    log("Connecting to OpenAI API...", "info", "describeSetting/describe_setting")
    client = OpenAI()
    log("Connected to OpenAI API...", "success", "describeSetting/describe_setting")

    # Function to create a file with the Files API
    def create_file(img_path):
      with open(img_path, "rb") as file_content:
        result = client.files.create(
            file=file_content,
            purpose="vision",
        )
        return result.id

    # Getting the file ID
    file_id = create_file(img_path)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Who can you see in this image? what are they wearing? what colors are their clothes? briefly describe the scene"},
                {
                    "type": "input_image",
                    "file_id": file_id,
                },
            ],
        }],
    )

    log("Captured setting, returning setting", "success", "describeSetting/describe_setting")
    return response.output_text
