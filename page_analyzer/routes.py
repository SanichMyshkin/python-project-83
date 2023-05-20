from page_analyzer.connected import get_connection
from page_analyzer.models import get_all_db, get_one_db, insert_to_db
from datetime import datetime
from page_analyzer.checks_request import get_status


def get_all_url():
    query = '''SELECT
                   urls.id,
                   urls.name,
                   url_checks.created_at,
                   url_checks.status_code
                FROM urls LEFT JOIN
                      (
                         SELECT url_id, MAX(id) AS max_id
                         FROM url_checks GROUP BY url_id
                      )
                      AS max_checks
                      ON urls.id = max_checks.url_id
                   LEFT JOIN
                      url_checks
                      ON max_checks.max_id = url_checks.id
                      ORDER BY urls.id DESC'''

    with get_connection() as connected:
        responce = get_all_db(connected, query)
        return responce


def get_url_id(id):
    url_id = f'''SELECT * FROM urls WHERE id = {id}'''
    with get_connection() as connection:
        ids_urls = get_all_db(connection, url_id)
        return ids_urls


def check_id(id):
    url_id_check = f'''SELECT * FROM url_checks WHERE url_id = {id}
                           ORDER BY id DESC'''
    with get_connection() as connection:
        id_checked = get_all_db(connection, url_id_check)
        return id_checked


def url_id(url_name):
    query = f"SELECT * FROM urls WHERE name = '{url_name}'"
    with get_connection() as connection:
        id = get_one_db(connection, query)[0]
        if id:
            return id[0]
        return None


def add_url(current_url):
    sql_query = f'''INSERT INTO urls(name, created_at)
                        VALUES('{current_url}','{datetime.today()}')'''
    with get_connection() as connection:
        insert_to_db(connection, sql_query)


def add_all(id, url_status_code, data_html):
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


def get_status_and_name(id):
    query_select = f'''SELECT * FROM urls WHERE id={id}'''
    with get_connection() as connection:
        data_url = get_all_db(connection, query_select)
        url_name = data_url[0][1]
        url_status_code = get_status(connection, id)
        return url_name, url_status_code
