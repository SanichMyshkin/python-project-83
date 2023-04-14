import requests
from bs4 import BeautifulSoup
from page_analyzer.connected import get_all_db


def get_status(id):
    url = f"SELECT name FROM urls WHERE id={id}"
    url_name = get_all_db(url)
    try:
        r = requests.get(url_name[0][0])
    except Exception as _ex:
        return _ex
    return r.status_code


def get_data_html(url):
    data = {
        "h1": '',
        'title': '',
        'description': ''
    }

    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    if soup.h1:
        data['h1'] = soup.h1.text.strip()
    if soup.title:
        data['title'] = soup.title.text.strip()
    if soup.find_all(attrs={"name": "description"}):
        description = soup.find_all(attrs={"name": "description"})[0]
        data['description'] = description['content'].strip()

    return data
