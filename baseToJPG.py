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
        """imgdata = base64.b64decode(str(base64_string))
        image = Image.open(io.BytesIO(imgdata))"""

        with open("imageToSave.png", "wb") as fh:
            """fh.write(base64.decodebytes(bytes(base64_string, encoding='utf-8')))"""
            png_recovered = base64.decodestring(bytes(base64_string, encoding="utf-8"))
            fh.write(png_recovered)

        image = cv.imread("imageToSave.png")
        """cv.imshow("Searching", image)
        cv.waitKey()"""
        return image
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