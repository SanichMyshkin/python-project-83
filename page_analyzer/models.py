from page_analyzer.db import get_connection
from datetime import datetime
from page_analyzer.checks_request import get_status


def get_all_url(conn):
    query = '''SELECT urls.id, urls.name,
        url_checks.created_at, url_checks.status_code
    FROM urls LEFT JOIN (
        SELECT DISTINCT ON (url_id) url_id, created_at, status_code
    FROM url_checks ORDER BY url_id, created_at DESC)
    AS url_checks ON urls.id = url_checks.url_id ORDER BY urls.id DESC'''
    conn.execute(query)
    return conn.fetchall()


def get_data_of_id(id):
    query = '''SELECT * FROM urls WHERE id = %s'''
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        return cursor.fetchall()


def check_id(id):
    url_id_check = '''SELECT * FROM url_checks WHERE url_id = %s
                      ORDER BY id DESC'''
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(url_id_check, (id,))
        return cursor.fetchall()


def get_data_of_name(url_name):
    query = "SELECT id FROM urls WHERE name = %s"
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (url_name,))
        id = cursor.fetchone()
        if id is None:
            return None
        return id[0]


def get_status_and_name(id):
    query = '''SELECT name FROM urls WHERE id = %s'''
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        data_url = cursor.fetchall()
        url_name = data_url[0][0]
        url_status_code = get_status(connection, id)
        return url_name, url_status_code


def add_url(current_url):
    query = '''INSERT INTO urls(name, created_at)
               VALUES(%s, %s)'''
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (current_url, datetime.today()))
        connection.commit()


def add_checked(id, url_status_code, data_html):
    url_date = datetime.today()
    query = '''INSERT INTO
                url_checks(url_id, status_code, h1, title,
                           description, created_at)
               VALUES(%s, %s, %s, %s, %s, %s)'''
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (id,
                               url_status_code,
                               data_html["h1"],
                               data_html["title"],
                               data_html["description"],
                               url_date))
        connection.commit()
