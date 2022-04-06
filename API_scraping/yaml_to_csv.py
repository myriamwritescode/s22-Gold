#! /usr/bin/env python3

# Created: 4/6/22
# Author : Brett Warren
# Project: s22-Gold
# File   : yaml_to_csv.py

"""
Description:

"""
import yaml
import csv


def main():
    """Current Committees"""
    with open('congress-legislators/committees-current.yaml') as committee:
        committee_dict = yaml.load(committee, Loader=yaml.FullLoader)

    id_list = []
    committee_list = []
    for dic in committee_dict:
        chamber = dic.get('type')
        name = dic.get('name')
        thomas_id = dic.get('thomas_id')
        committee_id = dic.get('house_committee_id')
        if committee_id is None:
            committee_id = dic.get('senate_committee_id')
        committee_list.append([chamber, name, thomas_id, committee_id])
        id_list.append(thomas_id)

    # for cur in committee_list:
    #     print(cur)

    # committees.csv header
    committee_header = ['chamber', 'name', 'thomas_id', 'committee_id']

    with open('committees.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(committee_header)

        for committee in committee_list:
            writer.writerow(committee)

    """Committee Membership Informations"""
    with open('congress-legislators/committee-membership-current.yaml') as membership:
        membership_dict = yaml.load(membership, Loader=yaml.FullLoader)

    membership_list = []
    for item_id in id_list:
        for x in membership_dict.get(item_id):
            name = x.get('name')
            rank = x.get('rank')
            bioguide_id = x.get('bioguide')
            membership_list.append([item_id, name, rank, bioguide_id])

    # membership.csv header
    membership_header = ['thomas_id', 'name', 'rank', 'bioguide_id']

    with open('membership.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(membership_header)

        for member in membership_list:
            writer.writerow(member)


if __name__ == '__main__':
    main()
