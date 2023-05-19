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
s = 1.0 # default scalar

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
            print("Error: faulty driver_address argument.")
            quit()

        # username and password
        self.username = username
        self.password = password
        
    
    # MAIN FUNCTIONS
    
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
        self.driver.find_element("xpath", "//button[@class='_acan _acap _acas _aj1-']").click()
        self.wait(5, 7)
        
        # deal with "Save Your Login Info?" popup if present, choose "Save Info" button
        try:
            self.driver.find_element("xpath", "//button[text()='Save Info']").click()
            self.wait(3, 5)
        except:
            pass
        
        # deal with "Turn on Notifications" popup if present, choose "Not Now" button
        notifications_popup_has_appeared = False
        while not notifications_popup_has_appeared:
            try:
                self.driver.find_element("xpath", "//button[text()='Not Now']").click()
                notifications_popup_has_appeared = True
            except:
                self.wait(1, 1)
        del notifications_popup_has_appeared
        
        # do a quick scrolling jittery action to fool ReCAPTCHA
        yi, yd, yf = 0, 0, 0 # initial y, change in y, final y
        for i in range(int(uniform(0, 3))): # (inclusive, exlusive), determine number of scrolling movements
            yd = int(uniform(m + 1, 50)) # change in y
            yf = (yi + yd) if i % 2 == 0 else (yi - yd) # scroll up or down depending on iteration number
            yf = 0 if yf < 0 else yf # final y, set to 0 if negative because we can't scroll negative
            self.scroll(a = yi, b = yf) # conduct scrolling action
            self.wait(0.4, 0.5)
        del yi, yd, yf
        
        self.wait(3, 4)
    
    # click on the search button on side tab
    def click_search(self):
        self.driver.find_element("xpath", "//a[@href='#']/div/div/div/div/*[name()='svg'][@aria-label='Search']").click()
        self.wait(2, 3)
        
        try: # if seach has opened, not closed
            # check for search input
            self.driver.find_element("xpath", "//input[@aria-label='Search input']").clear()
        
            # clear search history
            if len(self.driver.find_elements("xpath", "//a[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz xh8yej3 x193iq5w x1lliihq x1dm5mii x16mil14 xiojian x1yutycm']")) > 3:
                self.driver.find_element("xpath", "//div[text()='Clear all']").click()
                self.wait(0.5, 1)
                self.driver.find_element("xpath", "//button[text()='Clear all']").click()
                self.wait(1, 2)
            
        except:
            pass
        
        self.wait(0.5, 1)
        
    # click on the messages button on side tab
    def click_messages(self):
        self.driver.find_element("xpath", "//a[@href='/direct/inbox/']").click()
        self.wait(2, 3)
    
    # send a message; MUST BE IN MESSAGES PANE FOR THIS FUNCTION TO WORK
    def send_message(self, text, scalar = s / 2):
        # type in message
        self.simulate_typing(element = self.driver.find_element("xpath", "//textarea[@placeholder='Message...']"),
                             text = text, scalar = scalar)
        self.wait(0.75, 1.5)
        # send message
        self.driver.find_element("xpath", "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp x173jzuc x1yc6y37'][@role='button']").click()
        self.wait(1.5, 2.5)
        
    
    # HELPER FUNCTIONS
    
    # a function to wait a random amount of time within range (lower, upper)
    def wait(self, lower, upper):
        sleep(uniform(lower, upper))
        
    # a function that types in a given text into a given text entry element like an actual human (one letter at a time)
    def simulate_typing(self, element, text, scalar = s): # scalar is the speed of which it takes to type (scalar = 2 is double the time)
        first_iter = True
        
        for letter in text:
            
            if first_iter:
                self.wait(1.25, 2.25) # add wait time for when bot clicks on a text box
                first_iter = False
            
            element.send_keys(letter)
            self.wait(scalar * 0.1, scalar * 0.25) # scalar affects time between each character is entered
            
        del letter, first_iter
        
    # a function that scrolls from point a to point b in a "natural" way
    def scroll(self, a, b, scalar = s, element = None):
        n = (b - a) // m # number of iterations
        d = n / abs(n) if n != 0 else 0.0 # direction of scroll
        for i in range(abs(n)):
            # conduct scrolling action
            if element is None:
                self.driver.execute_script(f"window.scrollTo({a}, {a + (d * m)})")
            else:
                self.driver.execute_script(f"arguments[0].scrollTo({a}, {a + (d * m)})", element)
            a += d * m # recalculate a
            self.wait(scalar * 0.04, scalar * 0.11)
        # scroll the last little bit
        if element is None:
            self.driver.execute_script(f"window.scrollTo({a}, {a + ((b - a) % m)})")
        else:
            self.driver.execute_script(f"arguments[0].scrollTo({a}, {a + ((b - a) % m)})", element)
        
        del a, b, d, n
