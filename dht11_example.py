import RPi.GPIO as GPIO
import dht11
import time
import datetime

def dhtfunc():
    print ("dhtfunc is running...")
    #DHT pin =CE1
    dhtpin=7 #(CE1)
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # read data using pin 7
    instance = dht11.DHT11(dhtpin)

    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %d C" % result.temperature)
            print("Humidity: %d %%" % result.humidity)
        time.sleep(1)

dhtfunc()
