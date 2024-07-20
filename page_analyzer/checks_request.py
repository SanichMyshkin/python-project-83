import requests
from bs4 import BeautifulSoup


def get_status(con, id):
    query = "SELECT name FROM urls WHERE id = %s"
    with con.cursor() as cursor:
        cursor.execute(query, (id,))
        url_name = cursor.fetchone()
    if not url_name:
        return "URL not found"

    url = url_name[0]
    try:
        r = requests.get(url)
        return r.status_code
    except requests.RequestException as ex:
        return str(ex)


def get_data_html(url):
    data = {
        "h1": '',
        'title': '',
        'description': ''
    }

    try:
        r = requests.get(url)
        r.raise_for_status()
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        if soup.h1:
            data['h1'] = soup.h1.text.strip()
        if soup.title:
            data['title'] = soup.title.text.strip()
        if soup.find('meta', attrs={"name": "description"}):
            description = soup.find('meta', attrs={"name": "description"})
            data['description'] = description.get('content', '').strip()

    except requests.RequestException as ex:
        print(f"Error fetching URL: {ex}")
    return data
