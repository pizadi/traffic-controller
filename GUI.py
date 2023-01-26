#!/usr/bin/python3
import pygame
import threadin
import time

import socketio
sio = socketio.AsyncServer()
# sio.set('transports', ['xhr-polling'])
# app = socketio.WSGIApp(sio, static_files={
#     '/': {'content_type': 'text/html', 'filename': 'index.html'}
# })
from aiohttp import web
app = web.Application()
map_colors = {'white': (255, 255, 255), 'green': (51, 165, 50), 'yellow': (247, 181, 0), 'red': (187, 30, 16)} # Green Yellow Red 
rect, pol, cir = map_colors[0] * 4, map_colors[1] * 4, map_colors[2] * 4
sleep_time = 2
LED = []
def show_lcd():
	pygame.init()

	# Set up the drawing window
	screen = pygame.display.set_mode([480, 320], pygame.FULLSCREEN)

	# Run until the user asks to quit
	running = 2

	while running > 0:

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				running -= 1

    screen.fill((255, 255, 255))
	    
		font = pygame.font.SysFont(None, 30)
		s1 = font.render('Street number 1', True, map_colors['white'])
		s2 = font.render('Street number 2', True, map_colors['white'])
		s3 = font.render('Street number 3', True, map_colors['white'])
		s4 = font.render('Street number 4', True, map_colors['white'])

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


	pygame.quit()
	
#show_lcd()

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')


def cb(t, light):
  lights = light
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


@sio.event
def disconnect(sid):
    print('disconnect ', sid)

def main():
  t = threading.Thread(target=show_lcd)
  t.start()
  time.sleep(5)
  rect, pol, cir = ['red'] * 4, ['blue'] * 4, ['green'] * 4
  time.sleep(5)
  rect, pol, cir = ['green'] * 4, ['red'] * 4, ['blue'] * 4
  time.sleep(5)
  rect, pol, cir = ['blue'] * 4, ['green'] * 4, ['red'] * 4
  sio = socketio.Client()

  sio = socketio.Client()
  sio.connect('http://localhost:8080')
  

  picap = PiCap()
  while True:
      t = time.time()
      num_cars = picap.camproc()
      print(num_cars, time.time() - t)
      
      sio.emit('light', {'client_id': CLIENT_ID}, callback=cb)
      time.sleep(sleep_time)
      print('sent')
  t.join()
        
        
if __name__ == "__main__":
    main()

