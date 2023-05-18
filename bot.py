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
# output_directory = path to directory to output various files


# IMPORTS
from login import instagram_driver # my own class that logs into instagram for me while creating a driver
import sys # for stdin arguments
from os.path import exists # for checking if files exist
from os import makedirs, listdir, remove, rmdir # for making and removing directories
from urllib.request import urlretrieve # for downloading media from URL
from PIL import Image # for OCR
import pytesseract # for OCR
pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract" # location of pytesseract executable file

# ARGUMENTS
# sys.argv = ("bot.py", "/Users/philliplong/Desktop/Coding/chromedriver", "", "", "/Users/philliplong/Desktop/Coding/finding_a_roommate/outputs")
driver_address = sys.argv[1] # driver_address
username = sys.argv[2] # username
password = sys.argv[3] # password
output_directory = sys.argv[4] # directory to output to

# make sure file doesn't end with a /
correct_filepath = lambda filepath: filepath[:len(filepath) - 1] if filepath.endswith("/") else filepath

# edit arguments
output_directory = correct_filepath(output_directory) + "/"


# CREATE DRIVER AND LOGIN
driver = instagram_driver(driver_address = driver_address, username = username, password = password) # create instance of chrome driver
driver.login()

# GO TO DMS
driver.click_messages()


# READ IN FILES, CREATE SETS
# succesful posts
accounts_success = set(()) # set of accounts that I have successfully posted (no duplicates)
accounts_success_output = output_directory + "successful_posts.txt"
if exists(accounts_success_output):
    for line in open(accounts_success_output):
        accounts_success.add(str(line).strip())
accounts_success_writable = open(accounts_success_output, "a")

# failed posts
accounts_concern = set(()) # set of accounts that I have failed to post (error in the posting process) or I need to look at personally for other reasons (no duplicates)
accounts_concern_output = output_directory + "concerns.txt"
if exists(accounts_concern_output):
    for line in open(accounts_concern_output):
        accounts_concern.add(str(line).strip())
accounts_concern_writable = open(accounts_concern_output, "a")


# CREATE OUTPUT DIRECTORY IF IT DOES NOT YET EXIST
if not exists(output_directory): # if output directory doesn't exist yet
    makedirs(output_directory) # create the new directory

# CREATE TEMPORARY FILE STORAGE DIRECTORY
temporary_output = output_directory + "temp"
if not exists(temporary_output):
    makedirs(temporary_output)


# HELPER FUNCTIONS

# clear a directory of all files
def clear_dir(directory):
    directory = correct_filepath(directory) # deal with / at end of directory
    for file in listdir(directory):
        remove(directory + "/" + file)
clear_dir(temporary_output) # clear in case there is anything
    
# analyze chats
def get_chats():
    
    # get DMs (only from other user, since mine are irrelevant)
    chats = driver.driver.find_elements("xpath", "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv xuk3077 x1oa3qoh x1nhvcw1']/div[@class='_ac72']/div/div/div[@class='_acqt _acqu']/div/div/div/div/*")
    
    # create list of dms; note the source link for image and video (media)
    for i, chat in enumerate(chats):
        if chat.text != "": # deal with text
            chats[i] = ("text", chat.text)
        elif chat.tag_name == "img": # deal with images
            chats[i] = ("image", chat.get_attribute("src"))
        elif chat.tag_name == "video": # deal with videos
            chats[i] = ("video", chat.find_element("xpath", f"./source").get_attribute("src"))
        else: # in the event the attachment is not text, an image, or a video
            chats[i] = None
    
    # remove empty values, since we don't care about them
    chats = list(filter(lambda chat: chat is not None, chats))
    
    return chats

# decide what pictures to post
def decide_post(chats, media_directory = temporary_output): # media_directory is the directory in which all the files to post will be (labelled in order of how to post)
    
    # deal with media_directory
    media_directory = correct_filepath(media_directory)
    if not exists(media_directory): # if media directory doesn't exist yet
        makedirs(media_directory) # create the new directory
       
    # determine media to post
    media = list(chat for chat in chats if chat[0] in ("image", "video"))
    acceptance_letter_indicies = [False, ] * len(media)
    for i in range(len(media)):
        if media[i][0] == "image":
            if image_is_acceptance_letter(image_url = media[i][1]): # if first image is an acceptance letter remove it
                acceptance_letter_indicies[i] = True
    media = list(media[i] for i in range(len(media)) if not acceptance_letter_indicies[i]) # remove any acceptance letter image
    acceptance_letter_present = any(acceptance_letter_indicies)
    del acceptance_letter_indicies
    
    # check for and remove duplicates in media
    media = list(dict.fromkeys(media[::-1]))[::-1] # remove duplicates (keep media most recently sent)
    
    # download media to device
    media_filepaths = list("" for i in range(len(media)))
    for i, file in enumerate(media):
        suffix = "jpg" if file[0] == "image" else "mp4" # determine filetype
        output_filepath = f"{media_directory}/{i}.{suffix}" # determine filepath
        media_filepaths[i] = output_filepath # add filpath to media_filepaths
        urlretrieve(file[1], output_filepath) # download media to local device
        del suffix, output_filepath
    del media
    
    return media_filepaths, acceptance_letter_present

# post pictures
def post(caption, media_filepaths):
    
    # click on Create
    driver.driver.find_element("xpath", "//a[@href='#']/div/div/div/div/*[@aria-label='New post']").click()
    driver.wait(1, 2)
    
    # upload to instagram
    driver.driver.find_element("xpath", "//input[@type='file'][@accept='image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime']").send_keys("\n".join(media_filepaths))
    driver.wait(6, 8)
    
    # wait for pictures to upload
    done_uploading = False
    seconds_elapsed = 0
    max_seconds_elapsed = 12
    while not done_uploading and seconds_elapsed <= max_seconds_elapsed:
        try:
            driver.driver.find_element("xpath", "//div[text()='Crop']")
            done_uploading = True
        except:
            seconds_elapsed += 1
            driver.wait(1, 1)
    if seconds_elapsed > max_seconds_elapsed:
        return False
    del done_uploading, seconds_elapsed
    
    # if there is the "Videos are now reels" popup
    try:
        driver.driver.find_element("xpath", "//button[text()='OK']").click()
        driver.wait(1, 1.5)
    except:
        pass
    
    # click Next to go to Filters section
    driver.driver.find_element("xpath", "//div[text()='Next']").click()
    driver.wait(1, 1.5)
    
    # click Next again to go to create new post section
    driver.driver.find_element("xpath", "//div[text()='Next']").click()
    driver.wait(1, 1.5)
    
    # type in caption
    driver.simulate_typing(element = driver.driver.find_element("xpath", "//div[@aria-label='Write a caption...']/p"),
                           text = caption, scalar = 0.5)
    driver.wait(1, 1.5)
    
    # click Share
    driver.driver.find_element("xpath", "//div[text()='Share']").click()
    done_posting = False
    seconds_elapsed = 0
    while not done_posting and seconds_elapsed <= max_seconds_elapsed:
        try:
            driver.driver.find_element("xpath", "//img[@alt='Animated checkmark']")
            done_posting = True
        except:
            seconds_elapsed += 1
            driver.wait(1, 1)
    if seconds_elapsed > max_seconds_elapsed:
        return False
    del done_posting, seconds_elapsed
    driver.wait(1, 2)
    
    # close posting window
    driver.driver.find_element("xpath", "//div/div/*[@aria-label='Close']").click()
    driver.wait(3, 4)
    
    return True
        
# check if the first image in a given an image url is a screenshot of an acceptance letter
def image_is_acceptance_letter(image_url):
    image_filepath = correct_filepath(temporary_output) + "/is_acceptance_letter.jpg" # determine temporary filepath to image
    urlretrieve(image_url, image_filepath) # download image to local device
    image_text = pytesseract.image_to_string(Image.open(image_filepath)) # OCR
    remove(image_filepath) # remove image file
    del image_filepath
    return "muir" in image_text.lower()

# try to post, given that the bot is already in the chat with the other person
def try_to_post(account, checking_for_acceptance_letter):
    
    # get chats
    driver.scroll(a = 600, b = 0, element = driver.driver.find_element("xpath", "//div[@class='_ab5z _ab5_']")) # scroll up to load in DMs
    chats = get_chats()
    
    # determine caption
    caption = list(chat[1] for chat in chats if chat[0] == "text")
    if "ERROR" in list(map(lambda x: x.upper(), caption)): # if any chat is ERROR, add to accounts concern and have me manually review it
        accounts_concern_writable.write(account + "\n")
        accounts_concern.add(account)
        return None
    caption.sort(key = len) # sort caption by string length; the longest string is almost always the desired caption
    caption = caption[len(caption) - 1] # the longest string is the last string
    
    # decide what to post
    media_filepaths, acceptance_letter_present = decide_post(chats = chats)
    del chats
    driver.wait(2, 3)
    
    if checking_for_acceptance_letter and not acceptance_letter_present: # if no acceptance letter present, and I am checking for acceptance letter
        driver.send_message(text = "Hi! Thanks for your interest in this account. Could you please send a screenshot of your acceptance letter showing that you are in Muir? Some of the functions of this account are automated, so if this IS an error, please respond with ERROR (in all caps) for the account administrator to manually review your submission.")
        return None
    
    if acceptance_letter_present and len(media_filepaths) == 0: # if there is no media other than screenshot of acceptance letter
        driver.send_message(text = "Hi fellow Muiron! Thanks for sending in your acceptance letter. Congratulations! Please send 3-5 pictures of yourself + a bio, in that order (personally, I would reuse what I sent / plan to send to @ucsandiego.2027). Though this account is supervised by a real person, many of its functions are automated, so if you could abide by the aforementioned rules, it would make the posting process a lot smoother. Thanks for your time, and again, congrats!")
        return None
    
    if not acceptance_letter_present and len(media_filepaths) == 0: # not checking_for_acceptance_letter is implied from first if statement
        driver.send_message(text = "Hi! Congratulations on your acceptance! Would you like to be posted to this account? If yes, please respond by sending 3-5 pictures of yourself + a bio, in that order (personally, I would reuse what I sent / plan to send to @ucsandiego.2027). If no, just don't respond. Though this account is supervised by a real person, many of its functions are automated, so if you could abide by the aforementioned rules, it would make the posting process a lot smoother. Thanks for your time, and again, congrats!")
        return None
    
    # no need to return to messages at this point because we never left messages pane to begin with

    # post
    posted = post(caption = caption, media_filepaths = media_filepaths)
    del caption, media_filepaths
    
    if not posted: # if post was not successful
        failure_protocol(account)
        
    # send dm confirming post
    driver.click_messages() # return to Messages pane
    driver.driver.find_element("xpath", f"//img[@alt=\"{account}'s profile picture\"]").click() # return to Chat with person
    driver.send_message(text = "Your information has been posted! Please notify me if there are any issues with your post.")
    
    # write to file
    accounts_success_writable.write(account + "\n")
    accounts_success.add(account)

# protocol for if info fails to be posted for some reason
def failure_protocol(account):
    # go to dms in case I'm not already there
    driver.click_messages()

    # click on message
    driver.driver.find_element("xpath", f"//img[@alt=\"{account}'s profile picture\"]").click()
    driver.wait(1, 2)
        
    # send error message
    driver.send_message(text = "Unfortunately, there was an error in the posting process. I have notified the account administrator, who will deal with the issue personally as soon as possible.")
    accounts_concern_writable.write(account + "\n")
    accounts_concern.add(account)


# GET A LIST OF UNREAD MESSAGES
driver.scroll(a = 0, b = 800, element = driver.driver.find_element("xpath", "//div[@class='_abyk']")) # scroll down in the messages pane
unread_messages = driver.driver.find_elements("xpath", "//div[@aria-label='Unread']")
unread_messages = list(element.find_element("xpath", "./../../../../../..") for element in unread_messages)

# RESPOND TO EACH UNREAD MESSAGE
# A DM will pop up in the normal messages tab if I follow the account
# The instagram account controlled by the bot should only follow people previously vetted by @ucsandiego.2027
# This means there is no requirement for the people to show their acceptance letter
for unread_message in unread_messages:
    
    # GET ACCOUNT NAME
    account = unread_message.find_element("xpath", "./div/div/div/div/div/div/span/img[@class='x6umtig x1b1mbwd xaqea5y xav7gou xk390pu x5yr21d xpdipgo xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3']").get_attribute("alt")
    account = account[:len(account) - len("'s profile picture")]
    
    if account in accounts_success: # if I have already succesfully posted this account, skip and let me deal with it manually
        accounts_concern.add(account) # add to accounts concern so I can see what else they have to say
        continue
    
    # CLICK ON MESSAGE
    unread_message.click()
    driver.wait(1, 2)
    
    # TRY TO POST
    try:
        try_to_post(account = account, checking_for_acceptance_letter = False) # no need to vet these users, because @ucsandiego.2027 has already done so
    except: # if it didn't work for some reason
        failure_protocol(account = account)
    
    # REMOVE LOCAL TEMPORARY FILES
    clear_dir(temporary_output)


# RESPOND TO EACH MESSAGE REQUEST (IF THERE ARE ANY)
try:
    # CLICK ON REQUESTS BUTTON
    driver.driver.find_element("xpath", "//span[contains(text(),'Request')]").click()

    # GET A LIST OF REQUESTS
    requests = driver.driver.find_elements("xpath", "//div/div/div/div/div/div/span/img[@class='x6umtig x1b1mbwd xaqea5y xav7gou xk390pu x5yr21d xpdipgo xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3']")

    # ADDRESS EACH REQUEST
    for i, request in enumerate(requests):
        
        # GET ACCOUNT NAME
        account = request.get_attribute("alt")
        account = account[:len(account) - len("'s profile picture")]
        
        # CLICK ON REQUEST
        request.click()
        driver.wait(1, 2)
        
        # CLICK ON ACCEPT
        driver.driver.find_element("xpath", "//span[text()='Accept']").click()
        
        try:
            try_to_post(account = account, checking_for_acceptance_letter = True) # vet these users because they were not vetted by @ucsandiego.2027
        except:
            failure_protocol(account = account)
        
        # CLICK ON REQUESTS BUTTON IF IT IS THERE
        if i <= len(requests) - 2:
            driver.scroll(a = 800, b = 0, element = driver.driver.find_element("xpath", "//div[@class='_abyk']")) # scroll up in the messages pane to see requests
            driver.driver.find_element("xpath", "//span[contains(text(),'Request')]").click()

        # REMOVE LOCAL TEMPORARY FILES
        clear_dir(temporary_output)
            
except:
    pass


# OUTPUT VARIOUS FILES
rmdir(temporary_output)

# CLOSE OUTPUTS
accounts_success_writable.close()
accounts_concern_writable.close()

driver.driver.quit()