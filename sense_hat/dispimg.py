#!/usr/bin/python3
#from sense_hat import SenseHat
from sense_hat import *
import time
from PIL import Image
import os
import sys


if len(sys.argv)>1:
    imax=int(sys.argv[1])
else:
    imax=20

for i in range(imax):
    print("!... TAKING PHOTO RIGHT NOW", i,'/',imax)
    CMD='wget http://localhost:8088/\?action\=snapshot -O pic.jpg 2>/dev/null'
    a=os.popen(CMD)
    time.sleep(1)  # need some time to save to SD
    image_file="pic.jpg"
    print("!... PHOTO TAKEN, openning ...",image_file,'...')
    #CMD="/usr/bin/convert  pic.jpg -resize 8x8! pic64.jpg"
    #print('i... trying to convert')
    #os.popen(CMD)
    #time.sleep(1)
    #########################
    # Open image file
    #image_file = os.path.join(os.sep,"/home","pi","SenseHAT","pixelart.png")
    #image_file=sys.argv[1]
    #print('i... opening', image_file)

    img = Image.open(image_file)
    print('i... opened, resizing ...')
    ###img=img.thumbnail( (8,8) , Image.ANTIALIAS )
    img=img.resize(  (8,8)  , Image.ANTIALIAS )
    # Generate rgb values for image pixels
    rgb_img = img.convert('RGB')
    image_pixels = list(rgb_img.getdata())
    
    # Get the 64 pixels you need
    pixel_width = 1
    image_width = pixel_width*8
    sense_pixels = []
    start_pixel = 0
    while start_pixel < (image_width*64):
        sense_pixels.extend( image_pixels[start_pixel:(start_pixel+image_width):pixel_width] )
        start_pixel += (image_width*pixel_width)

    # Display the image
    sense = SenseHat()
    sense.set_rotation(r=180)
    sense.set_pixels(sense_pixels)
    time.sleep (3)
    print('i... next',i)
########### end of for
sense.clear()
