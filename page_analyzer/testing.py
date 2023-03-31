import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
sql_query = 'SELECT * FROM urls'
cursor.execute(sql_query)
print(list(cursor))
