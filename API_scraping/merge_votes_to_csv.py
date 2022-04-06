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
from re import compile, match, findall, split
from operator import itemgetter


def main():
    bill_set = set()

    # Read csv and fill lists
    with open('bills.csv', 'r') as myriam_bills:
        csv_reader1 = csv.reader(myriam_bills)
        # skip header
        next(csv_reader1)
        for row in csv_reader1:
            bill_id = row[0]
            bill_set.add(bill_id)

    bill_set = sorted(bill_set)

    bill_list = []
    for bill in bill_set:
        bill_split = split('(\d+)', bill)
        bill_split.remove(bill_split[2])
        bill_list.append(bill_split)

    bill_dict = {}
    for bill in bill_list:
        bill_dict.update({bill[1]: bill[0]})

    print(bill_dict)
    print(len(bill_list))
    print(len(bill_set))
    print(len(bill_dict))

    # all_votes.csv header
    header = ['voter_id', 'state', 'bill_type', 'number', 'roll', 'value',
              'result', 'chamber', 'sess', 'yr', 'category', 'type_vote']

    counter = 0
    counter2 = 0
    test_set = set()

    with open('all_votes.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(header)

        # parse data of every .xml votes data file
        # for name in glob.glob('./congress/data/117/votes/**/*.xml', recursive=True):
        for name in glob.glob('data/117/votes/**/*.xml', recursive=True):
            print(name)  # current xml file being inserted
            tree = ET.parse(name)

            root = tree.getroot()

            #  Variable names for value data in xml file
            try:
                number = root.find('bill').get('number')
                counter += 1
            except AttributeError:
                counter2 += 1
                continue
            if number in bill_dict:
                result = root.find('result').text
                if result == 'Agreed to' or result == 'Passed':
                    try:
                        bill_type = root.find('bill').get('type')
                    except AttributeError:
                        bill_type = 'Not_A_Bill'
                    # if bill_type == 'h' or bill_type == 's':
                    chamber = root.get('where')
                    sess = root.get('session')
                    yr = root.get('year')
                    roll = root.get('roll')
                    # datetime = root.get('datetime')
                    # updated = root.get('updated')
                    category = root.find('category').text
                    # continue parsing xml file if the vote is on passage of a bill or
                    # an amendment
                    # substring = 'passage'
                    # if substring in category:
                    type_vote = root.find('type').text
                    # if type_vote == 'On Passage of the Bill' or type_vote == 'On the Resolution':
                    # every variable before this point will be the same for each voter
                    # (i.e.: all the general information about the vote)
                    # the following variables will be specific to the voter
                    test_set.add(number)
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
        for bill in test_set:
            writer2.writerow(bill)

    print(counter)
    print(counter2)
    print(len(test_set))


if __name__ == '__main__':
    main()
