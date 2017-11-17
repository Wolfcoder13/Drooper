#!/usr/bin/env python
import time
from time import gmtime, strftime
from threading import Thread
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#import pyaudio
from pydub import AudioSegment
from pydub.playback import play

from DrumButton import DrumButton

class DrumpadService(object):
	#TODO: See if we should make this into a singleton class.

	def __init__(self):
		# TODO: need to verify these are the right numbers for the pins.
		# Software SPI configuration:
		self.CLK  = 18   #pin 12
		self.MISO = 23   #pin 16
		self.MOSI = 24   #pin 18
		self.CS   = 25   #pin 22
		self.CS2  = 7	#pin 26 
		self.mcp = Adafruit_MCP3008.MCP3008(clk=self.CLK, cs=self.CS, miso=self.MISO, mosi=self.MOSI)
		#make sure this works as second input
		self.mcp2 = Adafruit_MCP3008.MCP3008(clk=self.CLK, cs=self.CS2, miso=self.MISO, mosi=self.MOSI)
		
		self.drums = "Drums_0"
		
		self.listOfDrums = [0]*16
		self.initalizeDrums()

	# TODO: initialize drum sounds
	def initalizeDrums (self):
		#perhaps keep sounds in array
		for i in range(16):
			self.listOfDrums[i] = DrumButton("../Sounds/Drums/"+self.drums+"/sound"+str(i)+".wav")
			
	def changeDrums (self, Nr):
		self.drums = "Drums_"+str(Nr)
		self.initalizeDrums()
		
		
	#def changeDrums (self,pick):
		#load other drums, pick will chose frome selectable drums
		#change drum folder, and load new sounds.

	def playButton (self,buttonNr, volume):
		button = self.listOfDrums[buttonNr]
		if volume == 0:
			button.playing=False
		elif button.playing == False :
			button.playing = True
			t = Thread(target = button.playSound, args=(volume,))
			t.start()

	def getVolume (self,input):
		#calculates the volume from 10 bit input resolution (1023 values)
		#perhaps add more resolution.
		if input < 500:
			return 0
		elif input < 600:
			return 20
		elif input < 700:
			return 40
		elif input < 800:
			return 60
		elif input < 900:
			return 80
		return 100
		
	def gatherInput(self):
		pass
		
	def mainDrum(self):
		while True:
			for i in range(8):
				value = self.mcp.read_adc(i)
				#print(str(value))
				volume = self.getVolume(value)
				self.playButton(i, volume)
				
				value = self.mcp2.read_adc(i)
				#print(str(value))
				volume2 = self.getVolume(value)
				self.playButton(i+8, volume2)

			# Pause for some time
			time.sleep(0.05)
		
		

	# TODO: see if its possible to use interrupt, instead of constant polling of 
	# Drumpad loop. Should be run asynchronously
def main():
	service = DrumpadService()
	while True:
		for i in range(8):
			value = service.mcp.read_adc(i)
			#print(str(value))
			volume = service.getVolume(value)
			service.playButton(i, volume)
			
			value = service.mcp2.read_adc(i)
			#print(str(value))
			volume2 = service.getVolume(value)
			service.playButton(i+8, volume2)

		# Pause for some time
		time.sleep(0.05)
		
if __name__ == '__main__':main()