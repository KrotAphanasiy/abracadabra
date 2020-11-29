try:
 from NeuroUtils import NeuroUtils
 import json
except:
 print("Error")


util = NeuroUtils()
with open("D:/PyCharmProjects/abracadabra/venv/nodeBack/arg.json", "r") as file:
    tempD = json.load(file)
    util.imageStr = tempD["photo"]

util.NewJsonBase("C:/vkUsers.json")
ans = util.ProcessPhotoByString(util.imageStr)
print(ans)
        