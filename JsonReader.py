import json

class JsonReader:
    def __int__(self):
        pass

    def ConstructDict(self, jsonPath):
        with open('vkUsers.json') as jsonFile:
            return json.load(jsonFile)



unit = JsonReader()
dict = unit.ConstructDict("example.json")
print(dict)