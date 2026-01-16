import json

def getConfigSettings(settings : list):
    """"""
    returnedSettings = []
    with open("config.json") as file:
        config = json.load(file)
        for setting in settings:
            returnedSettings.append(config[setting])

    return returnedSettings

a = getConfigSettings(["API_KEY"])
print(a)