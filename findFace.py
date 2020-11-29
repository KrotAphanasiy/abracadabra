print("Hello")
try:
 from NeuroUtils import NeuroUtils
 import json
 print("Imported")
except:
 print("Error")

if __name__ == '__main__':
    print("300 bucks\n")
    util = NeuroUtils()
    util.NewJsonBase(util.args["json"])
    ans = util.ProcessPhotoByString(util.args["base"])
    with open(jsonPath, 'w') as jsonFile:
        json.dumps(ans, jsonFile)
        