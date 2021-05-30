from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from collections import OrderedDict

import os
import wget

import time
from selenium.webdriver.chrome.options import Options


#bot is taking user's insta username, password and hashtag or username to be searched
def bot(username1,password1,instaname1):
    PATH = "chrome/chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("http://www.instagram.com")

    #Searching for username input field
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    #Searching for password input field
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    #enter username and password
    username.clear()
    username.send_keys(username1)
    password.clear()
    password.send_keys(password1)

    #target the login button and click it
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    #logged in!

    not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()


    #target the search input field
    searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()

    #search for the hashtag or username
    keyword = instaname1
    searchbox.send_keys(keyword)
    
    # Wait for 2 seconds
    time.sleep(2)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)

    # driver.execute_script("window.scrollTo(0, 4000);")
    #scroll down to scrape more images
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    images = list()
    while(match==False):
            lastCount = lenOfPage
            time.sleep(2)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            time.sleep(1)
            imagesdriver = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME,'img')))
            #imagesdriver = driver.find_elements_by_tag_name('img')
            images2 = [image.get_attribute('src') for image in imagesdriver]
            for o in images2[:-2]:
                images.append(o)
            if lastCount==lenOfPage:
                match=True
    #target all images on the page
    # images = driver.find_elements_by_tag_name('img')
    # images = [image.get_attribute('src') for image in images]
    # images = images[:-2]
    res = list(OrderedDict.fromkeys(images))
    print(len(res))
    return res

    #here the bot returns a list of image urls