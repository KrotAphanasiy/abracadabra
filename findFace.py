from NeuroUtils import NeuroUtils
import json

if __name__ == '__main__':
    util = NeuroUtils()
    util.NewJsonBase(util.args["json"])
    ans = util.ProcessPhotoByString(util.args["base"])
    with open(jsonPath, 'w') as jsonFile:
        json.dumps(ans, jsonFile)