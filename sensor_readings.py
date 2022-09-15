'''Take measurements of desired environmental factors and save data to CSV file'''

import sensor_settings
import sys
import time
import threading
import os.path
import csv
from datetime import date, datetime
from lcd_display import display_text


try:
    # transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559() # initialise LTR559 light/proximity sensor
except ImportError:
    import ltr559
from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas

bme280 = BME280() # initialise BME280 temperature/pressure/humidity sensor
pms5003 = PMS5003() # intitialise PMS5003 particulate sensor



class SensorReadings(): # class containing methods to take sensor readings
    def __init__(self):
        now = datetime.now() # get current date and time
        self.date = now.strftime("%d/%m/%Y") # get date when sensor readings begin in correct format
        self.time = now.strftime("%H:%M:%S") # get time when sensor readings begin in current format
        self.sensors = sensor_settings.sensors # access sensor settings defined by user in file 'sensor_settings.py' 
        self.factor = sensor_settings.factor # adjust factor by which temperature reading is compensated
        self.sensors_dict = {1:self.temp_queue(), 2:self.pressure_queue(), 3:self.humidity_queue(), 4:self.light_queue(), 5:self.co_queue(), 6:self.no2_queue(), 7:self.nh3_queue(), 8:self.pm_queue()} # dictionary to translate between sensor number and sensor queue method (which triggers sensor execution)
        self.queue = [] # queue stores sensors which are due to take readings - this avoids multiple sensors taking readings simultaneously and therefore prevents collisions

    def get_cpu_temperature(self): # get the temperature of the CPU for compensation
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = f.read()
                temp = int(temp) / 1000.0
            return temp

    def temp_queue(self, freq): # appends 'temp' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        threading.Timer(freq, self.temp).start() # recursively call 'temp' method at frequency specified by 'freq' to take readings at desired frequency
        self.queue.append(self.temp())

    def temp(self): # measure temperature
        sensor = 'temp'
        freq = list(filter(lambda x: x[0] == 1, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for temperature sensor (sensor number 1)
        data_heading = ['Temperature (C)']
        cpu_temp = self.get_cpu_temperature() # get current CPU temperature
        cpu_temps = cpu_temps[1:] + [cpu_temp] # remove oldest reading of CPU temp and append latest reading of CPU temp to 'cpu_temps'
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps)) # get average of CPU temp to decrease jitter
        raw_temp = bme280.get_temperature() # get raw reading of temp
        compensated_temp = raw_temp - ((avg_cpu_temp - raw_temp) / self.factor) # temp value ajdusted to compensate for CPU heating
        data = [compensated_temp]
        self.save_data(sensor, freq, data, data_heading)
        return

    def pressure_queue(self, freq): # appends 'pressure' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        threading.Timer(freq, self.pressure).start() # recursively call 'pressure' method at frequency specified by 'freq' to take readings at desired frequency
        self.queue.append(self.pressure())

    def pressure(self): # measure pressue
        sensor = 'pressure'
        freq = list(filter(lambda x: x[0] == 2, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for pressure sensor (sensor number 2)
        data_heading = ['Pressure (hPa)']
        pressure = bme280.get_pressure() # get reading of pressure
        data = [pressure]
        self.save_data(sensor, freq, data, data_heading)
        return

    def humidity_queue(self, freq): # appends 'humidity' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        threading.Timer(freq, self.humidity).start() # recursively call 'humidity' method at frequency specified by 'freq' to take readings at desired frequency
        self.queue.append(self.humidity())

    def humidity(self): # measure humidiity
        sensor = 'humidity'
        freq = list(filter(lambda x: x[0] == 3, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for humidity sensor (sensor number 3)
        data_heading = ['Humidity (%)']
        humidity = bme280.get_humidity() # get reading of humidity
        data = [humidity]
        self.save_data(sensor, freq, data, data_heading)
        return

    def light_queue(self, freq): # appends 'light' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        threading.Timer(freq, self.light).start() # recursively call 'light' method at frequency specified by 'freq' to take readings at desired frequency
        self.queue.append(self.light())

    def light(self): # measure light intensity
        sensor = 'light'
        freq = list(filter(lambda x: x[0] == 4, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for light sensor (sensor number 4)
        data_heading = ['Light (lux)']
        proximity = ltr559.get_proximity() # get reading of proximity
        if proximity < 10: # no object near the sensor (small values of proximity indicate greater proximity)
            light = ltr559.get_lux() # get reading of light intensity
        else: # larger value of proximity --> closer proximity --> object near the sensor --> cannot take reading of light intensity
            light = 1 # dark
        data = [light]
        self.save_data(sensor, freq, data, data_heading)
        return


    def co_queue(self, freq): # appends 'co' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        threading.Timer(freq, self.co).start() # recursively call 'co' method at frequency specified by 'freq' to take readings at desired frequency
        self.queue.append(self.co())

    def co(self): # measures concentration of carbon monoxide (reducing) gas
        sensor = 'co'
        freq = list(filter(lambda x: x[0] == 5, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for carbon monoxide sensor (sensor number 5)
        data_heading = ['Carbon monoxide (k0)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        co = gas_data.reducing / 1000 # convert carbon monoxide gas concentration from resistance to ppm
        data = [co]
        self.save_data(sensor, freq, data, data_heading)
        return

    def no2_queue(self, freq): # appends 'no2' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        threading.Timer(freq, self.no2).start() # recursively call 'no2' method at frequency specified by 'freq' to take readings at desired frequency
        self.queue.append(self.no2())

    def no2(self): # measures concentration of nitrogen dioxide (oxidising) gas
        sensor = 'no2'
        freq = list(filter(lambda x: x[0] == 6, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for nitrogen dioxide sensor (sensor number 6)
        data_heading = ['Nitrogen dioxide (k0)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        no2 = gas_data.oxidising / 1000 # convert nitrogen dioxide gas concentration from resistance to ppm
        data = [no2]
        self.save_data(sensor, freq, data, data_heading)
        return

    def nh3_queue(self, freq): # appends 'nh3' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        threading.Timer(freq, self.nh3).start() # recursively call 'nh3' method at frequency specified by 'freq' to take readings at desired frequency
        self.queue.append(self.nh3())

    def nh3(self): # measures concentration of ammonia gas
        sensor = 'nh3'
        freq = list(filter(lambda x: x[0] == 7, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for ammonia sensor (sensor number 7)
        data_heading = ['Ammonia (k0)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        nh3 = gas_data.nh3 / 1000 # convert ammonia gas concentration from resistance to ppm
        data = [nh3]
        self.save_data(sensor, freq, data, data_heading)
        return

    def pm_queue(self, freq): # appends 'pm' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        threading.Timer(freq, self.pm).start() # recursively call 'pm' method at frequency specified by 'freq' to take readings at desired frequency
        self.queue.append(self.pm())

    def pm(self): # measures concentration of PM1.0, PM2.5 and PM10 particulate matter
        sensor = 'pm'
        freq = list(filter(lambda x: x[0] == 8, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for pm sensor (sensor number 8)
        data_heading = ['PM1.0 (ug/m3)','PM2.5 (ug/m3)', 'PM10 (ug/m3)']
        try:
            data = pms5003.read() # get readings of concentration of PM1.0, PM2.5 and PM10 particulate matter
        except pmsReadTimeoutError:
            display_text('Failed to read PMS5003')
            pass
        else:
            pm1 = float(data.pm_ug_per_m3(1.0)) # get readings of concentration of PM1.0
            pm25 = float(data.pm_ug_per_m3(2.5)) # get readings of concentration of PM2.5
            pm10 = float(data.pm_ug_per_m3(10)) # get readings of concentration of PM10
            data = [pm1,pm25,pm10]
            self.save_data(sensor, freq, data, data_heading)
        return

    def save_data(self, sensor, freq, data, data_heading): # save sensor data to CSV file
        filename = sensor+'-'+self.date+'-'+self.time+'.csv' # filename stores sensor type and current date
        file_exists = False
        if os.path.isfile(f'data/{filename}'): # if CSV file storing data for 'sensor' already exists
            file_exists = True
        f = open(f'data/{filename}', 'a') # create/open CSV file to store data for 'sensor'
        writer = csv.writer(f)
        if not file_exists: # if CSV file storing data for 'sensor' has just been created
            heading = ['Date', 'Time'] + data_heading # enables unlimited number of data headings as 'data_heading' stores an array of each data heading (applicable as pm sensor takes three readings (PM1.0, PM2.5 and PM10), whereas all other sensor only take one reading)
            writer.writerow(['Frequency(sec)',freq]) # record frequency of sensor readings
            writer.writerow(['']) # empty row
            writer.writerow(heading) # write headings to file
        row = [data, time] + data # enables unlimited number of data readings to be stored as 'data' stores an array of each data reading (applicable as pm sensor takes three readings (PM1.0, PM2.5 and PM10), whereas all other sensor only take one reading)
        writer.writerow(row) # write current date, current time, data reading to file
        f.close() # close file
 
    def dequeue(self): # remove each queued sensor reading from the queue and execute the sensor reading, avoiding multiple sensors taking readings simultaneously  
        while True:
            if len(self.queue) >= 1: # if there are sensors readings to be taken
               self.queue.pop(0) # execute reading for front sensor in queue and remove sensor from queue
               time.sleep(1) # 1 second delay between each sensor reading

    def main(self): # control operation of active sensors
        queue_thread = threading.Thread(target=self.dequeue) # run queue in background thread
        queue_thread.start()
        for sensor in self.sensors: # iterate through active sensors as defined by user in 'sensor_settings.py'
            sensor_num, sensor_freq = sensor[0], sensor[1] # first element in tuple stores sensor number, second element stores reading frequency for sensor 
            sensor_method = self.sensors_dict[sensor_num] # lookup sensor method that is associated with the sensor number ('sensor_num') using 'sensors_dict'
            sensor_method(sensor_freq) # call method to executed readings for desired sensor, passing the frequency (secs) at which readings should be taken








# TODO: 10 min delay before gas readings to allow time to stabalise