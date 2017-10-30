import pyaudio
import wave
import numpy

CHUNK = 1024 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 #sample rate
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "record"
FILE_EXTENSION = ".wav"

class RecordChannel:
	
	def __init__(self):
		# The first recording in a song will determine how many frames each loop clip will be.
		self.frameCount = 0
		self.currentFrameCount = 0
		
		#when this is true, then if you press a loop channel button, it will record on it instead of playing it.
		self.record = False
		self.loop = 0
		self.volume = 0
		self.pan = 0
		
	def getFrameCount(self):
		return self.frameCount
		
	def getCurrentFrameCount(self):	
		return self.currentFrameCount
	def switchRecord(self):
		self.record = not self.record
		
	def isRecording(self):
		return self.record
		
	def recordr(self, index=""):
		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK) #buffer
						
		frames = []
		self.currentFrameCount = 0
		while(self.record):
			for i in range(self.frameCount):
				if(self.record):
					data = stream.read(CHUNK)
				else:
					if self.frameCount%self.currentFrameCount == 0 or self.frameCount == self.currentFrameCount*2 or self.frameCount == self.currentFrameCount*4 or self.frameCount == self.currentFrameCount*8:
						print("break me")
						break
					data = numpy.zeros(2*CHUNK, dtype=numpy.int16).tostring()
				frames.append(data) # 2 bytes(16 bits) per channel
				self.currentFrameCount += 1
			else:
				continue
			break

		print(str(self.frameCount))
		print(str(self.currentFrameCount))	
		stream.stop_stream()
		stream.close()
		p.terminate()
		
		wf = wave.open(WAVE_OUTPUT_FILENAME + str(index) + FILE_EXTENSION, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		
	def firstRecording(self):
		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK) #buffer
						
		#print("* recording")
		frames = []
		while(self.record):
			data = stream.read(CHUNK)
			frames.append(data) # 2 bytes(16 bits) per channel
			self.frameCount += 1
			# print(str(self.frameCount))
		#print("* done recording")
		print("Frame count is: " + str(self.frameCount))
		stream.stop_stream()
		stream.close()
		p.terminate()
		
		wf = wave.open(WAVE_OUTPUT_FILENAME + FILE_EXTENSION, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()