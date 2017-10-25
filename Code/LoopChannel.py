import pyaudio
import wave

class LoopChannel:

	CHUNK = 1024
	
	def __init__(self):
		# This might be a different sound wrapper, but will be used for testing purposes
		self.wave = wave.open('looptest.wav', 'rb')
	
		self.playing = False
	
		#this will contain the audio file that needs to be played
		self.loop = True
		
		#Volume is between 0 and 127
		self.volume = 0
		
		#Pan is between -63 and 64
		self.pan = 0
		
	def playLoop(self):
		CHUNK = 1024
		#wf = self.wave
		wf = wave.open('looptest.wav', 'rb')
		while(True):
	
			print("="*40)
			p = pyaudio.PyAudio()
			print("="*40)
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)

			data = wf.readframes(CHUNK)

			while self.loop :
				stream.write(data)
				data = wf.readframes(self.CHUNK)
				if data == '' : # If file is over then rewind.
					wf.rewind()
					data = wf.readframes(self.CHUNK)

			stream.stop_stream()
			stream.close()

			p.terminate()
			
	#def loadSound(self, path):
		#Load sound from specific file architecture.