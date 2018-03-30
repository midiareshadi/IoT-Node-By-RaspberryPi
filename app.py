from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import I2C_LCD_driver
from time import *
from time import sleep
import tm1637
from gpiozero import Buzzer
from gpiozero import MotionSensor

app = Flask(__name__)

##Character LCD instance
mylcd = I2C_LCD_driver.lcd()

def dhtfunc():
    print ("dhtfunc is running...")
    #DHT pin =CE1
    dhtpin=7 #(CE1)

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dhtpin, GPIO.IN)
    GPIO.cleanup()
    dhtdata=[]

    # Making instance
    instance = dht11.DHT11(dhtpin)

    #Reading from instance
    result = instance.read()
    if result.is_valid():
        dhtdata.append(result.temperature)
        dhtdata.append(result.humidity)
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % dhtdata[0])
        print("Humidity: %d %%" % dhtdata[1])
    return (dhtdata)


def pir():
    print("Enterin PIR function...")
    # Pin = PWM0 
    pirpin=12 #(PWM0)
    bzr=8 #(CE0)

    pir = MotionSensor(pirpin)
    
    buzzer = Buzzer(bzr)

    pir.wait_for_motion()
    buzzer.on()
    sleep(1)
    buzzer.off()

def main_call():
    DHTRetData=[]
    DHTRetData=(dhtfunc())

    ##Character LCD display 
    mylcd.lcd_display_string("Temperature: %d C" % DHTRetData[0], 1,0)
    mylcd.lcd_display_string("Humidity: %d %%" % DHTRetData[1], 2,0)

    # Pins  CLK: 15 (RXD)  DIO: 14 (TXD)
    Display = tm1637.TM1637(CLK=15, DIO=14, brightness=0)
    Display.SetBrightness(0)
    ### Basic Display Update:
    Display.Show1(0,DHTRetData[0]/10)
    Display.Show1(1,DHTRetData[0]%10)
    Display.Show1(2,DHTRetData[1]/10)
    Display.Show1(3,DHTRetData[1]%10)

    ##Print for return value checking
    print ("temp is= %d", DHTRetData[0])
    print ("Humidity is= %d %%", DHTRetData[1])


@app.route("/")
def index():
        dhtfuncsts='Disable'
        pirfuncsts='Disable'
              
        templateData = {
        'dhtsts'  : dhtfuncsts,
        'PIRsts'  : pirfuncsts,
         
        }
        return render_template('index.html', **templateData)
	
# The function below is executed when someone requests a URL with the actuator name and action in it:
@app.route("/<FuncName>")
def action(FuncName):
        a='disable'
        b='disable'
        if FuncName == 'dhtfunc':
         main_call()
         a = 'enable'
        if FuncName == 'PIRfunc':
	 pir()
         b = 'enable'

        dhtfuncsts=a
        pirfuncsts=b
        
	templateData = {
       'dhtsts'  : dhtfuncsts,
       'PIRsts'  : pirfuncsts,
	}
	return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

