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

Modify the values inside the brackets below for each active sensor with the following format 
(sensor number, delay between readings (secs), duration of data recording (mins)) 
i.e. to measure temperature and ammonia with a time delay between readings of 60 and 120 secs 
and a data recording duration of 4 hours and 7 hours respectively, you should write [(1,60,240), (7,120,420)]
'''
sensors = [(6,5,0.5)]


'''
ADJUST TEMPERATURE TUNING FACTOR

The temperature reading must be adjusted slightly to compensate for the heating effect of the CPU (computer processing unit on the sensor). 
To determine the factor required to correctly compensate the tenmperature reading, 
set 'calibrate_factor' to 'True' and follow the instructions in the documentation.

'''
factor = 1.31
calculate_factor = False

