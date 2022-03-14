# Created: 3/11/22
# Author : Myriam Souaya
# Project: s22-Gold
# File   : BillsToCategories.py


import requests
from bs4 import BeautifulSoup


#------------------------------------------------------------------------------

# CONVERT HTML INTO BEAUTIFULSOUP OBJECT

base_site = "https://www.congress.gov/search?q=%7B%22source%22%3A%22" \
            "legislation%22%2C%22congress%22%3A%22117%22%2C%22bill-" \
            "status%22%3A%22law%22%2C%22house-committee%22%3A%22Budget%22%7D"

response = requests.get(base_site)                          # get request
html = response.content                                     # document
soup = BeautifulSoup(html, "html.parser")                   # soup object


#------------------------------------------------------------------------------

# EXTRACT KEYS

span_tags_keys = soup.find_all('span', class_='result-heading')
for key_tag in range(len(span_tags_keys)):
    if key_tag % 2 == 0:
        print(span_tags_keys[key_tag].contents[0].string)


#------------------------------------------------------------------------------

# EXTRACT VALUES

span_tags_values = soup.find_all('span', class_='result-item')

for value_tag in span_tags_values:
    if value_tag.contents[2].string is not None:
        if value_tag.contents[2].string.strip() != '':
            print(value_tag.sourceline, value_tag.contents[
                2].string.strip())


#------------------------------------------------------------------------------

# CREATE DICTIONARY

# TBD
