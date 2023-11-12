from flask import Flask
from gpiozero import LED
from flask import Flask, render_template, request
from rpi_ws281x import Adafruit_NeoPixel
from rpi_ws281x import Color
import time
import threading

LED_COUNT = 10
LED_PIN = 10
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 255
LED_INVERT = False


app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello!!"


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)

strip.begin()


def colorWipe(strip, color, wait_ms=50):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

@app.route('/index')
def main():
	return render_template('index.html')

@app.route('/on/<status>', methods=['GET'])
def rgbon(status):
	if status == "on":
		colorWipe(strip, Color(255,255,255), wait_ms=10)
	else:
		colorWipe(strip, Color(0,0,0), wait_ms=10)
	return status


@app.route('/red/<status>', methods=['GET'])
def rgbred(status):
	if status == "on":
		colorWipe(strip, Color(255,0,0), wait_ms=10)
	else:
		colorWipe(strip, Color(0,0,0), wait_ms=10)
	return status
	
	
@app.route('/green/<status>', methods=['GET'])
def rgbgreen(status):
	if status == "on":
		colorWipe(strip, Color(0,255,0), wait_ms=10)
	else:
		colorWipe(strip, Color(0,0,0), wait_ms=10)
	return status

@app.route('/blue/<status>', methods=['GET'])
def rgbblue(status):
	if status == "on":
		colorWipe(strip, Color(0,0,255), wait_ms=10)
	else:
		colorWipe(strip, Color(0,0,0), wait_ms=10)
	return status


def blink_led():
    while blink_flag:
	    colorWipe(strip, Color(255,0,0), wait_ms=50)
	    colorWipe(strip, Color(0,255,0), wait_ms=50)
	    colorWipe(strip, Color(0,0,255), wait_ms=50)

		
	 
	   
blink_flag =False
threads = None


@app.route('/action/on', methods=['GET'])
def start_blink():
	global blink_flag, threads
	if not blink_flag:
		
		blink_flag = True
		threads = threading.Thread(target=blink_led)
		threads.start()
		
	
		
	return "start rgb blink" 
	
@app.route('/action/off', methods=['GET'])
def stop_blink():
	global blink_flag, threads
	blink_flag = False
	threads.join()
	colorWipe(strip, Color(0,0,0), wait_ms=10)
	strip.show()
	return "stop rgb blink"
	
		

if __name__ == "__main__":
   app.run()
