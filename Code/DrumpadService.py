#!/usr/bin/env python
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import pyaudio
from pydub import AudioSegment
from pydub.playback import play



#TODO: See if we should make this into a singleton class.

# TODO: need to verify these are the right numbers for the pins.
# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
CS2  = 26	#check this pin
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
#make sure this works as second input
mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS2, miso=MISO, mosi=MOSI)



# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# TODO: initialize drum sounds
def initalizeDrums ():
	#perhaps keep sounds in array
	
def changeDrums (pick):
	#load other drums, pick will chose frome selectable drums

def playSound (button_nr, volume):
	converted_volume = *0.2(-100+volume)
	play(song-converted_volume)) #song minus volume will decrese the songs volume by converted_volume desibels

def getVolume (input):
	#calculates the volume from 10 bit input resolution (1023 values)
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
def prototype:
	while True:
		for i in range(8):
			# The read_adc function will get the value of the specified channel (0-7).
			volume = getVolume(mcp.read_adc(i))
			volume2 = getVolume(mcp2.read_adc(i))
			if volume != 0:
				playSound(i, volume)
			if volume2 != 0:
				playSound(i+8, volume2)

		# Pause for half a second.
		time.sleep(0.01)
