"""
import mysql.connector
alliifmaaldb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='allif@1442',
)
#prepare a cursor object
allifcursorobj=alliifmaaldb.cursor()
allifcursorobj.execute("CREATE DATABASE allifdb")
print("db created")

"""