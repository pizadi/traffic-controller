# from socket import *

# client = socket(AF_INET, SOCK_STREAM)
# client.connect(("127.0.0.1", 1173))

# name = str(input("Name : "))
# client.send(bytes(name, 'ascii'))

# data = client.recv(1024)
# data = str(data, 'ascii')
# print(data)

import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established 2')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

def cb(m, d):
  print( m, d)


sio.connect('http://localhost:8080')
print('hello')
sio.emit('camera', {'id': 0, 'status': 300}, callback=cb)
print('sent')
import time
time.sleep(0.1)
sio.disconnect()