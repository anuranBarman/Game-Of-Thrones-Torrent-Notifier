#####################################
# Author: Anuran Barman             #
# Email: anuranbarman@gmail.com     #
# Website: www.mranuran.com         #
#####################################


#! /usr/bin/python3
from bs4 import BeautifulSoup
import urllib3
import smtplib
import sys
import time
from email.mime.multipart import *
from email.mime.base import *
from email import encoders
from crontab import CronTab

my_cron = CronTab(user='dante')
file = open("torrents.txt", "w+")
checkerFile = open("checker.txt", "r")
checkedData = checkerFile.read()
if checkedData.find("1") == -1:
    http = urllib3.PoolManager()

    ##############################################
    #          DO NOT CHANGE THIS LINK           #
    ##############################################

    url = "https://kickass.unblockall.xyz/usearch/game%20of%20thrones/?field=time_add&sorder=desc"

    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "lxml")

    torrents = soup.find_all('a', {"title": "Download torrent file"})
    names = soup.find_all('a', {"class": "cellMainLink"})
    torrentNames = []
    namesAll = []

    ####################################################################
    #   Change line 47 and 51 with new episode name in the format      #
    #   S##E@@ ---> ##=Season Number(double digit)                     #
    #               @@=Episode Number(double digit)                    #
    # ##################################################################

    for torrent in torrents:
        if "S07E04" in torrent['href']:
            torrentNames.append(torrent['href'])

    for name in names:
        if "S07E04" in name.text:
            namesAll.append(name.text)
    allTogether = dict(zip(namesAll, torrentNames))

    for name, torrent in allTogether.items():
        file.write("Name: " + name + "\nMagnet: " + torrent + "\n" + '*' * 50 + "\n")

    if len(torrentNames) > 0:
        checkerFile.close()
        checkerFile = open("checker.txt", "w")
        checkerFile.write("1")


    class SMTP(object):
        def title(self):
            print("Email Sending Starting...........")

        def SMTPconnect(self):
            print("Trying to log you in.........")
            self.smtpserver = "smtp.gmail.com" #smtp server of your mail service provider
            self.smtpport = 587 #smtp port
            try:
                self.mailServer = smtplib.SMTP(self.smtpserver, self.smtpport)
            except IOError as e:
                print(e)
                time.sleep(5)
                sys.exit(1)
            self.mailServer.starttls()
            self.username = "yourusername@domain.com"  # Username
            self.password = "dummypassword"  # password
            try:
                self.mailServer.login(self.username, self.password)
            except BaseException as e:
                print(e)
                time.sleep(3)
                sys.exit(1)

        def buildemail(self):
            msg = MIMEMultipart()
            msg['Subject'] = "Game of Thrones New Episode Torrent Links"
            msg['From'] = self.username
            msg['To'] = "example@domain.com" #your alternative email address where you wanna send the mail

            part = MIMEBase('application', "octet-stream")
            part.set_payload(open("torrents.txt", "rb").read())
            encoders.encode_base64(part)

            part.add_header('Content-Disposition', 'attachment; filename="torrents.txt"')

            msg.attach(part)

            self.mailServer.sendmail(self.username, "example@domain.com", msg.as_string())
            print("Email with Torrent Links sent Successfully.\nTorrent Links are stored in torrents.txt file")


    if len(torrentNames) > 0:
        s = SMTP()
        s.title()
        s.SMTPconnect()
        s.buildemail()

    else:
        job = my_cron.new(

            ########################################################################################################
            # change the directory names according to your system                                                  #
            # cd <where you placed your python script>                                                             #
            # <python3 interpreter location> <your script location>  >> <where you wanna store the log details>    #
            ########################################################################################################

            command='cd /home/dante/Desktop/got torrent notifier/ && /usr/bin/python3 /home/dante/Desktop/got torrent notifier/got_final.py >> /home/dante/Desktop/got torrent notifier/log.txt',
            comment="GameOfThrones")
        job.minute.every(2)
        my_cron.write()
        print("No Torrent Found.Added the Cron Job.Exiting....")
        sys.exit(0)

else:
    print(
        "If you are trying to find new episode after last use of the script\nmake sure you have updated the value to 0 in checker.txt and \nupdated the if clause in line 31")
    print("Removing Cron Job.\nExiting...........")
    for job in my_cron:
        if job.comment == "GameOfThrones":
            my_cron.remove(job)
            my_cron.write()
    sys.exit(0)
