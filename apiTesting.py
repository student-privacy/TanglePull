# Load in proper packages
import argparse
from pytangle.api import API
import pandas as pd

# Pull out the argeparse values
def pull_args():
    parser = argparse.ArgumentParser(description='Pull out JSON file for Districts within CrowdTangle using the pytangle API')
    parser.add_argument('--token', help='Include your particular token supplied by crowdtangle.', required=True, type=str)
    return parser.parse_args()

args = pull_args()

# Add the token
api = API(token=args.token)

# grabbed the id for Districts by checking before hand
# Put it into a list
list_id = [1451562,]

# Loop through posts within District
for n, a_post in enumerate(api.posts(listIds=list_id, count=4, sortBy='overperforming', timeframe='2 HOUR')):
    print(n, a_post, sep='\n')

