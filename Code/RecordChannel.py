import pyaudio
import wave
import numpy
import logging
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 #sample rate
WAVE_OUTPUT_FILENAME = "record"
FILE_EXTENSION = ".wav"

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class RecordChannel:
	
	def __init__(self):
		# The first recording in a song will determine how many frames each loop clip will be.
		self.frameCount = 0
		self.currentFrameCount = 0
		
		#current position of frame
		self.currentFramePosition = 0
		
		#when this is true, then if you press a loop channel button, it will record on it instead of playing it.
		self.record = False
		self.volume = 0
		self.pan = 0
		
		self.p = pyaudio.PyAudio()
		
		self.stream = self.p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						# output=True,
						frames_per_buffer=CHUNK)
		
		
	def setCurrentFramePosition(self, framePosition):
		self.currentFramePosition = 0
		
	def getCurrentFramePosition(self):
		return self.currentFramePosition
		
	def upCurrentFramePosition(self):
		self.currentFramePosition = (self.currentFramePosition + 1) % self.frameCount
		
	def getFrameCount(self):
		return self.frameCount
		
	def getCurrentFrameCount(self):	
		return self.currentFrameCount
		
	def switchRecord(self):
		self.record = not self.record
		
	def isRecording(self):
		return self.record		
		
	def recordr(self, index=""):
		# p = pyaudio.PyAudio()

		stream = self.p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK) #buffer
						
		frames = []
		frames.append(numpy.zeros(2*CHUNK * self.currentFramePosition, dtype=numpy.int16).tostring())
		logging.debug(str(self.currentFramePosition))
		self.currentFrameCount = self.currentFramePosition
		while(self.record):
			for i in range(self.frameCount):
				try:
					if(self.record):
						data = stream.read(CHUNK)
					else:
						if self.frameCount%self.currentFrameCount == 0 or self.frameCount == self.currentFrameCount*2 or self.frameCount == self.currentFrameCount*4 or self.frameCount == self.currentFrameCount*8:
							# print("break me")
							break
						data = numpy.zeros(2*CHUNK, dtype=numpy.int16).tostring()
					frames.append(data) # 2 bytes(16 bits) per channel
					self.currentFrameCount += 1
				except:
					logging.debug('EXCEPTION')
					data = numpy.zeros(2*CHUNK, dtype=numpy.int16).tostring()
					frames.append(data)
			else:
				continue
			break	
		stream.stop_stream()
		stream.close()
		# p.terminate()
		
		wf = wave.open(WAVE_OUTPUT_FILENAME + str(index) + FILE_EXTENSION, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(self.p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		
	def firstRecording(self):
		stream = self.p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK) #buffer
						
						
		frames = []
		while(self.record):
			try:
				data = stream.read(CHUNK)
				frames.append(data) # 2 bytes(16 bits) per channel
				self.frameCount += 1
			except:
				logging.debug('EXCEPTION')
				data = numpy.zeros(2*CHUNK, dtype=numpy.int16).tostring()
				frames.append(data)
		stream.stop_stream()
		stream.close()
		# p.terminate()
		
		wf = wave.open(WAVE_OUTPUT_FILENAME + FILE_EXTENSION, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(self.p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()