import tensorflow as tf
import glob
import numpy as np
import cv2
import os
import threading

from time import sleep

from IController import *
from keras import backend as K
from keras.models import load_model
from fr_utils import *
from inception_blocks_v2 import *
from keras.preprocessing.image import img_to_array
from concurrent.futures import Future

def call_with_future(fn, future, args, kwargs):
    try:
        result = fn(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)


def threaded(fn):
    def wrapper(*args, **kwargs):
        future = Future()
        threading.Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future

    return wrapper


class Record:
    def __init__(self):
        self.id = None
        self.label = None
        self.gender = None
        self.counter = None


class Recognizer:

    def __init__(self):
        K.set_image_data_format('channels_first')
        self.__LVmodel = None
        self.__GDmodel = None
        self.__FDmodel = None
        self.__FRmodel = None
        self.__identity_db = None
        self.__video_stream = None
        self.__cam_id = None
        self.__PADDING_FROM_FACE = 10
        self.__ready_to_detect_identity = True

        self.__to_pass_counter = 0
        self.__frames_toResponse_counter = 0
        self.__record_counter = 0
        self.__prev_labels = []

        self.__recognized_identity = None
        self.__recognized_identity_gender = None
        self.__recognized_identity_encoding = None

        self.__in_process_encoding = None

        self.__way = Way()

        self.__TEXT_COLOR = (0, 0, 255)


    # загружаем все модельки, нужные для работы
    def load_models(self, liveness_model_path, gender_model_path, FDmodel_path):
        try:
            print("[RECOGNIZER INFO] loading liveness detection model... ")
            self.__LVmodel = load_model(liveness_model_path)
            print("Done!\n")
            print("[RECOGNIZER INFO] loading gender detection model... ")
            self.__GDmodel = tf.keras.models.load_model(gender_model_path)
            print("Done!\n")
            print("[RECOGNIZER INFO] loading face detection model... ")
            self.__FDmodel = cv2.dnn.readNetFromCaffe(os.path.sep.join([FDmodel_path, "deploy.prototxt"]),
                                                      os.path.sep.join(
                                                          [FDmodel_path, "res10_300x300_ssd_iter_140000.caffemodel"]))
            print("Done!\n")
            print("[RECOGNIZER INFO] loading FaceNet, this may take a while... ")
            self.__FRmodel = tf.keras.models.load_model("facenet.h5", custom_objects={'triplet_loss':triplet_loss})
            print("Done!\n")
        except Exception as exc:
            print("Oops..! Looks like something went wrong while loading models... : ", exc)

    # готовим базу для фэйснета, разделенную на мужчин и женщин
    def prep_identityDB(self, identity_db_path):
        print("[RECOGNIZER INFO] loading faces db... ")
        try:
            self.__identity_db = [{}, {}]

            for file in glob.glob(identity_db_path + "/men/*"):
                identity = os.path.splitext(os.path.basename(file))[0]
                self.__identity_db[0][identity] = img_path_to_encoding(file, self.__FRmodel)
                print(self.__identity_db[0][identity])

            for file in glob.glob(identity_db_path + "/women/*"):
                identity = os.path.splitext(os.path.basename(file))[0]
                self.__identity_db[1][identity] = img_path_to_encoding(file, self.__FRmodel)
            print("Done!\n")
        except Exception as exc:
            print("Oops..! Looks like something went wrong while loading database... : ", exc)

    # запуск распознавания
    def start_recognizer(self, cam_id):
        self.__cam_id = cam_id

        print("[RECOGNIZER INFO] starting recognition on cam {}\n".format(self.__cam_id))

        self.__cam_id = cam_id
        self.__video_stream = cv2.VideoCapture(self.__cam_id)
        win_name = "Casting " + str(self.__cam_id)

        print("Done!\n")

        while self.__video_stream.isOpened():
            _, frame = self.__video_stream.read()

            try:
                processed_frame = self.__process_frame(frame)
            except Exception as exc:
                processed_frame = cv2.putText(frame, str(exc), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)
                print(exc)

            # ТУТ МОЖЕТ ДОБАВИТЬСЯ ЛИБО ВЫВОД КАДРА В ПОТОК, ЛИБО
            # НЕПОСРЕДСТВЕННО В ТКИНТЕР (НУ ИЛИ КУДА-ТО ЕЩЕ, МНЕ НЕ СКАЗАЛИ ПОКА)

            cv2.imshow(win_name, processed_frame)

            ####################################################################

            key = cv2.waitKey(100)
            if key == 27:
                break

        cv2.destroyWindow("Casting" + str(self.__cam_id))

    # обработка кадра
    def __process_frame(self, frame):
        (frame_h, frame_w) = frame.shape[:2]
        FDblob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        self.__FDmodel.setInput(FDblob)
        FDdetections = self.__FDmodel.forward()

        for i in range(0, FDdetections.shape[2]):
            FDconfidence = FDdetections[0, 0, i, 2]

            if FDconfidence > 0.52:
                FDbox = FDdetections[0, 0, i, 3:7] * np.array([frame_w, frame_h, frame_w, frame_h])
                (startX, startY, endX, endY) = FDbox.astype("int")
                (startX, startY, endX, endY) = self.__adj_face_edjes((startX, startY, endX, endY), frame_w, frame_h)

                face = frame[startY:endY, startX:endX]

                if not self.__check_relative_area((startX, startY, endX, endY), frame_w, frame_h):
                    continue
                elif self.__ready_to_detect_identity:

                    face_forLV = self.__prep_forLV(face)

                    LVpredictions = self.__LVmodel.predict(face_forLV)[0]
                    LVlabel = np.argmax(LVpredictions)

                    if LVlabel:
                        frame = self.emph_object(frame, (startX, startY, endX, endY), (0, 255, 0))

                        face_forGD = self.__prep_forGD(face)

                        GDpredictions = self.__GDmodel.predict(face_forGD)[0]
                        GDlabel = np.argmax(GDpredictions)

                        (ensured, identity, gender, current_encoding) = self.__ensure(face, GDlabel)

                        same_person = False

                        same_in_process = False

                        try:
                            dist = np.linalg.norm(self.__recognized_identity_encoding - current_encoding)
                        except:
                            dist = 10


                        if (self.__recognized_identity is not None) and (dist <= 0.1) and (self.__recognized_identity_gender == GDlabel):
                            same_person = True

                        if not ensured:
                            if self.__in_process_encoding is None:
                                self.__in_process_encoding = current_encoding

                            if np.linalg.norm(self.__in_process_encoding - current_encoding) <= 0.1:
                                same_in_process = True
                            else:
                                self.__in_process_encoding = current_encoding
                        else:
                            self.__in_process_encoding = None
                            same_in_process = True


                        if not same_in_process:
                            self.__frames_toResponse_counter = 0
                            self.__record_counter = 0
                            self.__prev_labels.clear()


                        if not same_person:
                            self.__recognized_identity = identity
                            self.__recognized_identity_gender = gender
                            self.__recognized_identity_encoding = current_encoding
                            self.__TEXT_COLOR = (0, 0, 255)

                        #print("{} {} {}".format(same_person, self.__recognized_identity_gender, GDlabel))

                        if same_person and self.__to_pass_counter > 0:
                            self.__to_pass_counter -= 1
                            if self.__recognized_identity_gender == 1:
                                cv2.putText(frame, self.__recognized_identity + ", female", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, self.__TEXT_COLOR, thickness=2)
                            else:
                                cv2.putText(frame, self.__recognized_identity + ", male", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, self.__TEXT_COLOR, thickness=2)
                        else:
                            if ensured:
                                    if self.__recognized_identity is not "unknown":
                                        self.__process_identity(self.__recognized_identity)
                                        self.__TEXT_COLOR = (0, 255, 0)

                                    #debugging
                                    if self.__recognized_identity_gender == 1:
                                        cv2.putText(frame, self.__recognized_identity + ", female", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, self.__TEXT_COLOR, thickness=2)
                                    else:
                                        cv2.putText(frame, self.__recognized_identity + ", male", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, self.__TEXT_COLOR, thickness=2)
                                    ##########
                            else:
                                cv2.putText(frame, "recognizing...", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)
                            self.__to_pass_counter = 100
                    else:
                        frame = self.emph_object(frame, (startX, startY, endX, endY), (0, 0, 255))
                else:
                    frame = self.emph_object(frame, (startX, startY, endX, endY), (100, 100, 100))
        return frame

    # идентифицирует личность в течение 10 кадров
    def __ensure(self, image, GDlabel):
        if self.__frames_toResponse_counter is 0:
            record = Record()

            (record.label, current_encoding) = self.__recognize_identity(image, self.__identity_db[GDlabel], self.__FRmodel)

            if record.label is not None:

                record.counter = 1
                record.id = self.__record_counter
                record.gender = GDlabel
                self.__record_counter += 1
                self.__prev_labels.append(record)

            self.__frames_toResponse_counter += 1

            return False, None, GDlabel, current_encoding
        elif self.__frames_toResponse_counter < 15:

            (label, current_encoding) = self.__recognize_identity(image, self.__identity_db[GDlabel], self.__FRmodel)

            if label is not None:

                found = False

                for record in self.__prev_labels:
                    if record.label is label:
                        record.counter += 1
                        found = True

                if not found:
                    record = Record()
                    record.id = self.__record_counter
                    self.__record_counter += 1
                    record.label = label
                    record.counter = 1
                    record.gender = GDlabel
                    self.__prev_labels.append(record)

            self.__frames_toResponse_counter += 1

            return False, None, GDlabel, current_encoding
        else:
            self.__frames_toResponse_counter = 0

            (label, current_encoding) = self.__recognize_identity(image, self.__identity_db[GDlabel], self.__FRmodel)

            if len(self.__prev_labels) > 0:
                max_counter = 0
                rec_index = None

                for record in self.__prev_labels:
                    if record.counter > max_counter:
                        max_counter = record.counter
                        rec_index = record.id

                if max_counter > 4:
                    identity = self.__prev_labels[rec_index].label
                else:
                    identity = "unknown"
                gender = self.__prev_labels[rec_index].gender
                self.__prev_labels.clear()
                self.__record_counter = 0
                return True, identity, gender, current_encoding
            else:
                identity = "unknown"
                self.__record_counter = 0
                return True, identity, GDlabel, current_encoding

    def __adj_face_edjes(self, box, w, h):
        (startX, startY, endX, endY) = box

        startX = startX - self.__PADDING_FROM_FACE
        startY = startY - self.__PADDING_FROM_FACE
        endX = endX + self.__PADDING_FROM_FACE
        endY = endY + self.__PADDING_FROM_FACE

        startX = max(0, startX)
        startY = max(0, startY)
        endX = min(w, endX)
        endY = min(h, endY)

        box = (startX, startY, endX, endY)

        return box

    # распознать личность
    @staticmethod
    def __recognize_identity(image, database, model):
        encoding = img_to_encoding(image, model)

        min_dist = 100
        identity = None

        for (name, db_enc) in database.items():

            dist = np.linalg.norm(db_enc - encoding)

            # If this distance is less than the min_dist, then set min_dist to dist, and identity to name
            if dist < min_dist:
                min_dist = dist
                identity = name

        if min_dist > 0.13:
            return None, encoding
        else:
            return str(identity), encoding

    # обработать личность на вход-выход, открыть турникет
    def __process_identity(self, identity):
        self.__ready_to_detect_identity = False
        # TO DO#
        self.open_way()
        self.__ready_to_detect_identity = True

    # открыть турникет
    @threaded
    def open_way(self):
        # TO DO #
        self.__way.open()
        sleep(2)
        self.__way.close()


    # подготовка для liveness модели
    @staticmethod
    def __prep_forLV(img):
        img = cv2.resize(img, (32, 32))
        img = img.astype("float") / 255.0
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = np.transpose(img, (0, 2, 3, 1))
        return img

    @staticmethod
    # подготовка для gender модели
    def __prep_forGD(img):
        img = cv2.resize(img, (96, 96))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = img.astype("float")
        img[0] = img[0] / 179
        img[1] = img[1] / 255
        img[2] = img[2] / 255
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = np.transpose(img, (0, 2, 3, 1))
        return img

    @staticmethod
    def emph_object(img, box, color):
        (startX, startY, endX, endY) = box

        cv2.line(img, (startX, startY), (startX, startY + 25), color, 2)
        cv2.line(img, (startX, startY), (startX + 25, startY), color, 2)
        cv2.line(img, (endX, startY), (endX - 25, startY), color, 2)
        cv2.line(img, (endX, startY), (endX, startY + 25), color, 2)
        cv2.line(img, (endX, endY), (endX - 25, endY), color, 2)
        cv2.line(img, (endX, endY), (endX, endY - 25), color, 2)
        cv2.line(img, (startX, endY), (startX, endY - 25), color, 2)
        cv2.line(img, (startX, endY), (startX + 25, endY), color, 2)

        return img

    @staticmethod
    def __check_relative_area(box, w, h):
        (startX, startY, endX, endY) = box
        area = w * h
        rel_area = (endX - startX) * (endY - startY)

        if rel_area / area > 0.05:
            return True
        else:
            return False