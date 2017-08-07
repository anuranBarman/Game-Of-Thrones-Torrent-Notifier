# Game Of Thrones Torrent Notifier


this python script web scraps KickAss Torrent site for game of thrones episode torrent and stores the magnet link of those torrents with their name in a file named torrents.txt and also send an email to a predefined email address with the txt file as attachment.

  - Stores the torrent magnet link sorting 'age' wise.
  - Emails the file as attachment.
  - Adds a Cron Job (Linux) with time interval of 15 minutes.

# Usage

  - Change the episode number in line 47 and 51 (see the got_final.py file)
  - set your email address smtp settings and alternative email address
  - change the directory settings for Cron Job
  - Whenever you want to search for a new episode change the value to 0 in checker.txt (only the number 0, nothing else.Otherwise it won't work)
  - If you want to remove the Cron Job just change the value in checker.txt to 1 and run the script from terminal.
  - You can see if cron job is registered or not from terminal by using command: crontab -l

# Modules Needed
 - BeautifulSoup
 - urllib3
 - smtplib
 - sys
 - time
 - email (mime submodule specially)
 - python-crontab
  
