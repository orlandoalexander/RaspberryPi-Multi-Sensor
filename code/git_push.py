# '''
# Automatically pushes latest data readings to git repo when Raspberry Pi is booted and connected to WiFi
# File run at startup as a cron job 
# '''

# import time
# import requests
# from git import Repo
# from lcd_display import display_text, backlight_off, backlight_on

# time.sleep(20) # delay to allow Raspberry Pi to connect to WiFi and latest changes to be pulled from git repo

# while True:
#     try: 
#         time.sleep(2)
#         requests.get('https://www.google.com/') # check if Raspberry Pi is connected to internet (request will cause error if not connected to internet --> except statement triggered)
#         repo = Repo('/home/ecoswell/RaspberryPi-Sensor/') # access local git repo
#         repo.index.add('**') # stage all files for commit
#         repo.index.commit('upload latest data files') # commit all staged files
#         origin = repo.remotes.origin # access remote git repo 
#         origin.pull () # pull before push to ensure successfull pull
#         origin.push() # push all commits to remote git repo
#         print('Git push - success')
#         sleep_time = 60 # following successful push sleep for 60 secs
#     except:
#         print('Git push - fail')
#         sleep_time = 0 # following unsuccessful push sleep for 0 secs
#     time.sleep(sleep_time)