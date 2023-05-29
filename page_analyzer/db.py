import psycopg2
from psycopg2 import pool
from page_analyzer.settings import DB_HOST, DB_PORT, \
    DB_USER, DB_PASS, DB_NAME
from contextlib import contextmanager


def create_connection(*args, **kwargs):
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME)


def create_pool(min_conn=1, max_conn=5):
    return pool.SimpleConnectionPool(minconn=min_conn,
                                     maxconn=max_conn,
                                     connection_factory=create_connection,
                                     host=DB_HOST,
                                     port=DB_PORT,
                                     user=DB_USER,
                                     password=DB_PASS,
                                     database=DB_NAME)


@contextmanager
def get_connection():
    conn = None
    try:
        conn = conn_pool.getconn()
        yield conn
        conn.commit()
    except Exception as error:
        conn.rollback()
        raise Exception(f'Connection lost. Changes abort. {error}')
    finally:
        if conn:
            conn_pool.putconn(conn)


@contextmanager
def get_cursor():
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()


conn_pool = create_pool()
