import json

def getConfigSettings(settings : list):
    """"""
    returnedSettings = []
    with open("src\\config.json") as file:
        config = json.load(file)
        for setting in settings:

            returnedSettings.append(config[setting])

    return returnedSettings

one = getConfigSettings(["CAMERA_DIGITS"])

for each in one[0]:
    print(each)
            
