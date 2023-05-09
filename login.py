# README
# Phillip Long
# May 9, 2023

# This script contains a class that logs into Instagram, given a username and password, and acts as the actual web driver for future operations.


# IMPORTS
from selenium import webdriver
from time import sleep
from random import uniform

# FUNCTIONS

# a function to wait a random amount of time within range (lower, upper)
def wait(lower, upper):
    sleep(uniform(lower, upper))

# a function that types in a given text into a given text entry element like an actual human (one letter at a time)
def simulate_typing(element, text):
    for letter in text:
        element.send_keys(letter)
        wait(0.05, 0.2)
    del letter


# CREATE THE CLASS
class instagram_window:
    
    # INITIALIZE (CREATE WEB DRIVER WINDOW)
    def __init__(self, driver_address, username, password):
        
        # check if driver_address is valid
        try:
            driver_test = webdriver.Chrome(executable_path = driver_address)
            driver_test.quit()
            del driver_test
            
            # if we make it this far (that is, if driver_address is valid), create driver window
            self.driver = webdriver.Chrome(executable_path = driver_address)
            self.driver.maximize_window() # maximize the driver window
            
        except: # invalid driver_address, quit program
            print(f"Error: faulty driver_address argument.")
            quit()
            

        # username and password
        self.username = username
        self.password = password
        
        
        # call login function (see below)
        self.login()
    
        
        
    # LOGIN TO INSTAGRAM
    def login:
        
        # go to Instagram
        self.driver.get("https://www.instagram.com")
        wait(3, 5)
        
        # enter username
        simulate_typing(element = self.driver.find_element_by_xpath("//input[@aria-label='Phone number, username, or email']"),
                        text = self.username)
        wait(0.5, 1.5)
        
        # enter password
        simulate_typing(element = self.driver.find_element_by_xpath("//input[@aria-label='Password']"),
                        text = self.password)
        wait(0.5, 1.5)
        
        # click login button, get sent to new page
        login = self.driver.find_element_by_xpath("//button[@class='_acan _acap _acas _aj1-']")
        login.click()
        del login
        wait(3, 5)


        # scroll to bottom to load in everything
        # driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", driver.find_element_by_xpath('//div[@class="a1cdxe01"]'))
        wait(0.5, 1.5)


        # enter username
        simulate_typing(driver.find_element_by_id("username"), "phillipl915")
        wait(0.5, 1.5)


        # enter password
        simulate_typing(driver.find_element_by_id("password"), "090105PNL")
        wait(0.5, 1.5)


        # click login button
        login = driver.find_element_by_xpath("//button[@type='submit']")
        login.click()
        del login
        wait(1, 3)







