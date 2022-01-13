# TanglePull

This repo is in conjunction with the Behavior, Research, & Teaching (BRT) school at the University of Oregon. 

TanglePull is a package to scrape Facebook Profiles. It will iterate through the specified amount of posts within profiles and then return relevant information to you in a JSON file.

## Required

Two files are needed to be able to use this package. Make sure to include both of these files in the same directory as this repo on your local computer. 

1. `credentials.json`

 You must supply it with a file that passes your credentials to FaceBook so that you can access FaceBook like as if you are logged in normally. You can pass your normal account email and password to this file. 

```
{
	"email":"bar",
	"pass":"foo"
}
```

2. `posts_urls.json`

This will be a file that contains the URLs to school district's FaceBook Profile. This will be used to iterate through and pull all the desired posts from.

```
[
 "www.facebook.com/Profile1",
 "www.facebook.com/Profile2"
]
```

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

## Example Output

The script will scrape three things of interest from the posts:
1. Post URL
2. Post's Text
3. Post's Image/s

Then write it to a JSON file named `profile_posts_data.json`. The output looks like this:

```
[
    {
        "url": "/story.php?story_fbid=10161047792297069&id=378286107068&refid=17&_ft_=mf_story_key.10161047792297069%3Atop_level_post_id.10161047792297069%3Atl_objid.10161047792297069%3Acontent_owner_id_new.378286107068%3Athrowback_story_fbid.10161047792297069%3Apage_id.378286107068%3Astory_location.4%3Astory_attachment_style.photo%3Aott.AX-M_5NlD_8yHYRF%3Atds_flgs.3%3Athid.378286107068%3A306061129499414%3A2%3A0%3A1643702399%3A-1323917819246680865%3A%3A%3Apage_insights.%7B%22378286107068%22%3A%7B%22page_id%22%3A378286107068%2C%22page_id_type%22%3A%22page%22%2C%22actor_id%22%3A378286107068%2C%22dm%22%3A%7B%22isShare%22%3A0%2C%22originalPostOwnerID%22%3A0%7D%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22post_context%22%3A%7B%22object_fbtype%22%3A266%2C%22publish_time%22%3A1641852003%2C%22story_name%22%3A%22EntStatusCreationStory%22%2C%22story_fbid%22%3A%5B10161047792297069%5D%7D%2C%22role%22%3A1%2C%22sl%22%3A4%2C%22targets%22%3A%5B%7B%22actor_id%22%3A378286107068%2C%22page_id%22%3A378286107068%2C%22post_id%22%3A10161047792297069%2C%22role%22%3A1%2C%22share_id%22%3A0%7D%5D%7D%7D&__tn__=%2AW-R#footer_action_list",
        "text": "We're hiring! Milford Exempted Village Schools is currently seeking a full-time custodian. All interested applicants should visit MilfordSchools.org/Employment.",
        "media_url": "https://scontent.fhio2-1.fna.fbcdn.net/v/t39.30808-6/271658631_10161047322962069_4518899084223467302_n.png?_nc_cat=103&ccb=1-5&_nc_sid=730e14&_nc_ohc=klDjZREGi5UAX-28HbA&_nc_ht=scontent.fhio2-1.fna&oh=00_AT9lmI6r5uRPdpy08B5LhiuxKZlbSbfCVq8dKAjrEzepeg&oe=61E571D3"
    },
]
```

