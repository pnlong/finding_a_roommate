# README
# Phillip Long
# May 9, 2023

# This script is meant to find other individuals who were admitted to muir by scraping the @ucsandiego.2027 Instagram account.

# python ~/finding_a_roommate/find_accounts.py driver_address username password username_to_scrape

# driver_address = filepath to Selenium Chrome Web Driver, download at: https://chromedriver.chromium.org/downloads
# username = Instagram username
# password = Instagram password
# username_to_scrape = username of Instagram account meant to be scraped

# IMPORTS
from login import instagram_driver # my own class that logs into instagram for me while creating a driver
import sys # for stdin arguments
import numpy # for storing data

# ARGUMENTS
# sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "", "ucsandiego.2027")
sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "jcreek_rec", "phillip5143", "ucsandiego.2027")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2].replace("@", "") # username, remove @ symbol if included
password = sys.argv[3] # password
username_to_scrape = sys.argv[4].replace("@", "") # username_to_scrape, remove @ symbol if included

# CREATE DRIVER
driver = instagram_driver(driver_address = driver_address, username = username, password = password) # create instance of chrome driver

# CLICK SEARCH BUTTON TO FIND ACCOUNT
search_button = driver.driver.find_element_by_xpath("//a[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd']")
search_button.click()
del search_button
driver.wait(2, 3)

# FIND DESIRED INSTAGRAM ACCOUNT





