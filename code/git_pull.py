'''
Automatically pulls latest changes from git repo when Raspberry Pi is booted and connected to WiFi
This allows the sensor settings to be modified via the git repo file 'sensor_settings.py'
File run at startup as a cron job 
'''

from git import Repo
import requests
import time
from lcd_display import display_text, backlight_off, backlight_on


time.sleep(10) # delay to allow Raspberry Pi to connect to WiFi

try: 
    requests.get('https://www.google.com/') # check if Raspberry Pi is connected to internet (request will cause error if not connected to internet --> except statement triggered)
    repo = Repo('/home/ecoswell/RaspberryPi-Sensor/') # access local git repo
    origin = repo.remotes.origin # access remote git repo
    origin.pull() # pull latest changes from git repo to update sensor settings
    backlight_on() # turn on LCD backlight
    display_text('Successfully retrieved\n sensor changes \nfrom Github repo',15) # display status message on LCD 
    time.sleep(30)
    display_text('',1)
    backlight_off() # turn off LCD backlight
    print('Git pull - success')
except:
    backlight_on() # turn on LCD backlight
    display_text('Failed to retrieve\nsensor changes from \nGitHub repo.\nNo internet connection.',13) # display status message on LCD 
    time.sleep(30)
    display_text('',1)
    backlight_off() # turn off LCD backlight
    print('Git pull - fail')

