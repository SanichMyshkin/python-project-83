from page_analyzer.connected import get_connection
from datetime import datetime
from page_analyzer.checks_request import get_status


def get_all_url():
    query = '''SELECT urls.id, urls.name,
                    url_checks.created_at, url_checks.status_code
                    FROM urls LEFT JOIN (
                    SELECT DISTINCT ON (url_id) url_id, created_at, status_code
                    FROM url_checks
                    ORDER BY url_id, created_at DESC) AS url_checks
                    ON urls.id = url_checks.url_id
                    ORDER BY urls.id DESC'''
    with get_connection() as connected:
        responce = get_all_db(connected, query)
        return responce


def get_data_of_id(id):
    query = f'''SELECT * FROM urls WHERE id = {id}'''
    with get_connection() as connection:
        data = get_all_db(connection, query)
        return data


def check_id(id):
    url_id_check = f'''SELECT * FROM url_checks WHERE url_id = {id}
                           ORDER BY id DESC'''
    with get_connection() as connection:
        id_checked = get_all_db(connection, url_id_check)
        return id_checked


def get_data_of_name(url_name):
    query = f"SELECT id FROM urls WHERE name = '{url_name}'"
    with get_connection() as connection:
        id = get_one_db(connection, query)
        if id is None:
            return None
        return id[0]


def get_status_and_name(id):
    query = f'''SELECT name FROM urls WHERE id={id}'''
    with get_connection() as connection:
        data_url = get_all_db(connection, query)
        url_name = data_url[0][0]
        url_status_code = get_status(connection, id)
        return url_name, url_status_code


def add_url(current_url):
    query = f'''INSERT INTO urls(name, created_at)
                        VALUES('{current_url}','{datetime.today()}')'''
    with get_connection() as connection:
        insert_to_db(connection, query)


def add_checked(id, url_status_code, data_html):
    url_date = datetime.today()
    query = f'''INSERT INTO
                url_checks(url_id, status_code, h1, title,
                            description, created_at)
                VALUES({id},
                        {url_status_code},
                        '{data_html["h1"]}',
                        '{data_html["title"]}',
                        '{data_html["description"]}',
                        '{url_date}')'''
    with get_connection() as connection:
        insert_to_db(connection, query)


def get_all_db(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        response = cursor.fetchall()
        return response


def get_one_db(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        response = cursor.fetchone()
        return response


def insert_to_db(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)

        connection.commit()
