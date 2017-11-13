import pyaudio
import wave

class LoopChannel:

	CHUNK = 1024
	
	def __init__(self):
		# This might be a different sound wrapper, but will be used for testing purposes
		self.wave = wave.open('looptest.wav', 'rb')
		
		# PERHAPS RETHINK THIS VARIABLE... BUT WE NEED RECORDING TO FOLLOW
		self.emtpyWave = None
	
		# its the number of frames this loop has. 
		self.frameCount = 0
	
		#this says if current channel is looping or not
		self.loop = False
		
		#Volume is between 0 and 1.27
		self.volume = 0.5
		
		#Pan is between -45 and 45
		self.pan = 0
		
	def isLooping(self):
		return self.loop
		
	def setFrameCount(self, frameCount):
		self.frameCount = frameCount
		
	def getFrameCount(self):
		return self.frameCount
		
	def getVolume(self):
		return self.volume
		
	def setVolume(self, volume):
		self.volume = volume
		
	def getPan(self):
		return self.pan
		
	def setPan(self, pan):
		self.pan = pan	
		
	#switches the boolean value of loop.	
	def switchLoop(self):
		self.loop = not self.loop
		
	def setWave(self, path):
		self.wave = wave.open(path, 'rb')
		
	def rewindWave(self):
		self.wave.rewind()
	
	def readChunk(self, CHUNK):
		chunk = self.wave.readframes(CHUNK)
		if chunk == '' : # If file is over then rewind.
			# print("chunk empty")
			self.wave.rewind()
			chunk = self.wave.readframes(self.CHUNK) 
		return chunk
		
	def playLoop(self):
		CHUNK = 1024
		#wf = self.wave
		wf = wave.open('looptest.wav', 'rb')
		while(True):
	

			p = pyaudio.PyAudio()
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)

			data = wf.readframes(CHUNK)

			while self.loop :
				stream.write(data)
				data = wf.readframes(self.CHUNK)
				if data == '' : # If file is over then rewind.
					# print("do we enter?")
					wf.rewind()
					data = wf.readframes(self.CHUNK)

			stream.stop_stream()
			stream.close()

			p.terminate()
			
	#def loadSound(self, path):
		#Load sound from specific file architecture.