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
from os.path import exists # for checking if files exist
from os import makedirs
from re import sub # for string substitution

# ARGUMENTS
# sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "", "ucsandiego.2027", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs/")
sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "jcreek_rec", "phillip5143", "ucsandiego.2027", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs/")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2].replace("@", "") # username, remove @ symbol if included
password = sys.argv[3] # password
username_to_scrape = sys.argv[4].replace("@", "") # username_to_scrape, remove @ symbol if included
output_directory = sys.argv[5] if sys.argv[5].endswith("/") else sys.argv[5] + "/" # directory to output to


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
driver.scroll(a = 0, b = 400)
driver.wait(1.5, 3)

# CLICK ON FIRST POST
first_post = driver.driver.find_element_by_xpath(".//a[contains(@href,'/p/')]") # finds all posts (href that contains "/p/"), returns the first one! 
first_post.click()
del first_post


# CREATE LIST OF ACCOUNT NAMES
accounts_muir = set(()) # set of accounts that mention muir (no duplicates)
accounts_muir_output = output_directory + "accounts_muir.txt" # note that output directory already has "/" on the end
if exists(accounts_muir_output):
    for line in open(accounts_muir_output):
        accounts_muir.add(str(line).strip())

accounts_already_scraped = set(()) # set of accounts that the program has already looked at (no duplicates)
accounts_already_scraped_output = output_directory + "accounts_already_scraped.txt" # note that output directory already has "/" on the end
if exists(accounts_already_scraped_output):
    for line in open(accounts_already_scraped_output):
        accounts_already_scraped.add(str(line).strip())


# FUNCTION FOR CLICKING TO NEXT POST
def next_post(): # click the next button
    next_button = driver.driver.find_element_by_xpath("//div[@class=' _aaqg _aaqh']")
    next_button.click() # click on next button
    del next_button
    

# BEGIN SCRAPING PAGE
while True:
    
    # WAIT TIME REGARDLESS OF WHETHER PROGRAM HAS SEEN POST BEFORE
    driver.wait(1.5, 2)

    # READ CAPTION
    caption = driver.driver.find_element_by_xpath("//h1[@class='_aacl _aaco _aacu _aacx _aad7 _aade']")
    caption = caption.text.lower() # put into lower case to make comparisons easier, also puts account into lower case
    caption = sub(pattern = r"@[^A-Za-z0-9_.]", repl = "", string = caption) # deal with randomly-used @ symbols that aren't social media usernames
    
    # DETERMINE ACCOUNT NAME
    if caption.count("@") == 0: # if there is no @, I can't DM them for a bio, so no point in including them on the account
        next_post()
        continue
    
    elif caption.count("@") == 1: # one @ symbol
        account = caption
        
    else: # if multiple @ symbols (perhaps one for snapchat also), pick the account handle that follows "instagram" or some variant of it
        if "insta" in caption: # if the word insta is in the caption
            account = caption[caption.index("insta"):]
        elif "ig" in caption: # if the word ig is in the caption
            account = caption[caption.index("ig"):]
        else: # select the last instance of @ and hope for the best, though the postee should have clarified which account is which if there are multiple socials
            account = caption[caption.rindex("@"):]        
    
    account = account[account.index("@") + 1:]
    account = account.split()[0] # the first word after @

    # SKIP ITERATION IF PROGRAM HAS ALREADY SCRAPED ACCOUNTS BEFORE 
    if account in accounts_already_scraped:
        next_post()
        continue
    else: # have not yet scraped this account
        accounts_already_scraped.add(account) # add account to list

    
    # CHECK DATE OF POST TO MAKE SURE POSTS ARE STILL RELEVANT
    date_of_post = driver.driver.find_element_by_xpath("//time[@class='_a9ze _a9zf']").get_attribute("datetime")
    date_of_post = date_of_post[0:date_of_post.index("T")] # subset date of post to just include the date
    date_of_post = datetime.strptime(date_of_post, "%Y-%m-%d")
    if date_of_post < datetime.strptime("2023-01-01", "%Y-%m-%d"): # if post before January 1, 2023, break the while loop
        break # if there is no more posts, exit the while loop
    del date_of_post
    
    
    # ADD SOME EXTRA WAIT TIME TO SIMULATE READING CAPTION
    driver.wait(3.5, 6)
    
    
    # IF ACCOUNT MENTIONS MUIR, FOLLOW THEM
    if "muir" in caption:
        accounts_muir.add(account)
        
        # MAKE NOTE OF CURRENT URL
        current_url = str(driver.driver.current_url).split("/")
        current_url = current_url[len(current_url) - 2]
        
        # CLICK ON ACCOUNT
        driver.driver.find_element_by_xpath(f"//a[@href='/{account}/']").click()
        driver.wait(2, 3)
        driver.scroll(a = driver.driver.execute_script("return window.pageYOffset;"), b = 0) # scroll to top of page if not there already
        driver.wait(0.5, 1)
        
        # CLICK FOLLOW
        driver.driver.find_element_by_xpath("//button[@class='_acan _acap _acas _aj1-']").click()
        driver.wait(2, 3)
    
        # GO BACK
        driver.driver.back()
        
        # RELOCATE POST WE WERE JUST LOOKING AT
        driver.wait(0.75, 1.25)
        a = 0 # where to start scrolling from
        scroll_per_iter = 2400 # amount to scroll each time
        back_to_post = False # whether the program can locate the post element
        while not back_to_post:
            try:
                relocated_post = driver.driver.find_element_by_xpath(f"//a[@href='/p/{current_url}/']") # if this succeeds, we are near the post (its loaded in)
                driver.scroll(a = a, b = relocated_post.location["y"]) # scroll to previous post
                driver.wait(0.5, 1.25)
                relocated_post.click() # click on post
                del relocated_post
                back_to_post = True
            except: # back_to_post remains False
                driver.scroll(a = a, b = a + scroll_per_iter)
                a += scroll_per_iter # update a
                driver.wait(0.75, 1)

    del caption
    

    # CLICK NEXT BUTTON
    try:
        next_post()
    except: # if there is no next post
        break # exit loop

del date_of_post_is_valid


# WRITE ACCOUNT LISTS TO FILES
if not exists(output_directory): # if output directory doesn't exist yet
    makedirs(output_directory) # create the new directory

accounts_muir_writable = open(accounts_muir_output, "w")
accounts_muir_writable.write("\n".join(accounts_muir))
accounts_muir_writable.close()

accounts_already_scraped_writable = open(accounts_already_scraped_output, "w")
accounts_already_scraped_writable.write("\n".join(accounts_already_scraped))
accounts_already_scraped_writable.close()

