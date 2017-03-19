#!/usr/bin/python3

# 5x3 digits for Sense Hat - Demo
# Tony Goodhew 22 September 2015
from sense_hat import SenseHat
import time
import datetime
import random

sense = SenseHat()
sense.clear()

#Global variables

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
hrs = 0
mins = 0

def show_num(val,xd,yd,r,g,b):
    offset = val * 15
    for p in range(offset,offset + 15):
        if nums[p] == 1:
            xt = p % 3
            yt = (p-offset) // 3
            sense.set_pixel(xt+xd,yt+yd,r,g,b)       
    
def show_number(val,r,g,b):
    abs_val = abs(val)
    tens = abs_val // 10
    units = abs_val % 10
    sense.clear()
    if (abs_val > 9): show_num(tens,0,2,r,g,b)
    show_num(units,4,2,r,g,b)
    if abs_val == 100:
        sense.clear()
        show_num(10,3,2,r,g,b) # 'T' for ton = 100
    if val < 0 :
        for i in range(0,8):
            sense.set_pixel(i,0,0,0,128)

def show_time(r,g,b):   
    for i in range(0,10):
        sense.clear()
        tens = hrs // 10
        units = hrs % 10
        show_num(tens,0,2,r,g,b)
        show_num(units,4,2,r,g,b)
        show_colon(7,3)
        time.sleep(0.9)
        sense.clear()
        tens = mins // 10
        units = mins % 10
        show_num(tens,1,2,r,g,b)
        show_num(units,5,2,r,g,b)
        show_colon(0,3)
        time.sleep(0.9)

def show_colon(x,y):
    sense.set_pixel(x,y,128,0,0)
    sense.set_pixel(x,y+2,128,0,0)

def show_block(x,y,r,g,b):
    sense.set_pixel(x,y,0,0,128)
    sense.set_pixel(x+1,y,0,0,128)

def show_large(val,r,g,b): #Range 0 to 399
    orig_val = val
    hundreds = val // 100
    val = val - hundreds * 100
    tens = val // 10
    units = val % 10
    sense.clear()
    if (orig_val > 9): show_num(tens,0,2,r,g,b)
    show_num(units,4,2,r,g,b)
    # Blobs on top line to indicate hundreds
    if hundreds >0: show_block(3,0,0,0,128) #Centre - 100
    if hundreds >1: show_block(0,0,0,0,128) #Right  - 200
    if hundreds >2: show_block(6,0,0,0,128) #Left   - 300

#========== MAIN ===============

print("** Small digits for the Sense HAT **")
print("**  Tony Goodhew -- 22 Sept 2015  **")
print("")

#Counting from -100 to +100
print("Counting from -100 to 100")
print("Can be used for percentages, such as Humidity, or temperatures")
print("")
for i in range(-10,10):
    show_number(i,128,50,30)
    time.sleep(0.2)
    if abs(i) == 100: time.sleep(0.9) # Longer "T"
sense.clear()
print("")

#Display current time HH:MM - alternating HH: & :MM
print("Display current time")
currTime=datetime.datetime.now()
hrs = currTime.hour
mins = currTime.minute
show_time(0,128,30)
sense.clear()
print("")

#15 Random numbers between 0 and 399
print("15 numbers in range 0 to 399 inclusive")
print("Can be used for angles 0 to 360 degrees")
print("")
for i in range(0,13):
    val = random.randint(0,399)
    print(val)
    show_large(val,0,0,128)
    time.sleep(1.7)
    sense.clear()

print(7)
show_large(7,0,0,128) # Suppressed leading zero
time.sleep(1.7)
sense.clear()
print(107)
show_large(107,0,0,128) # Necessary leading zero
time.sleep(1.7)
sense.clear()

print("")
print("Done")
