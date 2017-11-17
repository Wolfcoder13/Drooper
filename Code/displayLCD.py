import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class DisplayLCD:

	def __init__(self):
		# Raspberry Pi software SPI config:
		self.SCLK = 2
		self.DIN = 3
		self.DC = 14
		self.RST = 15
		self.CS = 8

		# Software SPI usage (defaults to bit-bang SPI interface):
		self.disp = LCD.PCD8544(self.DC, self.RST, self.SCLK, self.DIN, self.CS)

		self.disp.begin(contrast=50)

		self.highlight = "top"



	def displayList(self, listTitle, listOfText, index):

		# Clear display.
		self.disp.clear()
		self.disp.display()

		# Create blank image for drawing. Make sure to create image with mode '1' for 1-bit color.
		image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

		# Get drawing object to draw on image.
		draw = ImageDraw.Draw(image)

		# Draw a white filled box to clear the image.
		draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=350, fill=350)

		# Load default font.
		font = ImageFont.load_default()

		topFill = middleFill = bottomFill = 0

		if (self.highlight == "top"):
			draw.rectangle((7,15,77,25), outline=0, fill=0)
			topDisplay = index
			topFill = 128
		elif (self.highlight == "middle"):
			draw.rectangle((7,25,77,35), outline=0, fill=0)
			topDisplay = index-1
			middleFill = 128
		else:
			draw.rectangle((7,35,77,45), outline=0, fill=0)
			topDisplay = index-2
			bottomFill = 128

		# Write some text.
		draw.text((8,0), listTitle)
		draw.line((8, 12, 75, 12), fill=0)
		draw.text((8,15), listOfText[topDisplay], font=font, fill = topFill)
		draw.text((8,25), listOfText[topDisplay+1], font=font, fill = middleFill)
		draw.text((8,35), listOfText[topDisplay+2], font=font, fill = bottomFill)

		# Display image.
		self.disp.image(image)
		self.disp.display()

	def down(self, listTitle, listOfText, index):
		if self.highlight == "top":
			self.highlight = "middle"
		else:
			self.highlight = "bottom"
		self.displayList(listTitle, listOfText, index)

	def up(listTitle, listOfText, index):
		if self.highlight == "bottom":
			self.highlight = "middle"
		else:
			self.highlight = "top"
		self.displayList(listTitle, listOfText, index)

	def showSuccess(self, text):

		texti = text.split()

		# Clear display.
		self.disp.clear()
		self.disp.display()

		# Create blank image for drawing.
		image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

		# Get drawing object to draw on image.
		draw = ImageDraw.Draw(image)

		# Draw a white filled box to clear the image.
		draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=350, fill=350)

		# Load default font.
		font = ImageFont.load_default()



		# Write some text.
		draw.text((17,15), texti[0], font=font)
		draw.text((17,25), texti[1], font=font)

		# Display image.
		self.disp.image(image)
		self.disp.display()


def main():
    texti = input("Hvad viltu birta? ")
    showSuccess(texti)

if __name__ =="__main__":
    main()

print('Press Ctrl-C to quit.')
while True:
    time.sleep(1.0)
