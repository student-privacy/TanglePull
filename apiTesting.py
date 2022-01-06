# Load in proper packages
import argparse
from pytangle.api import API
import pandas as pd
import re
# import request
from datetime import datetime
from urllib.request import urlopen
import time
import numpy as np
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Pull out the argeparse values
def pull_args():
    parser = argparse.ArgumentParser(description='Pull out JSON file for Districts within CrowdTangle using the pytangle API')
    parser.add_argument('--token', help='Include your particular token supplied by crowdtangle.', required=True, type=str)
    return parser.parse_args()

args = pull_args()

# Load in our Facebook login credentials
with open("FacebookCredentials.txt") as file:
        EMAIL = file.readline().split('"')[1]
        PASSWORD = file.readline().split('"')[1]

def _extract_post_text(item):
    actualPosts = item.find_all(attrs={'data-ad-comet-preview':"message"})
    print(actualPosts)
    text = ""
    print('Actual Posts Text:', actualPosts, sep='\n')
    if actualPosts:
        for posts in actualPosts:
            print(posts)
            paragraphs = posts.find_all(dir='auto', style='text-align: start;')
            print(paragraphs)
            text = ""
            for index in range(0, len(paragraphs)):
                text += paragraphs[index].text

    return text

def _extract_altimage(item):
    postPictures = item.find_all(id="jsc_s_8")
    image = ""
    print('Alt Image Extract:', postPictures, sep='\n')
    for postPicture in postPictures:
        alt = postPicture.get('alt')
    return alt 

def _extract_image(item):
    postPictures = item.find_all(id="jsc_s_8")
    image = ""
    print('Image Extract:', postPictures, sep='\n')
    for postPicture in postPictures:
        image = postPicture.get('src')
    return image

def _extract_html(bs_data):

    with open('./bs.html', 'w', encoding="utf-8") as file:
        file.write(str(bs_data.prettify()))

    postBigDict = list()
    postDict = dict()
    postDict['Post'] = list()
    postDict['Image'] = list()
    postDict['AltImage'] = list()

    for item in bs_data:
        postDict['Post'].append(_extract_post_text(item))
        postDict['Image'].append(_extract_image(item))
        postDict['AltImage'].append(_extract_altimage(item))

        postBigDict.append(postDict)
        
        print(postBigDict)

        with open('./postBigDict.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(postBigDict, ensure_ascii=False).encode('utf-8').decode())

    return postBigDict

# define login function for facebook
def _login(browser, email, password):
    """
    Will go to the facebook website and login to the website using the account that you have specified
    """
    browser.get("http://facebook.com")
    browser.maximize_window()
    browser.find_element_by_name("email").send_keys(email)
    browser.find_element_by_name("pass").send_keys(password)
    browser.find_element_by_name("login").click()
    time.sleep(5)

def _crowd(count):
    """Grab Urls for all of the posts within the CrowdTangle Posts that are specified by the ID and Count number
    """
    # Add the token
    api = API(token=args.token)

    # grabbed the id for Districts by checking before hand
    # Put it into a list
    list_id = [1451562,]
    
    # List containing post urls
    url_list = list()

    # Loop through posts within District
    for n, a_post in enumerate(api.posts(listIds=list_id, count=count, sortBy='overperforming', timeframe='2 HOUR')):
        if a_post['type'] == 'photo':
            post_url = a_post['postUrl']
            url_list.append(post_url) 

    return url_list

# Pull page into beautifulsoup
def extract(urlList, infinite_scroll=False, scrape_comment=False):
    """
    Pull out the particular page of interest from the crowdtangle info. Then pass that pages html into beautifulsoup for parsing
    """
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Chromedrive needs to be in the same folder at this file
    browser = webdriver.Chrome(executable_path="./chromedriver", options=option)
    _login(browser, EMAIL, PASSWORD)
    bs_list = list()
    for page in urlList:
        browser.get(page)
        source_data = browser.page_source
        
        # Throw source code into BeautifulSoup and parse
        bs_data = BeautifulSoup(source_data, 'html.parser')
        
        postBigDict = _extract_html(bs_data)
        bs_list.append(postBigDict)

    browser.close()

    return bs_list
new = _crowd(3)
print(extract(new), new)
