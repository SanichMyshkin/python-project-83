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
