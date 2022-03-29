#! /usr/bin/env python3

# Created: 3/27/22
# Author : Myriam Souaya
# Project: s22-Gold
# File   : scraping_urls.py

from BillsToCategories import billsToCategories

url_arguments = ['house-committee%22%3A%22Veterans%27+Affairs',
                 'house-committee%22%3A%22Energy+and+Commerce',
                 'house-committee%22%3A%22Oversight+and+Reform',
                 'house-committee%22%3A%22Judiciary',
                 'house-committee%22%3A%22Natural+Resources',
                 'house-committee%22%3A%22Transportation+and+Infrastructure',
                 'house-committee%22%3A%22Ways+and+Means',
                 'house-committee%22%3A%22Appropriations',
                 'house-committee%22%3A%22Financial+Services',
                 'house-committee%22%3A%22Foreign+Affairs',
                 'house-committee%22%3A%22Science%2C+Space%2C+and+Technology',
                 'house-committee%22%3A%22Armed+Services',
                 'house-committee%22%3A%22Small+Business',
                 'senate-committee%22%3A%22Veterans%27+Affairs',
                 'senate-committee%22%3A%22Homeland+Security+and+Governmental'
                 '+Affairs',
                 'senate-committee%22%3A%22Health%2C+Education%2C+Labor%2C'
                 '+and+Pensions',
                 'senate-committee%22%3A%22Judiciary',
                 'senate-committee%22%3A%22Banking%2C+Housing%2C+and+Urban'
                 '+Affairs',
                 'senate-committee%22%3A%22Energy+and+Natural+Resources',
                 'senate-committee%22%3A%22Environment+and+Public+Works',
                 'senate-committee%22%3A%22Foreign+Relations',
                 'senate-committee%22%3A%22Agriculture%2C+Nutrition%2C+and+Forestry'
                 ]


def main():

    base_url = "https://www.congress.gov/search?pageSize=250&q=%7B%22congress" \
               "%22%" \
               "3A%22117%22%2C%22bill-status%22%3A%22law%22%2C%22"

    url_closing = "%22%7D"

    for url in url_arguments:
        #url_to_scrape = base_url + url_arguments[i] + url_closing
        url_to_scrape = f'{base_url}url[i]{url_closing}'
        #print(url_to_scrape)
        billsToCategories(url_to_scrape)




if __name__ == '__main__':
    main()












