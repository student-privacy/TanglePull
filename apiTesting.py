# Load in proper packages
import argparse
from pytangle.api import API
import pandas as pd
import re
import request
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


# define login function for facebook
def _login(browser, email, password):
    """
    Will go to the facebook website and login to the website using the account that you have specified
    """
    browser.get("http://facebook.com")
    browser.maximize_window()
    browser.find_element_by_name("email").send_keys(email)
    browser.find_element_by_name("pass").send_keys(password)
    browser.find_element_by_id("loginbutton").click()
    time.sleep(5)

# Pull page into beautifulsoup
def extract(page, infinite_scroll=False, scrape_comment=False):
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
    browser.get(page)
    source_data = browser.page_source
    
    # Throw source code into BeautifulSoup and parse
    bs_data = BeautifulSoup(source_data, 'html.parser')

    browser.close()

    return bs_data 

# Add the token
api = API(token=args.token)

# grabbed the id for Districts by checking before hand
# Put it into a list
list_id = [1451562,]

# Loop through posts within District
for n, a_post in enumerate(api.posts(listIds=list_id, count=1, sortBy='overperforming', timeframe='2 HOUR')):
    if a_post['type'] == 'photo':
        post_url = a_post['postUrl']
        print(extract(post_url))
