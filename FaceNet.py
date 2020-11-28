from FaceNetCustoms import *
from fr_utils import *
from keras.models import load_model

import cv2

class FaceNet:
    def __int__(self):
        self.model = None
        
    def LoadNet(self):
        self.model = load_model('facenet_keras.h5', compile=False)
           
    def ForwardImgToEnc(self, imageNpArr):
        encoding = get_embedding(self.model, imageNpArr)
        return encoding


a = FaceNet()
a.LoadNet()
print("loaded model")
image = cv2.imread("Vlad.jpg")
emb = a.ForwardImgToEnc(image)
print(emb)