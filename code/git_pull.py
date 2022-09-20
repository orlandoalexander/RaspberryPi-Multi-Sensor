'''
Automatically pulls latest changes from git repo when Raspberry Pi is booted and connected to WiFi. 
This allows the sensor settings to be modified via the git repo file 'sensor_settings.py'
'''

from git import Repo
import requests
import time
from lcd_display import display_text


time.sleep(10) # delay to allow Raspberry Pi to connect to WiFi

try: 
    requests.get('https://www.google.com/') # check if Raspberry Pi is connected to internet (request will cause error if not connected to internet --> except statement triggered)
    repo = Repo('') # access local git repo (current directory)
    origin = repo.remotes.origin # access remote git repo
    origin.pull() # pull latest changes from git repo to update sensor settings
    git_message = 'Successfully retrieved changes to settings from GitHub Repo'
except:
    git_message = 'Failed to retrieve changes to settings from GitHub Repo\nNo internet connection'

display_text(git_message) # display git pull status on LCD screen

