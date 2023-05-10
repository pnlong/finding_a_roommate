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
        self.wait(3, 5)

    
    # HELPER FUNCTIONS
    
    # a function to wait a random amount of time within range (lower, upper)
    def wait(self, lower, upper):
        sleep(uniform(lower, upper))
        
    # a function that types in a given text into a given text entry element like an actual human (one letter at a time)
    def simulate_typing(self, element, text):
        self.wait(0.75, 2) # add wait time for when bot clicks on a text box
        for letter in text:
            element.send_keys(letter)
            self.wait(0.05, 0.2)
        del letter
    
