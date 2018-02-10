
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

    EYE_ASP_RAT_THRESHOLD = 0.3
    EYE_CLOSED_CONSEC_FRAMES = 48


    ALARM_SOUND_PATH = "path"
    def __init__(self):
        self.counter = 0
        self.alarmOn = False
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(Detector.LANDMARK_DETECTOR)
        self.cap = cv2.VideoCapture(0)


    def soundAlarm(self):
        # plays an alarm sound
        playsound.playsound(Detector.ALARM_SOUND_PATH)
        
    def eyeAspectRatio(self, eye):
        # compute the euclidean distances between the 
        # two sets of vertical landmarks for eyes
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the distance between the horizontal eye landmark
        C = dist.euclidean(eye[0], eye[3])
        # this returns the aspect ratio from 
        ear = (A + B) / (2.0 * C)

        return ear

    def getEyeLandmarks(self):
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        print("lStart", lStart, "lEnd", lEnd)
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        return EyeLandmark((lStart, lEnd), (rStart, rEnd))

    
    def detectDrowsiness(self):
        while True:
            ret, self.frame = self.cap.read() 
            # self.frame = imutils.resize(self.frame, width=250)
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("black and white", self.frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

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
                print("left eye", leftEye) 
                rightEye = shape[eyes.rightEye()[0] : eyes.rightEye()[1]]
                print("right eye", rightEye)
                # calculates the eye aspect ratio of each eye
                self.drawEyes(leftEye, rightEye)
                print("Getting here") 
                leftEAR = self.eyeAspectRatio(leftEye)
                rightEAR = self.eyeAspectRatio(rightEye)

                ear = (leftEAR + rightEAR) / 2.0

    def drawEyes(self, leftEye, rightEye):
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        print("leftEyeHull", leftEyeHull)
        print("rightEyeHull", rightEyeHull)
        cv2.drawContours(self.frame, leftEyeHull, -1, (0, 255, 0), 1)
        cv2.drawContours(self.frame, rightEyeHull, -1, (0, 255, 0), 1)



                # print("Shape type: ", shape)


class EyeLandmark(object):

    def __init__(self, leftTuple, rightTuple):
        
        self.leftTuple = leftTuple
        self.rightTuple = rightTuple

    def rightEye(self):
        return self.rightTuple
    
    def leftEye(self):
        return self.leftTuple
        

def main():
    d = Detector()
    d.detectDrowsiness()

if __name__ == "__main__":
    main()