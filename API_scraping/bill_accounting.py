#! /usr/bin/env python3

# Created: 3/30/22
# Author : Brett Warren
# Project: s22-Gold
# File   : bill_accounting.py

"""
Description:
Checks for duplicates in bill identifiers.
Compare bills collected by Brett and Myriam for equality. (Not yet implemented)
"""

from csv import reader
from operator import itemgetter


def duplicate_numbers(list_of_bills):
    duplicate_list = []
    set_of_bills = set()
    for bill in list_of_bills:
        if bill in set_of_bills:
            duplicate_list.append(bill)
        else:
            set_of_bills.add(bill)
    return duplicate_list


# def check_for_same_number(list_of_bills):
#     just_numbers = []
#     for i in range(len(list_of_bills)):
#         just_numbers.append(list_of_bills[i][1])
#     set_of_numbers = set()
#     for j in range(len(just_numbers)):
#         if just_numbers[j] in set_of_numbers:
#             print(list_of_bills[i])


def main():
    # Create a list of full bill titles and just numbers
    all_votes_set = set()
    bills_set = set()
    necessary_bills_set = set()

    # Create a list of lists containing bill information with 1 committee
    # myriam_list_full = []
    # Create a list (1) of lists (2), where the committees in (2) are also in a list (3)
    # In other words, a list where no bill occurs twice, and all the committees for a bill are grouped.
    # myriam_list_compressed = []

    # Read csv and fill lists
    with open('all_votes.csv', 'r') as votes:
        csv_reader1 = reader(votes)
        # skip header
        next(csv_reader1)
        for row in csv_reader1:
            all_votes_set.add(row[3])

    all_votes_set = sorted(all_votes_set)

    with open('bills.csv', 'r') as bills:
        csv_reader2 = reader(bills)
        # skip header
        next(csv_reader2)
        for row in csv_reader2:
            bills_set.add(row[0])

    bills_set = sorted(bills_set)

    with open('necessary_bills.csv', 'r') as nec:
        csv_reader3 = reader(nec)
        for row in csv_reader3:
            necessary_bills_set.add(row[1])

    necessary_bills_set = sorted(necessary_bills_set)

    # If you want to look at the lists
    print(len(all_votes_set))
    print(len(bills_set))
    print(len(necessary_bills_set))

    # sort by bill id
    # brett_list_full = sorted(brett_list_full, key=itemgetter(1))
    # for i in brett_list_full:
    #     print(i)

    # myriam_list_full = sorted(myriam_list_full, key=itemgetter(0))
    # for j in myriam_list_full:
    #     print(j)

    # print(myriam_list_full)
    # print(myriam_list_compressed[-1][0])

    # compress Myriam's list
    # for k in range(len(myriam_list_full)):
    #     try:
    #         last_bill = myriam_list_compressed[-1][0]
    #     except IndexError:
    #         myriam_list_compressed.append([myriam_list_full[k][0], myriam_list_full[k][1],
    #                                        [myriam_list_full[k][2]], myriam_list_full[k][3]])
    #         last_bill = myriam_list_compressed[-1][0]
    #         continue
    #     if myriam_list_full[k][0] == last_bill:
    #         myriam_list_compressed[-1][2].append(myriam_list_full[k][2])
    #     else:
    #         myriam_list_compressed.append([myriam_list_full[k][0], myriam_list_full[k][1],
    #                                        [myriam_list_full[k][2]], myriam_list_full[k][3]])
    # for item in myriam_list_full:
    #     bill = item[0]
    #     chamber = item[1]
    #     committee = item[2]
    #     sponsor = item[3]
    #     if len(myriam_list_compressed) == 0:
    #         if chamber == 'House':
    #             myriam_list_compressed.append({'bill': bill, 'House': [committee], 'Senate': [], 'sponsor': sponsor})
    #         else:
    #
    #     elif bill == myriam_list_compressed[-1].get('bill'):
    #         if chamber == myriam_list_compressed[-1].get()


    # for j in myriam_list_compressed:
    #     print(j)

    # Check the list of just numbers for duplicates
    # numbers = duplicate_numbers(brett_list_number)

    # If list of just numbers contains duplicates, print full bill titles
    # for item in brett_list_full:
    #     if item[1] in numbers:
    #         print(item)
    # print(f'Search Complete')


if __name__ == '__main__':
    main()
