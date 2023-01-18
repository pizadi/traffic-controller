import torch
import torchvision
import cv2
import time

import socketio



class PiCap:
    def __init__(self, cid=0, res=(1080, 1920)):
        self.model = torch.hub.load("yolov5", "custom", "./yolov5n6.pt", source="local")
        self.cap = cv2.VideoCapture(cid)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, res[0])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, res[1])
        self.classes = ["car", "truck", "bus"]

    def camproc(self):
        ret, frame = self.cap.read()
        if ret is None:
            raise ValueError()
        results = self.model(frame)
        df = results.pandas().xyxy[0]
        df = df[df["confidence"] > 0.5]
        cars = df[(df["name"].isin(self.classes))]
        return len(cars)

    def improc(self, img):
        image = cv2.imread(img)
        results = self.model(image)
        return results

def main():

    sio = socketio.Client()

    @sio.event
    def connect():
        print('connection established')

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://localhost:5000')

    picap = PiCap()
    while True:
        t = time.time()
        num_cars = picap.camproc()
        print(num_cars, time.time() - t)
        
        sio.emit('message', {'client_id': CLIENT_ID , 'num_cars': num_cars, 'time': t})
        print('sent')
        
        
if __name__ == "__main__":
    main()

