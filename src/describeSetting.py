

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


def describe_setting(img_path : str):

    client = OpenAI()

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

    print(response.output_text)
    return response.output_text
