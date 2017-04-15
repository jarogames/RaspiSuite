#!/usr/bin/python3
#from sense_hat import SenseHat
from sense_hat import *
import time
from PIL import Image
import os
import sys
import urllib.request
import io  # create file like object with jpg

if len(sys.argv)>1:
    imax=int(sys.argv[1])
else:
    imax=20

    
for i in range(imax):
    start_time=time.time()
    print("!... TAKING PHOTO RIGHT NOW", i,'/',imax)
    req=urllib.request.Request("http://localhost:8088/?action=snapshot")
    with urllib.request.urlopen(req) as url:
        f=io.BytesIO( url.read() )
    
    print("!... PHOTO TAKEN, openning ...")
    img = Image.open( f )
    print('i... opened, resizing ...', end="")

#    img=img.resize(  (8,8)  , Image.NEAREST )
    img=img.resize(  (8,8)  , Image.BILINEAR )
#    img=img.resize(  (8,8)  , Image.BICUBIC )
#    img=img.resize(  (8,8)  , Image.ANTIALIAS )

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

    #---- recalculate to have floor 10 96% or 20, 92%
#    sense_pixels=[ tuple([ int(a*0.96+10) for a in x])  for x in sense_pixels ]
    #print( sense_pixels )
    #time.sleep(3)
    # Display the image
    sense = SenseHat()
    sense.set_rotation(r=180)
    sense.set_pixels(sense_pixels)
    print('m...                 {:.2f}sec.'.format( time.time()-start_time ))
    time.sleep (0.1)
    #print('i... next',i)
########### end of for
print("e...  ending....")
time.sleep(1)
sense.clear()
