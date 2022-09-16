'''Configures proximity sensor as button to begin sensor readings after Raspberry Pi boot'''

import sys
path = '/Users/orlandoalexander/Library/Mobile Documents/com~apple~CloudDocs/Documents/South America/EcoSwell/RaspberryPi-Sensor/RaspberryPi-Sensor' # path to folder storing 'sensor_settings' module
sys.path.append(path) # enable importing module ('sensor_settings') from outside directory
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
            display_text('Sensor readings starting in 2 minutes')
            time.sleep(120)
            sensor_thread = threading.Thread(target=SensorReadings().main) # create new thread to take sensor readings in background
            sensor_thread.start() # start background thread to take sensor readings
        elif button_pressed == True and threading.active_count() > 1: # if user has held finger on proximity sensor for at least 5 seconds (i.e. pressed button to start sensor readings) and another thread is currently active (i.e. sensor is currently taking readings)
            display_text('Sensor currently active!\nPlease reboot Raspberry Pi to restart sensor readings')


