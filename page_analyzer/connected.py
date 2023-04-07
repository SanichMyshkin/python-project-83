import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_to_db(request, *args):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        # print('Sql connected')

        with conn.cursor() as cursor:
            cursor.execute(request, args)
            response = cursor.fetchall()
            return response

    except Exception as _ex:
        print('Error while working with PSQL', _ex)
    finally:
        if conn:
            conn.close()
            # print("Connection Database closed")


def insert_to_db(request):
    try:
        conn = psycopg2.connect(DATABASE_URL)

        # print("Sql connected")

        with conn.cursor() as cursor:
            cursor.execute(request)

    except Exception as _ex:
        print('Error while working with PSQL', _ex)

    finally:
        if conn:
            conn.commit()
            conn.close()
            # print("Connection close")
