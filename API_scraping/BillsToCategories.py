#! /usr/bin/env python3

# Created: 3/11/22
# Author : Myriam Souaya
# Project: s22-Gold
# File   : BillsToCategories.py


import requests
from bs4 import BeautifulSoup
import re

# ------------------------------------------------------------------------------

# CONVERT HTML INTO BEAUTIFULSOUP OBJECT

base_site = "https://www.congress.gov/search?q=%7B%22congress%22%3A%22117%22%" \
            "2C%22bill-status%22%3A%22law%22%2C%22house-committee%22%3A%22" \
            "Budget%22%7D"

response = requests.get(base_site)                              # 'get' request
html = response.content                                         # document
soup = BeautifulSoup(html, "html.parser")                       # soup object

# ------------------------------------------------------------------------------

# EXTRACT BILL ID

bills = []
billID_list = []
billID_tags = soup.find_all('span', class_='result-heading')

for bill_tag in range(len(billID_tags)):
    if bill_tag % 2 == 0:
        billID_list.append(billID_tags[bill_tag].contents[0].string)

# for bill in range(len(billID_list)):
#     print(billID_list[bill])


#print(billID_tags[bill_tag].contents[0].string)

# ------------------------------------------------------------------------------

# EXTRACT COMMITTEE

committee_list = []
committee_tags = soup.find_all('span', class_='result-item')

for committee_tag in committee_tags:
    if committee_tag.contents[2].string is not None:
        if committee_tag.contents[2].string.strip() != '':
            committee_list.append(committee_tag.contents[2].string.strip())

# for k in range(len(committee_list)):
#     print(committee_list[k])


#print(committee_tag.sourceline, committee_tag.contents[2].string.strip())


# ------------------------------------------------------------------------------

# EXTRACT ROLL, HOUSE AND SENATE

# tag_list = []
# tags = soup.find_all('div', class_='sol-step-info')
#
# for i in range(len(tags)):
#     print(tags[i].contents)
#     matchstr_h = re.search(r'no\.\s\d+\)\.', tags[i].contents[0])     # House
#     matchstr_s = re.search(r'Number:\s\d+\.', tags[i].contents[0])    # Senate
#     matchvoice = re.search(r'voice\svote', tags[i].contents[0])       # Voice
#     if matchstr_h:
#         if len(matchstr_h.group(0)) == 9:     # 9 char in regex = 3 digit roll
#             snippet = matchstr_h.group(0)
#             print(tags[i].sourceline, "House Roll: " + snippet[4:7])
#         elif len(matchstr_h.group(0)) == 8:   # 8 char in regex = 2 digit roll
#             snippet = matchstr_h.group(0)
#             print(tags[i].sourceline, "House Roll: " + snippet[4:6])
#     if matchstr_s:
#         if len(matchstr_s.group(0)) == 12:
#             snippet = matchstr_s.group(0)
#             print(tags[i].sourceline, "Senate Vote Number: " + snippet[8:11])
#         if len(matchstr_s.group(0)) == 11:
#             snippet = matchstr_s.group(0)
#             print(tags[i].sourceline, "Senate Vote Number: " + snippet[8:10])
#     if matchvoice:
#         print(tags[i].sourceline, "Voice Vote")


# ------------------------------------------------------------------------------

# EXTRACT SPONSORS

sponsors_list = []
sponsor_list = []
sponsor_tags = soup.find_all('a', target="_blank")

for i in range(len(sponsor_tags)):
    sponsor = re.search(r'Rep\.\s[a-zA-Z]+,.+\[', str(sponsor_tags[i].contents[0]))
    if sponsor:
        snippet = sponsor.group(0)
        sponsor_list.append(snippet[5:len(snippet) - 2])

for j in range(len(sponsor_list)):
    if j % 2 == 0:
        sponsors_list.append(sponsor_list[j])

# for l in range(len(sponsors_list)):
#     print(sponsors_list[l])



#-------------------------------------------------------------------------------

# FORMAT OUTPUT BY BILL: BILLID, COMMITTEE, SPONSORS

rows, cols = (13, 3)
arr = [[0]*cols]*rows


for row in range(len(arr)):
    arr[row][0] = billID_list[row]
    arr[row][1] = committee_list[row]
    arr[row][2] = sponsors_list[row]
    print(arr[row])



