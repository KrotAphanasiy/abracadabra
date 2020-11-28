from base64 import decodestring
from base64 import encodestring
import base64
import io
from PIL import Image
import numpy as np
import cv2 as cv

class Converter:
    def __int__(self):
        pass

    def stringToRGB(self, base64_string):
        imgdata = base64.b64decode(str(base64_string))
        image = Image.open(io.BytesIO(imgdata))
        return cv.cvtColor(np.array(image), cv.COLOR_BGR2RGB)

"""
    ###DEBUGGING####
    def TestToShow(self, path):
        file = open(path, 'r')
        for line in file:
            print(line)
            image = self.stringToRGB(line)
            
            cv.imshow("test", image)

            cv.waitKey()

conv = Converter()
conv.TestToShow("base64.txt")
"""