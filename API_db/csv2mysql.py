#! /usr/bin/env python3

from typing import Any
import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd

# Read the csv into dataFrame and examine its shape
dataset = pd.read_csv('current_legislators.csv',
                      index_col=False, delimiter=',')
dataset.shape

# Explore null cells and view total by columns
dataset.isnull()
dataset.isnull().sum()
# To view the number of null values in a specific column:
# dataset['column name'].isnull().sum()

# Fill all null values w/ something and score it into current data frame
dataset.fillna('0', inplace=True)

# Store the dataframe into a new CSV
dataset.to_csv('legislators_db.csv', index=False)

# Note - must already have a database created (i.e. 'APIdb')
# create a table and import CSV data into MySQL table:
try:
    connect2db = mysql.connect(host='localhost', database='APIdb',
                               user='root', password='')  # provide mysql pass
    if connect2db.is_connected():
        cursor = connect2db.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Now connected to database: ", record)

        cursor.execute('DROP TABLE IF EXISTS APIdb_data;')
        print('Creating table....')

        # pass the create table statement which you want to create:
        cursor.execute("CREATE TABLE APIdb_data(last_name varchar(255),first_name varchar(255),middle_name varchar(255),suffix varchar(255),nickname varchar(255),full_name varchar(255),birthday varchar(255),gender varchar(255),type varchar(255),state varchar(255),district int,senate_class int,party varchar(255),url varchar(255),address varchar(255),phone varchar(255),contact_form varchar(255),rss_url varchar(255),twitter varchar(255),facebook varchar(255),youtube varchar(255),youtube_id varchar(255),bioguide_id varchar(255),thomas_id int,opensecrets_id varchar(255),lis_id varchar(255),fec_ids varchar(255),cspan_id int,govtrack_id int,votesmart_id int,ballotpedia_id varchar(255),washington_post_id varchar(255),icpsr_id int,wikipedia_id varchar(255))")
        print("Table has been created....")

        # loop through the data frame:
        for i, row in dataset.iterrows():
            # %s means string values
            sql = "INSERT INTO APIdb.APIdb_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # commit to save the changes
            connect2db.commit()

except Error as e:
    print("Error while connecting to MySQL!", e)
