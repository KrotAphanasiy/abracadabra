import tensorflow as tf
import glob
import numpy as np
import cv2
import os
from keras import backend as K
from keras.models import load_model
from fr_utils import *
from inception_blocks_v2 import *
from keras.preprocessing.image import img_to_array

K.set_image_data_format('channels_first')

FRmodel = faceRecoModel(input_shape=(3, 96, 96))
FRmodel.compile(optimizer='adam', loss=triplet_loss, metrics=['accuracy'])
load_weights_from_FaceNet(FRmodel, "facenet_weights")

FRmodel.save("facenet.h5")
