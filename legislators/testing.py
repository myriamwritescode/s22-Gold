#! /usr/bin/env python3

# Created: 3/29/22
# Author : Brett Warren
# Project: s22-Gold
# File   : testing.py

"""
Description:

"""


def main():
    """MULTIPLE MODELS ALGORITHM IN VIEWS.PY"""
    # reps = ['rep1', 'rep2', 'rep3']
    # x = [1, 2, 3]
    # y = [4, 5, 6]
    # z = [7, 8, 9]
    #
    # rep_values = [x, y, z]
    #
    # data = {'rep_values': rep_values, 'other': [9, 5, 1]}
    #
    # print(type(data))

    """PARSING COMMITTEES"""
    # example_1 = "House - Veterans' Affairs; Budget"
    # example_2 = "House - Veterans' Affairs | Senate - Veterans' Affairs"
    # example_3 = "House - Transportation and Infrastructure; Ways and Means; Natural Resources; Science, Space, and Technology; Energy and Commerce; Oversight and Reform"
    #
    # test_lists = [example_1, example_2, example_3]
    #
    # # line = example_2.split(' - ')
    # # print(line[0])
    #
    # csv_output = []
    #
    # delimiter_1 = ' | '
    # delimiter_2 = ' - '
    # delimiter_3 = '; '
    #
    # for item in test_lists:
    #     if delimiter_1 in item:
    #         two_chambers = item.split(delimiter_1)
    #         for count, text in enumerate(two_chambers):
    #             chamber_and_committees = two_chambers[count].split(delimiter_2)
    #             chamber = chamber_and_committees[0]
    #             committee_listx = chamber_and_committees[1]
    #             if delimiter_3 in committee_listx:
    #                 committee_listx = committee_listx.split(delimiter_3)
    #                 for committee in committee_listx:
    #                     csv_output.append([chamber, committee])
    #             else:
    #                 csv_output.append([chamber, committee_listx])
    #     else:
    #         chamber_and_committees = item.split(delimiter_2)
    #         chamber = chamber_and_committees[0]
    #         committee_listx = chamber_and_committees[1]
    #         if delimiter_3 in committee_listx:
    #             committee_listx = committee_listx.split(delimiter_3)
    #         for committee in committee_listx:
    #             csv_output.append([chamber, committee])
    #
    # for line in csv_output:
    #     print(line)

    # if delimiter_1 in line[1]:
    #     partitioned = line[1].partition(delimiter_1)
    #     line[1] = partitioned[0]
    # if delimiter_2 in line[1]:
    #     partitioned = line[1].partition(delimiter_2)
    #     line[1] = partitioned[0]
    # print(line[1])
    # print(example_1.split(' - '))

    """Name Reordering"""
    # name1 = 'Hassan, Margaret Wood'
    # name2 = 'Margaret Wood Hassan'
    #
    # new1 = name1.split(', ')
    # new1 = f'{new1[1]} {new1[0]}'
    # print(new1)

    """Normalizing Scores"""
    a = 0
    b = 1
    c = 10
    d = 2
    e = 40
    f = 1
    g = 1
    h = 20
    i = 81
    j = 0

    total = a + b + c + d + e + f + g + h + i + j

    print(total)

    a = int(a / total)

    print(a)

if __name__ == '__main__':
    main()
