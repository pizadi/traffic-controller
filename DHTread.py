import Adafruit_DHT

class sensor():
    def __init__(self, pin = 4):
        self.sensor = Adafruit_DHT.AM2302
        self.pin = pin

    def read(self):
        return Adafruit_DHT.read_retry(self.sensor, self.pin)
        
