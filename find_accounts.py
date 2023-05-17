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
# sys.argv = ("find_accounts.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "", "ucsandiego.2027", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs/")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2].replace("@", "") # username, remove @ symbol if included
password = sys.argv[3] # password
username_to_scrape = sys.argv[4].replace("@", "") # username_to_scrape, remove @ symbol if included
output_directory = sys.argv[5] if sys.argv[5].endswith("/") else sys.argv[5] + "/" # directory to output to

stop_key = "*******************" # string to put at the end of files signaling they are complete
stop_date = "2023-01-01" # date to stop scraping account


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

if stop_key in accounts_muir or stop_key in accounts_already_scraped:
    print("All relevant accounts parsed.")
    stop_date = "2023-05-10" # reset stop_date to a more sooner, quicker to scrape date

# FUNCTION FOR CLICKING TO NEXT POST
def next_post(): # click the next button
    driver.driver.find_element("xpath", "//div[@class=' _aaqg _aaqh']").click()
    

# CLICK SEARCH BUTTON TO FIND ACCOUNT AND ENTER DESIRED INSTAGRAM ACCOUNT
driver.click_search()
driver.simulate_typing(element = driver.driver.find_element("xpath", "//input[@aria-label='Search input']"),
                       text = username_to_scrape)
driver.wait(1, 2)

# GO TO DESIRED INSTAGRAM ACCOUNT
driver.driver.find_element("xpath", f"//a[@href='/{username_to_scrape}/']").click() # click on account with the correct username
driver.wait(3, 4)

# SCROLL DOWN TO FIRST POST
y_scroll_most_recent = 400
driver.scroll(a = 0, b = y_scroll_most_recent)
driver.wait(1.5, 3)

# CLICK ON FIRST POST
driver.driver.find_element("xpath", ".//a[contains(@href,'/p/')]").click() # finds all posts (href that contains "/p/"), returns the first one! 
# wait time is added in loop


# BEGIN SCRAPING PAGE
date_of_post_is_valid = True
while date_of_post_is_valid:
    
    # WAIT TIME REGARDLESS OF WHETHER PROGRAM HAS SEEN POST BEFORE
    driver.wait(0.5, 1.5)

    # READ CAPTION
    caption = driver.driver.find_element("xpath", "//h1[@class='_aacl _aaco _aacu _aacx _aad7 _aade']")
    caption = caption.text.lower() # put into lower case to make comparisons easier, also puts account into lower case
    caption = sub(pattern = r"@[^A-Za-z0-9_.]", repl = "", string = caption) # deal with randomly-used @ symbols that aren't social media usernames
    caption = sub(pattern = r"[:-=/()]", repl = "", string = caption) # remove separator charactors
    
    
    # DETERMINE ACCOUNT NAME
    if any(instagram in caption.split() for instagram in ("insta", "ig", "instagram")):
        account = caption.split()
        i = tuple(i for i in range(len(account)) if any(instagram == account[i] for instagram in ("insta", "ig", "instagram", "instasnap", "instagramsnap", "igsnap", "snapinsta", "snapinstagram", "snapig", "instasnapchat", "instagramsnapchat", "igsnapchat", "snapchatinsta", "snapchatinstagram", "snapchatig")))[-1] # choose the final mention of instagram
        if any(account[i + 1] == x for x in ("is", "<3", "and", "snap")):
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

    # SKIP ITERATION IF PROGRAM HAS ALREADY SCRAPED ACCOUNTS BEFORE 
    if account in accounts_already_scraped:
        next_post()
        continue
    else: # have not yet scraped this account
        accounts_already_scraped.add(account)
        accounts_already_scraped_writable.write(account + "\n")

    
    # CHECK DATE OF POST TO MAKE SURE POSTS ARE STILL RELEVANT
    date_of_post = driver.driver.find_element("xpath", "//time[@class='_a9ze _a9zf']").get_attribute("datetime")
    date_of_post = date_of_post[0:date_of_post.index("T")] # subset date of post to just include the date
    date_of_post = datetime.strptime(date_of_post, "%Y-%m-%d")
    if date_of_post < datetime.strptime(stop_date, "%Y-%m-%d"): # if post before January 1, 2023, break the while loop
        accounts_muir_writable.write(stop_key + "\n") # write
        accounts_already_scraped_writable.write(stop_key + "\n")
        del date_of_post
        date_of_post_is_valid = False
        break # if there is no more posts, exit the while loop
    del date_of_post
    
    
    # ADD SOME EXTRA WAIT TIME TO SIMULATE READING CAPTION
    driver.wait(3, 5)
    
    
    # IF ACCOUNT MENTIONS MUIR, FOLLOW THEM
    if "muir" in caption:

        # MAKE NOTE OF CURRENT URL
        current_url = str(driver.driver.current_url).split("/")
        current_url = current_url[len(current_url) - 2]
        
        # IF ACCOUNT HAS BEEN DELETED OR THE USER DIDN'T LINK THEIR INSTAGRAM PROPERLY
        try:
            
            # CLICK ON ACCOUNT
            driver.driver.find_element("xpath", f"//a[@href='/{account}/']").click()
            driver.wait(2, 3)
            
            # SCROLL TO TOP OF PAGE IF NOT ALREADY THERE
            driver.scroll(a = driver.driver.execute_script("return window.pageYOffset;"), b = 0)
            driver.wait(0.5, 1)
                        
            # CLICK FOLLOW
            driver.driver.find_element("xpath", "//button[@class='_acan _acap _acas _aj1-']").click()
            driver.wait(2, 3)
            
            # GO BACK
            driver.driver.back()
            
            # ADD ACCOUNT TO ACCOUNTS_MUIR
            if account not in accounts_muir:
                accounts_muir.add(account)
                accounts_muir_writable.write(account + "\n")
            
        except:
            # GO BACK
            driver.driver.get(f"https://www.instagram.com/p/{current_url}/")
            driver.wait(2, 2.5)
            
            # GO TO USERNAME_TO_SCRAPE
            driver.driver.find_element("xpath", f"//a[@href='/{username_to_scrape}/'][@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp xqnirrm xj34u2y x568u83 x3nfvp2']").click()
            driver.wait(1, 1.3)


        # RELOCATE POST WE WERE JUST LOOKING AT
        driver.wait(0.75, 1.25)
        
        # get us most of the way there (to the y_scroll_most_recent) at a faster speed
        while driver.driver.execute_script("return window.pageYOffset;") < y_scroll_most_recent:
            try:
                driver.scroll(a = driver.driver.execute_script("return window.pageYOffset;"), b = y_scroll_most_recent, scalar = 0.14) # scroll to previous post
            except:
                pass
            driver.wait(0.5, 1.25)
        
        # get us the rest of the way there, more slowly
        a = driver.driver.execute_script("return window.pageYOffset;") # where to start scrolling from
        scroll_per_iter = 300 # amount to scroll each time
        back_to_post = False # whether the program can locate the post element
        while not back_to_post:
            try:
                relocated_post = driver.driver.find_element("xpath", f"//a[@href='/p/{current_url}/']") # if this succeeds, we are near the post (its loaded in)
                driver.scroll(a = a, b = relocated_post.location["y"]) # scroll to previous post
                y_scroll_most_recent = relocated_post.location["y"] # update y_scroll_most_recent
                driver.wait(0.5, 1.25)
                relocated_post.click() # click on post
                del relocated_post
                driver.wait(1, 1.25)
                back_to_post = True
            except: # back_to_post remains False
                driver.scroll(a = a, b = a + scroll_per_iter)
                a += scroll_per_iter # update a
                driver.wait(0.75, 1)
        del a, scroll_per_iter, back_to_post
        
    
    del caption
    

    # CLICK NEXT BUTTON
    try:
        next_post()
    except: # if there is no next post
        break # exit loop

del date_of_post_is_valid, y_scroll_most_recent




# BEGIN SCRAPING PAGE, MAKING NOTE OF MUIR ACCOUNTS
while True:
    
    # WAIT TIME REGARDLESS OF WHETHER PROGRAM HAS SEEN POST BEFORE
    driver.wait(0.5, 1.5)

    # READ CAPTION
    caption = driver.driver.find_element("xpath", "//h1[@class='_aacl _aaco _aacu _aacx _aad7 _aade']")
    caption = caption.text.lower() # put into lower case to make comparisons easier, also puts account into lower case
    caption = sub(pattern = r"@[^A-Za-z0-9_.]", repl = "", string = caption) # deal with randomly-used @ symbols that aren't social media usernames
    caption = sub(pattern = r"[:-=/()]", repl = "", string = caption) # remove separator charactors
    
    # DETERMINE ACCOUNT NAME
    if any(instagram in caption.split() for instagram in ("insta", "ig", "instagram")):
        account = caption.split()
        i = tuple(i for i in range(len(account)) if any(instagram == account[i] for instagram in ("insta", "ig", "instagram", "instasnap", "instagramsnap", "igsnap", "snapinsta", "snapinstagram", "snapig", "instasnapchat", "instagramsnapchat", "igsnapchat", "snapchatinsta", "snapchatinstagram", "snapchatig")))[-1] # choose the final mention of instagram
        if any(account[i + 1] == x for x in ("is", "<3", "and", "snap")):
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
    if date_of_post < datetime.strptime(stop_date, "%Y-%m-%d"): # if post before January 1, 2023, break the while loop
        accounts_muir_writable.write(stop_key + "\n") # write
        accounts_already_scraped_writable.write(stop_key + "\n")
        del date_of_post
        break # if there is no more posts, exit the while loop
    del date_of_post
    
    # SKIP ITERATION IF PROGRAM HAS ALREADY SCRAPED ACCOUNTS BEFORE 
    if account in accounts_already_scraped:
        next_post()
        continue
    else: # have not yet scraped this account
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

for account in (account for account in accounts_muir if account not in accounts_followed):
    
    driver.wait(0.75, 1.5)
    
    # TYPE IN ACCOUNT NAME
    driver.simulate_typing(element = driver.driver.find_element("xpath", "//input[@aria-label='Search input']"), text = account)
    driver.wait(0.5, 2)

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
    except:
        driver.wait(0.5, 1.5)
        
    # write to file
    accounts_followed.add(account)
    accounts_followed_writable.write(account + "\n")
        
    # click on search again
    driver.click_search()


# CLOSE OUTPUTS
accounts_followed_writable.close()
driver.driver.quit()