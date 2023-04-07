import requests
from page_analyzer.connected import connect_to_db


def get_status(id):
    url = f"SELECT name FROM urls WHERE id={id}"
    url_name = connect_to_db(url)
    try:
        r = requests.get(url_name[0][0])
    except Exception as _ex:
        return _ex
    return r.status_code
