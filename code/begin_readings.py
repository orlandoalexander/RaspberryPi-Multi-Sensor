'''
Configures proximity sensor as button to begin sensor readings after Raspberry Pi boot
File run at startup as a cron job 
'''

import sys
path = '/home/ecoswell/RaspberryPi-Sensor' # path to folder storing 'sensor_settings' module
sys.path.append(path) # enable importing module ('sensor_settings') from outside directory
import os
import time
import threading
from sensor_readings import SensorReadings
from lcd_display import display_text, backlight_off, backlight_on


try:
    # transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559() # initialise LTR559 light/proximity sensor
except ImportError:
    import ltr559

os.system("sudo python3 git_pull.py")

display_text('Sensor booting...', 19) # display boot message on sensor LCD 
time.sleep(10)
display_text('Welcome!', 30) 

while True: 
    proximity = ltr559.get_proximity() # get proximity above proximity sensor
    if proximity > 1500: # if proximity crosses threshold, indicates that user has put finger on proximity sensor (i.e. starts pressing 'button')
        stime = time.time() # initial time when user put finger on proximity sensor
        button_pressed = True
        backlight_on() # turn on LCD backlight
        while time.time() - stime < 5: # loop for 5 seconds, checking whether user's finger is still on proximity sensor
            proximity = ltr559.get_proximity() # get proximity above proximity sensor
            if proximity < 1000: # if user takes finger off proxmity sensor (i.e. stops pressing 'button')
                button_pressed = False
                break
            else:
                pass
        if button_pressed == True and threading.active_count() <= 1: # if user has held finger on proximity sensor for at least 5 seconds (i.e. pressed button to start sensor readings) and no other threads are currently active (i.e. sensor not currently taking readings)
            display_text('Sensor readings\n starting in 2 mins',18) # display status message on LCD 
            #time.sleep(5) # TODO delay to allow user to place sensor in desired location to take readings
            display_text('Sensor readings\n have started',20)
            sensor_thread = threading.Thread(target=SensorReadings().main) # create new thread to take sensor readings in background
            sensor_thread.start() # start background thread to take sensor readings
            time.sleep(10) 
            display_text('',1)
            backlight_off() # turn off LCD backlight
        elif button_pressed == True and threading.active_count() > 1: # if user has held finger on proximity sensor for at least 5 seconds (i.e. pressed button to start sensor readings) and another thread is currently active (i.e. sensor is currently taking readings)
            display_text('Sensor currently active!\nContinue to hold for 20\n to reboot sensor.',13)
            while time.time() - stime < 25: # continue looping for 25 seconds after user first pressed proximity sensor, checking whether user's finger is still on proximity sensor
                proximity = ltr559.get_proximity() # get proximity above proximity sensor
                if proximity < 1000: # if user takes finger off proxmity sensor (i.e. stops pressing 'button')
                    button_pressed = False
                    break
                else:
                    pass
            if button_pressed == True: # if user held proximity sensor for 25 seconds in total
                display_text('Sensor rebooting...',17) # display status message on LCD 
                time.sleep(5)
                #os.system("sudo reboot") # reboot Raspberry Pi
            else:
                display_text('Reboot cancelled.\nSensor will continue\n with readings.',16) # display status message on LCD 
                time.sleep(5)
                display_text('',1)
                backlight_off() # turn off LCD backlight


