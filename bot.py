# README
# Phillip Long
# May 6, 2023

# I was recently admitted to UC San Diego, and on Instagram, there is this account called @ucsandiego.2027
# A lot of incoming freshmen post to this account, both to make friends and find potential roommates
# However, the page is chaotic to say the least...there are thousands of people posting about themselves
# and since I can't dorm with most of the people posting, I want a page just for Muir College Class of 2027
# This will make things a lot more manageable and easier to find a roommate.

# python ~/finding_a_roommate/bot.py $driver_address $username $password $output_directory

# driver_address = filepath to Selenium Chrome Web Driver, download at: https://chromedriver.chromium.org/downloads
# username = Instagram username
# password = Instagram password
# output_directory = path to directory to output various files


# IMPORTS
from login import instagram_driver # my own class that logs into instagram for me while creating a driver
import sys # for stdin arguments
from os.path import exists # for checking if files exist
from os import makedirs, listdir, remove, rmdir # for making and removing directories
from cleantext import clean # for removing emojis from captions
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
messages_window_scrollable_xpath = "//div[@data-pagelet='IGDThreadList']/div[@aria-label='Chats']/div/div/div"


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
    chats = driver.driver.find_elements("xpath", "//div[@class='x1qjc9v5 x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x78zum5 xdt5ytf x2lah0s xk390pu xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xggy1nq x11njtxf']/div[@class='x78zum5 xh8yej3']/div[@class='x1cy8zhl x78zum5 xdt5ytf x193iq5w x1n2onr6']")
    
    # create list of dms; note the source link for image and video (media)
    for i, chat in enumerate(chats):
        if chat.text != "": # deal with text
            chats[i] = ("text", chat.text)
            continue
        chat = chat.find_element("xpath", "./div/div/div/div/div/div/div/div/div/*")
        if chat.tag_name == "img": # deal with images
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
        media_filepaths[i] = output_filepath # add filepath to media_filepaths
        urlretrieve(file[1], output_filepath) # download media to local device
        image = Image.open(output_filepath)
        dims = list(image.size)
        if dims[0] > 1080: # width
            k = 1080 / dims[0]
            dims = [int(k * dims[0]), int(k * dims[1])]
        if dims[1] > 1080: # height
            k = 1080 / dims[1]
            dims = [int(k * dims[0]), int(k * dims[1])]
        if tuple(dims) != image.size:
            image.resize(dims).save(output_filepath)
        image.close()
        del suffix, output_filepath, image, dims
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
    return any(keyword in image_text.lower().replace("\n", "") for keyword in ("muir", "triton", "san diego", "2027", "150,000", "application", "admission"))

# try to post, given that the bot is already in the chat with the other person
def try_to_post(account, account_name, checking_for_acceptance_letter):
    
    # get chats
    driver.scroll_to_end(element = driver.driver.find_element("xpath", "//div[@data-pagelet='IGDOpenMessageList']/div/div/div/div/div"), direction = -1, scalar = 0.5) # scroll up to load in DMs
    chats = get_chats()
    
    # see if the person sent a collection instead of photos
    try:
        collection_sent = chats[::-1].index(("text", "Use latest app\nUse the latest version of the Instagram app to see this type of message")) in (0, 1)
    except:
        collection_sent = False
        
    # determine caption
    caption = list(chat[1] for chat in chats if chat[0] == "text")
    if "ERROR" in list(map(lambda x: x.upper(), caption)): # if any chat is ERROR, add to accounts concern and have me manually review it
        accounts_concern_writable.write(account + "\n")
        accounts_concern.add(account)
        driver.click_messages()
        return None
    caption.sort(key = len) # sort caption by string length; the longest string is almost always the desired caption
    caption = caption[len(caption) - 1] # the longest string is the last string
    caption = clean(caption, no_emoji = True)
    
    # decide what to post
    media_filepaths, acceptance_letter_present = decide_post(chats = chats)
    del chats
    driver.wait(2, 3)
    
    if checking_for_acceptance_letter and not acceptance_letter_present: # if no acceptance letter present, and I am checking for acceptance letter
        driver.send_message(text = "Hi! Thanks for your interest in this account. Could you please send a screenshot of your acceptance letter showing that you are in Muir? Some of the functions of this account are automated, so if this IS an error, please respond with ERROR (in all caps) for the account administrator to manually review your submission.")
        driver.click_messages()
        return None
    
    elif len(media_filepaths) == 0 and collection_sent: # if the person sent a collection (which I can't open)
        driver.send_message(text = "I know this sounds weird, but could you resend your pictures one-by-one? I use an old version of Instagram and I can't download the collection of pictures you sent. Thanks!")
        driver.click_messages()
        return None
        
    elif acceptance_letter_present and len(media_filepaths) == 0: # if there is no media other than screenshot of acceptance letter
        driver.send_message(text = "Thanks for sending in your acceptance letter. Congratulations! Please send 3-5 pictures of yourself + a bio, in that order (personally, I would reuse what I sent / plan to send to @ucsandiego.2027). Though this account is supervised by a real person, many of its functions are automated, so if you could abide by the aforementioned rules, it would make the posting process a lot smoother. Thanks for your time, and again, congrats!")
        driver.click_messages()
        return None
    
    elif not acceptance_letter_present and len(media_filepaths) == 0: # not checking_for_acceptance_letter is implied from first if statement
        driver.click_messages()
        return None
    
    # no need to return to messages at this point because we never left messages pane to begin with

    # post
    posted = post(caption = caption, media_filepaths = media_filepaths)
    del caption, media_filepaths
    
    if not posted: # if post was not successful
        failure_protocol(account)
        
    # send dm confirming post
    driver.click_messages() # return to Messages pane
    driver.scroll_to_end(element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), direction = +1, scalar = 0.5)
    driver.scroll_to_end(element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), direction = -1, scalar = 0.1)
    try:
        return_account = driver.driver.find_element("xpath", f"//span[text()='{account_name}']")
        driver.scroll(a = 0, b = return_account.location["y"], element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), scalar = 0.5)
        return_account.click()
        del return_account
        driver.wait(0.5, 1)
        driver.send_message(text = "Your information has been successfully posted. Please reach out if there are any issues.")
    except:
        pass
    
    # write to file
    accounts_success_writable.write(account + "\n")
    accounts_success.add(account)
    
    driver.wait(1, 2)

# protocol for if info fails to be posted for some reason
def failure_protocol(account, account_name):
    # go to dms in case I'm not already there
    try:
        driver.click_messages()
        driver.scroll_to_end(element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), direction = +1, scalar = 0.5)
        driver.scroll_to_end(element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), direction = -1, scalar = 0.1)
        return_account = driver.driver.find_element("xpath", f"//span[text()='{account_name}']")
        driver.scroll(a = 0, b = return_account.location["y"], element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), scalar = 0.5)
        return_account.click()
        del return_account
        driver.wait(0.5, 1)
            
        # send error message
        driver.send_message(text = "Unfortunately, there was an error in the posting process. I have notified the account administrator, who will deal with the issue personally as soon as possible.")
    except:
        pass
    accounts_concern_writable.write(account + "\n")
    accounts_concern.add(account)
    
    driver.wait(1, 2)


# GET A LIST OF UNREAD MESSAGES
driver.scroll_to_end(element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), direction = +1, scalar = 0.5) # scroll down in the messages pane
unread_messages = list(element.find_element("xpath", "./../../../..") for element in driver.driver.find_elements("xpath", "//span[@class='x3nfvp2 x1emribx x1tu34mt x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi xdk7pt x1xc55vz x972fbf xcfux6l x1qhh985 xm0m39n x14yjl9h xudhj91 x18nykt9 xww2gxu']"))

# RESPOND TO EACH UNREAD MESSAGE
# A DM will pop up in the normal messages tab if I follow the account
# The instagram account controlled by the bot should only follow people previously vetted by @ucsandiego.2027
# This means there is no requirement for the people to show their acceptance letter
while len(unread_messages) > 0:
    
    driver.wait(1, 2)
    
    # CLICK ON MESSAGE
    unread_message = unread_messages[0]
    driver.scroll_to_end(element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), direction = -1, scalar = 0.1) # scroll to top of messages pane
    driver.scroll(a = 0, b = unread_message.location["y"], element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), scalar = 0.5)
    unread_message.click()
    driver.wait(1, 2)
    
    # GET ACCOUNT NAME
    account_name = unread_message.find_element("xpath", "./div/div/div/span/span").text
    account = unread_message.find_element("xpath", "//a[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz xjp7ctv xeq5yr9']").get_attribute("href")
    account = account.split("/")[-1]
    
    if account in accounts_success: # if I have already succesfully posted this account, skip and let me deal with it manually
        accounts_concern.add(account) # add to accounts concern so I can see what else they have to say
        continue
    
    # TRY TO POST
    try:
        try_to_post(account = account, account_name = account_name, checking_for_acceptance_letter = False) # no need to vet these users, because @ucsandiego.2027 has already done so
    except: # if it didn't work for some reason
        failure_protocol(account = account, account_name = account_name)
    
    # REMOVE LOCAL TEMPORARY FILES
    clear_dir(temporary_output)
    
    # UPDATE UNREAD MESSAGES
    unread_messages = list(element.find_element("xpath", "./../../../..") for element in driver.driver.find_elements("xpath", "//span[@class='x3nfvp2 x1emribx x1tu34mt x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi xdk7pt x1xc55vz x972fbf xcfux6l x1qhh985 xm0m39n x14yjl9h xudhj91 x18nykt9 xww2gxu']"))

print("Finished responding to unread messages.")


# RESPOND TO EACH MESSAGE REQUEST (IF THERE ARE ANY)
# CLICK ON REQUESTS BUTTON
requests_xpath = "//span[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj']"
driver.driver.find_element("xpath", requests_xpath).click()
driver.wait(1, 2)

# GET A LIST OF REQUESTS
requested_chats_xpath = "//div[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x168nmei x13lgxp2 x5pf9jr xo71vjh x1lliihq xdj266r x11i5rnm xat24cr x1mh8g0r xg6hnt2 x18wri0h x1l895ks xbbxn1n xxbr6pl x1y1aw1k xwib8y2']"
requests = driver.driver.find_elements("xpath", requested_chats_xpath)
requests = requests[:len(requests) - 1] # remove hidden requests

# ADDRESS EACH REQUEST
while len(requests) > 0:
        
    request = requests[0]
    driver.wait(1, 2)
    
    # CLICK ON MESSAGE
    request.click()
    driver.wait(1, 2)
    
    # GET ACCOUNT NAME
    account_header = driver.driver.find_element("xpath", "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xsyo7zv x16hj40l x10b6aqq x1yrsyyn']")
    account_name = account_header.text
    account = account_header.find_element("xpath", "./a").get_attribute("href")
    account = account.split("/")[-1]
    del account_header
        
    # CLICK ON ACCEPT
    driver.driver.find_element("xpath", "//div[text()='Accept']").click()
        
    try:
        try_to_post(account = account, account_name = account_name, checking_for_acceptance_letter = True) # vet these users because they were not vetted by @ucsandiego.2027
    except:
        failure_protocol(account = account, account_name = account_name)
        
    # CLICK ON REQUESTS BUTTON IF IT IS THERE
    driver.scroll_to_end(element = driver.driver.find_element("xpath", messages_window_scrollable_xpath), direction = -1, scalar = 0.5) # scroll up in the messages pane
    driver.wait(0.5, 1)
    driver.driver.find_element("xpath", requests_xpath).click()
    driver.wait(1, 2)
    requests = driver.driver.find_elements("xpath", requested_chats_xpath) # update requests
    requests = requests[:len(requests) - 1] # remove hidden requests

    # REMOVE LOCAL TEMPORARY FILES
    clear_dir(temporary_output)

print("Finished responding to requests.")


# OUTPUT VARIOUS FILES
rmdir(temporary_output)

# CLOSE OUTPUTS
accounts_success_writable.close()
accounts_concern_writable.close()

driver.driver.quit()