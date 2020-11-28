from NeuroUtils import NeuroUtils

if __name__ == '__main__':
    util = NeuroUtils()
    util.NewJsonBase(util.args["json"])
    util.ProcessPhotoByString(util.args["base"])