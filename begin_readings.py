'''Configures proximity sensor as button to begin sensor readings after Raspberry Pi boot'''

import time
try:
    # Transitional fix for breaking change in LTR559
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
        if button_pressed == True:
            # TODO: start readings


