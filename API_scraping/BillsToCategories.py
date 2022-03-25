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

span_tags_hr = soup.find_all('span', class_='result-heading')
#for key_tag in range(len(span_tags_hr)):
#    if key_tag % 2 == 0:
        #print(span_tags_hr[key_tag].contents[0].string)


#------------------------------------------------------------------------------

# EXTRACT COMMITTEE

span_tags_committee = soup.find_all('span', class_='result-item')

#for value_tag in span_tags_committee:
#    if value_tag.contents[2].string is not None:
#        if value_tag.contents[2].string.strip() != '':
            #print(value_tag.contents[2].string.strip())


#------------------------------------------------------------------------------

# EXTRACT ROLL, HOUSE AND SENATE

tag_list = []
tags = soup.find_all('div', class_='sol-step-info')

for i in range(len(tags)):
    matchstr_h = re.search(r'no\.\s\d+\)\.', tags[i].contents[0])     # House
    matchstr_s = re.search(r'Number:\s\d+\.', tags[i].contents[0])    # Senate
    matchvoice = re.search(r'voice\svote', tags[i].contents[0])       # Voice
    if matchstr_h:
        if len(matchstr_h.group(0)) == 9:     # 9 char in regex = 3 digit roll
            snippet = matchstr_h.group(0)
            print("House Roll: " + snippet[4:7])
        elif len(matchstr_h.group(0)) == 8:   # 8 char in regex = 2 digit roll
            snippet = matchstr_h.group(0)
            print("House Roll: " + snippet[4:6])
    if matchstr_s:
        if len(matchstr_s.group(0)) == 12:
            snippet = matchstr_s.group(0)
            print("Senate Vote Number: " + snippet[8:11])
        if len(matchstr_s.group(0)) == 11:
            snippet = matchstr_s.group(0)
            print("Senate Vote Number: " + snippet[8:10])
    if matchvoice:
        print("Voice Vote")


#------------------------------------------------------------------------------

# EXTRACT SPONSORS

tags = soup.find_all('a', target="_blank")

for i in range(len(tags)):
    matchvoice = re.search(r'Rep\.\s[a-zA-Z]+,.+\[', str(tags[i].contents[0]))
    if matchvoice:
        snippet = matchvoice.group(0)
        print(snippet[5:len(snippet)-2])
