import socket
import RPi.GPIO as GPIO
import time

host = '192.168.43.252'
port = 5567


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
        print(dataMessage) #an array of commands and parameters, separated by ' '
        # Send the reply back to the client
        conn.sendall(reply.encode('utf-8'))
        print(reply)
        print("Data has been sent!")
        break
s = setupServer()
conn = setupConnection()
while not stopHammerTime:
    try:
        dataTransfer(conn)
    except Exception as e:
         print(e)

s.close()
