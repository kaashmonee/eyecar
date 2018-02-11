import pygame
import socket
from time import sleep
from time import time
import math
import cv2
import urllib.request
import numpy as np
import sys
import threading
import time
import detect_drowsiness

carhost = '192.168.43.252'
port = 5566

class DetectDrowsy(object):
    def __init__(self, width=500, height=500):
        self.drowsy = False
        self.angle = 0
        self.auton = False
        self.width = width
        self.height = height
        self.frameRate = 5
        self.done = False
        self.image = []
        self.detector = detect_drowsiness.Detector()
        self.imageData = {"image": None, "framesElapsed": 0}
        self.camera = cv2.VideoCapture(0)
        self.threshold = 0

    def timerFired(self):

        host = "192.168.43.149:8080/shot.jpg"
        # host = "128.237.136.203:8080/shot.jpg"

        if len(sys.argv)>1:
            host = sys.argv[1]

        # for streaming video
        url = 'http://' + host
        imgResp = urllib.request.urlopen(url)

        # Numpy to convert into a array
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        # Finally decode the array to OpenCV usable format ;)
        img = cv2.imdecode(imgNp,-1)
        # put the image on screen
        self.image = img

        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.flip(self.image, 1)
        self.image = np.rot90(self.image)
        self.image = pygame.surfarray.make_surface(self.image)


        # for monitoring the user
        ret, self.frame = self.camera.read()
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.imageData["image"] = self.frame
        self.imageData['framesElapsed'] += 1

        data = self.detector.detectDrowsiness(self.imageData)
        try:
            self.imageData["image"] = data[1]
            self.drowsy = data[0]
        except:
            pass

        if self.drowsy:
            self.imageData['framesElapsed'] = 0
            print("drowsy")
            transmit('stop')

        self.frame = self.frame[0:1000, 310:910]
        self.frame = cv2.resize(self.frame, (180, 240), interpolation = cv2.INTER_LINEAR)
        self.frame = np.rot90(self.frame)
        self.frame = pygame.surfarray.make_surface(self.frame)

        pygame.display.flip()
        time.sleep(0.001)
        # Quit if q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.done = True

    def redrawAll(self, screen):
        screen.fill([0,0,0])

        # pygame.draw.rect(screen, (192, 192, 192), (self.width * .07, self.height * .82, self.width * .03,self.height * .05))
        screen.blit(self.image, (0,0))
        if self.done == True: return
        color = (0, 100, 100)

        if self.frame != None:
            screen.blit(self.frame, (self.width * .75,self.height * .05))

        path = "images/steering.png"
        image = pygame.transform.scale(pygame.image.load(path),(720, 720))  # rotate
        theta = self.angle * math.pi/180
        screen.blit(self.rot_center(image, self.angle),
            (self.width*.13,
            self.height*.53))

        if self.drowsy or self.threshold % 12000 != 0:
            self.threshold += pygame.time.Clock().get_time() + 1000
            message = "YOU ARE SLEEPY! YOU WILL STOP DRIVING!"
            text = pygame.font.SysFont('monospace', 40).render(message, 1,(255, 0, 0))
            screen.blit(text, (self.width * .07, self.height * .1))

    def keyPressed(self, keyCode, modifier):
        if not self.drowsy and not self.threshold % 12000 != 0:
            if keyCode == pygame.K_LEFT and self.angle < 60:
                self.angle += 10
                transmit("left")
            elif keyCode == pygame.K_RIGHT and self.angle > -60:
                self.angle -= 10
                transmit("right")
            elif keyCode == pygame.K_UP:
                transmit("forward")
            elif keyCode == pygame.K_DOWN:
                transmit("back")
            elif keyCode == pygame.K_SPACE:
                transmit("stop")

    def rot_center(self,image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def mousePressed(self, x, y):
        pass

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        self.done = False
        while not self.done:
            time = clock.tick(self.frameRate)

            self.timerFired()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePressed(*(event.pos))
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()

def setup():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((carhost, port))
  print("Connected to " + carhost)
  return sock

def transmit(message):
  global s
  if s is not None:
    send(s, message)
    return "Sent " + message

def send(s, message):
    s.send(str.encode(message))
    return

def main():
    global s
    s = setup()
    drive = DetectDrowsy(960, 720)
    drive.run()

if __name__ == '__main__':
    main()
