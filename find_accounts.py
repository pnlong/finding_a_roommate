# README
# Phillip Long
# May 9, 2023

# This script is meant to find other individuals who were admitted to muir by scraping the @ucsandiego.2027 Instagram account.

# python ~/finding_a_roommate/find_accounts.py driver_address username password username_to_scrape output_directory

# driver_address = filepath to Selenium Chrome Web Driver, download at: https://chromedriver.chromium.org/downloads
# username = Instagram username
# password = Instagram password
# username_to_scrape = username of Instagram account meant to be scraped
# output_directory = directory that program will output to


# IMPORTS
from login import instagram_driver # my own class that logs into instagram for me while creating a driver
import sys # for stdin arguments
from datetime import datetime # for figuring out when to stop scraping

# ARGUMENTS
# sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "", "ucsandiego.2027")
sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "jcreek_rec", "phillip5143", "ucsandiego.2027", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2].replace("@", "") # username, remove @ symbol if included
password = sys.argv[3] # password
username_to_scrape = sys.argv[4].replace("@", "") # username_to_scrape, remove @ symbol if included
output_directory = sys.argv[5] # directory to output to

# CREATE DRIVER
driver = instagram_driver(driver_address = driver_address, username = username, password = password) # create instance of chrome driver

# CLICK SEARCH BUTTON TO FIND ACCOUNT
search_button = driver.driver.find_element_by_xpath("//a[@href='#']")
search_button.click()
del search_button
driver.wait(2, 3)

# FIND DESIRED INSTAGRAM ACCOUNT
driver.simulate_typing(element = driver.driver.find_element_by_xpath("//input[@aria-label='Search input']"),
                       text = username_to_scrape)
driver.wait(1, 2)

# GO TO DESIRED INSTAGRAM ACCOUNT
desired_account = driver.driver.find_element_by_xpath(f"//a[@href='/{username_to_scrape}/']")
desired_account.click() # click on account with the correct username
del desired_account
driver.wait(3, 4)

# SCROLL DOWN TO FIRST POST
b = 20 # pixels per scroll movement
a = 0
for i in range(400 // b):
    driver.driver.execute_script(f"window.scrollTo({a}, {a + b})") # conduct scrolling action
    driver.wait(0.05, 0.15)
    a += b
del a, b
driver.wait(2, 3)

# CLICK ON FIRST POST
first_post = driver.driver.find_element_by_xpath(".//a[contains(@href,'/p/')]") # finds all posts (href that contains "/p/"), returns the first one! 
first_post.click()
del first_post

# CREATE LIST OF ACCOUNT NAMES
accounts_muir = set(()) # set of accounts that mention muir (no duplicates)
accounts_already_scraped = set(()) # set of accounts that the program has already looked at (no duplicates)

# BEGIN SCRAPING PAGE
date_of_post_is_valid = True
while date_of_post_is_valid:
    
    # WAIT TIME
    driver.wait(7, 10) # add some wait time for each post

    # READ CAPTION
    caption = driver.driver.find_element_by_xpath("//h1[@class='_aacl _aaco _aacu _aacx _aad7 _aade']").text
    caption = caption.lower() # put into lower case to make comparisons easier, also puts account into lower case
    
    
    # DETERMINE ACCOUNT NAME
    if caption.count("@") >= 2: # if multiple @ symbols (perhaps one for snapchat also), pick the one after instagram
        account = caption[caption.index("insta"):] if "insta" in caption else caption[caption.index("ig"):] # use ig
        
    elif caption.count("@") == 0: # if there is no @, I can't DM them for a bio, so no point in including them on the account
        continue
    
    account = account[account.index("@") + 1:]
    account = account.split()[0] # the first word after @
         
    accounts_already_scraped.add(account) # add account to list
    del caption

    # SKIP ITERATION IF PROGRAM HAS ALREADY SCRAPED ACCOUNTS BEFORE 
    if account in accounts_already_scraped:
        continue
    
    
    # IF ACCOUNT IS IN MUIR, FOLLOW THEM
    if "muir" in caption.lower():
        accounts_muir.add(account)
        
    # CLICK NEXT BUTTON
    next_button = driver.driver.find_element_by_xpath("//button[@class='_abl-']")
    next_button.click() # click on next button
    del next_button
            
    # CHECK DATE OF POST
    date_of_post = driver.driver.find_element_by_xpath("//time[@class='_a9ze _a9zf']").get_attribute("datetime")
    date_of_post = date_of_post[0:date_of_post.index("T")] # subset date of post to just include the date
    date_of_post = datetime.strptime(date_of_post, "%Y-%m-%d")
    if date_of_post < datetime.strptime("2023-01-01", "%Y-%m-%d"): # if post before January 1, 2023, render date_of_post_is_valid False
        del date_of_post
        date_of_post_is_valid = False # if there is no more posts, reset the boolean to exit the while loop


