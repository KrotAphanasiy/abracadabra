import numpy as np
import cv2

class FaceDetector:
    def __init__(self, dnnPath, protoPath):
        self.dnnPath = dnnPath
        self.protoPath = protoPath
        self.net = None

    def LoadNet(self):
        self.net = cv2.dnn.readNetFromCaffe(self.protoPath, self.dnnPath)

    def Detect(self, image):
        (W, H) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 0.007843, (W, H), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        boundingBoxes = []

        for i in np.arange(0, detections.shape[2]):

            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                boundingBoxes.append(box)

        return boundingBoxes
    
    @staticmethod
    def ExtractFace(image, boundingBox):
        (startX, startY, endX, endY) = boundingBox
        return image[startY:endY, startX:endX]
  
