#! /usr/bin/env python3

# First connect to MySQL and create Database
import mysql.connector as mysql
from mysql.connector import Error

try:
    conn = mysql.connect(host='localhost', user='root',
                         password='')  # give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE APIdb")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)
