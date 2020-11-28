from base64 import decodestring
from base64 import encodestring
from PIL import Image
import numpy as np

class Converter:
    def __int__(self):
        pass

    def DecodeToNp(self, imagestr):
        image = Image.fromstring('RGB',(400,400),decodestring(imagestr))
        toReturn = np.array(image)
        return toReturn

    def Encode(self):
        pass