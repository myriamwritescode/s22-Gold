#! /usr/bin/env python3

# Created: 3/11/22
# Author : Brett Warren
# Project: s22-Gold
# File   : votes_to_db.py

"""
Description:

"""

import glob
import xml.etree.ElementTree as ET
import mysql.connector


def main():
    conn = mysql.connector.connect(user='',
                                   password='',
                                   host='localhost',
                                   database='')

    if conn:
        print("Connected Successfully")
    else:
        print("Connection Not Established")

    for name in glob.glob('./congress/data/117/votes/**/*.xml', recursive=True):
        print(name)
        tree = ET.parse(name)

        root = tree.getroot()

        where = root.get('where')
        session = root.get('session')
        year = root.get('year')
        roll = root.get('roll')
        datetime = root.get('datetime')
        updated = root.get('updated')
        category = root.find('category').text

        if category == 'passage' or category == 'amendment':  # band aide
            type_vote = root.find('type').text
            result = root.find('result').text
            bill_type = root.find('bill').get('type')
            number = root.find('bill').get('number')

            for voter in root.iter('voter'):
                id = voter.get('id')
                value = voter.get('value')
                state = voter.get('state')

                data = """INSERT INTO VOTES (where, session, year, roll, 
                datetime, updated, category, type, result, billType, billNumber, 
                voterID, voterValue, voterState) VALUES(%s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s)"""

                cursor = conn.cursor()
                cursor.execute(data, (where, session, year, roll, datetime,
                                      updated, category, type_vote, result,
                                      bill_type, number, id, value, state))
                conn.commit()
                print("Data Inserted Successfully")


if __name__ == '__main__':
    main()
