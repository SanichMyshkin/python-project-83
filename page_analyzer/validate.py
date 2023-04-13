import validators
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def is_valid(item):
    errors = dict()
    current_url = item['url']

    if not current_url:
        errors['name'] = "URL Обязателен"
    if not validators.url(current_url):
        errors['name'] = 'Некорректный URL'
    if len(current_url) > 255:
        errors['name'] = 'URL превышает 255 символов'

    return errors


'''    if db:
        for url in db:
            if current_url == url[0]:
                errors['name'] = 'Страница уже существует'
                errors['id'] = existing_id[0][0]'''


def get_normalize_domain(url):
    scheme = urlparse(url).scheme
    hostname = urlparse(url).hostname
    return f"{scheme}://{hostname}"
