'''Automatically pushes latest data readings to git repo when Raspberry Pi is booted and connected to WiFi.'''

import time
import requests
from git import Repo
from lcd_display import display_text

#time.sleep(20) # delay to allow Raspberry Pi to connect to WiFi and latest changes to be pulled from git repo

#while True:
    #try: 
requests.get('https://www.google.com/') # check if Raspberry Pi is connected to internet (request will cause error if not connected to internet --> except statement triggered)
repo = Repo('/home/ecoswell/RaspberryPi-Sensor/') # access local git repo
repo.index.add('**') # stage all files for commit
repo.index.commit('upload latest data files') # commit all staged files
origin = repo.remotes.origin # access remote git repo 
origin.push() # push all commits to remote git repo
git_message = 'Latest version of data files will be uploaded to GitHub Repo every 60s'
    #except:
        #git_message = 'Cannot upload latest version of data files to GitHub Repo\nNo internet connection' 
    #display_text(git_message) # display git push status on LCD screen
    #time.sleep(60)