import RPi.GPIO as GPIO
import pyaudio
import wave
import numpy
from LoopChannel import LoopChannel
from RecordChannel import RecordChannel
from functools import reduce

CHUNK = 1024 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 #sample rate

wf = wave.open('lead.wav', 'rb')
player = pyaudio.PyAudio()

FORMAT = player.get_format_from_width(wf.getsampwidth())
CHANNELS = wf.getnchannels()
RATE = wf.getframerate()

#pick GPIO pins that are not in use. We might look into other solutions, using less pins though
RECBUTTON = 4		#pin 7 on board
LOOPBUTTON1 = 17	#pin 11 on board
LOOPBUTTON2 = 27	#pin 13 on board
LOOPBUTTON3 = 22	#pin 15 on board

GPIO.setmode(GPIO.BCM)
GPIO.setup(RECBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(LOOPBUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(LOOPBUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(LOOPBUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

		
#this might make one mixed chunk louder or more quiet. Debug it later if necessary
def loopButton(LS, index):
	print("do I get in here?")
	if self.record:
		print("finish this later")
	else:
		self.listOfLoopChannels[i].switchLoop()
		

class LoopService:
	def __init__(self):
		#loopLength will be used to make sure all loop clips are of the same length
		self.loopLength = None
		self.bpmSet = False
		self.bpm = 0
		self.numberOfLoopChannels = 3
		self.listOfLoopChannels = [0]*self.numberOfLoopChannels
		self.recordChannel = RecordChannel()
		self.initializeChannels()
		self.initializeButtons()
		
		#when this is true, then if you press a loop channel button, it will record on it instead of playing it.
		self.record = False
		
		
		#for testing
		#self.playLoop()
		self.listOfLoopChannels[0].setWave('drums.wav')
		self.listOfLoopChannels[0].switchLoop()
		self.listOfLoopChannels[1].setWave('lead.wav')
		self.listOfLoopChannels[2].setWave('pads.wav')
		self.loop = True
		self.playMixed()
		
		
		
	def initializeChannels(self):
		for i in range(self.numberOfLoopChannels):
			self.listOfLoopChannels[i] = LoopChannel()
			
	def initializeButtons(self):
		# GPIO.add_event_detect(RECBUTTON, GPIO.FALLING, callback=record(), bouncetime=300)
		GPIO.add_event_detect(LOOPBUTTON1, GPIO.FALLING, callback=lambda x: loopButton(self, 0), bouncetime=300)
		GPIO.add_event_detect(LOOPBUTTON2, GPIO.FALLING, callback=lambda x: loopButton(self, 1), bouncetime=300)
		GPIO.add_event_detect(LOOPBUTTON3, GPIO.FALLING, callback=lambda x: loopButton(self, 2), bouncetime=300)

			
	def record(self):
		self.record = not self.record
		
	#this might make one mixed chunk louder or more quiet. Debug it later if necessary
	def loopButton(self, index):
		print("do I get in here?")
		if self.record:
			print("finish this later")
		else:
			self.listOfLoopChannels[i].switchLoop()
			
	def playLoop(self):
		# This will is just for testing purposes, We will need to mix our loopChannels into one audio.
		self.listOfLoopChannels[0].playLoop()
		
	
	# This iterates through all the LoopChannel objects, and sees how many are turned on
	def findNrOfChannelsOn(self):
		number = 0
		for i in range(self.numberOfLoopChannels):
			if self.listOfLoopChannels[i].loop:
				number += 1
		return number
		
	#mixChunks kannski?	
	# takes chunks of audio from all channels, and combins (or mixes) them into one chunk of audio
	def mixChannels(self):
		data = [0]*self.numberOfLoopChannels
		decodedData = [0]*self.numberOfLoopChannels
		constant= 1/self.findNrOfChannelsOn()
		#constant= 1
		combinedData = 0
		for i in range(self.numberOfLoopChannels):
			data[i] = self.listOfLoopChannels[i].readChunk(CHUNK)
			decodedData[i] = numpy.fromstring(data[i], numpy.int16)
			if self.listOfLoopChannels[i].loop:
				combinedData = combinedData + constant* decodedData[i]
			
		newData = combinedData.astype(numpy.int16)
		return newData
	
	def rewindChannels(self):
		for i in range(self.numberOfLoopChannels):
			self.listOfLoopChannels[i].rewindWave()
	
	def playMixed(self):
		p = pyaudio.PyAudio()
		stream = p.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				output=True)
				
		data = self.mixChannels().tostring()
		while self.loop :			
			stream.write(data)
			data = self.mixChannels().tostring()
			#print(data)
			if data == b'' : # If file is over then rewind.
				self.rewindChannels()
				data = self.mixChannels().tostring()
		
		
# TODO: see if its possible to use interrupt, instead of constant polling of 
# Drumpad loop. Should be run asynchronously
def main():
	# GPIO.setup(RECBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	# GPIO.setup(LOOPBUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	# GPIO.setup(LOOPBUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	# GPIO.setup(LOOPBUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
	ls = LoopService()

		
if __name__ == '__main__':main()