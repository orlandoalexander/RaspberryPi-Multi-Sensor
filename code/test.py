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
# # # t.loop()

# #  #import os.path

# # # import csv

# # # # open the file in the write mode
# # # f = open('test.csv', 'w')

# # # # create the csv writer
# # # writer = csv.writer(f)
# # # from datetime import datetime

# # # now = datetime.now()
# # # date = now.strftime("%d/%m/%Y")
# # # time = now.strftime("%H:%M:%S")
# # # writer.writerow(['frequency',60])
# # # writer.writerow([''])
# # # l = ['date','time']+['reading1']
# # # data = [69]
# # # d = [date, time] + data
# # # writer.writerow(l)

# # # writer.writerow(d)


# # # # write a row to the csv file

# # # # close the file
# # # f.close()

# # # import time
# # # def func():
# # #     print('start 1')
# # #     time.sleep(3)
# # #     print('stop 1')
# # #     return

# # # def func2():
# # #     print('start 2')
# # #     time.sleep(3)
# # #     print('stop 2')
# # #     return

# # # l = [func(), func2()]


# # # while True:
# # #     if len(l) >= 1: # if there are sensors readings to be taken
# # #         l.pop(0) # execute reading for front sensor in queue and remove sensor from queue


# # # from git import Repo
# # # repo = Repo('')

# # # repo.index.add('**')
# # # repo.index.commit('updates')
# # # origin = repo.remotes.origin
# # # origin.push()

# # # from concurrent.futures import thread
# # # import time
# # # import threading

# # # def func():
# # #     while True:
# # #         print('Hello world')
# # #         time.sleep(5)

# # # t = threading.Thread(target = func)
# # # t.start()
# # # print('hey')

# # # import time
# # # import threading
# # # import random

# # # def func():
    
# # #     while True:
# # #         r = random.randint(0,2)
# # #         print('hey')
# # #         if r == 0:
# # #             print('break')
# # #             break
# # #         time.sleep(3)
         

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# fromaddr = "aorlando04@gmail.com"
# toaddr = "itsorlando@outlook.com"

# msg = MIMEMultipart()

# msg['From'] = fromaddr
# msg['To'] = toaddr
# msg['Subject'] = "SUBJECT OF THE EMAIL"

# body = "TEXT YOU WANT TO SEND"

# msg.attach(MIMEText(body, 'plain'))

# filename = "log"
# attachment = open("log.txt", "rb")

# part = MIMEBase('application', 'octet-stream')
# part.set_payload((attachment).read())
# encoders.encode_base64(part)
# part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# msg.attach(part)

# server = smtplib.SMTP('smtp.gmail.com', 993)
# server.starttls()
# server.login(fromaddr, "vihpyn-pyfqik-guTvu7")
# text = msg.as_string()
# server.sendmail(fromaddr, toaddr, text)
# server.quit()



import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'aorlando04@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'dygqdxaybbyrcxma' #change this to match your gmail app-passwor
class Emailer:
    def sendmail(self, recipient, subject, content):

        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
            "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)


        msg = MIMEMultipart()
        


        for f in ['log.txt']:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)


        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, msg.as_string())
        session.quit

sender = Emailer()
sendTo = 'itsorlando@outlook.com'
emailSubject = "Hello World"
emailContent = "This is a test of my Emailer Class"

#Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
sender.sendmail(sendTo, emailSubject, emailContent)

