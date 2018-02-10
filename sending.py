import socket
from time import sleep
from time import time
host = '192.168.43.252'
port = 5566


def setup():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((host, port))
  print("Connected to " + host)
  return sock

def transmit(message):
  global s
  if s is not None:
    send(s, message)
    return "Sent " + message

def send(s, message):
    s.send(str.encode(message))
    s.close()
    return

global s
s = setup()

while True:
    message = input()
    transmit(message)
