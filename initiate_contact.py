# README
# Phillip Long
# May 11, 2023

# This script is meant to, given a list of accounts, initiate contact via DM to these accounts.

# python ~/finding_a_roommate/initiate_contact.py driver_address username password accounts_to_dm

# driver_address = filepath to Selenium Chrome Web Driver, download at: https://chromedriver.chromium.org/downloads
# username = Instagram username
# password = Instagram password
# accounts_to_dm = absolute filepath to list of accounts generated by find_accounts.py


# IMPORTS
from login import instagram_driver # my own class that logs into instagram for me while creating a driver
import sys # for stdin arguments
from os.path import exists, dirname # for checking if files exist and determining the output file

# ARGUMENTS
# sys.argv = ("intiate_contact.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs/accounts_followed.txt")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2].replace("@", "") # username, remove @ symbol if included
password = sys.argv[3] # password
accounts_muir_output = sys.argv[4] # accounts_to_dm

stop_key = "*******************" # string to put at the end of files signaling they are complete

# CREATE DRIVER AND LOGIN
driver = instagram_driver(driver_address = driver_address, username = username, password = password) # create instance of chrome driver
driver.login()

# CLICK ON DM BUTTON
driver.click_messages()


# READ IN FILES, CREATE SETS
accounts_muir = set(()) # set of accounts that mention muir (no duplicates)
if exists(accounts_muir_output):
    for line in open(accounts_muir_output):
        if stop_key not in line:
            accounts_muir.add(str(line).strip())

accounts_initiated_contact = set(()) # set of accounts that the program might have initiated contact with (no duplicates)
accounts_initiated_contact_output = dirname(accounts_muir_output) + "/accounts_initiated_contact.txt"
if exists(accounts_initiated_contact_output):
    for line in open(accounts_initiated_contact_output):
        accounts_initiated_contact.add(str(line).strip())
accounts_initiated_contact_writable = open(accounts_initiated_contact_output, "a")

unread_messages = driver.driver.find_elements("xpath", "//div[@aria-label='Unread']")
unread_messages = list(element.find_element("xpath", "./../../../../../..") for element in unread_messages)
unread_accounts = ["", ] * len(unread_messages)
for i in range(len(unread_messages)):
    account = unread_messages[i].find_element("xpath", "./div/div/div/div/div/div/span/img[@class='x6umtig x1b1mbwd xaqea5y xav7gou xk390pu x5yr21d xpdipgo xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3']").get_attribute("alt")
    unread_accounts[i] = account[:len(account) - len("'s profile picture")]
    del account
del unread_messages

accounts_to_dm = set((account for account in accounts_muir if not (account in accounts_initiated_contact or account in unread_accounts)))
del accounts_muir, accounts_initiated_contact, unread_accounts

# DM ACCOUNTS
message = "Hi fellow Muiron! Congratulations on your acceptance! I created this account to deal with the backlog on @ucsandiego.2027; at the same time, a lot of the people posted to the account were irrelevant to me, since they were not in Muir and I cannot room with them. Would you like to be posted to this account? If yes, please respond by sending 3-5 pictures of yourself + a bio, in that order (personally, I would reuse what I sent / plan to send to @ucsandiego.2027). If no, just don't respond. Though this account is supervised by a real person, many of its functions are automated, so if you could abide by the aforementioned rules, it would make the posting process a lot smoother. Thanks for your time, and again, congrats!"
if message == "":
    print("Error: faulty message. Message must be at least one character long.")
    quit()
first_account_to_dm = True
for account in accounts_to_dm:
    
    try:
        # CLICK ON NEW MESSAGE ICON
        driver.driver.find_element("xpath", "//button[@class='_abl- _abm2']").click()
        driver.wait(2, 4.5)
        
        # ENTER ACCCONT NAME
        driver.simulate_typing(element = driver.driver.find_element("xpath", "//input[@name='queryBox'][@placeholder='Search...']"),
                               text = account)
        driver.wait(1, 2)

        # SELECT ACCOUNT TO DM
        driver.driver.find_element("xpath", f"//span[@class='x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft'][text()='{account}']").click()
        driver.wait(1, 1.5)
        
        # CLICK ON NEXT BUTTON
        driver.driver.find_element("xpath", "//button[@class='_acan _acao _acas _acav _aj1-']/div[text()='Next']").click()
        driver.wait(2, 3)
        
        # CHECK IF THEY HAVE INITIATED CONTACT WITH ME ALREADY
        if len(driver.driver.find_elements("xpath", "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv xuk3077 x1oa3qoh x1nhvcw1']/div[@class='_ac72']/div/div/div[@class='_acqt _acqu']/div/div/div/div/*")) != 0:
            continue
        
        # SEND MESSAGE, ALSO DETERMINE HOW FAST TO TYPE
        if first_account_to_dm: # if first iteration, type out the message slowly
            scalar = 3.0
            first_account_to_dm = False # update boolean
        else: # not the first iteration
            scalar = 0.0
        driver.send_message(text = message, scalar = scalar)
        driver.wait(0.5, 1.5)
        
        # WRITE ACCOUNT TO ACCOUNTS I HAVE INITIATED CONTACT WITH FILE
        accounts_initiated_contact_writable.write(account + "\n")

    except:
        driver.wait(1.5, 2) # if for some reason the account doesn't exist anymore or something, wait, and move on
        driver.driver.find_element("xpath", "//div[@class='_abm0']/*[name()='svg'][@aria-label='Close']").click()
        driver.wait(0.5, 1.5)


# CLOSE OUTPUTS
accounts_initiated_contact_writable.close()
driver.driver.quit()