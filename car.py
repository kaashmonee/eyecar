import socket
import RPi.GPIO as GPIO
import time

MAX_SPEED = 100

motorPinLeft = 13
motorPinRight = 12
motorEnablePin = 25
motorInputPinLeft1 = 4
motorInputPinLeft2 = 17
motorInputPinRight1 = 27
motorInputPinRight2 = 22

speedLeft = MAX_SPEED / 2
speedRight = MAX_SPEED / 2

host = '192.168.43.252'
port = 5567

global left
global right
global turningLeft
turningLeft = False
global turningRight
turningRight = False
global reversing
reversing = False
global moving
moving = False

storedTime = time.time()

stopHammerTime = False

def setupPins():
    global left, right
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    #setup motor PWMs
    GPIO.setup(motorPinLeft, GPIO.OUT)
    GPIO.setup(motorPinRight, GPIO.OUT)
    GPIO.setup(motorEnablePin, GPIO.OUT)
    GPIO.output(motorEnablePin, GPIO.HIGH)

    #setup logic pins
    GPIO.setup(motorInputPinLeft1, GPIO.OUT)
    GPIO.setup(motorInputPinLeft2, GPIO.OUT)
    GPIO.setup(motorInputPinRight1, GPIO.OUT)
    GPIO.setup(motorInputPinRight2, GPIO.OUT)
       
    left = GPIO.PWM(motorPinLeft, 100)
    left.start(0)
    right = GPIO.PWM(motorPinRight, 100)
    right.start(0)

    setLogicPinsFwd()

def testMotors():
    global left, right
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    setLogicPinsFwd()

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s

def setupConnection(): #add handshake!!!
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def dataTransfer(conn):
    while True:
        data = conn.recv(1024) # receive the data
        data = str(data.decode('utf-8'))
        dataMessage = data.split(' ')
        command = int(dataMessage[0], 2)
        print(command)
        if command == 0b111:
            self_drive()
        elif command == 0b110:
            stop()
        elif command & 0b001 == 1: #turn right
            turn(0)
        elif command & 0b001 == 0: #turn left
            turn(2)
        elif command >> 1 & 0b001 == 1:
            setLogicPinsFwd()
        elif command >> 1 & 0b001 == 0:
            setLogicPinsBwd()
        else:
            stopHammerTime = True
        conn.sendall("sending".encode('utf-8'))
        break
        
def turn(direction):
    global left, right
    if direction == 0:
        speedLeft = 30
        speedRight = 70
    elif direction == 1:
        speedLeft = 60
        speedRight = 60
    else:
        speedLeft = 70
        speedRight = 30
    if moving:    
        right.ChangeDutyCycle(speedLeft)
        left.ChangeDutyCycle(speedRight)
        
def setLogicPinsFwd():
    GPIO.output(motorInputPinLeft1, GPIO.LOW)
    GPIO.output(motorInputPinRight2, GPIO.HIGH)
    GPIO.output(motorInputPinRight1, GPIO.LOW)
    GPIO.output(motorInputPinLeft2, GPIO.HIGH)

def setLogicPinsBwd():
    GPIO.output(motorInputPinLeft1, GPIO.HIGH)
    GPIO.output(motorInputPinRight2, GPIO.LOW)
    GPIO.output(motorInputPinRight1, GPIO.HIGH)
    GPIO.output(motorInputPinLeft2, GPIO.LOW)

setupPins()
s = setupServer()

#testMotors()
moving = False
#onDoubleBlink()

conn = setupConnection()
while not stopHammerTime:
    try:
        dataTransfer(conn)
    except Exception as e:
         print(e)
        
s.close()


