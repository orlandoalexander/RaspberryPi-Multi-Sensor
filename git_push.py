'''Automatically pushes latest data readings to git repo when Raspberry Pi is booted and connected to WiFi.'''

import subprocess
import time
from lcd_display import display_text

boot_text = 'Sensor booting...'
display_text(boot_text) # display boot message on sensor LCD

time.sleep(10) # delay to allow Raspberry Pi to connect to WiFi

try: 
    url.urlopen('http://google.com') # checks if Raspberry Pi is connected to WiFi
    subprocess.run(["git", "pull"], check=True, stdout=subprocess.PIPE).stdout # pull latest changes from git repo to update sensor settings
    git_message = 'Duccessfully retrieved latest changes from GitHub Repo'
except:
    git_message = 'No internet connection --> failed to retrieve latest changes from GitHub Repo'