import Adafruit_DHT
import time
import socketio
class Sensor():
    def __init__(self, pin = 4):
        self.sensor = Adafruit_DHT.AM2302
        self.pin = pin

    def read(self):
        return Adafruit_DHT.read_retry(self.sensor, self.pin)


def main():

    sio = socketio.Client()

    @sio.event
    def connect():
        print('connection established')

    @sio.event
    def disconnect():
        print('disconnected from server')

    sio.connect('http://localhost:8080')

    sensor = Sensor()
    while True:
        humidity, temperature = sensor.read()
        sio.emit('humidity', {'humidity': humidity, 'temperature': temperature})
        time.sleep(5)
        print('sent')
        
        
if __name__ == "__main__":
    main()

        
