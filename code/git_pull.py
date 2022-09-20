'''
Automatically pulls latest changes from git repo when Raspberry Pi is booted and connected to WiFi. 
This allows the sensor settings to be modified via the git repo file 'sensor_settings.py'
'''

from git import Repo
import requests
import time
from lcd_display import display_text


#time.sleep(10) # delay to allow Raspberry Pi to connect to WiFi

try: 
    requests.get('https://www.google.com/') # check if Raspberry Pi is connected to internet (request will cause error if not connected to internet --> except statement triggered)
    repo = Repo('/home/ecoswell/RaspberryPi-Sensor/') # access local git repo
    origin = repo.remotes.origin # access remote git repo
    origin.pull() # pull latest changes from git repo to update sensor settings
    display_text('Successfully retrieved\n sensor changes \nfrom Github repo',15) # display status message on LCD 
    print('Git pull - success')
except:
    display_text('Failed to retrieve\nsensor changes from \nGitHub repo.\nNo internet connection.',13) # display status message on LCD 
    print('Git pull - fail')

