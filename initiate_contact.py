# README
# Phillip Long
# May 11, 2023

# This script is meant to, given a list of accounts, initiate contact via DM to these accounts.

# python ~/finding_a_roommate/initiate_contact.py driver_address username password accounts_to_dm

# driver_address = filepath to Selenium Chrome Web Driver, download at: https://chromedriver.chromium.org/downloads
# username = Instagram username
# password = Instagram password
# accounts_to_dm = filepath to list of Muir accounts generated by find_accounts.py


# IMPORTS
from login import instagram_driver # my own class that logs into instagram for me while creating a driver
import sys # for stdin arguments
from os.path import exists # for checking if files exist
from os.path import dirname # for determining the output file
from os import makedirs
from re import sub # for string substitution

# ARGUMENTS
# sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs/accounts_muir.txt")
sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "jcreek_rec", "phillip5143", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs/accounts_muir.txt")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2].replace("@", "") # username, remove @ symbol if included
password = sys.argv[3] # password
accounts_to_dm = sys.argv[4] # muir_accounts.txt


# CREATE DRIVER
driver = instagram_driver(driver_address = driver_address, username = username, password = password) # create instance of chrome driver
