import RPi.GPIO as GPIO
import threading  
GPIO.setmode(GPIO.BCM)  

class ButtonStuff:
	def __init__(self):
		GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
		GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.boolean = True
		self.doStuff()
		
	  
	# now we'll define the threaded callback function  
	# this will run in another thread when our event is detected  
	def my_callback(self):   
		# we need to run this in new thread, so current thread finishes execution and the interrupt event queue can continue
		t1 = threading.Thread(target=self.thread1)
		t1.start()
			
	def thread1(self):
		while self.boolean:
			print("lala")
			
	def my_callback2(self):
		self.boolean = not self.boolean
		print("button2")
	
	def doStuff(self):
		print("Make sure you have a button connected so that when pressed") 
		print("it will connect GPIO port 23 (pin 16) to GND (pin 6)\n")
		print("You will also need a second button connected so that when pressed")
		print("it will connect GPIO port 24 (pin 18) to 3V3 (pin 1)")
		# raw_input("Press Enter when ready\n>")  
		  
		# The GPIO.add_event_detect() line below set things up so that  
		# when a rising edge is detected on port 24, regardless of whatever   
		# else is happening in the program, the function "my_callback" will be run  
		# It will happen even while the program is waiting for  
		# a falling edge on the other button.  
		GPIO.add_event_detect(27, GPIO.RISING, callback=lambda x: self.my_callback())
		GPIO.add_event_detect(22, GPIO.RISING, callback=lambda x: self.my_callback2())
		# GPIO.add_event_detect(22, GPIO.FALLING, callback=lambda x: self.my_callback(), bouncetime=300)
		# GPIO.add_event_detect(self.LOOPBUTTON2, GPIO.FALLING, callback=lambda x: self.loopButton(1), bouncetime=300)
		# GPIO.add_event_detect(self.LOOPBUTTON3, GPIO.FALLING, callback=lambda x: self.loopButton(2), bouncetime=300)		
		  
		try:  
			print("Waiting for falling edge on port 23")
			GPIO.wait_for_edge(17, GPIO.FALLING)  
			print ("Falling edge detected. Here endeth the second lesson.")
		  
		except KeyboardInterrupt:  
			GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
		GPIO.cleanup()           # clean up GPIO on normal exit  
	
def main(): 
	bt = ButtonStuff()


		
if __name__ == '__main__':main()