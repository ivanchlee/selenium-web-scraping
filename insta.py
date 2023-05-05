from selenium import webdriver
from time import sleep
# from secrets import username, pw
import logging
from datetime import datetime
  
start = datetime.now()
dt_start_string = start.strftime("%Y%m%d_%H%M%S")  
date_string = start.strftime("%Y%m%d")

#Create and configure logger 
logging.basicConfig(filename="insta" + date_string + ".log", 
                    format='%(asctime)s %(message)s', 
                    filemode='a') 
  
#Creating an object 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 
username = 'username'
pw = 'password'

class InstaBot:
    
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(3)
        logger.info("---------------------------------------------------------------------------------------------------------")
        logger.info("in loop")
        user = self.driver.find_element_by_xpath("//input[@name=\"username\"]")
        user.send_keys(username)
        
        password = self.driver.find_element_by_xpath("//input[@name=\"password\"]")
        password.send_keys(pw)
            
        submit = self.driver.find_element_by_xpath('//button[@type="submit"]')
        submit.click()
        sleep(5)

        b_not_now1 = self.driver.find_element_by_xpath('//button[text()="Not Now"]')
        b_not_now1.click()
        sleep(5)
        
        #b_not_now2 = self.driver.find_element_by_xpath('//button[text()="Not Now"]')
        #b_not_now2.click()
        #sleep(5)
        
        #explore = self.driver.find_element_by_xpath('//a[@href="/explore/"]')
        #explore.click()
        #sleep(5)
        
        #follow_nike = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div/div/div/div/div/div[3]/div[3]/button')
        #follow_nike.click()
        
        follow_first = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[3]/div[2]/div[2]/div/div/div/div[1]/div[3]/button')
        follow_first.click() 
 
        sleep(20)


InstaBot(username, pw)