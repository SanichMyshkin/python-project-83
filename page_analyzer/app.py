from flask import Flask, render_template, request, get_flashed_messages, flash, redirect, url_for
# import psycopg2
# import os
import validators

# DATABASE_URL = os.getenv('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)

app.secret_key = "secret_key"


@app.route('/', methods=['GET'])
def index():
    message = get_flashed_messages(with_categories=True)
    data = []
    errors = []
    return render_template('index.html',
                           data=data,
                           errors=errors,
                           message=message)


@app.post('/urls')
def all_sites():
    data = request.form.to_dict()
    url = data['url']
    errors = is_valid(url)
    if errors:
        flash(f"{errors['name']}")
        return render_template('index.html',
                               errors=errors,
                               data=data)

    return render_template(
        'urls.html',
        data=url
    )


def is_valid(item):
    errors = dict()
    if not validators.url(item):
        errors['name'] = 'Некорректный URL'
    if len(item) > 255:
        errors['name'] = 'URL превышает 255 символов'
    return errors
