import socket
host = '192.168.43.252'
port = 5567


def sendReceive(s, message):
    s.send(str.encode(message))
    return 

def setup():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((host, port))
  return sock

def transmit(message):
  global s
  if s is not None:
    response = sendReceive(s, message)
    return response


global s
s = setup()

while True:
    message = input()
    print(transmit(message))
