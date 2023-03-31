from flask import Flask, render_template, request, get_flashed_messages, flash
import psycopg2
import os
import validators
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")




@app.route('/', methods=['GET'])
def index():
    message = get_flashed_messages(with_categories=True)
    data = []
    errors = []
    return render_template('index.html',
                           data=data,
                           errors=errors,
                           message=message)


@app.route('/urls', methods=["POST", "GET"])
def all_sites():
    data = request.form.to_dict()

    errors = is_valid(data['url'])  # сделать проверку на пустоту
    if errors:
        flash(f"{errors['name']}")
        return render_template('index.html',
                               errors=errors,
                               data=data)
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    current_datetime = datetime.now()
    sql_query = f'''INSERT INTO urls(name, created_at)
                VALUES('{data['url']}','{current_datetime}')
                '''
    cursor.execute(sql_query)
    cursor.execute("Select * from urls")
    cur = cursor.fetchall()
    conn.commit()
    # cursor.close()
    # conn.close()
    flash("Страница успешно добавлена")
    return render_template(
        'urls.html',
        data=cur,
    )


@app.route("/urls/<int:id>")
def id_sites(id):
    message = get_flashed_messages(with_categories=True)
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    sql_query = f'''SELECT * FROM urls WHERE id={id}'''
    cursor.execute(sql_query)
    return render_template("url_id.html",
                           message=message,
                           id=id,
                           data=list(cursor))


def is_valid(item):
    errors = dict()
    if not validators.url(item):
        errors['name'] = 'Некорректный URL'
    if len(item) > 255:
        errors['name'] = 'URL превышает 255 символов'
    return errors
