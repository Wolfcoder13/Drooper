#!/usr/bin/env python
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import pyaudio
from pydub import AudioSegment
from pydub.playback import play

from DrumButton import DrumButton

class DrumpadService(object):
    #TODO: See if we should make this into a singleton class.

    def __init__(self):
        # TODO: need to verify these are the right numbers for the pins.
        # Software SPI configuration:
        self.CLK  = 18   #pin 12
        self.MISO = 23   #pin 16
        self.MOSI = 24   #pin 18
        self.CS   = 25   #pin 22
        self.CS2  = 8    #pin 24 
        self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        #make sure this works as second input
        self.mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS2, miso=MISO, mosi=MOSI)
		
		self.drums = "Drums_1"
        
        self.listOfDrums = []
        initalizeDrums()
        prototype()

    # TODO: initialize drum sounds
    def initalizeDrums (self):
        #perhaps keep sounds in array
        for i in range(16):
            self.listOfDrums[i] = DrumButton("../Sounds/"+self.drums+"/sound"+i+".wav")
        
        
    def changeDrums (self,pick):
        #load other drums, pick will chose frome selectable drums

    def playButton (self,buttonNr, volume):
        if volume==0
            return
        self.listOfDrums[buttonNr].playSound(volume)

    def getVolume (self,input):
        #calculates the volume from 10 bit input resolution (1023 values)
        #perhaps add more resolution.
        if input < 500:
            return 0
        else if input < 600:
            return 20
        else if input < 700:
            return 40
        else if input < 800:
            return 60
        else if input < 900:
            return 80
        return 100
        
        

    # TODO: see if its possible to use interrupt, instead of constant polling of 
    # Drumpad loop. Should be run asynchronously
    def prototype(self):
        while True:
            for i in range(8):
                volume = getVolume(mcp.read_adc(i))
                volume2 = getVolume(mcp2.read_adc(i))
                if volume != 0:
                    playButton(i, volume)
                if volume2 != 0:
                playButton(i+8, volume2)

            # Pause for half a second.
            time.sleep(0.01)
