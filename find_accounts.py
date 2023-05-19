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
from datetime import timedelta
from os.path import exists # for checking if files exist
from os import makedirs
from re import sub # for string substitution

# ARGUMENTS
# sys.argv = ("find_accounts.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "", "ucsandiego.2027", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs/")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2].replace("@", "") # username, remove @ symbol if included
password = sys.argv[3] # password
username_to_scrape = sys.argv[4].replace("@", "") # username_to_scrape, remove @ symbol if included
output_directory = sys.argv[5] if sys.argv[5].endswith("/") else sys.argv[5] + "/" # directory to output to

stop_key = "*******************" # string to put at the end of files signaling they are complete
stop_date = datetime.strptime("2023-01-01", "%Y-%m-%d") # date to stop scraping account
d = 7 # number of days ago to set new stop date

# CREATE DRIVER AND LOGIN
driver = instagram_driver(driver_address = driver_address, username = username, password = password) # create instance of chrome driver
driver.login()


# CREATE LIST OF ACCOUNT NAMES
# if output directory doesn't exist yet
if not exists(output_directory):
    makedirs(output_directory) # create the new directory

# set of accounts that mention muir (no duplicates)
accounts_muir = set(())
accounts_muir_output = output_directory + "accounts_muir.txt" # note that output directory already has "/" on the end
if exists(accounts_muir_output):
    for line in open(accounts_muir_output, "r"):
        accounts_muir.add(str(line).strip())
accounts_muir_writable = open(accounts_muir_output, "a")

# set of accounts that the program has already looked at (no duplicates)
accounts_already_scraped = set(())
accounts_already_scraped_output = output_directory + "accounts_already_scraped.txt" # note that output directory already has "/" on the end
if exists(accounts_already_scraped_output):
    for line in open(accounts_already_scraped_output, "r"):
        accounts_already_scraped.add(str(line).strip())
accounts_already_scraped_writable = open(accounts_already_scraped_output, "a")

# set of accounts that the program has already followed (no duplicates)
accounts_followed = set(())
accounts_followed_output = output_directory + "accounts_followed.txt" # note that output directory already has "/" on the end
if exists(accounts_followed_output):
    for line in open(accounts_followed_output, "r"):
        accounts_followed.add(str(line).strip())
accounts_followed_writable = open(accounts_followed_output, "a")

# ADJUST STOP DATE
stop_key_present = False # to avoid double writing stop_key
if stop_key in accounts_muir or stop_key in accounts_already_scraped: # reset stop_date to a more sooner, quicker-to-scrape date
    stop_key_present = True
    stop_date = datetime.now() - timedelta(days = d) # sooner date to stop scraping account sooner (a week ago)

# FUNCTION FOR CLICKING TO NEXT POST
def next_post(): # click the next button
    driver.driver.find_element("xpath", "//div[@class=' _aaqg _aaqh']").click()
    

# CLICK SEARCH BUTTON TO FIND ACCOUNT AND ENTER DESIRED INSTAGRAM ACCOUNT
driver.click_search()
driver.simulate_typing(element = driver.driver.find_element("xpath", "//input[@aria-label='Search input']"),
                       text = username_to_scrape)
driver.wait(1, 2)

# GO TO DESIRED INSTAGRAM ACCOUNT
try: # if it exists
    driver.driver.find_element("xpath", f"//a[@href='/{username_to_scrape}/']").click() # click on account with the correct username
    driver.wait(3, 4)
except: # if it does not exist
    print("Error: Invalid username_to_scrape argument. Account does not exist / cannot be found.")
    quit()

# SCROLL DOWN TO FIRST POST
y_scroll_most_recent = 400
driver.scroll(a = 0, b = y_scroll_most_recent)
driver.wait(1.5, 3)

# CLICK ON FIRST POST
driver.driver.find_element("xpath", ".//a[contains(@href,'/p/')]").click() # finds all posts (href that contains "/p/"), returns the first one! 
# wait time is added in loop


# BEGIN SCRAPING PAGE, MAKING NOTE OF MUIR ACCOUNTS
while True:
    
    # WAIT TIME REGARDLESS OF WHETHER PROGRAM HAS SEEN POST BEFORE
    driver.wait(0.5, 1.5)

    # READ CAPTION
    caption = driver.driver.find_element("xpath", "//h1[@class='_aacl _aaco _aacu _aacx _aad7 _aade']")
    caption = caption.text.lower() # put into lower case to make comparisons easier, also puts account into lower case
    caption = sub(pattern = r"[^A-Za-z0-9_.@]", repl = " ", string = caption) # remove all characters other than those that can be used in account names
    caption = sub(pattern = r"@[^A-Za-z0-9_.]", repl = " ", string = caption) # deal with randomly-used @ symbols that aren't social media usernames
    caption = caption[:len(caption) - 1] if caption.endswith("@") else caption
        
    # DETERMINE ACCOUNT NAME
    if any(instagram in caption.split() for instagram in ("insta", "ig", "instagram")):
        account = caption.split()
        i = tuple(i for i in range(len(account)) if any(instagram == account[i] for instagram in ("insta", "ig", "instagram",
                                                                                                  "instasnap", "instagramsnap", "igsnap",
                                                                                                  "snapinsta", "snapinstagram", "snapig",
                                                                                                  "instasnapchat", "instagramsnapchat", "igsnapchat",
                                                                                                  "snapchatinsta", "snapchatinstagram", "snapchatig",
                                                                                                  "instasc", "instagramsc", "igsc",
                                                                                                  "scinsta", "scinstagram", "scig")))[-1] # choose the final mention of instagram
        if any(account[i + 1] == x for x in ("is", "are", "<3", "and", "snap")):
            if account[i + 1] == "and" and account[i + 2] == "snap":
                account = account[i + 3][1:] if account[i + 3].startswith("@") else account[i + 3]
            else:
                account = account[i + 2][1:] if account[i + 2].startswith("@") else account[i + 2]
        else:
            account = account[i + 1][1:] if account[i + 1].startswith("@") else account[i + 1]
        del i
    
    elif caption.count("@") == 1: # one @ symbol
        account = caption[caption.index("@") + 1:]
        account = account.split()[0] # the first word after @
        
    elif caption.count("@") >= 2:
        account = caption[len(caption) - caption[::-1].index("@"):]
        account = account.split()[0] # get last @
    else: # if there is no @, I can't DM them for a bio, so no point in including them on the account
        next_post()
        continue

    # CHECK DATE OF POST TO MAKE SURE POSTS ARE STILL RELEVANT
    date_of_post = driver.driver.find_element("xpath", "//time[@class='_a9ze _a9zf']").get_attribute("datetime")
    date_of_post = date_of_post[0:date_of_post.index("T")] # subset date of post to just include the date
    date_of_post = datetime.strptime(date_of_post, "%Y-%m-%d")
    if date_of_post < stop_date: # if post before January 1, 2023, break the while loop
        if not stop_key_present:
            accounts_muir_writable.write(stop_key + "\n") # write
            accounts_already_scraped_writable.write(stop_key + "\n")
        print("All relevant accounts parsed.")
        del date_of_post
        break # if there is no more posts, exit the while loop
    
    # SKIP ITERATION IF PROGRAM HAS ALREADY SCRAPED ACCOUNTS BEFORE 
    if account in accounts_already_scraped or len(account) < 3:
        next_post()
        continue
    else: # if not in accounts_already_scraped, add to accounts_already_scraped (and the account name is 3 or more characters)
        accounts_already_scraped.add(account)
        accounts_already_scraped_writable.write(account + "\n")
        
    # ADD SOME EXTRA WAIT TIME TO SIMULATE READING CAPTION
    driver.wait(3, 5)
    
    # IF ACCOUNT MENTIONS MUIR, NOTE THEIR ACCOUNT NAME
    if "muir" in caption and account not in accounts_muir:
        accounts_muir.add(account)
        accounts_muir_writable.write(account + "\n")
    del caption
    
    # CLICK NEXT BUTTON, THOUGH THERE MIGHT BE NO NEXT
    try:
        next_post()
    except: # if there is no next post
        break # exit loop


# CLOSE OUTPUTS
accounts_muir_writable.close()
accounts_already_scraped_writable.close()


# FOLLOW ACCOUNTS

# click on exit button
driver.driver.find_element("xpath", "//*[name()='svg'][@aria-label='Close']").click()
driver.wait(0.5, 1)

# click on home button
driver.driver.find_element("xpath", "//a[@href='/']/div/div/div/div/*[name()='svg'][@aria-label='Home']").click()
driver.wait(0.5, 1)

# click the search button
driver.click_search()

for account in (account for account in accounts_muir if account not in accounts_followed and account != stop_key):
    
    driver.wait(0.75, 1.5)
    
    # TYPE IN ACCOUNT NAME
    driver.simulate_typing(element = driver.driver.find_element("xpath", "//input[@aria-label='Search input']"), text = account)
    driver.wait(3, 4)

    # TRY TO GO TO DESIRED INSTAGRAM ACCOUNT
    try:
        # click on account
        driver.driver.find_element("xpath", f"//a[@href='/{account}/']").click() # click on account with the correct username
        driver.wait(3, 4)
        
    except: # ACCOUNT NAME ENTERED WASN'T CORRECT, MEANING THEY PROVIDED A FAULTY ACCOUNT NAME
        driver.driver.find_element("xpath", "//input[@aria-label='Search input']").clear()
        continue
        
    # try to click follow, unless I already follow them
    try:
        driver.driver.find_element("xpath", "//button[@class='_acan _acap _acas _aj1-']").click()
        driver.wait(2, 3)
    except: # if I already requested/followed them, but they aren't in accounts_followed (because we wouldn't be looping over this account if they were), keep going
        driver.wait(0.5, 1.5)
        
    # write to file
    accounts_followed.add(account) # they are not in accounts followed
    accounts_followed_writable.write(account + "\n")
        
    # click on search again (click search if input area isn't there)
    try:
        driver.driver.find_element("xpath", "//div[@aria-label='Clear the search box']").click()
    except:
        driver.click_search()

print("Followed all accounts in accounts.muir.")

# CLOSE OUTPUTS
accounts_followed_writable.close()
driver.driver.quit()