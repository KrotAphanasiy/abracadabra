import json

class JsonReader:
    def __int__(self):
        pass

    def ConstructDict(self, jsonPath):
        with open(jsonPath) as jsonFile:
            return json.load(jsonFile)


