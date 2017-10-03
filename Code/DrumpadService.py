#!/usr/bin/env python
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import pyaudio
from pydub import AudioSegment
from pydub.playback import play

from DrumButton import DrumButton

class DrumpadService(object):
	#TODO: See if we should make this into a singleton class.

	def __init__(self):
	# TODO: need to verify these are the right numbers for the pins.
	# Software SPI configuration:
	self.CLK  = 18
	self.MISO = 23
	self.MOSI = 24
	self.CS   = 25
	self.CS2  = 26	#check this pin
	self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
	#make sure this works as second input
	self.mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS2, miso=MISO, mosi=MOSI)
	
	self.listOfDrums = []

	# Hardware SPI configuration:
	# SPI_PORT   = 0
	# SPI_DEVICE = 0
	# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

	# TODO: initialize drum sounds
	def initalizeDrums (self):
		#perhaps keep sounds in array
		for i in range(16):
			self.listOfDrums[i] = DrumButton("/sound"+i+".wav")
		
		
	def changeDrums (self,pick):
		#load other drums, pick will chose frome selectable drums

	def playButton (self,buttonNr, volume):
		self.listOfDrums[buttonNr].playSound(volume)

	def getVolume (self,input):
		#calculates the volume from 10 bit input resolution (1023 values)
		#perhaps add more resolution.
		if input < 600:
			return 0
		else if input < 700:
			return 20
		else if input < 800:
			return 40
		else if input < 900:
			return 60
		else if input < 1000:
			return 80
		return 100
		
		

	# TODO: see if its possible to use interrupt, instead of constant polling of 
	# Drumpad loop. Should be run asynchronously
	def prototype(self):
		while True:
			for i in range(8):
				# The read_adc function will get the value of the specified channel (0-7).
				volume = getVolume(mcp.read_adc(i))
				volume2 = getVolume(mcp2.read_adc(i))
				if volume != 0:
					playButton(i, volume)
				if volume2 != 0:
					playButton(i+8, volume2)

			# Pause for half a second.
			time.sleep(0.01)
