from pydub import AudioSegment
from pydub.playback import play

class DrumButton(object):
	#"""This represents a button on our raspberry pi
	#"""
	
	def __init__(self, path):
		#"""Initalizes the button to have a specific sound.
		#path is a string that holds the path to the sound, such as "path/to/sound1.wav" """
		self.sound = AudioSegment.from_file(path)
		
	def playSound(volume):
		#""" This will play the sound that is stored on this button
		#volume: is a variable that will control how loudly the sound will be played."""
		#converted_volume = *0.3(-100+volume)
		#play(song-converted_volume)) #song minus volume will decrese the songs volume by converted_volume desibels
		play(self.sound)