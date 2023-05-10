# README
# Phillip Long
# May 9, 2023

# This script contains a class that logs into Instagram, given a username and password, and acts as the actual web driver for future operations.


# IMPORTS
from selenium import webdriver
from time import sleep
from random import uniform

# CREATE THE CLASS
class instagram_driver:
    
    # INITIALIZE (CREATE WEB DRIVER WINDOW)
    def __init__(self, driver_address, username, password):
        
        # check if driver_address is valid
        try:
            self.driver = webdriver.Chrome(executable_path = driver_address)
            self.driver.maximize_window() # maximize the driver window
            # if we make it this far (that is, if driver_address is valid), the driver window has been created
                        
        except: # invalid driver_address, quit program
            print(f"Error: faulty driver_address argument.")
            quit()

        # username and password
        self.username = username
        self.password = password
        
        # call login function (see below)
        self.wait(0.5, 1.5)
        self.login()
        
        # add some wait time
        self.wait(4, 5)
        print("Successful login.")
    
        
    # LOGIN TO INSTAGRAM
    def login(self):
        
        # go to Instagram
        self.driver.get("https://www.instagram.com")
        self.wait(4, 5)
        
        # enter username
        self.simulate_typing(element = self.driver.find_element_by_xpath("//input[@aria-label='Phone number, username, or email']"),
                             text = self.username)
        self.wait(0.5, 3)
        
        # enter password
        self.simulate_typing(element = self.driver.find_element_by_xpath("//input[@aria-label='Password']"),
                             text = self.password)
        self.wait(0.5, 3)
        
        # click login button, get sent to new page
        login = self.driver.find_element_by_xpath("//button[@class='_acan _acap _acas _aj1-']")
        login.click()
        del login
        self.wait(2, 4)
        
        # deal with "Save Your Login Info?" popup, choose "Not Now"
        save_login_popup = self.driver.find_element_by_xpath("//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp x173jzuc x1yc6y37']")
        save_login_popup.click()
        del save_login_popup
        self.wait(2, 4)
        
        # deal with "Turn on Notifications" popup, choose "Not Now"
        notifications_popup = self.driver.find_element_by_xpath("//button[@class='_a9-- _a9_1']")
        notifications_popup.click()
        del notifications_popup
        self.wait(5, 6)
        
        # do a quick scrolling jittery action to fool ReCAPTCHA
        yi = 0 # initial y
        for i in range(int(uniform(0, 5))) # (inclusive, exlusive), determine number of scrolling movements
            yd = int(uniform(0, 300)) # change in y
            yf = (yi + yd) if i % 2 == 0 else (yi - yd) # scroll up or down depending on iteration number
            yf = 0 if yf < 0 else yf # final y, set to 0 if negative because we can't scroll negative
            driver.execute_script(f"window.scrollTo(yi, yf)") # conduct scrolling action
        del yi, yd, yf
    
    # HELPER FUNCTIONS
    
    # a function to wait a random amount of time within range (lower, upper)
    def wait(self, lower, upper):
        sleep(uniform(lower, upper))
        
    # a function that types in a given text into a given text entry element like an actual human (one letter at a time)
    def simulate_typing(self, element, text):
        self.wait(1.25, 2.25) # add wait time for when bot clicks on a text box
        for letter in text:
            element.send_keys(letter)
            self.wait(0.1, 0.25)
        del letter
    
