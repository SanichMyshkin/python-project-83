import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def get_id(url_name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT id FROM urls WHERE name = '{url_name}'")
        records = cursor.fetchone()
        return str(*records) if records else None


url = 'https://www.hexlet.io'

print(get_id(url))