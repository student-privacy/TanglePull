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



