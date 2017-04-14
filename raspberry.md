Prepare HDMI autotart and resolution  in /boot/config.txt
-------------------------------------------------


see: https://www.raspberrypi.org/documentation/configuration/config-txt.md

This shows current setting:
```
vcgencmd get_config int
```

This worked for me - 1024x768
```
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=16
```

```
# hdmi_safe .... uncommenting will CAUSE 640x480 etc...
# Force the monitor to HDMI mode so that sound will be sent over HDMI cable
hdmi_force_hotplug=1

hdmi_drive=2
# Set monitor mode to DMT
hdmi_group=2
# Set monitor resolution to 1024x768 XGA 60Hz (HDMI_DMT_XGA_60)
hdmi_mode=0x10
# Make display smaller to stop text spilling off the screen
#overscan_left=20
#overscan_right=12
#overscan_top=10
#overscan_bottom=10
```

remark ... 2/0x10 ... try for 1024x768

`tvservice -s` will tell current mode


https://www.raspberrypi.org/forums/viewtopic.php?t=5851

```
1. Run “tvservice –m CEA” to give a list of CEA supported modes.
2. Run “tvservice –m DMT” to give a list of DMT supported modes.
```

 Locale and others
---------------------

1/ Locale  en_US.UTF8

2/ timezone PRAGUE

3/ keyboard generic 105 ,  english US

4/ wifi cz

5/ ssh on

6/ hostname

**reboot**

1/ wifi signal

   sudo iwlist wlan0 scan

2/ aptitude update; aptitude install libusb-1.0-0-dev

  and phidgets

3/ aptitude -y upgrade

4/ aptitude install mc htop git screen sqlite3 mysql-client nc


 Install phidgets code from git
----------------------------------




 Better streaming solution from linuxjournal 
 --------------------------------------------
 http://www.linuxjournal.com/content/better-raspberry-pi-streaming-solution
 

add to /etc/apt/sources.list
```
deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ wheezy main
```

```
curl http://www.linux-projects.org/listing/uv4l_repo/lrkey.asc | sudo apt-key add -
```

Once that is done, simply install the program:

```
 aptitude install uv4l uv4l-raspicam \
uv4l-raspicam-extras uv4l-server uv4l-uvc uv4l-xscreen \
uv4l-mjpegstream uv4l-dummy

 aptitude install uv4l-webrtc
```

to run try this

```
/usr/bin/uv4l -nopreview --auto-video_nr --driver raspicam --encoding jpeg --quality 90 --metering matrix --drc low --width 1280 --height 720 --framerate 10 --server-option '--port=8080' --server-option '--max-queued-connections=10' --server-option '--max-streams=5' --server-option '--max-threads=15'
```
These things make uv4l runnig from start. Not very clear now....



PYTHON
-----------
```
pyserial
numpy
pandas
staticmap
pathos
http.server
#  after reboot
pandas
sensehat
```


WIFI
--------

dhcpcd.conf .. line :
```
SSID drakula5
inform 192.168.0.17
static routers=192.168.0.1
static domain_name_servers=8.8.8.8
```
What pi's?
```
pim  10 mobile
pi   11 old dead
pi4  12 
pi3  13 vrata
pib  14 gar
pix1 15 ?
pix2 16 new pi - sounds, hat
pix3 17 hat and reserve for organ
```
