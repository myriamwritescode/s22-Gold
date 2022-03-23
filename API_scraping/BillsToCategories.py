# Created: 3/11/22
# Author : Myriam Souaya
# Project: s22-Gold
# File   : BillsToCategories.py


import requests
from bs4 import BeautifulSoup
import re


#------------------------------------------------------------------------------

# CONVERT HTML INTO BEAUTIFULSOUP OBJECT

base_site = "https://www.congress.gov/search?q=%7B%22source%22%3A%22" \
            "legislation%22%2C%22congress%22%3A%22117%22%2C%22bill-" \
            "status%22%3A%22law%22%2C%22house-committee%22%3A%22Budget%22%7D"

response = requests.get(base_site)                          # get request
html = response.content                                     # document
soup = BeautifulSoup(html, "html.parser")                   # soup object


#------------------------------------------------------------------------------

# EXTRACT H.R.

span_tags_keys = soup.find_all('span', class_='result-heading')
#for key_tag in range(len(span_tags_keys)):
#    if key_tag % 2 == 0:
        #print(span_tags_keys[key_tag].contents[0].string)


#------------------------------------------------------------------------------

# EXTRACT COMMITTEE

span_tags_values = soup.find_all('span', class_='result-item')

#for value_tag in span_tags_values:
#    if value_tag.contents[2].string is not None:
#        if value_tag.contents[2].string.strip() != '':
            #print(value_tag.contents[2].string.strip())


#------------------------------------------------------------------------------

# EXTRACT ROLL, HOUSE AND SENATE

tag_list = []
tags = soup.find_all('div', class_='sol-step-info')

for i in range(len(tags)):
    matchstr = re.search(r'no\.\s\d+\)\.', tags[i].contents[0])
    matchvoice = re.search(r'voice\svote', tags[i].contents[0])
    if matchstr:
        if len(matchstr.group(0)) == 9:
            print("3 digits")
        if len(matchstr.group(0)) == 8:
            print("2 digits")
    if matchvoice:
        print("Voice Vote")


#tag = str(tags[1].contents[0])
#matchstr = re.search(r'no\.\s\d+\)\.', tag).group(0)

#print(type(tag))

#if len(matchstr) == 9:
#    print(matchstr[4:7])
#if len(matchstr) == 8:
#   print(matchstr[4:6])
