import validators
from page_analyzer.connected import connect_to_db
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def is_valid(item):
    errors = dict()
    current_url = item['url']

    resquest_all_db = '''SELECT name FROM urls'''
    request_existing_id = f'''SELECT id FROM urls
                            WHERE name='{current_url}'
                            '''
    db = connect_to_db(resquest_all_db)
    existing_id = connect_to_db(request_existing_id)

    if not current_url:
        errors['name'] = "URL Обязателен"

    if not validators.url(current_url):
        errors['name'] = 'Некорректный URL'
    if len(current_url) > 255:
        errors['name'] = 'URL превышает 255 символов'

    if db:
        for url in db:
            if current_url == url[0]:
                errors['name'] = 'Страница уже существует'
                errors['id'] = existing_id[0][0]
    return errors


def get_domain(url):
    scheme = urlparse(url).scheme.lower()
    hostname = urlparse(url).hostname.lower()
    return f"{scheme}://{hostname}"
