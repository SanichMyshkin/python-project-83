import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_to_db():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        connection.autocommit = True
    except Exception as _ex:
        print('Error while working with PSQL', _ex)
    return connection


def get_all(request):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute(request)
        response = cursor.fetchall()
        return response


def insert_to_db(request):
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor:
            cursor.execute(request)
            conn.commit()
    except Exception as _ex:
        print('Error while working with PSQL', _ex)


def get_id(url_name):
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT id FROM urls WHERE name = '{url_name}'")
            records = cursor.fetchone()
            return str(*records) if records else None
