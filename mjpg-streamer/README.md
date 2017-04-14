Compilation and installation of mjpg-streamer on RPi
-----------------------------

https://github.com/jacksonliam/mjpg-streamer


locate is for usage in CAMSON
```
 sudo aptitude install libjpeg8-dev imagemagick libv4l-dev
 sudo aptitude install cmake
 sudo aptitude install locate
 make
 mkdir -p $HOME/bin
 cd ..
 cp  -R mjpg-streamer-experimental ~/bin/
```


