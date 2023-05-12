# README
# Phillip Long
# May 9, 2023

# This script contains a class that logs into Instagram, given a username and password, and acts as the actual web driver for future operations.


# IMPORTS
from selenium import webdriver
from time import sleep
from random import uniform

# VARIABLES
m = 12 # pixels moved per scroll movement

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
        self.wait(3, 4)
    
        
    # LOGIN TO INSTAGRAM
    def login(self):
        
        # go to Instagram
        self.driver.get("https://www.instagram.com")
        self.wait(4, 5)
        
        # enter username
        self.simulate_typing(element = self.driver.find_element("xpath", "//input[@aria-label='Phone number, username, or email']"),
                             text = self.username)
        self.wait(0.5, 2.5)
        
        # enter password
        self.simulate_typing(element = self.driver.find_element("xpath", "//input[@aria-label='Password']"),
                             text = self.password)
        self.wait(0.5, 2.5)
        
        # click login button, get sent to new page
        login = self.driver.find_element("xpath", "//button[@class='_acan _acap _acas _aj1-']")
        login.click()
        del login
        self.wait(5, 7)
        
        # deal with "Save Your Login Info?" popup if present, choose "Save Info" button
        try:
            save_login_popup = self.driver.find_element("xpath", "//button[@class='_acan _acap _acas _aj1-']")
            save_login_popup.click()
            del save_login_popup
            self.wait(3, 5)
        except:
            pass
        
        # deal with "Turn on Notifications" popup if present, choose "Not Now" button
        try:
            notifications_popup = self.driver.find_element("xpath", "//button[@class='_a9-- _a9_1']")
            notifications_popup.click()
            del notifications_popup
            self.wait(3, 4)
        except:
            pass
        
        # do a quick scrolling jittery action to fool ReCAPTCHA
        yi, yd, yf = 0, 0, 0 # initial y, change in y, final y
        for i in range(int(uniform(0, 3))): # (inclusive, exlusive), determine number of scrolling movements
            yd = int(uniform(m + 1, 50)) # change in y
            yf = (yi + yd) if i % 2 == 0 else (yi - yd) # scroll up or down depending on iteration number
            yf = 0 if yf < 0 else yf # final y, set to 0 if negative because we can't scroll negative
            self.scroll(a = yi, b = yf) # conduct scrolling action
            self.wait(0.4, 0.5)
        del yi, yd, yf
    
    
    # HELPER FUNCTIONS
    
    # a function to wait a random amount of time within range (lower, upper)
    def wait(self, lower, upper):
        sleep(uniform(lower, upper))
        
    # a function that types in a given text into a given text entry element like an actual human (one letter at a time)
    def simulate_typing(self, element, text, scalar = 1.0): # scalar is the speed of which it takes to type (scalar = 2 is double the time)
        first_iter = True
        
        for letter in text:
            
            if first_iter:
                self.wait(1.25, 2.25) # add wait time for when bot clicks on a text box
                first_iter = False
            
            element.send_keys(letter)
            self.wait(scalar * 0.1, scalar * 0.25) # scalar affects time between each character is entered
            
        del letter, first_iter
        
    # a function that scrolls from point a to point b in a "natural" way
    def scroll(self, a, b):
        n = (b - a) // m # number of iterations
        d = n / abs(n) if n != 0 else 0.0 # direction of scroll
        for i in range(abs(n)):
            self.driver.execute_script(f"window.scrollTo({a}, {a + (d * m)})") # conduct scrolling action
            a += d * m # recalculate a
            self.wait(0.04, 0.11)
        
        self.driver.execute_script(f"window.scrollTo({a}, {a + ((b - a) % m)})") # scroll the last little bit
        
        del a, b, d, n
