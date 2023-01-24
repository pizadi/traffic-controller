# import json
# from socket import *
# import _thread

# count = 0
# traffic = [0]*4
# def other_crossroad(client):
#   data = client.recv(1024).decode()
#   print(data)
#   # y = json.loads()
#   client.send(bytes(str("hello {}".format(data)), 'ascii'))

# if __name__ == "__main__":

#   server = socket(AF_INET, SOCK_STREAM)
#   server.bind(("127.0.0.1", 1173))
#   server.listen(5)

#   while True:
#     print("Server is listening")
#     client, addr = server.accept()
#     count = count + 1

#     if count == 5:
#         client.send(bytes("Server Is Busy !!", 'ascii'))

#         client.close()
#         count = count - 1
#     else:
#         _thread.start_new_thread(other_crossroad, (client,))




import eventlet
import socketio

sio = socketio.AsyncServer()
# sio.set('transports', ['xhr-polling'])
# app = socketio.WSGIApp(sio, static_files={
#     '/': {'content_type': 'text/html', 'filename': 'index.html'}
# })
from aiohttp import web
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)
in_size = 4
light_status = [None] * in_size
humidity = 30
camera_in = [None] * in_size
neighbor_in = [None] * in_size

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.on('camera')
def my_message(sid, data):
  camera_in[data['client_id']] = data['num_cars']
  print('message ', data)
  return "OK", 20

@sio.on('neighbor')
def my_message(sid, data):
  light_status[light['id']] = light['status']
  print('message ', data)
  return "OK", 20

@sio.on('humidity')
def my_message(sid, h):
  humidity = h
  print('message ', h)
  return "OK", 200

@sio.on('light')
def my_message(sid, light):
  light_status[light['id']] = light['status']
  print('message ', light)
  return "OK", 200

@sio.on('*')
def error(sid, data):
  print(data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    #  eventlet.wsgi.server(eventlet.listen(('', 5000)), app
  web.run_app(app)

  if in_size == 4:
    horizental = camera_in[0] + camera_in[2]
    vertical  = camera_in[1] + camera_in[3]
    if horizental > vertical: 
      set_status()
      sleep_time = 20 + horizental//vertical
    