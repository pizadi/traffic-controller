import pygame
import _thread
import time

import socketio
sio = socketio.AsyncServer()
# sio.set('transports', ['xhr-polling'])
# app = socketio.WSGIApp(sio, static_files={
#     '/': {'content_type': 'text/html', 'filename': 'index.html'}
# })
from aiohttp import web
app = web.Application()
map_colors = {'green': (51, 165, 50), 'yellow': (247, 181, 0), 'red': (187, 30, 16)} # Green Yellow Red 
rect, pol, cir = map_colors[0] * 4, map_colors[1] * 4, map_colors[2] * 4

def show_lcd():
	pygame.init()

	# Set up the drawing window
	screen = pygame.display.set_mode([480, 320])

	# Run until the user asks to quit
	running = True

	while running:

	    # Did the user click the window close button?
	    '''
	    for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    running = False
	    '''
	    
	    screen.fill((255, 255, 255))
	    
	    font = pygame.font.SysFont(None, 30)
	    s1 = font.render('Street number 1', True, 'white')
	    s2 = font.render('Street number 2', True, 'white')
	    s3 = font.render('Street number 3', True, 'white')
	    s4 = font.render('Street number 4', True, 'white')

	    pygame.draw.rect(screen, rect[0], pygame.Rect(29, 15, 180, 60))
	    pygame.draw.rect(screen, rect[1], pygame.Rect(29, 15 + 76, 180, 60))
	    pygame.draw.rect(screen, rect[2], pygame.Rect(29, 15 + 2 * 76, 180, 60))
	    pygame.draw.rect(screen, rect[3], pygame.Rect(29, 15 + 3 * 76, 180, 60))
	    
	    pygame.draw.polygon(screen, pol[0], ((239, 45), (272, 15), (272, 30), (339, 30), (339, 60), (272, 60), (272, 75)))
	    pygame.draw.polygon(screen, pol[0], ((239, 45 + 76), (272, 15 + 76), (272, 30 + 76), (339, 30 + 76), (339, 60 + 76), (272, 60 + 76), (272, 75 + 76)))
	    pygame.draw.polygon(screen, pol[0], ((239, 45 + 2 * 76), (272, 15 + 2 * 76), (272, 30 + 2 * 76), (339, 30 + 2 * 76), (339, 60 + 2 * 76), (272, 60 + 2 * 76), (272, 75 + 2 * 76)))
	    pygame.draw.polygon(screen, pol[0], ((239, 45 + 3 * 76), (272, 15 + 3 * 76), (272, 30 + 3 * 76), (339, 30 + 3 * 76), (339, 60 + 3 * 76), (272, 60 + 3 * 76), (272, 75 + 3 * 76)))
	    
	    pygame.draw.circle(screen, cir[0], (404, 45), 30)
	    pygame.draw.circle(screen, cir[0], (404, 45 + 76), 30)
	    pygame.draw.circle(screen, cir[0], (404, 45 + 2 * 76), 30)
	    pygame.draw.circle(screen, cir[0], (404, 45 + 3 * 76), 30)
	    
	    screen.blit(s1, (43, 34))
	    screen.blit(s2, (43, 34 + 76))
	    screen.blit(s3, (43, 34 + 2 * 76))
	    screen.blit(s4, (43, 34 + 3 * 76))
	    
	    #pygame.draw.line(screen, (0, 0, 0), (239, 0), (239, 319), width = 2)
	    #pygame.draw.polygon(screen, 'red', ((0, 100), (100, 0), (100, 50), (300, 50), (300, 150), (100, 150), (100, 200)))
	    #pygame.draw.circle(screen, (0, 0, 255), (0, 0), 75)

	    pygame.display.flip()

	#pygame.quit()
	
#show_lcd()

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.on('light')
def my_message(sid, light):
  lights = light['LED']
  for i in range(4):
    if lights[i*5+0]:
      cir[i] = map_colors['green'] 
    elif lights[i*5+1]:
      cir[i] = map_colors['yellow']
    else:
      cir[i] = map_colors['red']
    if lights[i*5+3]:
      pol[i] = map_colors['green']
    else:
      pol[i] = map_colors['red'] 

  return "OK", 200

@sio.on('*')
def error(sid, data):
  print(data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

def main():
  _thread.start_new_thread(show_lcd, ())
  time.sleep(5)
  rect, pol, cir = ['red'] * 4, ['blue'] * 4, ['green'] * 4
  time.sleep(5)
  rect, pol, cir = ['green'] * 4, ['red'] * 4, ['blue'] * 4
  time.sleep(5)
  rect, pol, cir = ['blue'] * 4, ['green'] * 4, ['red'] * 4
  sio = socketio.Client()
  

  web.run_app(app, port=8081)
  

  picap = PiCap()
  while True:
      t = time.time()
      num_cars = picap.camproc()
      print(num_cars, time.time() - t)
      
      sio.emit('lights', {'client_id': CLIENT_ID , 'num_cars': num_cars, 'time': t})
      print('sent')
        
        
if __name__ == "__main__":
    main()


input()