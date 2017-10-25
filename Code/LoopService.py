import pyaudio
import wave
from LoopChannel import LoopChannel
from RecordChannel import RecordChannel

class LoopService:
	def __init__(self):
		self.numberOfLoopChannels = 5
		self.listOfLoopChannels = [0]*self.numberOfLoopChannels
		self.recordChannel = RecordChannel()
		self.initializeChannels()
		self.bpmSet = False
		self.bpm = 0
		
		#for testing
		self.playLoop()
		
		
	def initializeChannels(self):
		for i in range(self.numberOfLoopChannels):
			self.listOfLoopChannels[i] = LoopChannel()
			
	def playLoop(self):
		# This will is just for testing purposes, We will need to mix our loopChannels into one audio.
		self.listOfLoopChannels[0].playLoop()
		
		
		
		
		
# TODO: see if its possible to use interrupt, instead of constant polling of 
# Drumpad loop. Should be run asynchronously
def main():
	ls = LoopService()
	ls.playLoop()
		
if __name__ == '__main__':main()