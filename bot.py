# README
# Phillip Long
# May 6, 2023

# I was recently admitted to UC San Diego, and on Instagram, there is this account called @ucsandiego.2027
# A lot of incoming freshmen post to this account, both to make friends and find potential roommates
# However, the page is chaotic to say the least...there are thousands of people posting about themselves
# and since I can't dorm with most of the people posting, I want a page just for Muir College Class of 2027
# This will make things a lot more manageable and easier to find a roommate.

# python ~/finding_a_roommate/bot.py driver_address username password output_directory

# driver_address = filepath to Selenium Chrome Web Driver, download at: https://chromedriver.chromium.org/downloads
# username = Instagram username
# password = Instagram password


# IMPORTS
from login import instagram_driver # my own class that logs into instagram for me while creating a driver
import sys # for stdin arguments
import numpy # for storing data

# ARGUMENTS
# sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "jcreek_rec", "phillip5143")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2] # username
password = sys.argv[3] # password

# CREATE DRIVER AND LOGIN
driver = instagram_driver(driver_address = driver_address, username = username, password = password) # create instance of chrome driver
driver.login()

# GO TO DMS
driver.click_messages()



