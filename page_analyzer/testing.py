# import psycopg2
# import validators
from datetime import datetime

current_datetime = datetime.now()

print(current_datetime)
print(current_datetime.year)
print(current_datetime.month)
print(current_datetime.day)
print(current_datetime.hour)
print(current_datetime.minute)
print(current_datetime.second)
print(current_datetime.microsecond)

'''
conn = psycopg2.connect('postgresql://postgres:@localhost:5432/database')

cursor = conn.cursor()
cursor.execute("SELECT * FROM urls")
print(f'Server version:{cursor.fetchone()}')
'''
