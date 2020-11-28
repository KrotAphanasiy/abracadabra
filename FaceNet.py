from FaceNetCustoms import *
from fr_utils import *
from tensorflow.keras.models import load_model
class FaceNet:
    def __int__(self, h5Path):
        self.model = load_model(h5Path, custom_objects={'triplet_loss':triplet_loss})

            
    def ForwardImgToEnc(self, imageNpArr):
        encoding = img_to_encoding(imageNpArr, self.model)
        return encoding
