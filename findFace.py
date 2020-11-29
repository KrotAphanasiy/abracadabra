try:
 from NeuroUtils import NeuroUtils
 import json
except:
 print("Error")

if __name__ == '__main__':
    util = NeuroUtils()
    util.NewJsonBase("vkUsers.json")
    ans = util.ProcessPhotoByString(util.args["base"])
    print(ans)
        