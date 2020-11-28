import json

class JsonReader:
    def __int__(self):
        pass

    def ConstructDict(self, jsonPath):
        return json.load(jsonPath)



unit = JsonReader()
dict = unit.ConstructDict("example.json")
print(dict)