
# Drowsiness detection for TartanHacks inspired by Adrian Rosebrock
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
import sys
import os
import pyglet
# import gi
# import simpleaudio as sa
# import wave
# import pygame
from playsound import playsound
# import pyaudio
# import wave


class Detector(object):

    LANDMARK_DETECTOR = "./assets/shape_predictor_68_face_landmarks.dat"
    ALARM_SOUND_PATH = "./assets/alarm.wav"
<<<<<<< HEAD

=======
    
>>>>>>> d58cfd0c06ca0ad8597a867d1b07523f377426db

    EYE_ASP_RAT_THRESHOLD = 0.3
    EYE_CLOSED_CONSEC_FRAMES = 20


    def __init__(self):
        # counts the number of frames that have passed since eyes closed
        self.counter = 0
        # initial status of alarm = off
        self.alarmOn = False
        # initializes the detector which detects faces
        self.detector = dlib.get_frontal_face_detector()
        # initializes the facial landmarks predictor
        self.predictor = dlib.shape_predictor(Detector.LANDMARK_DETECTOR)
        # starts the video capture using the webcam (param 0)
        self.cap = cv2.VideoCapture(0)

        # waveRead = wave.open(Detector.ALARM_SOUND_PATH, "rb")
        # self.wavObj = sa.WaveObject.from_wave_read(waveRead)
        # self.wavObj = sa.WaveObject.from_wave_file(Detector.ALARM_SOUND_PATH)
        # print("CWD:", os.getcwd())
        # pygame.mixer.init()
        # pygame.mixer.music.load(Detector.ALARM_SOUND_PATH)



    def soundAlarm(self):
        # plays an alarm sound
        # playsound.playsound(Detector.ALARM_SOUND_PATH)
        # os.system("aplay ~/Documents/eyecar/assets/Airhorn-SoundBible.com-975027544.wav")
        # self.stream = self.audioDriver.open(format=self.audioDriver()
        # self.playObject = self.wavObj.play()
        # self.playObject.wait_done()
        # pygame.mixer.music.play()
        playsound(Detector.ALARM_SOUND_PATH)

    # def stopAlarm(self):
        # self.playObject.stop()


    def eyeAspectRatio(self, eye):
        # compute the euclidean distances between the
        # two sets of vertical landmarks for eyes
        # print("eye", eye)
        # list of coordinates that are numpy arrays that contain important
        # featuers of each eye

        # calculates the euclidean distance (distance) between two vertical
        # points
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])      # print("Shape type: ", shape)

        # compute the distance between the horizontal eye landmark
        # calculates horizontal euclidean distance
        C = dist.euclidean(eye[0], eye[3])
        # this returns the aspect ratio from
        ear = (A + B) / (2.0 * C)

        return ear

    def getEyeLandmarks(self):
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        # print("lStart", lStart, "lEnd", lEnd)
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        # starting and ending indices of the landmakrs for the features
        # that represent the right eye and the left eye
        return EyeLandmark((lStart, lEnd), (rStart, rEnd))


    def detectDrowsiness(self):

        while True:

            ret, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)
            # self.frame = imutils.resize(self.frame, width=250)
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # converts from color to grayscale

            # detects faces in grayscale form
            self.rects = self.detector(self.gray, 0)
            # print("Type rects:", self.rects)

            for rect in self.rects:
                # determines the facial landmakrs for the face region,
                # converts the facial (x,y) coordinates to a numpy array
                shape = self.predictor(self.gray, rect)
                # print("shape type: ", shape)
                shape = face_utils.shape_to_np(shape)
                eyes = self.getEyeLandmarks()
                # Left and right eye is the coordinates of the left eye that the
                # eye aspect ratio function uses.
                leftEye = shape[eyes.leftEye()[0] : eyes.leftEye()[1]]
                rightEye = shape[eyes.rightEye()[0] : eyes.rightEye()[1]]
                # print("right eye", rightEye)
                # calculates the eye aspect ratio of each eye

                leftEAR = self.eyeAspectRatio(leftEye)
                rightEAR = self.eyeAspectRatio(rightEye)

                ear = (leftEAR + rightEAR) / 2.0

                self.drawEyes(leftEye, rightEye)
                self.detectSleepy(ear)

            cv2.imshow("frame", self.frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                sys.exit(0)

            print("Loop terminates")


    def drawEyes(self, leftEye, rightEye):
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(self.frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(self.frame, [rightEyeHull], -1, (0, 255, 0), 1)

    def detectSleepy(self, ear):
        # function to determine if the person is actually drowsy or not
        # if the aspect ratio of the eyes closed is smaller than the necessary
        # threshold
        if ear < Detector.EYE_ASP_RAT_THRESHOLD:
            self.counter += 1

            if self.counter >= Detector.EYE_CLOSED_CONSEC_FRAMES:
                # turns on the alarm if alarm is not true
                alarmOn = True if not self.alarmOn else False

                # starting a new thread to turn on the alarm sound
                alarmThread = Thread(target=self.soundAlarm)
                alarmThread.daemon = True
                alarmThread.start()

                # alerting the user that there is some drowsiness on
                # the screen
                cv2.putText(self.frame, "fuckface you are drowsy", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                cv2.putText(self.frame, "EAR: {:.2f}".format(ear), (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        else:
            self.counter = 0
            self.alarmOn = False






class EyeLandmark(object):

    def __init__(self, leftTuple, rightTuple):

        self.leftTuple = leftTuple
        self.rightTuple = rightTuple

    def rightEye(self):
        return self.rightTuple

    def leftEye(self):
        return self.leftTuple


def main():
    print(os.getcwd())
    d = Detector()
    d.detectDrowsiness()

if __name__ == "__main__":
    main()
