#!/usr/bin/python3
# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
from hx711 import HX711
import Adafruit_DHT
import urllib2



DEBUG = 1
# Setup the pins we are connect to
#RCpin = 24
DHTpin = 4
hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6,
            channel='A',
            gain=64
        )
		
#Setup API and delay for Thingspeak channel
myAPI = "B6IYS9WQIKAEPJTL"
myDelay = 15 #seconds between posting data

GPIO.setmode(GPIO.BCM)
#GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    
    #Convert from Celius to Farenheit
    TWF = 9/5*TW+32
   
    # return dict
    return (str(RHW), str(TW),str(TWF))

def getWeight():
	hx711.reset()   #Reset the HX711
	#Then Weigh
	WW = hx711.get_raw_data(num_measures=3)
	return (str(WW))
	
#def RCtime(RCpin):
#    LT = 0
#    if (GPIO.input(RCpin) == True):
#        LT += 1
#    return (str(LT))
# main() function

def main():
    
    print ('starting...')
	#URL + API Key
    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print (baseURL)
    
    while True:
        try:
            RHW, TW, TWF = getSensorData()
			WW = getWeight()
            #LT = RCtime(RCpin)
            f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s&field3=%s&field4=%s" % (TW, TWF, RHW, WW))
            print (f.read())
            print (TW + " " + TWF+ " " + RHW)
            f.close()
            sleep(int(myDelay))
        except:
			GPIO.cleanup()
            print ('exiting.')
            break

# call main
if __name__ == '__main__':
    main()
