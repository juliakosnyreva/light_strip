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

@app.route('/on/', methods=['GET'])
def rgbon():
	status = request.args.get('status')
	bright = request.args.get('bright')
	status1 = int(bright)
	if status == "on":
		colorWipe(strip, Color(status1,status1,status1), wait_ms=10)
	else:
		colorWipe(strip, Color(0,0,0), wait_ms=10)
		strip.show()	
	return status



	
@app.route('/red/', methods=['GET'])
def rgbred():
	status = request.args.get('status')
	bright = request.args.get('bright')
	status1 = int(bright)
	if status == "on":
		colorWipe(strip, Color(status1,0,0), wait_ms=10)
	else:
		colorWipe(strip, Color(0,0,0), wait_ms=10)
		strip.show()	
	return status
	
	
@app.route('/green/', methods=['GET'])
def rgbgreen():
	status = request.args.get('status')
	bright = request.args.get('bright')
	status1 = int(bright)
	if status == "on":
		colorWipe(strip, Color(0,status1,0), wait_ms=10)
	else:
		colorWipe(strip, Color(0,0,0), wait_ms=10)
		strip.show()	
	return status

@app.route('/blue/', methods=['GET'])
def rgbblue():
	status = request.args.get('status')
	bright = request.args.get('bright')
	status1 = int(bright)
	if status == "on":
		colorWipe(strip, Color(0,0,status1), wait_ms=10)
	else:
		colorWipe(strip, Color(0,0,0), wait_ms=10)
		strip.show()	
	return status

	   
blink_flag = False
threads = None
rainbow_flag = False
threadsrainbow = None

def blink_led():
    while blink_flag:
	    colorWipe(strip, Color(255,0,0), wait_ms=50)
	    colorWipe(strip, Color(0,255,0), wait_ms=50)
	    colorWipe(strip, Color(0,0,255), wait_ms=50)
	    
    colorWipe(strip, Color(0,0,0), wait_ms=10)
    strip.show()

def wheel(pos):
	if pos < 85:
	    return Color(pos*3,255-pos*3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255-pos*3, 0 ,pos*3)
	else:
		pos -= 170
		return Color(0, pos*3, 255 - pos*3)
	
def rainbow_cicle(wait):
	for j in range(256):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
			strip.show()
			time.sleep(wait/1000)
	
				
	

def rainbow():
	while rainbow_flag:
		rainbow_cicle(1)
	colorWipe(strip, Color(0,0,0), wait_ms=10)
	strip.show()
			    
@app.route('/rainbow/on', methods=['GET'])
def start_rainbow():
	global rainbow_flag, threads_rainbow
	if not rainbow_flag:
		rainbow_flag = True
		threadsrainbow = threading.Thread(target=rainbow)
		threadsrainbow.start()

	return "start rgb rainbow" 
	
@app.route('/rainbow/off', methods=['GET'])
def stop_rainbow():
	global rainbow_flag, threads_rainbow
	if rainbow_flag:
	    rainbow_flag = False
	    threadsrainbow.join()
	
	return "stop rgb rainbow"		

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
	if blink_flag:
	    blink_flag = False
	    threads.join()
	
	return "stop rgb blink"
	



if __name__ == "__main__":
   app.run()
