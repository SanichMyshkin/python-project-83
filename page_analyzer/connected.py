import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_to_db(request, *args):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cursor:
            cursor.execute(request, args)
            response = cursor.fetchall()
            return response

    except Exception as _ex:
        print('Error while working with PSQL', _ex)


def insert_to_db(request):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cursor:
            cursor.execute(request)
            conn.commit()
    except Exception as _ex:
        print('Error while working with PSQL', _ex)


def get_id(url_name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT id FROM urls WHERE name = '{url_name}'")
        records = cursor.fetchone()
        return str(*records) if records else None


def get_name(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT name FROM urls WHERE name = {id}")
        return cursor.fetchone()
