import psycopg2
from dotenv import load_dotenv
import psycopg2.extras
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


def get_all_db(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        response = cursor.fetchall()

        # connection.close()

        return response


def get_one_db(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        response = cursor.fetchone()

        # connection.close()

        return response


def insert_to_db(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)

        connection.commit()
        # connection.close()


def get_id(conn, url_name):
    query = f"SELECT * FROM urls WHERE name = '{url_name}'"
    response = get_one_db(conn, query)
    if response:
        return response[0]
    return None
