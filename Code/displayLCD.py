import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi software SPI config:
SCLK = 4
DIN = 17
DC = 23
RST = 24
CS = 8

# Software SPI usage (defaults to bit-bang SPI interface):
disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

disp.begin(contrast=50)

highlight = "top"

def displayList(listTitle, listOfText, index):

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing. Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white filled box to clear the image.
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=350, fill=350)

    # Load default font.
    font = ImageFont.load_default()

    topFill = middleFill = bottomFill = 0

    if (highlight == "top"):
        draw.rectangle((7,15,77,25), outline=0, fill=0)
        topDisplay = index
        topFill = 128
    elif (highlight == "middle"):
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
    disp.image(image)
    disp.display()

def down(listTitle, listOfText, index):
    if highlight == "top":
        global highlight
        highlight = "middle"
    else:
        global highlight
        highlight = "bottom"
    displayList(listTitle, listOfText, index)

def up(listTitle, listOfText, index):
    if highlight == "bottom":
        global highlight
        highlight = "middle"
    else:
        global highlight
        highlight = "top"
    displayList(listTitle, listOfText, index)

def showSuccess(text):

    texti = text.split()

    # Clear display.
    disp.clear()
    disp.display()

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
    disp.image(image)
    disp.display()


def main():
    texti = input("Hvad viltu birta? ")
    showSuccess(texti)

if __name__ =="__main__":
    main()

print('Press Ctrl-C to quit.')
while True:
    time.sleep(1.0)
