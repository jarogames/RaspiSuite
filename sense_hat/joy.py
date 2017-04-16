#!/usr/bin/python3

try:
    from sense_hat import SenseHat
    blue=50
    white=210
except:
    from sense_emu import SenseHat
    blue=200
    white=250

    
from signal import pause
import time
from datetime import datetime
from PIL import Image
import urllib.request
import os
from os.path import expanduser
import io  # create file like object with jpg

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


x = y = 1
hat = SenseHat()
joymenu={ 'row':1, 'pos':1,  'res':1, 'speed':1 }
joymenulow={ 'row':0, 'pos':1,  'res':1, 'speed':0 }
joymenuhig={ 'row':3, 'pos':1,  'res':3, 'speed':3 }



def getstamp():
    now=datetime.now()
    stamp="{:4d}{:02d}{:02d}_{:02d}{:02d}{:02d}_{:01d}".format(now.year,now.month,now.day,now.hour,now.minute,now.second,int(now.microsecond/1e+5))
    return stamp


def take_photo():
    try:
        #req=urllib.request.Request('http://pix3:8088/?action=snapshot')
        req=urllib.request.Request("http://localhost:8088/?action=snapshot")
        with urllib.request.urlopen(req) as url:
            f=io.BytesIO( url.read() )
    except:
        print('!... not image from camera', end="\r" )
        f="pic.png"
        f="letters/A.png"
    return f


def label_photo(img, stamp):
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    #font = ImageFont.truetype("sans-serif.ttf", 16)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((0, 0), stamp ,(255,255,255))
    return img


def photo_on_matrix( img ):
    #img = Image.open( f )
    img2=img.resize(  (8,8)  , Image.BILINEAR )
    rgb_img = img2.convert('RGB')
    image_pixels = list(rgb_img.getdata())
    # Get the 64 pixels you need
    pixel_width = 1
    image_width = pixel_width*8
    sense_pixels = []
    start_pixel = 0
    while start_pixel < (image_width*64):
        sense_pixels.extend( image_pixels[start_pixel:(start_pixel+image_width):pixel_width] )
        start_pixel += (image_width*pixel_width)
    #hat.set_rotation(r=180)
    print('i... photo sent to matrix, pixels=',len(sense_pixels))
    hat.set_pixels(sense_pixels)
    #time.sleep(1)
    #hat.set_rotation(r=0)
    #print('D... leaving update scr')



# if fname == ""    : no file save
def save_image(fname, joyraw=1 ):
    home = expanduser("~")
    directory=home+'/'+'motion/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    f=take_photo()
    img=Image.open(f)
    if joyraw==3:
        print('D... updating matrix')
        photo_on_matrix( img )
    if fname == "":
        return
    label_photo( img, fname )
    #img.show()
    print('s... saving', directory+fname+'.jpg')
    img.convert('RGB').save(directory+fname+'.jpg')
    img.close()
    return 0





#one row per 5x3 digit - 0 to 9 and T
nums =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1, # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,
       1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,
       1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,
       1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,
       1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,
       1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,
       1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,
       1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,
       1,1,1,1,0,1,1,1,1,0,0,1,0,0,1, # 9
       1,1,1,0,1,0,0,1,0,0,1,0,0,1,0] # T

def show_num(val,xd,yd,r,g,b):
    offset = val * 15
    for p in range(offset,offset + 15):
        if nums[p] == 1:
            xt = p % 3
            yt = (p-offset) // 3
            hat.set_pixel(xt+xd,yt+yd,r,g,b)       

            
def show_number(val,r,g,b):
    abs_val = abs(val)
    tens = abs_val // 10
    units = abs_val % 10
    hat.clear()
    if (abs_val > 9): show_num(tens,0,2,  r,g,b )
    show_num(units,4,2,r,g,b)
    if abs_val == 100:
        hat.clear()
        show_num(10,3,2,  r,g,b ) # 'T' for ton = 100
    if val < 0 :
        for i in range(0,8):
            hat.set_pixel(i,0,0,0,128)


            
def update_screen(event):
    if event is None:
        print('i... initial update screen')
    else:
        if not event.action in ('pressed', 'held'):
            return
    #print('D... update scr')
    hat.clear()
    if joymenu['row']==0:  # red - resolution
        #show_number( joymenu['res'], 230 ,0, 0  )
        if joymenu['res']==1: hat.show_letter('S', (240,0,0) )
        if joymenu['res']==2: hat.show_letter('M', (240,0,0) )
        if joymenu['res']==3: hat.show_letter('L', (240,0,0) )
        if joymenu['res']==4: hat.show_letter('X', (240,0,0) )
        return
    if joymenu['row']==1:  #silent
        #hat.set_pixel(x, y, 0, 0, 100)
        show_number( joymenu['speed'],0,0,blue )
        return
    if joymenu['row']==2: # number selection
        show_number( joymenu['speed'], white , white , white )
        
    if joymenu['row']==3: # show camera picture
        #hat.set_pixel(x, y, 255, 255, 255)
        f=take_photo()
        photo_on_matrix( Image.open(f) )
        return

    

def clampy(value, min_value=0, max_value=3):
    return min(max_value, max(min_value, value))
def clampx(value, min_value=0, max_value=3):
    return min(max_value, max(min_value, value))


def clamp(n, minn, maxn): return min(max(n, minn), maxn)


def move_dot(event):
    global x, y
    global joymenu
    if event.action in ('pressed', 'held'):
        
        if joymenu['row']==0: # ---------------------- red  - resolution
            joymenu['res'] = joymenu['res'] + {
                'left': -1,
                'right': 1,
                }.get(event.direction, 0)
            joymenu['res']=clamp(joymenu['res'],joymenulow['res'],joymenuhig['res'] )
            #
            ##########  this is a place we need to make the action ######
            #      1/ write to file
            home = expanduser("~")
            camfile=home+'/'+'.camson.rpires'
            with open( camfile , 'w' ) as f:
                if joymenu['res']==1:
                    f.write('640\n')
                if joymenu['res']==2:
                    f.write('1024\n')
                if joymenu['res']==3:
                    f.write('1280\n')
            if event.direction == 'middle':
                CMD='screen -X -S picam quit'
                print('!... killing picam',CMD)
                os.popen( CMD )
                
        if joymenu['row']==1: # ---------------------------- blue
            joymenu['speed'] = joymenu['speed'] + {
                'left': -1,
                'right': 1,
                }.get(event.direction, 0)
            joymenu['speed']=clamp(joymenu['speed'],joymenulow['speed'],joymenuhig['speed'] )
            if event.direction == 'middle':
                save_image( getstamp()  )
        if joymenu['row']==2: # -------------------------   white
            joymenu['speed'] = joymenu['speed'] + {
                'left': -1,
                'right': 1,
                }.get(event.direction, 0)
            joymenu['speed']=clamp(joymenu['speed'],joymenulow['speed'],joymenuhig['speed'] )
            if event.direction == 'middle':
                save_image( getstamp()  )
        if joymenu['row']==3: # -------------------------- pic - do nothing
            print("", end="\r")
#            joymenu['res'] = joymenu['res'] + {
#                'left': -1,
#                'right': 1,
#                }.get(event.direction, 0)
            if event.direction == 'middle':
                save_image( getstamp()  )
        joymenu['row'] = joymenu['row'] - {
            'up': -1,
            'down': 1,
            }.get(event.direction, 0)
        joymenu['row']=clamp(joymenu['row'],joymenulow['row'],joymenuhig['row'] )
        print(joymenu)

update_screen( None )
hat.stick.direction_up = move_dot
hat.stick.direction_down = move_dot
hat.stick.direction_left = move_dot
hat.stick.direction_right = move_dot
hat.stick.direction_middle = move_dot
hat.stick.direction_any = update_screen
#print('a')
#pause()
start_time=time.time()
for i in range(987654321):
    time.sleep(0.2)
    tdelta = time.time() - start_time
    print(i,  joymenu , "{:.1f}".format( tdelta ) , end="\r"   )
    
#    if joymenu['row'] in (0,):
#        print('red')
    if joymenu['row'] in (1,2,3):
        #                ==0:  nothing happens
        if joymenu['speed']==0:
            save_image( ""  ,  joymenu['row'] )  # 3 means matrix
        if joymenu['speed']==1 and tdelta>100:
            start_time=time.time()
            print('A... ',tdelta)
            save_image( getstamp() ,  joymenu['row'] )  # 3 means matrix
            
        if joymenu['speed']==2 and tdelta>10:
            start_time=time.time()
            print('A... ',tdelta)
            save_image( getstamp()  ,  joymenu['row']  )
           
        if joymenu['speed']==3 and tdelta>1:
            start_time=time.time()
            print('A... ',tdelta)
            save_image( getstamp()  ,  joymenu['row']  )
            
            
            

