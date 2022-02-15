# First connect to MySQL and create Database
import mysql.connector as mysql
from mysql.connector import Error

try:
    conn = mysql.connect(host='localhost', user='root',
                         password=' ')  # give ur mysql password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE testDB")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)
