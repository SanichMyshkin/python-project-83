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
