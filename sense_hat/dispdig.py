#!/usr/bin/python3
# This file has been written to your home directory for convenience. It is
# saved as "/home/pi/sensor_menu-2017-03-18-17-25-56.py"

import sys # arguments
print( str(sys.argv) )

import os

from sense_hat import *
import time
import numpy as np

import subprocess

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
    if (abs_val > 9): show_num(tens,0,2,r,g,b)
    show_num(units,4,2,r,g,b)
    if abs_val == 100:
        hat.clear()
        show_num(10,3,2,r,g,b) # 'T' for ton = 100
    if val < 0 :
        for i in range(0,8):
            #hat.set_pixel(i,0,0,0,128)
            hat.set_pixel(i,0, r,g ,b)

################################################
#
#  from tony Goodhew
#
################################################
tcal=0.0
trpi=0.0
# Draw the foreground (fg) into a numpy array
Rd = (255, 0, 0)
Gn = (0, 255, 0)
Bl = (0, 0, 255)
Gy = (128, 128, 128)
__ = (0, 0, 0)
fg = np.array([
    [Rd, Rd, Rd, __, Gn, Gn, __, __],
    [__, Rd, __, __, Gn, __, Gn, __],
    [__, Rd, __, __, Gn, Gn, __, __],
    [__, Rd, __, __, Gn, __, __, __],
    [Bl, __, Bl, __, __, Gy, __, __],
    [Bl, Bl, Bl, __, Gy, __, Gy, __],
    [Bl, __, Bl, __, Gy, __, Gy, __],
    [Bl, __, Bl, __, __, Gy, Gy, __],
    ], dtype=np.uint8)
# Mask is a boolean array of which pixels are transparent
mask = np.all(fg == __, axis=2)



def get_cpu_t():
    global trpi
    #cpuTemp0
    proc=subprocess.Popen('cat /sys/class/thermal/thermal_zone0/temp'.split(),stdout=subprocess.PIPE )
    out,err=proc.communicate()
    tcpu=int( out.decode('utf') )
    
    tcpu=tcpu/1000
    #tcpu=tcpu/1000+( tcpu/100 % tcpu/1000)/1000
#    print(tcpu)
    
    #gpuTemp
    proc=subprocess.Popen('/opt/vc/bin/vcgencmd measure_temp'.split(),stdout=subprocess.PIPE )
    out,err=proc.communicate()
    tgpu=float( out.decode('utf')[5:-3] )
    trpi= (tcpu+tgpu)/2
    print( "TCPU=",tcpu, "TGPU=",tgpu, end="" )
    return trpi




def display(hat, selection):
    # Draw the background (bg) selection box into another numpy array
    left, top, right, bottom = {
        'T': (0, 0, 4, 4),
        'P': (4, 0, 8, 4),
        'Q': (4, 4, 8, 8),
        'H': (0, 4, 4, 8),
        }[selection]
    bg = np.zeros((8, 8, 3), dtype=np.uint8)
    bg[top:bottom, left:right, :] = (255, 255, 255)
    # Construct final pixels from bg array with non-transparent elements of
    # the menu array
    hat.set_pixels([
        bg_pix if mask_pix else fg_pix
        for (bg_pix, mask_pix, fg_pix) in zip(
            (p for row in bg for p in row),
            (p for row in mask for p in row),
            (p for row in fg for p in row),
            )
        ])

def execute(hat, selection):
    global tcal
    speed=0.08
    if selection == 'T':
        trpi=get_cpu_t()
        
        tcal = hat.temp - (( trpi - hat.temp)/5.466)
        # ht - trpi/5.466 + ht/5.466
        # 
        #hat.show_message('T %.f' % tcal , speed , Rd)
        show_number( int(tcal),180,0,0)
        time.sleep(2)
        hat.clear()
        show_number( int(hat.temp),50,00,0)
        time.sleep(0.5)
        hat.clear()
        show_number( int(trpi),60,60,50)
        time.sleep(0.5)
        hat.clear()
        show_number( int(tcal),180,0,0)
        time.sleep(2)
        hat.clear()
        show_number( int(hat.temp),50,0,0)
        time.sleep(0.5)
        hat.clear()
        show_number( int(trpi),60,60,50)
        time.sleep(0.5)
        hat.clear()
        print("   Calibr={:.1f}".format( tcal ) )
    elif selection == 'P':
        hat.show_message('%.f' % hat.pressure, speed, Gn)
    elif selection == 'H':
        #hat.show_message('%.f%%' % hat.humidity, speed, Bl)
        show_number( int(hat.humidity), 0,0,180)
        time.sleep(3)
        hat.clear()
    else:
        return True
    return False

def move(selection, direction):
    return {
        ('T', DIRECTION_RIGHT): 'P',
        ('T', DIRECTION_DOWN):  'H',
        ('P', DIRECTION_LEFT):  'T',
        ('P', DIRECTION_DOWN):  'Q',
        ('Q', DIRECTION_UP):    'P',
        ('Q', DIRECTION_LEFT):  'H',
        ('H', DIRECTION_RIGHT): 'Q',
        ('H', DIRECTION_UP):    'T',
        }.get((selection, direction), selection)

####################################
#
# MAIN
#
#######################################
#quit();
if len(sys.argv)>1:
    numero=int(sys.argv[1])
else:
    numero=88
from subprocess import Popen
Popen( "echo "+str(numero)+" >/tmp/TEMPOUT_ACTUAL", shell=True )    

#hat = SenseHat()
selection = 'T'

#os.stat('/tmp/TEMPOUT_ACTUAL')
#print( stat.st_birthtime )
quit()

for i in range(3):
    show_number( numero ,180,0,0)
    #display(hat, selection)
    #execute(hat,'T')
    #time.sleep(0.2)
    #execute(hat,'H')
    #time.sleep(0.2)
    time.sleep(7)
    hat.clear()
    time.sleep(1)
quit()
########################################## QUIT

import os
import datetime
with open('/home/pi/sense_hat.log','a') as f:
    f.write("# {}\n".format(datetime.datetime.now() )  )
    f.write( "{:%s} ".format(datetime.datetime.now() ) )
    f.write("{:5.1f} {:5.1f} {:5.1f}   {:5.1f} {:7.1f}\n".format(tcal, hat.temp, trpi,
                                                                hat.humidity,hat.pressure) )
    f.close()
#    execute(hat,'P')
#    time.sleep(0.2)
    #event = hat.stick.wait_for_event()
    #if event.action == ACTION_PRESSED:
    #    if event.direction == DIRECTION_MIDDLE:
    #        if execute(hat, selection):
    #            break
    #    else:
    #        selection = move(selection, event.direction)
hat.clear()

