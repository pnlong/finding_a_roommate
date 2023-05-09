# README
# Phillip Long
# May 6, 2023

# I was recently admitted to UC San Diego, and on Instagram, there is this account called @ucsandiego.2027
# A lot of incoming freshmen post to this account, both to make friends and find potential roommates
# However, the page is chaotic to say the least...there are thousands of people posting about themselves
# and since I can't dorm with most of the people posting, I want a page just for Muir College Class of 2027
# This will make things a lot more manageable and easier to find a roommate.

# ACCOUNT INFO
email = "p1long@ucsd.edu"
fullname = "John Muir"
username = "muircollege2027"
password = "UEcYN9e7i85nmKpquAaB"
birthday = "September 19, 1967"

# IMPORTS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import numpy

# create instance of chrome driver
driver = webdriver.Chrome(executable_path = "/Users/philliplong/Desktop/Coding/chromedriver")

class bot:
 
    def __init__(self, username, password, audience, message):
       
        # initializing the username
        self.username = username
         
        # initializing the password
        self.password = password
         
        # passing the list of user or initializing
        self.user = user
         
        # passing the message of user or initializing
        self.message = message
         
        # initializing the base url.
        self.base_url = 'https://www.instagram.com/'
         
        # here it calls the driver to open chrome web browser.
        self.bot = driver
         
        # initializing the login function we will create
        self.login()
        
    
    def login(self):
 
        self.bot.get(self.base_url)
         
        # ENTERING THE USERNAME FOR LOGIN INTO INSTAGRAM
        enter_username = WebDriverWait(self.bot, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, 'username')))
     
        enter_username.send_keys(self.username)
         
        # ENTERING THE PASSWORD FOR LOGIN INTO INSTAGRAM
        enter_password = WebDriverWait(self.bot, 20).until(
            expected_conditions.presence_of_element_located((By.NAME, 'password')))
        enter_password.send_keys(self.password)
     
        # RETURNING THE PASSWORD and login into the account
        enter_password.send_keys(Keys.RETURN)
        time.sleep(5)
    
        # first pop-up box
        self.bot.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(3)
         
        # 2nd pop-up box
        self.bot.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        
        time.sleep(4)
        
        # this will click on message(direct) option.
        self.bot.find_element_by_xpath(
            '//a[@class="xWeGp"]/*[name()="svg"][@aria-label="Direct"]').click()
         
        time.sleep(3)

        # This will click on the pencil icon as shown in the figure.
        self.bot.find_element_by_xpath(
            '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div/button').click()
        time.sleep(2)
        
        
        for i in user:
         
            # enter the username
            self.bot.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/input').send_keys(i)
            time.sleep(2)
         
            # click on the username
            self.bot.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[2]/div[2]/div').click()
            time.sleep(2)
         
            # next button
            self.bot.find_element_by_xpath(
                '/html/body/div[4]/div/div/div[1]/div/div[2]/div/button').click()
            time.sleep(2)
         
            # click on message area
            send = self.bot.find_element_by_xpath(
                '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
         
            # types message
            send.send_keys(self.message)
            time.sleep(1)
         
            # send message
            send.send_keys(Keys.RETURN)
            time.sleep(2)
         
            # clicks on pencil icon
            self.bot.find_element_by_xpath(
                '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button').click()
            time.sleep(2)
            # here will take the next username from the user's list.


def init():
    # you can take any valid username
    audience = [ 'sundarpichai','virat.kholi','rudymancuso']
    message = "testing of a bot"
    
    # you can even enter your personal account.
    bot('username', 'password', user, message_)
    input("DONE")


init()
