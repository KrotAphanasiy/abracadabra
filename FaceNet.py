from FaceNetCustoms import *
from fr_utils import *
from tensorflow.keras.models import load_model

class FaceNet:
    def __int__(self):
        self.model = None
        
    def LoadNet(self):
        self.model = load_model("facenet.h5", custom_objects={'triplet_loss': triplet_loss})
           
    def ForwardImgToEnc(self, imageNpArr):
        encoding = img_to_encoding(imageNpArr, self.model)
        return encoding

