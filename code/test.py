# # import threading
# # queue = [0,1,2]
# # print(queue.pop(0))
# # class test():
# #     def __init__(self):
# #        self.queue = []
    
# #     def dequeue(self):
# #         while True:
# #             if len(self.queue) >= 1:
# #                 print(self.queue.pop())

# #     def printit(self):
# #         threading.Timer(5.0, self.printit).start()
# #         self.queue.append("Hello, World!")
# #         print('appended1')
    
# #     def printit2(self):
# #         threading.Timer(7.0, self.printit2).start()
# #         self.queue.append("Hello, Universe!")
# #         print('appended2')
    
# #     def loop(self):
# #         l = [self.printit(), self.printit2()]
# #         self.dequeue()
# #         for i in l:
# #             l

# # t = test()
# # t.loop()

#  #import os.path

# # import csv

# # # open the file in the write mode
# # f = open('test.csv', 'w')

# # # create the csv writer
# # writer = csv.writer(f)
# # from datetime import datetime

# # now = datetime.now()
# # date = now.strftime("%d/%m/%Y")
# # time = now.strftime("%H:%M:%S")
# # writer.writerow(['frequency',60])
# # writer.writerow([''])
# # l = ['date','time']+['reading1']
# # data = [69]
# # d = [date, time] + data
# # writer.writerow(l)

# # writer.writerow(d)


# # # write a row to the csv file

# # # close the file
# # f.close()

# # import time
# # def func():
# #     print('start 1')
# #     time.sleep(3)
# #     print('stop 1')
# #     return

# # def func2():
# #     print('start 2')
# #     time.sleep(3)
# #     print('stop 2')
# #     return

# # l = [func(), func2()]


# # while True:
# #     if len(l) >= 1: # if there are sensors readings to be taken
# #         l.pop(0) # execute reading for front sensor in queue and remove sensor from queue


# # from git import Repo
# # repo = Repo('')

# # repo.index.add('**')
# # repo.index.commit('updates')
# # origin = repo.remotes.origin
# # origin.push()

# # from concurrent.futures import thread
# # import time
# # import threading

# # def func():
# #     while True:
# #         print('Hello world')
# #         time.sleep(5)

# # t = threading.Thread(target = func)
# # t.start()
# # print('hey')

# # import time
# # import threading
# # import random

# # def func():
    
# #     while True:
# #         r = random.randint(0,2)
# #         print('hey')
# #         if r == 0:
# #             print('break')
# #             break
# #         time.sleep(3)
         


# # while True:
# #     inp = input('Type: ')
# #     print(threading.active_count())
# #     if inp == 'i':
# #         t = threading.Thread(target=func)
# #         t.start()
        
# # import threading
# # import time
# # def hey():
# #     print('Hey')
# #     return

    
# # def func(freq, start, dur): # appends 'pm' method to queue every 'freq' secs to take readings at desired intervals, whilst avoiding collisions which may occur if multiple sensors take readings simultaneously 
# #     print(time.time()-start)
# #     if time.time() - start >= dur:
# #         print('done')
# #         return
# #     threading.Timer(freq, func, [freq, start, dur]).start() # recursively call 'pm' method at frequency specified by 'freq' to take readings at desired frequency
# #     print('hey')
    

# # func(3, time.time(), 9)

# # import sys

# # path = '/Users/orlandoalexander/Library/Mobile Documents/com~apple~CloudDocs/Documents/South America/EcoSwell/RaspberryPi-Sensor/RaspberryPi-Sensor'
# # sys.path.append(path)

# # import sensor_settings

# # print (sensor_settings.factor)

# # import csv
# # from datetime import datetime

# # f = open(f'data/example.csv', 'w') # create/open CSV file to store data for 'sensor'
# # writer = csv.writer(f)
# # heading = ['Date', 'Time'] + ['temp (C)'] # enables unlimited number of data headings as 'data_heading' stores an array of each data heading (applicable as pm sensor takes three readings (PM1.0, PM2.5 and PM10), whereas all other sensor only take one reading)
# # writer.writerow(['Time between readings(sec): ',60]) # record delay between sensor readings
# # writer.writerow(['Duration of readings (mins): ', 240]) # record duration of sensor readings
# # writer.writerow(heading) # write headings to file

# # now = datetime.now() # get current date and time
# # time = now.strftime("%H:%M:%S") # get current time in correct format
# # date = now.strftime("%d.%m.%Y") # get current date in correct format
# # row = [date, time] + ['35'] # enables unlimited number of data readings to be stored as 'data' stores an array of each data reading (applicable as pm sensor takes three readings (PM1.0, PM2.5 and PM10), whereas all other sensor only take one reading)
# # writer.writerow(row) # write current date, current time, data reading to file


# # f.close() # close file


# import threading 
# import time
# from test2 import main
# sensor_thread = threading.Thread(target=main) # create new thread to take sensor readings in background
# sensor_thread.start()
# time.sleep(5)
# print('j')
# main.data = False
