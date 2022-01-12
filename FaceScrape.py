from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib.request
import json
import re
import logging
import collections
import requests

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    base_url = 'https://mobile.facebook.com'
    session = requests.session()

    # Grab credentials and all other profiles URL to scrape
    credentials = json_to_obj('credentials.json')
