'''
Automatically pushes latest data readings to git repo when Raspberry Pi is booted and connected to WiFi
File run at startup in /etc/rc.local file
'''

import time
import requests
from git import Repo
from lcd_display import display_text, backlight_off, backlight_on

#time.sleep(20) # delay to allow Raspberry Pi to connect to WiFi and latest changes to be pulled from git repo

while True:
    try: 
        time.sleep(2)
        requests.get('https://www.google.com/') # check if Raspberry Pi is connected to internet (request will cause error if not connected to internet --> except statement triggered)
        repo = Repo('/home/ecoswell/RaspberryPi-Sensor/') # access local git repo
        repo.index.add('**') # stage all files for commit
        repo.index.commit('upload latest data files') # commit all staged files
        origin = repo.remotes.origin # access remote git repo 
        origin.pull () # pull before push to ensure successfull pull
        origin.push() # push all commits to remote git repo
        backlight_on() # turn on LCD backlight
        display_text('Latest version of data\n files uploaded\n to GitHub repo',14) # display git push status on LCD screen
        print('Git push - success')
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        sleep_time = 60 # following successful push sleep for 60 secs
    except:
        backlight_on() # turn on LCD backlight
        display_text('Cannot upload latest\n version of data files \nto GitHub Repo.\nNo internet connection.',13) # display git push status on LCD screen
        print('Git push - fail')
        time.sleep(30)
        display_text('',1)
        backlight_off() # turn off LCD backlight
        sleep_time = 0 # following unsuccessful push sleep for 0 secs
    time.sleep(sleep_time)