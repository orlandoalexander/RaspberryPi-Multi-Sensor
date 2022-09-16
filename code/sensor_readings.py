'''Take measurements of desired environmental factors and save data to CSV file'''

import sys
path = '/Users/orlandoalexander/Library/Mobile Documents/com~apple~CloudDocs/Documents/South America/EcoSwell/RaspberryPi-Sensor/RaspberryPi-Sensor' # path to folder storing 'sensor_settings' module
sys.path.append(path) # enable importing module ('sensor_settings') from outside directory
import sensor_settings
import time
import threading
import os.path
import csv
from datetime import datetime
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
        self.time = now.strftime("%H:%M:%S") # get time when sensor readings begin in correct format
        self.sensors = sensor_settings.sensors # access sensor settings defined by user in file 'sensor_settings.py' 
        self.factor = sensor_settings.factor # adjust factor by which temperature reading is compensated
        self.sensors_dict = {1:self.temp_queue(), 2:self.pressure_queue(), 3:self.humidity_queue(), 4:self.light_queue(), 5:self.co_queue(), 6:self.no2_queue(), 7:self.nh3_queue(), 8:self.pm_queue()} # dictionary to translate between sensor number and sensor queue method (which triggers sensor execution)
        self.queue = [] # queue stores sensors which are due to take readings - this avoids multiple sensors taking readings simultaneously and therefore prevents collisions
        self.sensor_status = [False for i in range(8)] # queue stores status of each sensor (True = active, False = inactive)

    def get_cpu_temperature(self): # get the temperature of the CPU for compensation
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = f.read()
                temp = int(temp) / 1000.0
            return temp

    def temp_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'temp' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.temp()) # add 'temp' method to 'queue' at set intervals to take sensor readings at desired frequency
        display_text('Temperature readings complete') # display sensor reading status on LCD once all readings are complete
        self.sensor_status[0] = False # change temp sensor status to False (i.e. inactive) as all readings are now complete
        return

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

    def pressure_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'pressure' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.pressure()) # add 'pressure' method to 'queue' at set intervals to take sensor readings at desired frequency
        display_text('Pressure readings complete') # display sensor reading status on LCD once all readings are complete
        self.sensor_status[1] = False # change pressure sensor status to False (i.e. inactive) as all readings are now complete
        return

    def pressure(self): # measure pressue
        sensor = 'pressure'
        freq = list(filter(lambda x: x[0] == 2, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for pressure sensor (sensor number 2)
        data_heading = ['Pressure (hPa)']
        pressure = bme280.get_pressure() # get reading of pressure
        data = [pressure]
        self.save_data(sensor, freq, data, data_heading)
        return

    def humidity_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'humidity' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.humidity()) # add 'humidity' method to 'queue' at set intervals to take sensor readings at desired frequency
        display_text('Humidity readings complete') # display sensor reading status on LCD once all readings are complete
        self.sensor_status[2] = False # change humidity sensor status to False (i.e. inactive) as all readings are now complete
        return

    def humidity(self): # measure humidiity
        sensor = 'humidity'
        freq = list(filter(lambda x: x[0] == 3, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for humidity sensor (sensor number 3)
        data_heading = ['Humidity (%)']
        humidity = bme280.get_humidity() # get reading of humidity
        data = [humidity]
        self.save_data(sensor, freq, data, data_heading)
        return

    def light_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'light' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.light()) # add 'light' method to 'queue' at set intervals to take sensor readings at desired frequency
        display_text('Light readings complete') # display sensor reading status on LCD once all readings are complete
        self.sensor_status[3] = False # change light sensor status to False (i.e. inactive) as all readings are now complete
        return 

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

    def co_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'co' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.co()) # add 'co' method to 'queue' at set intervals to take sensor readings at desired frequency
        display_text('Carbon monoxide readings complete') # display sensor reading status on LCD once all readings are complete
        self.sensor_status[4] = False # change co sensor status to False (i.e. inactive) as all readings are now complete
        return 

    def co(self): # measures concentration of carbon monoxide (reducing) gas
        sensor = 'co'
        freq = list(filter(lambda x: x[0] == 5, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for carbon monoxide sensor (sensor number 5)
        data_heading = ['Carbon monoxide (k0)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        co = gas_data.reducing / 1000 # convert carbon monoxide gas concentration from resistance to ppm
        data = [co]
        self.save_data(sensor, freq, data, data_heading)
        return
    
    def no2_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'no2' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.no2()) # add 'no2' method to 'queue' at set intervals to take sensor readings at desired frequency
        display_text('Nitrogen dioxide readings complete') # display sensor reading status on LCD once all readings are complete
        self.sensor_status[5] = False # change no2 sensor status to False (i.e. inactive) as all readings are now complete
        return 

    def no2(self): # measures concentration of nitrogen dioxide (oxidising) gas
        sensor = 'no2'
        freq = list(filter(lambda x: x[0] == 6, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for nitrogen dioxide sensor (sensor number 6)
        data_heading = ['Nitrogen dioxide (k0)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        no2 = gas_data.oxidising / 1000 # convert nitrogen dioxide gas concentration from resistance to ppm
        data = [no2]
        self.save_data(sensor, freq, data, data_heading)
        return
    
    def nh3_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'nh3' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.nh3()) # add 'nh3' method to 'queue' at set intervals to take sensor readings at desired frequency
        display_text('Ammonia readings complete') # display sensor reading status on LCD once all readings are complete
        self.sensor_status[6] = False # change nh3 sensor status to False (i.e. inactive) as all readings are now complete
        return 
        
    def nh3(self): # measures concentration of ammonia gas
        sensor = 'nh3'
        freq = list(filter(lambda x: x[0] == 7, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for ammonia sensor (sensor number 7)
        data_heading = ['Ammonia (k0)']
        gas_data = gas.read_all() # get readings of concentration of all gasses
        nh3 = gas_data.nh3 / 1000 # convert ammonia gas concentration from resistance to ppm
        data = [nh3]
        self.save_data(sensor, freq, data, data_heading)
        return

    def pm_queue(self, freq, dur, stime): # calls 'queue_op' method with appropriate parameters to add 'pm' method to 'queue' at set intervals to take sensor readings at desired frequency
        self.queue_op(freq, dur, stime, self.pm()) # add 'pm' method to 'queue' at set intervals to take sensor readings at desired frequency
        display_text('Particulate matter readings complete') # display sensor reading status on LCD once all readings are complete
        self.sensor_status[7] = False # change pm sensor status to False (i.e. inactive) as all readings are now complete
        return 

    def pm(self): # measures concentration of PM1.0, PM2.5 and PM10 particulate matter
        sensor = 'pm'
        freq = list(filter(lambda x: x[0] == 8, self.sensors))[0][1] # lambda function filters list 'self.sensors' (which stores active sensors and sensor reading frequency in tuple format: (active sensor number, sensor reading frequency)) to access reading frequency for pm sensor (sensor number 8)
        data_heading = ['PM1.0 (ug/m3)','PM2.5 (ug/m3)', 'PM10 (ug/m3)']
        try:
            data = pms5003.read() # get readings of concentration of PM1.0, PM2.5 and PM10 particulate matter
        except pmsReadTimeoutError:
            display_text('Failed to read PMS5003') # display error message on LCD screen
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
            writer.writerow(['Time between readings(sec)',freq]) # record delay between sensor readings
            writer.writerow(['']) # empty row
            writer.writerow(heading) # write headings to file
        now = datetime.now() # get current date and time
        date = now.strftime("%d/%m/%Y") # get current date in correct format
        time = now.strftime("%H:%M:%S") # get current time in correct format
        row = [date, time] + data # enables unlimited number of data readings to be stored as 'data' stores an array of each data reading (applicable as pm sensor takes three readings (PM1.0, PM2.5 and PM10), whereas all other sensor only take one reading)
        writer.writerow(row) # write current date, current time, data reading to file
        f.close() # close file
        return

    def queue_op(self, freq, dur, stime, sensor_method): # general operation for sensor queue - adds sensor execution method to 'self.queue' every 'freq' seconds to take sensor readings at desired intervals to take sensor readings for 'dur' secs, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
        if time.time() - stime >= dur: # if duration for which sensor readings should be taken (as defined by the user in 'sensor_settings.py') has been reached, terminate execution of sensor readings
            return
        else:
            threading.Timer(freq, self.queue_op, [freq, dur, stime, sensor_method]).start() # recursively call 'queue_op' method at frequency specified by 'freq' to add sensor method to 'queue' (which executes sensor readings such that collisions are avoided) at desired frequency and pass required arguments in list
            self.queue.append(sensor_method) # add sensor method to 'self.queue' to schedule execution of sensor reading

    def dequeue(self): # remove each queued sensor reading from the queue and execute the sensor reading, avoiding multiple sensors taking readings simultaneously  
        while True:
            if len(self.queue) >= 1: # if there are sensors readings to be taken
               self.queue.pop(0) # execute reading for front sensor in queue and remove sensor from queue
               time.sleep(1) # 1 second delay between each sensor reading
            if True not in self.sensor_status: # if all sensors are inactive
                display_text('All readings are now complete\nYou can safely power off the Raspberry Pi now') # display sensor reading status on LCD screen
                break # all readings are complete, so terminate

    def main(self): # control operation of active sensors
        queue_thread = threading.Thread(target=self.dequeue) # run queue in background thread
        queue_thread.start()
        for sensor in self.sensors: # iterate through active sensors as defined by user in 'sensor_settings.py'
            sensor_num, sensor_freq, sensor_dur = sensor[0], sensor[1], sensor[2]*60 # first element in tuple stores sensor number, second element stores reading frequency for sensor, third element stores duration of sensor recordings (in minutes)
            self.sensor_status[sensor_num-1] = True # change sensor status to True (i.e. active) for each sensor which user has defined to be active in 'sensor_settings.py'
            sensor_method = self.sensors_dict[sensor_num] # lookup sensor method that is associated with the sensor number ('sensor_num') using 'sensors_dict'
            sensor_method(sensor_freq, sensor_dur, time.time()) # call method to executed readings for desired sensor, passing frequency (secs) at which readings should be taken, duration (secs) for which the readings should be taken, current time (i.e. time at which sensor readings begin)


