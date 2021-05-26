import re
import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def get_tweet_data(card):
    """Extract data from tweet card"""
    username = card.find_element_by_xpath('.//span').text
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NoSuchElementException:
        return
    
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    
    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    
    # get a string of all emojis contained in the tweet
    """Emojis are stored as images... so I convert the filename, which is stored as unicode, into 
    the emoji character."""
    emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    emoji_list = []
    for tag in emoji_tags:
        filename = tag.get_attribute('src')
        try:
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)
    
    tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt)
    return tweet
# application variables

def tweetbot(username1,password1,nooftweets,search1):
# create instance of web driver
    PATH = "chrome/chromedriver.exe"


    #specify the path to chromedriver.exe (download and save on your computer)
    driver = webdriver.Chrome(PATH)
    # navigate to login screen
    driver.get('https://www.twitter.com/login')
    driver.maximize_window()

    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))

    #enter username and password
    username.clear()
    #username.send_keys("TigerMa66454538")
    username.send_keys(username1)
    password.clear()
    #password.send_keys("12345tiger12345")
    password.send_keys(password1)

    buttonlogin = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button']")))
    buttonlogin.click()
    sleep(1)

    # find search input and search for term
    search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
    search_input.send_keys(search1)
    search_input.send_keys(Keys.RETURN)
    sleep(1)

    # navigate to historical 'latest' tab
    driver.find_element_by_link_text('Latest').click()
    sleep(2)

    nooftweets = int(int(nooftweets)/10)

    # get all tweets on the page
    data = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = 0
    nooftweets = int(nooftweets)
    while scrolling<nooftweets:
        #page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        sleep(0.5)
        page_cards = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweet"]')))
        for card in page_cards:
            tweet = get_tweet_data(card)
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                
            # check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(0.5)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            break
        scrolling = scrolling + 1

    # close the web driver
    driver.close()
    return data

    # with open('turkcell_tweets.csv', 'w', newline='', encoding='utf-8') as f:
    #     header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets']
    #     writer = csv.writer(f)
    #     writer.writerow(header)
    #     writer.writerows(data)




















