import argparse
from FaceDetector import FaceDetector
from FaceNet import FaceNet
from baseToJPG import Converter
from JsonReader import JsonReader
from numpy import linalg

class NeuroUtils:
    def __int__(self):
        self.argumentParser = argparse.ArgumentParser()
        self.argumentParser.add_argument('-b', "--base", type=str, required=True,
                                         help="base64 string")
        self.argumentParser.add_argument("-j","--json", type=str, required=True,
                                         help="path o required json")
        self.args = vars(self.argumentParser.parse_args())

        self.faceDetector = FaceDetector("res10_300x300_ssd_iter_140000.caffemodel", "FaceDetDeploy.prototxt")
        self.faceDetector.LoadNet()
        self.faceNet = FaceNet("facenet.h")
        self.faceNet.LoadNet()
        self.imgStrConverter = Converter()
        self.jsonReader = JsonReader()

        self.idsNBasesDict = dict()
        

    def ProcessPhotoByString(self, imageStr):
        image = self.imgStrConverter.stringToRGB(imageStr)
        box = self.faceDetector.Detect(image)[0]
        
        face = self.faceDetector.ExtractFace(image, box)
        
        encoding = self.faceNet.ForwardImgToEnc(face)   
        
        vkIdStr = self.FindMatch(encoding)     
        return vkIdStr

    def NewJsonBase(self, jsonPath):
        self.idsNBasesDict = self.jsonReader.ConstructDict(jsonPath=jsonPath)
        
    def FindMatch(self, encoding):
        matchId = None

        minEncDistance = 100

        for item in self.idsNBasesDict:
            encDistance = linalg.norm(self.imgStrConverter.stringToRGB(item['avatar']) - encoding)
            if encDistance < minEncDistance:
                minEncDistance = encDistance
                if(minEncDistance < 0.3):
                    matchId = item['vkId']

        return matchId


if __name__ == '__main__':
    util = NeuroUtils()
    util.NewJsonBase(util.args["json"])
    util.ProcessPhotoByString(util.args["base"])


    
    