#! /usr/bin/env python3

# Created: 3/11/22
# Author : Myriam Souaya
# Project: s22-Gold
# File   : BillsToCategories.py


import requests
from bs4 import BeautifulSoup
import re
import csv




def bills_to_categories(url):

    # CONVERT HTML INTO BEAUTIFULSOUP OBJECT

    response = requests.get(url)                # GET request
    html = response.content                     # document
    soup = BeautifulSoup(html, "html.parser")   # soup object

    # ------------------------------------------------------------------------------

    # EXTRACT BILL ID

    bill_id_list = []
    bill_id_tags = soup.find_all('span', class_='result-heading')

    for bill_tag in range(len(bill_id_tags)):
        if bill_tag % 2 == 0:
            bill_id_list.append(bill_id_tags[bill_tag].contents[0].string)


    # ------------------------------------------------------------------------------

    # EXTRACT COMMITTEE

    committee_list = []
    committee_tags = soup.find_all('span', class_='result-item')

    for committee_tag in committee_tags:
        if committee_tag.contents[2].string is not None:
            if committee_tag.contents[2].string.strip() != '':
                committee_list.append(committee_tag.contents[2].string.strip())

    for element in committee_list:
        if element == 'The House Rules Committee Print':
            committee_list.remove(element)


    # ------------------------------------------------------------------------------

    # EXTRACT SPONSORS

    sponsors_list = []
    sponsor_list = []
    sponsor_tags = soup.find_all('a', target="_blank")

    # parsing rep and sen names from a longer string

    for i in range(len(sponsor_tags)):
        sponsor_rep = re.search(r'Rep\.\s[a-zA-Z\s]+,.+\[',
                                str(sponsor_tags[i].contents[0]))
        sponsor_sen = re.search(r'Sen\.\s[a-zA-Z\s]+,.+\[',
                                str(sponsor_tags[i].contents[0]))
        if sponsor_rep:
            snippet_rep = sponsor_rep.group(0)
            sponsor_list.append(snippet_rep[5:len(snippet_rep) - 2])
        if sponsor_sen:
            snippet_sen = sponsor_sen.group(0)
            sponsor_list.append(snippet_sen[5:len(snippet_sen) - 2])

    for j in range(len(sponsor_list)):
        if j % 2 == 0:
            sponsors_list.append(sponsor_list[j])


    # -------------------------------------------------------------------------------

    # FORMAT OUTPUT BY BILL: BILLID, COMMITTEE, SPONSORS
    # CREATES A LIST OF TUPLES

    new_list = list(zip(bill_id_list, committee_list, sponsors_list))

    return new_list












    # rows, cols = (len(bill_id_list), 3)
    # arr = [[0] * cols] * rows
    #
    # for row in range(len(bill_id_list)):
    #     arr[row][0] = bill_id_list[row]
    #     arr[row][1] = committee_list[row]
    #     arr[row][2] = sponsors_list[row]
















def main():
    print('didn\'t work')


if __name__ == '__main__':
    main()






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