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


def get_id(conn, url_name):
    query = f"SELECT * FROM urls WHERE name = '{url_name}'"
    response = get_one_db(conn, query)
    if response:
        return response[0]
    return None
