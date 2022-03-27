#! /usr/bin/env python3

# Created: 3/11/22
# Author : Brett Warren
# Project: s22-Gold
# File   : votes_to_db.py

"""
Description:
This file merges vote data from every 'roll' into a csv
(legislators/all_votes.csv).
Vote data is at ./congress/data/*/votes/**/*.xml
all_votes.csv is used to import data to Django Model
To execute this file at the command line, run: ./merge_votes_to_csv.py
"""

import glob
import xml.etree.ElementTree as ET
import csv


def main():
    #  all_votes.csv header
    header = ['voter_id', 'state', 'bill_type', 'number', 'roll', 'value',
              'result', 'chamber', 'sess', 'yr', 'category', 'type_vote']

    with open('../legislators/all_votes.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(header)

        # parse data of every .xml votes data file
        for name in glob.glob('./congress/data/117/votes/**/*.xml', recursive=True):
            print(name)  # current xml file being inserted
            tree = ET.parse(name)

            root = tree.getroot()

            #  Variable names for value data in xml file
            chamber = root.get('where')
            sess = root.get('session')
            yr = root.get('year')
            roll = root.get('roll')
            # datetime = root.get('datetime')
            # updated = root.get('updated')
            category = root.find('category').text

            # continue parsing xml file if the vote is on passage of a bill or
            # an amendment
            if category == 'passage' or category == 'amendment':
                # more variables
                type_vote = root.find('type').text
                result = root.find('result').text
                if result == 'Agreed to' or result == 'Passed':

                    bill_type = root.find('bill').get('type')
                    if bill_type == 'hr' or bill_type == 's':

                        number = root.find('bill').get('number')

                        # every variable before this point will be the same for each voter
                        # (i.e.: all the general information about the vote)
                        # the following variables will be specific to the voter
                        for voter in root.iter('voter'):
                            voter_id = voter.get('id')
                            value = voter.get('value')
                            state = voter.get('state')

                            #  Organize for row-entry to all_votes.csv
                            data = [voter_id, state, bill_type, number, roll, value, result,
                                    chamber, sess, yr, category, type_vote]
                            #  write to all_votes.csv
                            writer.writerow(data)


if __name__ == '__main__':
    main()
