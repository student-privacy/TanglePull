from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import json
import re
import logging
from collections import OrderedDict
import requests
import time


############ Functions

def json_to_obj(filename):
    """
    Extracts data from JSOn file and saves it into a Python object that can be called and passed into the scraper
    """
    obj = None
    with open(filename) as json_file:
        obj = json.loads(json_file.read())
    return obj

def make_login(session, base_url, credentials):
    """
    Returns a Session object logged in with the credentials passed from the json file
    """
    login_form_url = '/login/device-based/login/async/?refsrc=deprecated&lwv=100'

    params = {'email':credentials['email'], 'pass':credentials['pass']}

    while True:
        time.sleep(3)
        logged_request = session.post(base_url+login_form_url, data=params)

        if logged_request.ok:
            logging.info('[*] Logged in.')
            break

def posts_completed(scraped_posts, limit):
    """
    Returns true if the amount of posts scraped from profile has reached its limit
    """
    if len(scraped_posts) == limit:
        return True
    else:
        return False

def crawl_profile(session, base_url, profile_url, post_limit):
    """
    Goes to post's Url, crawls and extracts text and images
    """
    profile_bs = get_bs(session, profile_url)
    n_scraped_posts = 0
    scraped_posts = list()
    posts_id = None
    
    while n_scraped_posts < post_limit:
        try:
            posts_id = 'recent'
            posts = profile_bs.find('div', id=posts_id).div.div.contents
        except Exception:
            posts_id = 'structured_composer_async_container'
            posts = profile_bs.find('div', id=posts_id).div.div.contents
        
        posts_urls = [a['href'] for a in profile_bs.find_all('a', text='Full Story')]

        for posts_url in posts_urls:
            print('Next url')
            try:
                post_data = scrape_post(session, base_url, posts_url)
                scraped_posts.append(post_data)
            except Exception as e:
                logging.info('Error: {}'.format(e))
            n_scraped_posts += 1
            if posts_completed(scraped_posts, post_limit):
                break

    return scraped_posts

def get_bs(session, url, lang='lxml'):
    """
    Makes a GET requests using the given Session object and returns a BeautifulSoup object.
    """
    r = None
    while True:
        r = session.get(url)
        time.sleep(3)
        if r.ok:
            break
    return BeautifulSoup(r.text, lang)


def scrape_post(session, base_url, post_url):
    """
    Goes to post URL and extracts post data
    """
    post_data = OrderedDict()

    post_bs = get_bs(session, base_url+post_url)
    time.sleep(5)

    # Here we populate the OrderedDict object with post_url bs data
    post_data['url'] = post_url

    try:
        post_text_element = post_bs.find('script', type='application/ld+json')
        post_data['text'] = json.loads(post_text_element.text)['articleBody']
    except Exception:
        post_data['text'] = []

    try:
        image_script = post_bs.find('script', type=re.compile(r'.+\+json')) 
        post_data['media_url'] = json.loads(image_script.text)['image']['contentUrl']

    except Exception:
        post_data['media_url'] = list() 
        media = re.findall(r'"contentUrl":".{100,500}=[A-Z0-9]{8}"', str(post_bs.prettify()))
        for link in media:
            new_link = link.split(':', 1)[1].replace('"', "")
            post_data['media_url'].append(re.sub('\\\\', '', new_link))

    return dict(post_data)

def save_data(data):
    """
    Converts data to JSON
    """
    with open('profile_posts_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    base_url = 'https://www.facebook.com'
    session = requests.session()

    # Grab credentials and all other profiles URL to scrape
    credentials = json_to_obj('credentials.json')
    posts_urls = json_to_obj('posts_urls.json')

    make_login(session, base_url, credentials)

    posts_data = None
    for post_url in posts_urls:
        post_data = crawl_profile(session, base_url, post_url, 4)
    logging.info('[!] Scraping finished. Total {}'.format(len(post_data)))
    logging.info('[!] Saving.')
    save_data(post_data)
