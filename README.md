## <u>EcoSwell Multi-Sensor Documentation</u> 

The EcoSwell Multi-Sensor is easy to use and can measure eight different data types with adjustable parameters for data recording, including reading frequency and duration of data recording. The sensor can measure the following data types:

| Data type           | Unit  | Unit description                                             |
| ------------------- | ----- | ------------------------------------------------------------ |
| Temperature*        | *C    | Degrees celcius                                              |
| Pressure            | hPa   | Hectopascal                                                  |
| Humidity            | %     | Relative humidity as percentage                              |
| Light               | Lux   | Luminious flux per unit area                                 |
| Carbon monoxide*    | -     | Arbitrary - measure changes relative to baseline value (TODO) |
| Nitrogen dioxide*   | -     | Arbitrary - measure changes relative to baseline value (TODO) |
| Ammonia*            | -     | Arbitrary - measure changes relative to baseline value (TODO) |
| Particulate matter* | ug/m3 | Micrograms per cubic metre of air                            |

*see section **Data Type Details** for more details



## **Overview** 

The sensor is contained within a plastic container and comprises of three components: Raspberry Pi (model 4), [Enviro+ Sensor Board](https://shop.pimoroni.com/products/enviro?variant=31155658457171) and [PMS5003 Air Quality Sensor](https://www.adafruit.com/product/3686), all of which are stored inside a waterproof storage box for ease of transport and monitoring. The Raspberry Pi is the 'brain' of the sensor; it executes the code which controls the sensors, processes the data recorded by the sensors and uploads this data to the GitHub Repository (see section **GitHub Repository** for more details). The two sensors together contain the components which measure the eight data types listed above. 

While the sensor settings must be modified online using the GitHub Repository, the sensor can operate either online or offline. If operating online, data readings will be uploaded to the GitHub Repository every minute. If operating offline, data readings will be uploaded as soon as the sensor connects to the internet. Regardless of internet connectivity, all data will be saved locally to the Raspberry Pi whilst the readings are being recorded, so no data will be lost if power to the sensor temporarily fails.

The sensor also contains an LCD screen which will display status updates and feedback where appropriate.




## **Raspberry Pi Diagram**
<img width="832" alt="image-20220916124231553" src="https://user-images.githubusercontent.com/113472300/191034839-39f3fec2-b07c-4352-977d-f9d678b465e6.png">


The Raspberry Pi has loads of different ports and components, but luckily you don't need to worry about most of them! The four ports you need to be aware of are shown clearly in the diagram above, and are used during the initial setup process (see section **How To Use The Sensor** / **<u>Initial setup</u>**)





## **GitHub Repository**

The operational code, sensor settings and data readings are stored on an online platform called *GitHub* inside something called a repository. A repository (or 'repo') is essentially a collection of files (code, images, text files - anything goes) that is stored in an online server and can be accessed from anywhere in the world - think of it a bit like Microsoft OneDrive or Google Drive. For our EcoSwell Multi-Sensor, the repo is called [*RaspberryPi-Sensor*](https://github.com/EcoSwell/RaspberryPi-Sensor) and it belongs to the EcoSwell GitHub account. To edit any files inside this repo, you must be logged into the EcoSwell GitHub account - here are the login details:

​	*username:* EcoSwell	

​	*email:* info@ecoswell.org

​	*password*: *5u5t@1n@b1l1ty*

The GitHub repo looks a little like this:
<img width="1418" alt="image" src="https://user-images.githubusercontent.com/113472300/191466462-068fec5d-0a26-407e-845e-cbfd6e271239.png">


You will see three things in the GitHub repo:

1. *code* folder - you can <u>ignore</u> all files in this folder, unless you want/need to modify the sensor's core operational code
2. *data* folder - this file is <u>important</u> as it stores all the data readings captured by the sensor
3. *sensor_settings.py* folder - this file is <u>important</u> as it allows you to set which sensors are active, how often readings are taken and the duration of the data readings




## **How To Use The Sensor**

<u>**Initial setup**</u>

As the sensor must be connected to the internet to sync the latest settings changes from the GitHub Repo (see **<u>Sensor settings</u> **for more details) and to upload data readings, when you first set up the sensor (or wish to sync the settings/upload data readings from a new location), you must follow these steps to connect it to the internet:

***Using ethernet*** (very simple, but slightly more inconvenient)

1. Boot sensor by plugging micro USB power cable into Raspberry Pi *micro USB port* (see **Raspberry Pi Diagram**)
2. Plug ethernet cable into Raspberry Pi *ethernet port* (see **Raspberry Pi Diagram**)
3. You're good to go! Just make sure to remember to plug the ethernet cable in every time you want to connect the Raspberry Pi to the internet

***Using WiFi*** (slightly more complicated, but more convenient)

1. Boot sensor by plugging micro USB power cable into Raspberry Pi *micro USB port* (see **Raspberry Pi Diagram**)

2. Connect Raspberry to monitor by plugging HDMI cable into Raspberry Pi *HDMI port* (see **Raspberry Pi Diagram**)

3. Connect wired keyboard and mouse to Raspberry Pi by plugging USB cables into Raspberry Pi *USB ports* (see **Raspberry Pi Diagram**)

4. Navigate to the WiFi settings in the top right hand corner of the monitor screen, select the desired WiFi and enter the password (if required) 

   ADD PHOTO



<u>**Sensor settings**</u>

The sensor settings are adjusted in an online file called *sensor_settings.py* which is stored in the GitHub repo, and looks a bit like this:

<img width="1208" alt="image-20220916215144428" src="https://user-images.githubusercontent.com/113472300/191035159-8a300bc9-281d-4e07-b74f-966ee98b7855.png">

1. To modify the sensor settings you must edit the file *sensor_settings.py* by clicking the *pen icon* circled above

2. To change which sensors are active, the reading frequency for each sensor and the duration of data recording for each sensor, follow the instructions in *sensor_settings.py* under the heading `ACTIVE SENSORS, FREQUENCY OF DATA RECORDING & DURATION OF DATA RECORDING`

3. Note: If you wish to activate the temperature sensor (sensor no. 1), then you must first adjust the value of *factor* in the file *sensor_settings.py* under the heading `ADJUST TEMPERATURE TUNING FACTOR` to calibrate the sensor - see section **Data Type Details** / **<u>Temperature</u>** for instructions

4. To save your changes to the sensor settings file *sensor_settings.py*, click the *commit changes* button circled below:

   <img width="1072" alt="image-20220916215343225" src="https://user-images.githubusercontent.com/113472300/191035294-72ed0820-c9ee-4ec3-b1d3-3aa3aa18ed5c.png">

4. Finally, to sync these changes with the sensor, you must reboot the sensor by unplugging the micro USB cable and plugging it back in again - if the sensor successfully downloads the latest version of the settings file, the following message will be displayed on the sensor's LCD screen upon reboot: 

   ADD PHOTO

 

<u>**Start sensor readings**</u>

1. Boot sensor by plugging micro USB power cable into Raspberry Pi *micro USB port* (see **Raspberry Pi Diagram**)

2. Wait at least *20 seconds* to allow Raspberry Pi and sensors to start up

3. To start the readings, place finger on proximity sensor (labelled `Start`) for at least 5 seconds, or until the sensor's LCD screen displays the following message:

   ADD PHOTO

4. You now have 2 minutes to position the sensor in the desired location - after these 2 minutes, the readings will begin

5. Leave the sensor in place until all the readings are complete, which will be indicated on the LCD screen by the following message:

   ADD PHOTO



**<u>Download sensor data</u>**

1. All data recorded by the sensor will be uploaded in appropriately named files to the *data* folder in the GitHub repo

   - If the sensor is connected to the internet whilst it's recording data, the data files will be uploaded every 60 seconds
   - If the sensor is not connected to the internet whilst it's recording data, the data files will be uploaded as soon as the sensor connects to the internet

2. Data files are stored with the *csv* format and named with the following format: `sensor type - start date - start time`

   - For example, a file named `co-16.09.2022-12:58` would store carbon monoxide data readings which started to be measured at 12:58 on 16/09/2022 

3. To download the *csv* data file and import it into *Excel* for analysis, follow these steps:

   1. Open the GitHub repo using *Google Chrome* (<u>not</u> *Safari*)

   2. Navigate to the *data* folder inside the GitHub repo:

      <img width="1309" alt="image-20220916153944740" src="https://user-images.githubusercontent.com/113472300/191035399-beb80780-391b-48ae-b5d6-acbf6af4a8ce.png">

   

   3. Open the required *csv* data file:

      <img width="1274" alt="image-20220916160119981" src="https://user-images.githubusercontent.com/113472300/191035476-b5829e57-9369-4e1c-99f1-dcb4e12b772f.png">

   

   4. Click `Raw`: 
   
      <img width="1277" alt="image-20220916160224783" src="https://user-images.githubusercontent.com/113472300/191035532-2d40e57b-dab3-4a55-8a5a-8d1ed121c9fc.png">

      

   5. Right click on the screen and click `Save As...` to save the data as a *csv* file on your computer:

      <img width="1284" alt="image-20220916155417329" src="https://user-images.githubusercontent.com/113472300/191035557-fe3c618c-879a-44b6-8f2a-685b90e3d890.png">

      

   6. You can now open the *csv* data file in Excel and perform required analysis




<u>**Restart sensor readings**</u>

1. If you want to restart the sensor readings mid data recording, you must place finger on proximity sensor (labelled `Start`) for at least 15 seconds - don't worry, the current data will be saved! 

2. The sensor will show the following message before it restarts:

   ADD PHOTO



## **Data Type Details**

**<u>Temperature</u>**

The temperature reading must be adjusted slightly to compensate for the heating effect of the CPU (computer processing unit on the sensor). To tweak how much the temperature value is compensated, follow these steps:

1. Set `calculate_factor` to `True` in the file *sensor_settings.py*, as shown below:

   <img width="1230" alt="image-20220916220255521" src="https://user-images.githubusercontent.com/113472300/191035618-a98ebbc1-b2da-43a4-9f11-fe0b299f6f13.png">

   

2. Follow the steps in section **How To Use The Sensor** / **<u>Start sensor readings</u>** to begin the sensor readings

3. Open the Excel file [*Calculate temp factor*](https://docs.google.com/spreadsheets/d/1BLTTYUCHuqEoowzhjQEQhzlOlSYHIbCMgoVQX1paT3U/edit?usp=sharing):

   <img width="407" alt="image-20220916222157041" src="https://user-images.githubusercontent.com/113472300/191035628-3d6f7fe5-2cc4-4808-b847-8b46933d0628.png">

   

4. Use an external temperature sensor to record the temperature surrounding the sensor every 60 seconds for 10 minutes, starting when the sensor begins to record data. Record each data value in the `External temperature sensor (*C)` column within the Excel file

5. Download the data (see **<u>Download sensor data</u>** for details) and import the two data columns (`Data 1` and `Data 2`) into the columns with the same headers in the Excel file 

6. The required temperature compensation factor will be displayed at the bottom of the Excel file

7. Set `Factor` in *sensor_settings.py* to this calculated temperature compensation factor 



**<u>Carbon monoxide</u>**

The data values for the carbon monoxide readings are given in arbitrary units (technically, they are given as resistance values - but don't worry about this!). Therefore, it is not possible to measure exact concentrations of carbon monoxide in parts per million. Instead, you should use the results to measure the change in the concentration of carbon monoxide particles in the air relative to the baseline value of (TODO) - this value was calculated in an open space away from any buildings or sources of pollution.

**Important**: the carbon monoxide gas readings will *drop* with increasing concentration of carbon monoxide gas detected.
**Important**: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.



**<u>Nitrogen dioxide</u>**

The data values for the nitrogen dioxide readings are given in arbitrary units (technically, they are given as resistance values - but don't worry about this!). Therefore, it is not possible to measure exact concentrations of nitrogen dioxide in parts per million. Instead, you should use the results to measure the change in the concentration of nitrogen dioxide particles in the air relative to the baseline value of (TODO) - this value was calculated in an open space away from any buildings or sources of pollution.

**Important**: the nitrogen dioxide gas readings will *increase* with increasing concentration of the nitrogen dioxide gas detected. 
**Important**: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.



**<u>Ammonia</u>**

The data values for the ammonia readings are given in arbitrary units (technically, they are given as resistance values - but don't worry about this!). Therefore, it is not possible to measure exact concentrations of ammonia in parts per million. Instead, you should use the results to measure the change in the concentration of ammonia particles in the air relative to the baseline value of (TODO) - this value was calculated in an open space away from any buildings or sources of pollution.

**Important**: the ammonia gas readings will *drop* with increasing concentration of the ammonia gas detected. 
**Important**: the sensor takes around 10 minutes to stabalise, so ignore all readings taken within the first 10 minutes.



**<u>Particulate matter</u>**

Unlike the other data types, the particulate matter sensor records three data values: PM1.0, PM2.5 and PM10. These values refer to the size of the particles; PM10 readings include particles of 10 microns and smaller, PM2.5 readings include particles of 2.5 microns and smaller, and PM1.0 readings include particles of 1 micron and smaller. 











