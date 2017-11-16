
import os

from DrumService import DrumService
from LoopService import LoopService


class MasterController:
	
	def __init__(self):
		self.drumpadService = DrumpadService()
		self.loopService = LoopService()
		
		
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
		
		self.BACK_BUTTON    = 1
		self.SELECT_BUTTON  = 1
		self.UP_BUTTON      = 1
		self.DOWN_BUTTON    = 1
		self.initializeScreenButtons()
		
	def initializeDrumList(self, path):
		self.drumList = os.listdir(path)
		
	def initializeSongList(self, path):
		self.songList = os.listdir(path)
		
	def initializeMenuList(self, path):
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
			self.menuListIndex = (self.menuListIndex -1)%self.menuList.length
			# display updated menu list on screen
		elif(self.listPicked == 1):
			self.drumListIndex = (self.drumListIndex -1)%self.drumList.length
			# display updated drum list on screen
		elif(seef.listPicked == 2):
			self.songListIndex = (self.songListIndex -1)%self.songList.length
			# display updated song list on screen
		
	#TODO
	def down(self):
		if(self.listPicked == 0):
			self.menuListIndex = (self.menuListIndex +1)%self.menuList.length
			# display updated menu list on screen
		elif(self.listPicked == 1):
			self.drumListIndex = (self.drumListIndex +1)%self.drumList.length
			# display updated drum list on screen
		elif(seef.listPicked == 2):
			self.songListIndex = (self.songListIndex +1)%self.songList.length
			# display updated song list on screen
			
	#TODO
	def select(self):
		if(self.listPicked == 0):
			pass
			if(self.menuListIndex == 0):
				self.listPicked += 1
				# Switch list on drum display
			elif(self.menuListIndex == 1):
				self.listPicked += 2
				# Switch list on song display
			elif(self.menuListIndex == 2):
				# Reset loop player
				# display screen that new song is read
				# display menuList again after some time
		elif(self.listPicked == 1):
			self.drumpadService.changeDrums(self.drumListIndex)
			# Display "drums X picked"
			pass
		elif(slef.listPicked == 2):
			# Display "no sounds available at this moment"
			pass
			
	#TODO
	def back(self):
		if(self.listPicked == 0):
			pass
		elif(self.listPicked == 1 || self.listPicked == 2):
			self.listPicked = 0
			# display menuList
			
	#TODO
	def resetLoopService(self):
		self.loopService = None
		self.loopService = LoopService()
		pass
	
	#TODO
	def runDrumService(self):
		pass
		
	#TODO
	def runLoopService(self):
		pass
	
#TODO	
def main():
	controller = MasterController():
	while True:
		
		
if __name__ == '__main__':main()