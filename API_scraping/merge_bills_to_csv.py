#! /usr/bin/env python3

# Created: 3/30/22
# Author : Myriam Souaya
# Project: s22-Gold
# File   : merge_bills_to_csv.py


import csv

rows = [['H.R.5545', "House - Veterans' Affairs; Budget", 'Trone, David J.'],
        ['H.R.5293', "House - Veterans' Affairs; Budget", 'Mrvan, Frank J.'],
        ['H.R.4172', "House - Veterans' Affairs", 'Crow, Jason']]


def main():
    bills = []

    # bills.csv header
    fields = ['bill ID', 'committee(s)', 'sponsor']

    with open('bills.csv', 'w', encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(fields)

        writer.writerows(rows)







if __name__ == '__main__':
    main()
