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


def get_all_db(query, *args):
    connection = psycopg2.connect(DATABASE_URL)

    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) \
            as cursor:
        cursor.execute(query, args)
        response = cursor.fetchall()

        connection.close()

        return response


def insert_to_db(query, *args):
    connection = psycopg2.connect(DATABASE_URL)

    with connection.cursor() as cursor:
        cursor.execute(query, (args))

        connection.commit()
        connection.close()


def get_id(url_name):
    query = f"SELECT * FROM urls WHERE name = '{url_name}'"

    response = get_all_db(query, url_name)
    if response:
        return response['id']
    return None


def get_one_db(query, *args):
    connection = psycopg2.connect(DATABASE_URL)

    with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) \
            as cursor:
        cursor.execute(query, args)
        response = cursor.fetchone()

        connection.close()

        return response
