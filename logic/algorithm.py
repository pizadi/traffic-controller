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
from threading import *
# import RPi.GPIO as GPIO

sio = socketio.AsyncServer()
# sio.set('transports', ['xhr-polling'])
# app = socketio.WSGIApp(sio, static_files={
#     '/': {'content_type': 'text/html', 'filename': 'index.html'}
# })
from aiohttp import web
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
state = 0
sio.attach(app)
in_size = 4
map_led = {}
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

def set_lights(state):
  """
     G , Y , R , TG, TR
  C1 0 , 1 , 2 , 3 , 4
  C2 5 , 6 , 7 , 8 , 9
  C3 10, 11, 12, 13, 14
  C4 15, 16, 17, 18, 19
  """ 
  LED = [False] * 20
  
  if state == 0:
    LED[0] = True
    LED[3] = True
  elif state == 1:
    LED[0] = True
    LED[5] = True
  elif state == 2:
    LED[5] = True
    LED[1] = True
  elif state == 3:
    LED[5] = True
    LED[8] = True
  elif state == 4:
    LED[6] = True
  elif state == 5:
    LED[10] = True
    LED[13] = True
  elif state == 6:
    LED[10] = True
    LED[15] = True
  elif state == 7:
    LED[11] = True
    LED[15] = True
  elif state == 8:
    LED[15] = True
    LED[18] = True
  elif state == 9:
    LED[16] = True
  
  for i in range(4):
    LED[5*i+2] = not (LED[5*i] or LED[5*i+1])
    LED[5*i+4] = not LED[5*i+3]
  
  for i in range(20):
    GPIO.output(map_led[i], LED[i])

def change_state():
  @sio.event
  def connect():
      print('connection established')

  @sio.event
  def disconnect():
      print('disconnected from server')
  sio.connect('http://localhost:8081')
  while(True):
    b = 10
    horizental = camera_in[0] + camera_in[1]
    vertical  = camera_in[2] + camera_in[3]
    tot = horizental + vertical
    if state == 0: 
      t = b + camera_in[0]/tot
    elif state == 1:
      t = b + horizental/tot
    elif state == 3:
      t = b + camera_in[1]/tot
    elif state == 5:
      t = b + camera_in[2]/tot
    elif state == 6:
      t = b + vertical/tot
    elif state == 8:
      t = b + camera_in[3]/tot
    else:
      t = 5
    set_state(state)
    state = (state + 1) % 10
    time.sleep(t)
    

    
    sio.emit('light', {'LED': LED})
        

def run():
  web.run_app(app)

def main():
  WT = Thread(target = run)
  WT.start()
  WT.join()


  print("here")
  # GPIO.setmode(GPIO.BCM)
  
  for i in range(20):
    map_led[i] = i+5
    # GPIO.setup(map_led[i], GPIO.OUT)
  if in_size == 4:
    T = Thread(target = change_state, daemon = True)
    print(state)

if __name__ == '__main__':
  main()
    #  eventlet.wsgi.server(eventlet.listen(('', 5000)), app

    