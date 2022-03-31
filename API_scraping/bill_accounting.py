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
    brett_list_full = []
    brett_list_number = []

    # Read csv and fill lists
    with open('necessary_bills.csv', 'r') as brett_bills:
        csv_reader = reader(brett_bills)
        for row in csv_reader:
            brett_list_full.append(row)
            brett_list_number.append(row[1])

    # If you want to look at the lists
    # print(brett_list_full)
    # print(brett_list_number)

    # Check the list of just numbers for duplicates
    numbers = duplicate_numbers(brett_list_number)

    # If list of just numbers contains duplicates, print full bill titles
    for item in brett_list_full:
        if item[1] in numbers:
            print(item)
    print(f'Search Complete')


if __name__ == '__main__':
    main()
