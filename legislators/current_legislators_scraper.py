#! /usr/bin/env python3

# Created: 2/10/22
# Author : Brett Warren
# Project: s22-Gold
# File   : current_legislators_scraper.py

"""
Description:
Download/Update for current legislators...
Biographical information
Official social media accounts
List of committees
Committee membership
from  https://github.com/unitedstates/congress-legislators

3 file formats will be downloaded/updated. csv, yaml, json
To execute, run
./current_legislators_scraper.py
"""

import requests

def main():
    # open files
    current_csv = open("current_legislators.csv", "w")
    current_yaml = open("current_legislators.yaml", "w")
    current_json = open("current_legislators.json", "w")

    files = [current_csv, current_yaml, current_json]

    # associated urls
    csv_url = "https://theunitedstates.io/congress-legislators/legislators-current.csv"
    yaml_url = "https://theunitedstates.io/congress-legislators/legislators-current.yaml"
    json_url = "https://theunitedstates.io/congress-legislators/legislators-current.json"

    urls = [csv_url, yaml_url, json_url]

    # write to files
    for (file, url) in zip(files, urls):
        file.write(requests.get(url).text)


if __name__ == '__main__':
    main()
