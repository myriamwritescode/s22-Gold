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
    necessary_bills = []

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
                type_vote = root.find('type').text
                if type_vote == 'On Passage of the Bill' or type_vote == 'On the Resolution':
                    result = root.find('result').text
                    if result == 'Agreed to' or result == 'Passed':
                        bill_type = root.find('bill').get('type')
                        number = root.find('bill').get('number')

                        #  sidebar... need a list of necessary bills for other programs
                        # uppercase = bill_type.upper()
                        # with_period = '.'.join(uppercase[i:i + 1] for i in range(0, len(uppercase), 1))
                        # if bill_type.startswith('h'):
                        #     letter = 'H.'
                        #     bill_id = f'{letter}{number}'
                        # if bill_type.startswith('s'):
                        #     letter = 'S.'
                        bill_id = [bill_type, number]
                        necessary_bills.append(bill_id)  # ...end sidebar

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

    with open('necessary_bills.csv', 'w', encoding="utf-8") as f2:
        writer2 = csv.writer(f2)
        for bill in necessary_bills:
            writer2.writerow(bill)


if __name__ == '__main__':
    main()
