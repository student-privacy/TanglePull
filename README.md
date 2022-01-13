# TanglePull

This repo is in conjunction with the Behavior, Research, & Teaching (BRT) school at the University of Oregon. 

TanglePull is a package to scrape Facebook Profiles. It will iterate through the specified amount of posts within profiles and then return relevant information to you in a JSON file.

## Required

Two files are needed to be able to use this package. Make sure to include both of these files in the same directory as this repo on your local computer. 

1. credentials.json

 You must supply it with a file that passes your credentials to FaceBook so that you can access FaceBook like as if you are logged in normally. You can pass your normal account email and password to this file. 


2. posts_urls.json

This will be a file that contains the URLs to school district's FaceBook Profile. This will be used to iterate through and pull all the desired posts from.


### Packages
- BeautifulSoup
- Requests
- time
- re
- logging
- json
- urllib.request

You can create a conda environment using the below command in your terminal:

```
conda create env -f env/tanglepull.yml
```

## How to Run

All you need to do is run the python script `FaceScrape.py` within the terminal. You can do that by running the command below.

```
python FaceScrape.py
```

