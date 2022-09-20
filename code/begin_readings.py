'''Configures proximity sensor as button to begin sensor readings after Raspberry Pi boot'''

import sys
path = '/home/ecoswell/RaspberryPi-Sensor' # path to folder storing 'sensor_settings' module
sys.path.append(path) # enable importing module ('sensor_settings') from outside directory
import os
import time
import threading
from sensor_readings import SensorReadings
from lcd_display import display_text


try:
    # transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559() # initialise LTR559 light/proximity sensor
except ImportError:
    import ltr559

display_text('Sensor booting...') # display boot message on sensor LCD 
#time.sleep(5)
display_text('Welcome!') 

while True: 
    proximity = ltr559.get_proximity() # get proximity above proximity sensor
    if proximity > 1500: # if proximity crosses threshold, indicates that user has put finger on proximity sensor (i.e. starts pressing 'button')
        stime = time.time() # initial time when user put finger on proximity sensor
        button_pressed = True
        while time.time() - stime < 5: # loop for 5 seconds, checking whether user's finger is still on proximity sensor
            if proximity < 1000: # if user takes finger off proxmity sensor (i.e. stops pressing 'button')
                button_pressed = False
                break
            else:
                pass
        if button_pressed == True and threading.active_count() <= 1: # if user has held finger on proximity sensor for at least 5 seconds (i.e. pressed button to start sensor readings) and no other threads are currently active (i.e. sensor not currently taking readings)
            display_text('Sensor readings starting in 2 minutes') # display status message on LCD 
            #time.sleep(120) # delay to allow user to place sensor in desired location to take readings
            sensor_thread = threading.Thread(target=SensorReadings().main) # create new thread to take sensor readings in background
            sensor_thread.start() # start background thread to take sensor readings
            break
        elif button_pressed == True and threading.active_count() > 1: # if user has held finger on proximity sensor for at least 5 seconds (i.e. pressed button to start sensor readings) and another thread is currently active (i.e. sensor is currently taking readings)
            print('Rebooting')
            display_text('Sensor currently active!\nContinue to hold for 10 seconds to reboot sensor')
            while time.time() - stime < 15: # continue looping for 15 seconds after user first pressed proximity sensor, checking whether user's finger is still on proximity sensor
                if proximity < 1000: # if user takes finger off proxmity sensor (i.e. stops pressing 'button')
                    button_pressed = False
                    break
                else:
                    pass
            if button_pressed == True: # if user held proximity sensor for 15 seconds in total
                display_text('Sensor rebooting...') # display status message on LCD 
                time.sleep(5)
                #os.system("sudo reboot") # reboot Raspberry Pi
            else:
                display_text('Sensor will continue to take readings') # display status message on LCD 


