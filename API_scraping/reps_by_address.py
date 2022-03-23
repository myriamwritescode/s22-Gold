#! /usr/bin/env python3

# Created: 2/12/22
# Author : Myriam Souaya
# Project: s22-Gold
# File   : reps_by_address.py


#                                 IMPORTANT!!!!
# Please be aware that this script can only be run a limited number of times per
# month for free. This is because it makes an http request to the Google Civic
# Cloud Information API.Please do not run this script until we are ready to begin
# testing it's functionality with the front end. In the meantime, if you
# would like to experiment with the functionality of the Google Civic
# Information API, please visit this URL:https://developers.google.com/civic-
# information/docs/v2/representatives/representativeInfoByAddress

# The results of running this script have been written to the file
# test_reps_by_address.json

import requests
import json



file = open("test_reps_by_address.json", "w", encoding="utf-8")

# This URL is generated by the google api. If you look closely, you can see
# the address in the search parameters of the URL.

url = "https://civicinfo.googleapis.com/civicinfo/v2/representatives?address=" \
      "5102%20BALLYCASTLE%20CIR&includeOffices=true&levels=country&roles=legis" \
      "latorUpperBody&key=AIzaSyA2yJqqdsAUV33ryKp50gq5Njs4UC6o3bc "

# The response is a get request for the URL. The Google API then returns
# the politicians associated with the address in the above URL.

response = requests.get(url).text

file.write(response)