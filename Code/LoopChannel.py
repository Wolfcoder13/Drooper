import pyaudio
import wave

class LoopChannel:

	CHUNK = 1024
	
	def __init__(self):
		# This might be a different sound wrapper, but will be used for testing purposes
		self.wave = wave.open('looptest.wav', 'rb')
	
		#this says if current channel is looping or not
		self.loop = False
		
		#Volume is between 0 and 127
		self.volume = 0
		
		#Pan is between -63 and 64
		self.pan = 0
		
	#switches the boolean value of loop.	
	def switchLoop(self):
		self.loop = not self.loop
		
	def setWave(self, path):
		self.wave = wave.open(path, 'rb')
		
	def rewindWave(self):
		self.wave.rewind()
	
	def readChunk(self, CHUNK):
		chunk = self.wave.readframes(CHUNK)
		if len(chunk) < 10:
			print(chunk)
		if chunk == "''" : # If file is over then rewind.
			# print("chunk empty")
			wf.rewind()
			chunk = wf.readframes(self.CHUNK) 
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
					print("do we enter?")
					wf.rewind()
					data = wf.readframes(self.CHUNK)

			stream.stop_stream()
			stream.close()

			p.terminate()
			
	#def loadSound(self, path):
		#Load sound from specific file architecture.