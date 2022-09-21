import sys
path = '/home/ecoswell/RaspberryPi-Sensor' # path to folder storing 'sensor_settings' module
sys.path.append(path) # enable importing module ('sensor_settings') from outside directory
import sensor_settings
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
import os
import time

NOW = datetime.now() # get current date and time
DATE = NOW.strftime("%d.%m.%Y") # get date when sensor readings begin in correct format
TIME = NOW.strftime("%H:%M:%S") # get time when sensor readings begin in correct format
SMTP_SERVER = 'smtp.gmail.com' # email server 
SMTP_PORT = 587 # server port 
GMAIL_USERNAME = 'aorlando04@gmail.com' # change this to match your gmail account
GMAIL_PASSWORD = 'dygqdxaybbyrcxma' # change this to match your gmail app-password (see https://bc-robotics.com/tutorials/sending-email-using-python-raspberry-pi/)
RECIPIENT = sensor_settings.email_address
SUBJECT = 'Multi-sensor data '+DATE+'-'+TIME

# WIFI connection message
time.sleep(5)
#try: 
requests.get('https://www.google.com/') # check if Raspberry Pi is connected to internet (request will cause error if not connected to internet --> except statement triggered)

# connect to gmail server:
session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) 
session.ehlo()
session.starttls()
session.ehlo()

# login to gmail
session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

msg = MIMEMultipart() # create message data
msg['Subject'] = SUBJECT # assign message subject 

directory = '/home/ecoswell/RaspberryPi-Sensor/data'
for file in os.listdir(directory):
    filename = os.path.join(directory, file)
    with open(filename, "rb") as f:
        part = MIMEApplication(f.read(),Name=basename(filename))
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
    msg.attach(part)

# send email:
session.sendmail(GMAIL_USERNAME, RECIPIENT, msg.as_string())
session.quit

new_directory = '/home/ecoswell/RaspberryPi-Sensor/data_emailed'
for file in os.listdir(directory):
    filename = os.path.join(directory, file)
    new_filename = os.path.join(new_directory, file)
    os.rename(filename, new_filename)

#except:
   # pass        
    