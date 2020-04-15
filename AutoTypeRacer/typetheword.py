from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import random
import string

class TypeRacerBot():
    def __init__(self):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)

    def loadPage(self,url):
        #load the page
        self.browser.get(url)
        print("loading page")

        #skip accept terms
        element = WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="qcCmpButtons"]/button[2]')))
        element.click()
        print("skipped accept terms")
        
    def play_practice(self,url):
        self.loadPage(url)
        #press practice
        element = WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a')))
        time.sleep(1)
        element.click()
        print("selected practice")

        #wait for the timer and get the text
        path = '//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div'
        element = WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, path)))
        contect = element.get_attribute('innerHTML')
        print("waited for the text to be readable")

        #we must wait for the light
        path = '/html/body/div[6]/div/div/div'
        element = WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, path)))
        print("waited for the signs to pop up")


        print("running the virtual keyboard")
        #run the virtual keyboard
        self._virtualKeyboard(contect)
        

    def play_online(self, url):
        self.loadPage(url)

        #wait for the join to be clickable
        path = '//*[@id="gwt-uid-17"]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/a'
        element = WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, path)))
        element.click()

        #wait for the text
        path = '//*[@id="gwt-uid-17"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div'
        element = WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, path)))
        contect = element.get_attribute('innerHTML')

        #wait for the players to join , or just for the hint banner to appear
        path = '/html/body/div[7]/div/div/div'
        element = WebDriverWait(self.browser, 200).until(
        EC.presence_of_element_located((By.XPATH, path)))

        #run the virtual keyboard
        self._virtualKeyboard(contect)

    def play_practice_unlimited(self,url):
        # it needs work
        self.loadPage(url)
        #press practice
        element = WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a')))
        time.sleep(1)
        element.click()
        print("selected practice")

        #wait for the timer and get the text
        path = '//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div'
        element = WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, path)))
        contect = element.get_attribute('innerHTML')
        print("waited for the text to be readable")
        
        while True:
            
            #we must wait for the light
            path = '/html/body/div[6]/div/div/div'
            element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, path)))
            print("waited for the signs to pop up")


            print("running the virtual keyboard")
            #run the virtual keyboard
            self._virtualKeyboard(contect)

            # print("trying again")
            # path = '//*[@id="gwt-uid-15"]/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/a'
            # element = WebDriverWait(self.browser, 10).until(
            # EC.presence_of_element_located((By.XPATH, path)))
            # contect = element.click()



    def _virtualKeyboard(self,contect):
        #remove the tags and any character between them
        contect = re.sub('<[^>]+>', '', contect)    
        delay= 0.01
        for i in range(0,len(contect)-1):
            time.sleep(delay)
            actions = ActionChains(self.browser)
            actions.send_keys(contect[i])
            actions.perform()

        wpm = int(self.browser.find_element_by_class_name("rankPanelWpm").get_attribute('innerHTML').split('wpm')[0])
        while wpm >95:
            # from the browser find the first element which as the class 'rank etc' get the innerHtml and transform the text to get the number
            wpm = int(self.browser.find_element_by_class_name("rankPanelWpm").get_attribute('innerHTML').split('wpm')[0])
        actions = ActionChains(self.browser)
        actions.send_keys(contect[len(contect)-1])
        actions.perform()



    
    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()



typeRacerBot = TypeRacerBot()
typeRacerBot.play_practice('https://play.typeracer.com')
#typeRacerBot.play_practice_unlimited('https://play.typeracer.com')
#typeRacerBot.play_online('https://play.typeracer.com?rt=29avdgkppd')

