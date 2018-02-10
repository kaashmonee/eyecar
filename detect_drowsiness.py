# Drowsiness detection Adrian Rosebrock
# importing necessary packages

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils

from threading import Thread
import numpy as np
import playsound
import argparse

import imutils
import time
import dlib
import cv2


class Detector(object):

    LANDMARK_DETECTOR = "./assets/shape_predictor_68_face_landmarks.dat"

    ALARM_SOUND_PATH = "path"
    def __init__(self):
        pass

    def sound_alarm(self):
        # plays an alarm sound
        playsound.playsound(Detector.ALARM_SOUND_PATH)
        

        



    