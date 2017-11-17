import RPi.GPIO as GPIO
import os
import threading
import time

from DrumpadService import DrumpadService
from LoopService import LoopService
from DisplayLCD import DisplayLCD


class MasterController:
	
	def __init__(self):
		self.drumpadService = DrumpadService()
		self.loopService    = LoopService()
		self.displayLCD     = DisplayLCD()
		
		
		# list containing strings of drums available
		self.drumList = None
		# what seat is currently selected in drumlist
		self.drumListIndex = 0
		
		# list containing strings of songs available
		self.songList = None
		# what seat is currently selected in songlist
		self.songListIndex = 0
		
		# list containing strings of menu options available
		self.menuList = None
		# what seat is currently selected in menulist
		self.menuListIndex = 0
		
		# 0 = menulist, 1 = drumList, 2 = songList	
		self.listPicked = 0
		
		self.DRUMPATH = "../Sounds/Drums"
		self.SONGPATH = "../Sounds/Songs"
		
		self.initializeDrumList(self.DRUMPATH)
		self.initializeSongList(self.SONGPATH)
		self.initializeMenuList()
		self.displayLCD.displayList("Menu", self.menuList, self.menuListIndex)
		
		#VELJA NÚMER Á TÖKKUM
		self.BACK_BUTTON    = 12
		self.SELECT_BUTTON  = 16
		self.UP_BUTTON      = 20
		self.DOWN_BUTTON    = 21
		self.initializeScreenButtons()
		
	def initializeDrumList(self, path):
		self.drumList = os.listdir(path)
		
	def initializeSongList(self, path):
		self.songList = os.listdir(path)
		
	def initializeMenuList(self):
		self.menuList = ["Choose Drums", "Choose Song", "New Song"]
		
	def initializeScreenButtons(self):
		print("Initializing Interups for screen buttons")
		
		GPIO.setup(self.BACK_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
		GPIO.setup(self.SELECT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
		GPIO.setup(self.UP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
		GPIO.setup(self.DOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

		GPIO.add_event_detect(self.BACK_BUTTON,   GPIO.RISING, callback=lambda x: self.back(),      bouncetime=300)
		GPIO.add_event_detect(self.SELECT_BUTTON, GPIO.RISING, callback=lambda x: self.select(), bouncetime=300)
		GPIO.add_event_detect(self.UP_BUTTON, GPIO.RISING, callback=lambda x: self.up(), bouncetime=300)
		GPIO.add_event_detect(self.DOWN_BUTTON, GPIO.RISING, callback=lambda x: self.down(), bouncetime=300)
		
	#TODO
	def up(self):
		if(self.listPicked == 0):
			self.menuListIndex = (self.menuListIndex -1)%len(self.menuList)
			# display updated menu list on screen
			self.displayLCD.up("Menu", self.menuList, self.menuListIndex)
		elif(self.listPicked == 1):
			self.drumListIndex = (self.drumListIndex -1)%len(self.drumList)
			# display updated drum list on screen
			self.displayLCD.up("Drums", self.drumList, self.drumListIndex)
		elif(seef.listPicked == 2):
			self.songListIndex = (self.songListIndex -1)%len(self.songList)
			# display updated song list on screen
			self.displayLCD.up("Songs", self.songList, self.songListIndex)
		
	#TODO
	def down(self):
		if(self.listPicked == 0):
			self.menuListIndex = (self.menuListIndex +1)%len(self.menuList)
			# display updated menu list on screen
			self.displayLCD.down("Menu", self.menuList, self.menuListIndex)
		elif(self.listPicked == 1):
			self.drumListIndex = (self.drumListIndex +1)%len(self.drumList)
			# display updated drum list on screen
			self.displayLCD.down("Drums", self.drumList, self.drumListIndex)
		elif(seef.listPicked == 2):
			self.songListIndex = (self.songListIndex +1)%len(self.songList)
			# display updated song list on screen
			self.displayLCD.down("Songs", self.songList, self.songListIndex)
			
	#TODO
	def select(self):
		if(self.listPicked == 0):
			pass
			if(self.menuListIndex == 0):
				self.listPicked += 1
				# Switch list on drum display
				self.displayLCD.displayList("Drums", self.drumList, self.drumListIndex)
			elif(self.menuListIndex == 1):
				self.listPicked += 2
				# Switch list on song display
				self.displayLCD.displayList("Songs", self.songList, self.songListIndex)
			elif(self.menuListIndex == 2):
				# Reset loop player
				self.resetLoopService()
				# display screen that new song is read
				self.displayLCD.showSuccess("Starting NewSong")
				# display menuList again after some time
				self.displayLCD.displayList("Menu", self.menuList, self.menuListIndex)
		elif(self.listPicked == 1):
			self.drumpadService.changeDrums(self.drumListIndex)
			# Display "drums X picked"
			self.displayLCD.showSuccess("Drums_"+str(self.drumListIndex)+" Selected")
		elif(slef.listPicked == 2):
			# Display "no sounds available at this moment"
			pass
			
	#TODO
	def back(self):
		if(self.listPicked == 0):
			pass
		elif(self.listPicked == 1 or self.listPicked == 2):
			self.listPicked = 0
			# display menuList
			self.displayLCD.displayList("Menu", self.menuList, self.menuListIndex)
			
	#TODO
	def resetLoopService(self):
		self.loopService = None
		self.loopService = LoopService()
		pass
	
	#TODO
	def runDrumService(self):
		t1 = threading.Thread(target=self.drumpadService.mainDrum())
		t1.start()
		
	#TODO
	def runLoopService(self):
		t1 = threading.Thread(target=self.loopService.main())
		t1.start()
		pass
	
	
def main():
	controller = MasterController()
	controller.runDrumService()
	
		
		
if __name__ == '__main__':main()