import argparse
from FaceDetector import FaceDetector
from FaceNet import FaceNet
from baseToJPG import Converter
from JsonReader import JsonReader
from numpy import linalg
from numpy import expand_dims
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer

class NeuroUtils:
    def __init__(self):
        self.argumentParser = argparse.ArgumentParser()
        self.argumentParser.add_argument('-b', "--base", type=str, required=True,
                                         help="base64 string")
        self.argumentParser.add_argument("-o", "--output", required=True,
                                         help="path to output json")
        self.args = vars(self.argumentParser.parse_args())
        self.faceDetector = FaceDetector("res10_300x300_ssd_iter_140000.caffemodel", "FaceDetDeploy.prototxt")
        self.faceDetector.LoadNet()
        self.faceNet = FaceNet()
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
        return str(vkIdStr)


    def NewJsonBase(self, jsonPath):
        self.idsNBasesDict = self.jsonReader.ConstructDict(jsonPath=jsonPath)
        
    def FindMatch(self, encoding):
        matchId = None

        minEncDistance = 100

        for item in self.idsNBasesDict:
            itemEnc = self.faceNet.ForwardImgToEnc(self.imgStrConverter.stringToRGB(item['avatar']))
            encDistance = linalg.norm(itemEnc - encoding)
            if encDistance < minEncDistance:
                minEncDistance = encDistance
                if(minEncDistance < 0.3):
                    matchId = item['vkId']

        return matchId

    def FindMatchSVM(self, encoding):
        matchId = None

        inEncoder = Normalizer(norm="l2")
        outEncoder = LabelEncoder()

        embeddings = []
        labels = []
        for item in self.idsNBasesDict:
            itemEnc = self.faceNet.ForwardImgToEnc(self.imgStrConverter.stringToRGB(item['avatar']))
            embeddings.append(itemEnc)

            itemLabel = item['vkId']
            labels.append(itemLabel)

        embeddings = inEncoder.transform(embeddings)
        outEncoder.fit(labels)
        labels = outEncoder.transform(labels)
        svc = SVC(kernel='linear', probability=True)
        svc.fit(embeddings, labels)



        toPredictOn = expand_dims(encoding, axis=0)
        yhatClass = svc.predict(toPredictOn)
        yhatProb = svc.predict(toPredictOn)

        if yhatProb > 0.65:
            matchId = outEncoder.inverse_transform(yhatClass)

        return matchId



