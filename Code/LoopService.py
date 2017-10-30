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
		

class LoopService:
	def __init__(self):
		#loopLength will be used to make sure all loop clips are of the same length
		self.loopLength = 0
		self.bpmSet = False
		self.bpm = 0
		self.startSong = False
		self.numberOfLoopChannels = 3
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
		
		
		
	def initializeChannels(self):
		print("Initializing Each loop channel")
		for i in range(self.numberOfLoopChannels):
			self.listOfLoopChannels[i] = LoopChannel()
	
	
	def initializeButtons(self):
		print("Initializing Interups for buttons")
		GPIO.add_event_detect(RECBUTTON,   GPIO.FALLING, callback=lambda x: self.record(),      bouncetime=300)
		GPIO.add_event_detect(LOOPBUTTON1, GPIO.FALLING, callback=lambda x: self.loopButton(0), bouncetime=300)
		GPIO.add_event_detect(LOOPBUTTON2, GPIO.FALLING, callback=lambda x: self.loopButton(1), bouncetime=300)
		GPIO.add_event_detect(LOOPBUTTON3, GPIO.FALLING, callback=lambda x: self.loopButton(2), bouncetime=300)
		

	def record(self):
		self.recordChannel.switchRecord()
		# if self.recordChannel.isRecording():
			# print("Recording")
		# else:
			# print("stop recording")
			
		
	#this might make one mixed chunk louder or more quiet. Debug it later if necessary
	def loopButton(self, index):
		# print("You pressed loop button " + str(index))
		if not self.startSong:
			# I think this part is fully implemented
			self.recordChannel.firstRecording()
			self.listOfLoopChannels[index].setWave("record.wav")
			self.listOfLoopChannels[index].setFrameCount(self.recordChannel.getFrameCount)
			# print(str(self.recordChannel.getFrameCount()))
			self.loopLength = self.recordChannel.getFrameCount()
			self.listOfLoopChannels[index].switchLoop()
			self.startSong = True
		elif self.recordChannel.isRecording():
			if self.listOfLoopChannels[index].getFrameCount() == 0:
				#here we havent recorded anything on this channel
				self.recordChannel.recordr(index)
				self.listOfLoopChannels[index].setWave("record"+str(index)+".wav")
				self.listOfLoopChannels[index].switchLoop()
				self.listOfLoopChannels[index].setFrameCount(self.recordChannel.getCurrentFrameCount())
				if self.loopLength < self.recordChannel.getCurrentFrameCount():
					self.loopLength = self.recordChannel.getCurrentFrameCount()
				# print(str(self.recordChannel.getCurrentFrameCount()))
			else:
				#Here we have recorded something on this channel, and would like to record something on top of that
				print("implement a way to combine new loop with current loop")
		else:
			self.listOfLoopChannels[index].switchLoop()
			
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
		
	# mixChunks kannski?	
	# takes chunks of audio from all channels, and combines (or mixes) them into one chunk of audio
	def mixChannels(self):
		data = [0]*self.numberOfLoopChannels
		decodedData = [0]*self.numberOfLoopChannels
		nrC = self.findNrOfChannelsOn()
		if nrC == 0:
			constant = 0.0
		else:
			constant= 1.0/self.findNrOfChannelsOn()
		combinedData = numpy.zeros(2*CHUNK, dtype=numpy.int16)
		
		for i in range(self.numberOfLoopChannels):
			data[i] = self.listOfLoopChannels[i].readChunk(CHUNK)
			decodedData[i] = numpy.fromstring(data[i], numpy.int16)
			
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
		for i in range(self.numberOfLoopChannels):
			self.listOfLoopChannels[i].rewindWave()
	
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
			data = self.mixChannels().tostring()
			# print(data)
			if data == b'' : # If file is over then rewind.
				# print("rewind")
				self.rewindChannels()
				data = self.mixChannels().tostring()
		
		
# TODO: see if its possible to use interrupt, instead of constant polling of 
# Drumpad loop. Should be run asynchronously
def main(): 
	ls = LoopService()
	while(not ls.startSong):
		# print("waiting")
		pass
	print("we made it here")
	ls.playMixed()

		
if __name__ == '__main__':main()