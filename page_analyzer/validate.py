import validators
from page_analyzer.connected import connect_to_db
from dotenv import load_dotenv
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

    if not item:
        errors['name'] = "URL Обязателен"
        return errors

    if not validators.url(current_url):
        errors['name'] = 'Некорректный URL'

    if len(current_url) > 255:
        errors['name'] = 'URL превышает 255 символов'

    for url in db:
        if current_url == url[0]:
            errors['name'] = 'Страница уже существует'
            errors['id'] = existing_id[0][0]

    return errors
