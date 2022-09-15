'''Edit this file to modify the settings of the sensor'''

'''
ACTIVE SENSORS, FREQUENCY OF DATA RECORDING & DURATION OF DATA RECORDING 

The sensor has the following sensors: 

1. Temperature
2. Pressure
3. Humidity
4. Light
5. Carbon monoxide
6. Nitrogen dioxide
7. Ammonia
8. Particulate matter

Modify the values inside the brackets below for each active sensor with the following format (sensor number, delay between readings (secs), duration of data recording (mins)) - i.e. to measure temperature and ammonia with a time delay between readings of 60 and 120 secs and a data recording duration of 4 hours and 7 hours respectively, you should write [(1,60,240), (7,120,420)]
'''
sensors = [(1,60,240), (7,120,420)]


'''
ADJUST TEMPERATURE TUNING FACTOR

The temperature reading must be adjusted slightly to compensate for the heating effect of the CPU. 
To tweak how much the temperature value is compensated, adjust the variable 'factor' below as required. 
Making the value of 'factor' smaller will shift your compensated temperature further down, and making it larger will shift it back up towards the uncompensated temperaure.
'''
factor = 2.5

# TODO: Clear up and make more concise
