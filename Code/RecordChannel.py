import pyaudio
import wave

class RecordChannel:
	
	def __init__(self):
		self.loop = 0
		self.volume = 0
		self.pan = 0