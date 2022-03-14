#! /usr/bin/env python3

# Created: 3/11/22
# Author : Brett Warren
# Project: s22-Gold
# File   : votes_to_db.py

"""
Description:
This file inputs results of votes from the house and senate into a database.
Vote data is at ./congress/data/117/votes/**/*.xml
Database table name is: VOTES
To execute this file at the command line, run: ./votes_to_db.py
"""

import glob
import xml.etree.ElementTree as ET
import mysql.connector


def main():
    # fill in applicable connection information
    conn = mysql.connector.connect(user='',
                                   password='',
                                   host='localhost',
                                   database='')

    if conn:
        print("Connected Successfully")
    else:
        print("Connection Not Established")

    # iterate over every vote data file
    for name in glob.glob('./congress/data/117/votes/**/*.xml', recursive=True):
        print(name)  # current xml file being inserted
        tree = ET.parse(name)

        root = tree.getroot()

        '''Variable names for value data in xml file
        Be careful with these names, if you choose variable names that are 
        keywords in mysql you will get errors in the INPUT statements.
        Format: python_variable_name = root.get('xml_identifier')
        Example where = root.get('where')
        This will throw an error in mysql because 'where' is a keyword.
        You can either choose a different name or use escape characters'''
        body = root.get('where')
        sess = root.get('session')
        yr = root.get('year')
        roll = root.get('roll')
        datetime = root.get('datetime')
        updated = root.get('updated')
        category = root.find('category').text

        # continue parsing xml file if the vote is on passage of a bill or
        # an amendment
        if category == 'passage' or category == 'amendment':
            # more variables
            type_vote = root.find('type').text
            result = root.find('result').text
            bill_type = root.find('bill').get('type')
            number = root.find('bill').get('number')

            # every variable before this point will be the same for each voter
            # (i.e.: all the general information about the vote)
            # the following variables will be specific to the voter
            for voter in root.iter('voter'):
                voter_id = voter.get('id')
                value = voter.get('value')
                state = voter.get('state')

                # this was part of my attempt to INSERT all vote data,
                # it eventually failed because of variable names

                # data = """INSERT INTO VOTES (where, session, year, roll,
                # datetime, updated, category, type, result, billType, billNumber,
                # voter_id, voterValue, voterState) VALUES (%s, %s, %s, %s, %s, %s,
                # %s, %s, %s, %s, %s, %s, %s, %s)"""

                # this works because I changed the variable names
                data = """INSERT INTO VOTES (body, sess, yr, roll, voter_id) VALUES (%s, %s, %s, %s, %s)"""

                cursor = conn.cursor()

                # this was part of my attempt to INSERT all vote data,
                # it eventually failed because of variable names

                # cursor.execute(data, (where, session, year, roll, datetime,
                #                       updated, category, type_vote, result,
                #                       bill_type, number, voter_id, value, state))

                # this works because I changed the variable names
                cursor.execute(data, (body, sess, yr, roll, voter_id))

                conn.commit()
                # print("Data Inserted Successfully")  # prints to terminal every time a vote is inserted


if __name__ == '__main__':
    main()
