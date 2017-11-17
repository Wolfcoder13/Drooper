import RPi.GPIO as GPIO
import pyaudio
import wave
import numpy
import threading
import time
import logging
import math
import os
import sys


import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from LoopChannel import LoopChannel
from RecordChannel import RecordChannel
from functools import reduce

# os.close(sys.stderr.fileno())

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
					
GPIO.setmode(GPIO.BCM)

CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 #sample rate
		

class LoopService:
	def __init__(self):
		
		# for gathering volume and pan input
		self.CLK  = 18   #pin 12
		self.MISO = 23   #pin 16
		self.MOSI = 24   #pin 18
		self.CS   = 5    #pin 29
		self.CS2  = 6    #pin 31
		self.mcp  = Adafruit_MCP3008.MCP3008(clk=self.CLK, cs=self.CS , miso=self.MISO, mosi=self.MOSI)
		self.mcp2 = Adafruit_MCP3008.MCP3008(clk=self.CLK, cs=self.CS2, miso=self.MISO, mosi=self.MOSI)
		
		self.RECBUTTON   = 4	#pin 7 on board
		self.LOOPBUTTON1 = 17	#pin 11 on board
		self.LOOPBUTTON2 = 27	#pin 13 on board
		self.LOOPBUTTON3 = 10	#pin 19 on board
		self.LOOPBUTTON4 = 9	#pin 21 on board
		self.LOOPBUTTON5 = 11	#pin 23 on board
		self.listOfLoopButtonId = [self.LOOPBUTTON1, self.LOOPBUTTON2, self.LOOPBUTTON3,
								   self.LOOPBUTTON4, self.LOOPBUTTON5]
		
		# loopLength will be used to make sure all loop clips are of the same length or merge-able length
		# It has the length of the longest loop out of all the channels
		self.loopLength = 0
		
		# current frame position with respect to loop length and mix play
		self.currentFramePosition = 0
		
		self.startSong = False
		self.numberOfLoopChannels = 5
		self.listOfLoopChannels = [0]*self.numberOfLoopChannels
		self.recordChannel = RecordChannel()
		self.initializeChannels()
		self.initializeButtons()
		
		#when this is true, then if you press a loop channel button, it will record on it instead of playing it.
		#self.record = False
		
		
		#for testing
		#self.playLoop()
		
		# self.listOfLoopChannels[0].setWave('drums.wav')
		# self.listOfLoopChannels[0].switchLoop()
		# self.listOfLoopChannels[1].setWave('lead.wav')
		# self.listOfLoopChannels[1].switchLoop()
		# self.listOfLoopChannels[2].setWave('pads.wav')
		# self.listOfLoopChannels[2].switchLoop()
		self.loop = True
		# self.playMixed()
		
		
	# Fills our list of loop channels with empty LoopChannel objects	
	def initializeChannels(self):
		print("Initializing Each loop channel")
		for i in range(self.numberOfLoopChannels):
			self.listOfLoopChannels[i] = LoopChannel()
	
	
	# Adds interrupts for each hardware button.
	def initializeButtons(self):
		#Consider using busy waiting... interrupts are causing us pain
		print("Initializing Interups for buttons")
		
		GPIO.setup(self.RECBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
		for i in range(self.numberOfLoopChannels):
			GPIO.setup(self.listOfLoopButtonId[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)  

		
		GPIO.add_event_detect(self.RECBUTTON,   GPIO.RISING, callback=lambda x: self.record(),      bouncetime=300)
		GPIO.add_event_detect(self.LOOPBUTTON1, GPIO.RISING, callback=lambda x: self.loopButton(0), bouncetime=300)
		GPIO.add_event_detect(self.LOOPBUTTON2, GPIO.RISING, callback=lambda x: self.loopButton(1), bouncetime=300)
		GPIO.add_event_detect(self.LOOPBUTTON3, GPIO.RISING, callback=lambda x: self.loopButton(2), bouncetime=300)
		GPIO.add_event_detect(self.LOOPBUTTON4, GPIO.RISING, callback=lambda x: self.loopButton(3), bouncetime=300)
		GPIO.add_event_detect(self.LOOPBUTTON5, GPIO.RISING, callback=lambda x: self.loopButton(4), bouncetime=300)
		

	# Simply flips a boolean value in recordChannel, which is used to determine whether or not to record or not when you press a channel button
	def record(self):
		self.recordChannel.switchRecord()
		logging.debug('record')
		
	# calls the loop function in a new thread, so callback queue can be handled without too much delay
	def loopButton(self, index):
		logging.debug('loopButton'+str(index))
		# We need to start a new thread to allow other interrupt routines in the queue to be executed
		t1 = threading.Thread(target=self.loopFunction, args=(index,))
		t1.start()
			
	# loop function records, or turns on a loop channel, depending on the isRecording boolean variable in recordChannel.
	def loopFunction(self, index):
		logging.debug('loopButton'+str(index))
		if not self.startSong and self.recordChannel.isRecording():
			# I think this part is fully implemented
			self.recordChannel.firstRecording()
			self.listOfLoopChannels[index].setWave("record.wav")
			self.listOfLoopChannels[index].setFrameCount(self.recordChannel.getFrameCount)
			self.loopLength = self.recordChannel.getFrameCount()
			self.listOfLoopChannels[index].switchLoop()
			self.startSong = True
		elif self.recordChannel.isRecording():
			if self.listOfLoopChannels[index].getFrameCount() == 0:
				#here we havent recorded anything on this channel
				logging.debug('IF1')
				self.recordChannel.recordr(index)
				self.listOfLoopChannels[index].setWave("record"+str(index)+".wav")
				#currently in testing, trying to synchronize different recordings
				self.listOfLoopChannels[index].setFramePosition(self.currentFramePosition, CHUNK)
				
				
				self.listOfLoopChannels[index].switchLoop()
				self.listOfLoopChannels[index].setFrameCount(self.recordChannel.getCurrentFrameCount())
				if self.loopLength < self.recordChannel.getCurrentFrameCount():
					self.loopLength = self.recordChannel.getCurrentFrameCount()
				# print(str(self.recordChannel.getCurrentFrameCount()))
			else:
				#Here we have recorded something on this channel, and would like to record something on top of that
				logging.debug('IF2')
				self.recordChannel.recordr(str(index)+"a")
				self.listOfLoopChannels[index].combineToCurrent("record"+str(index)+"a"+".wav")
				pass
				
		else:
			self.listOfLoopChannels[index].switchLoop()
			
	def upCurrentFramePosition(self):

		# current frame position with respect to loop length and mix play
		self.currentFramePosition = (self.currentFramePosition+1)%self.loopLength
			
	def playLoop(self):
		# This will is just for testing purposes, We will need to mix our loopChannels into one audio.
		self.listOfLoopChannels[0].playLoop()
		
	
	# This iterates through all the LoopChannel objects, and sees how many are turned on
	def findNrOfChannelsOn(self):
		number = 0
		for i in range(self.numberOfLoopChannels):
			if self.listOfLoopChannels[i].isLooping():
				number += 1
		return number
		
	#npData has to be on numpy format
	def applyPan(self, npData, pan):
		if npData == []:
			return []
		npData[0::2] *= numpy.sqrt(2)/2.0 * (numpy.cos(numpy.radians(pan)) - numpy.sin(numpy.radians(pan)))
		npData[1::2] *= numpy.sqrt(2)/2.0 * (numpy.cos(numpy.radians(pan)) + numpy.sin(numpy.radians(pan)))
		return npData
		
	
	# takes chunks of audio from all channels, and combines (or mixes) them into one chunk of audio
	def mixChannels(self):
		data = [0]*self.numberOfLoopChannels
		decodedData = [0]*self.numberOfLoopChannels
		nrC = self.findNrOfChannelsOn()
		if nrC == 0:
			constant = 0.0
		else:
			constant= 1.0/nrC
		combinedData = numpy.zeros(2*CHUNK, dtype=numpy.int16)
		
		for i in range(self.numberOfLoopChannels):
			data[i] = self.listOfLoopChannels[i].readChunk(CHUNK)
			decodedData[i] = numpy.fromstring(data[i], numpy.int16)
			
			#apply pan on current channel:
			decodedData[i] = self.applyPan(decodedData[i], self.listOfLoopChannels[i].getPan())
			
			#Only combine audio from channels that are on.
			if self.listOfLoopChannels[i].loop:
				if decodedData[i] != []:
					combinedData = combinedData + self.listOfLoopChannels[i].getVolume() * constant * decodedData[i]
				else:
					combinedData = combinedData + numpy.zeros(2*CHUNK, dtype=numpy.int16)
			
		newData = combinedData.astype(numpy.int16)
		if numpy.array_equal(newData, numpy.zeros(2*CHUNK, dtype=numpy.int16)):
			return numpy.zeros(0, dtype=numpy.int16).astype(numpy.int16)
		return newData
	
	# Rewinds all the wave files in our loop channels
	def rewindChannels(self):
		self.recordChannel.setCurrentFramePosition(0)
		for i in range(self.numberOfLoopChannels):
			self.listOfLoopChannels[i].rewindWave()
		logging.debug('do we rewind')
	
	# plays all loops that are turned on in our loop channels.
	def playMixed(self):
		p = pyaudio.PyAudio()
		stream = p.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				output=True)
				
		data = self.mixChannels().tostring()
		while self.loop :			
			stream.write(data)
			self.upCurrentFramePosition()
			self.recordChannel.upCurrentFramePosition()
			# logging.debug(str(self.currentFramePosition))	
			# logging.debug(str(self.recordChannel.getCurrentFramePosition()))	
			data = self.mixChannels().tostring()
			# if data == b'' : # If file is over then rewind.
				# self.rewindChannels()
				# data = self.mixChannels().tostring()
				
	# gathers input for volume and pan for each channel
	def gatherInput(self):
		while(True):
			#get volume and pan for each loop channel
			for i in range(self.numberOfLoopChannels):
				volume_value = self.mcp.read_adc(i)
				self.listOfLoopChannels[i].setVolume(volume_value/1024*1.25)
				
				pan_value = self.mcp2.read_adc(i)
				self.listOfLoopChannels[i].setPan(pan_value/1024*90-45)
			# value = self.mcp.read_adc(0)
			# self.listOfLoopChannels[0].setVolume(value/1024*1.25)
			# logging.debug('Volume: ' + str(value/1024))
			
			# value = self.mcp.read_adc(1)
			# self.listOfLoopChannels[0].setPan(value/1024*90-45)
			
			# logging.debug('pan: ' + str(value/1024*90-45))
			# self.listOfLoopChannels[0].setPan(self.mcp.read_adc(1))
			
			time.sleep(0.1)
			
	def main(self):
		# We dont have to worry about race conditions. so just run that dive motherf*... SHUT YOUR MOUTH!... im just talking about Shaft.
		t1 = threading.Thread(target=self.gatherInput)
		t1.start()
		# ls.run()
		logging.debug('ready')
		while(not self.startSong):
			pass
		logging.debug('we started the song')
		self.playMixed()


def main(): 
	ls = LoopService()
	# We dont have to worry about race conditions. so just run that dive motherf*... SHUT YOUR MOUTH!... im just talking about Shaft.
	t1 = threading.Thread(target=ls.gatherInput)
	t1.start()
	# ls.run()
	logging.debug('ready')
	while(not ls.startSong):
		pass
	logging.debug('we started the song')
	ls.playMixed()

		
if __name__ == '__main__':main()