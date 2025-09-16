# import mysql.connector
#
# Start by creating a connection to the database.
#
# Use the username and password from your MySQL database:
#
# demo_mysql_connection.py:

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootroot"
)

print(mydb)