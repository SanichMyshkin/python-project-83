from flask import Flask, render_template, request
# import psycopg2
# import os
import validators

# DATABASE_URL = os.getenv('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)

app.secret_key = "secret_key"


@app.route('/', methods=['GET'])
def index():
    # message = get_flashed_messages(with_categories=True)
    data = []
    errors = []
    return render_template('index.html',
                           data=data,
                           errors=errors)


@app.post('/urls')
def all_sites():
    data = request.form.to_dict()
    return render_template(
        'urls.html',
        data=data
    )


def is_valid(item):
    errors = dict()
    if not validators.url(item):
        errors['name'] = 'Адрес не валидный. Проверьте правильность написания!'
    if len(item) > 255:
        errors['name'] = 'Длинна символов привышает 255!'
    return errors
