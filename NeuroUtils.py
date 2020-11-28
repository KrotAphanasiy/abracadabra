import argparse
from FaceDetector import FaceDetector
from FaceNet import FaceNet
from baseToJPG import Converter

class NeuroUtils:
    def __int__(self):
        self.argumentParser = argparse.ArgumentParser()
        self.argumentParser.add_argument("-u", "--photo-url", type=str, required=True,
                                         help="url to photo")
        self.argumentParser.add_argument("-j","--json", type=str, required=True,
                                         help="path o required json")


        self.faceDetector = FaceDetector("res10_300x300_ssd_iter_140000.caffemodel", "FaceDetDeploy.prototxt")
        self.faceDetector.LoadNet()
        
        self.faceNet = FaceNet("facenet.h")

        self.faceNet.LoadNet()
    
        self.imgStrConverter = Converter()

    def ProcessPhotoByString(self, imageStr):
        encoding = self.faceNet.ForwardImgToEnc(self.imgStrConverter.DecodeToNp(imageStr))
        
        
        
        


    
    