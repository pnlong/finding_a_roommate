# README
# Phillip Long
# May 6, 2023

# I was recently admitted to UC San Diego, and on Instagram, there is this account called @ucsandiego.2027
# A lot of incoming freshmen post to this account, both to make friends and find potential roommates
# However, the page is chaotic to say the least...there are thousands of people posting about themselves
# and since I can't dorm with most of the people posting, I want a page just for Muir College Class of 2027
# This will make things a lot more manageable and easier to find a roommate.

# python ~/finding_a_roommate/bot.py driver_address username password

# driver_address = filepath to Selenium Chrome Web Driver, download at: https://chromedriver.chromium.org/downloads
# username = Instagram username
# password = Instagram password


# IMPORTS
from selenium import webdriver
import numpy
from time import sleep
import sys

# ARGUMENTS
# sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2] # username
password = sys.argv[3] # password

# create instance of chrome driver
driver = webdriver.Chrome(executable_path = "/Users/philliplong/Desktop/Coding/chromedriver")


