from flask import Flask, render_template, \
    flash, request, redirect, url_for

import os
from dotenv import load_dotenv
from datetime import datetime

from page_analyzer.connected import connect_to_db, insert_to_db, get_id, get_name
from page_analyzer.checks_request import get_status, get_data_html
from page_analyzer.validate import is_valid, get_domain

app = Flask(__name__)
load_dotenv()

secret_key = os.getenv('SECRET_KEY', b'_5#y$$"F4f8z\n\xec]/')
app.secret_key = secret_key


@app.route('/', methods=['GET'])
def index():
    data = []
    errors = []
    return render_template('index.html',
                           data=data,
                           errors=errors)


@app.route('/urls', methods=["GET"])
def get_sites():
    request = '''SELECT
                   urls.id,
                   urls.name,
                   url_checks.created_at,
                   url_checks.status_code
                FROM
                   urls
                   LEFT JOIN
                      (
                         SELECT
                            url_id,
                            MAX(id) AS max_id
                         FROM
                            url_checks
                         GROUP BY
                            url_id
                      )
                      AS max_checks
                      ON urls.id = max_checks.url_id
                   LEFT JOIN
                      url_checks
                      ON max_checks.max_id = url_checks.id
                      ORDER BY urls.id DESC'''

    responce = connect_to_db(request)
    query = '''SELECT * from url_checks'''
    status = connect_to_db(query)
    return render_template('urls.html',
                           data=responce,
                           status=status)


@app.route('/urls', methods=["POST"])
def post_sites():
    data = request.form.to_dict()
    errors = is_valid(data)

    if errors:
        flash(f"{errors['name']}", 'alert alert-info')
        return render_template("index.html",
                               data=data,
                               errors=errors)
    current_url = get_domain(data['url'])
    id = get_id(current_url)

    if id:
        flash('Страница уже существует', 'alert alert-info')
        return redirect(url_for('id_sites', id=id), code=302)

    current_datetime = datetime.today()
    sql_query = f'''INSERT INTO urls(name, created_at)
                    VALUES('{current_url}','{current_datetime}')'''
    insert_to_db(sql_query)
    flash("Страница успешно добавлена", 'alert alert-success')
    id = get_id(current_url)
    return redirect(url_for('id_sites', id=id), code=302)


@app.route("/urls/<int:id>", methods=["POST", "GET"])
def id_sites(id):
    # message = get_flashed_messages(with_categories=True)
    url_id = f'''SELECT * FROM urls WHERE id={id}'''
    data_of_url = connect_to_db(url_id)

    if not data_of_url:
        return render_template('error.html')

    url_id_check = f'''SELECT * FROM url_checks WHERE url_id={id}
                       ORDER BY id DESC'''
    data_cheking = connect_to_db(url_id_check)
    return render_template("url_id.html",
                           id=id,
                           data=data_of_url,
                           checks=data_cheking)


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    query_data = f'SELECT * FROM urls WHERE id={id}'
    data_url = connect_to_db(query_data)
    url_id = data_url[0][0]
    url_name = data_url[0][1]
    url_date = datetime.today()
    url_status_code = get_status(id)

    if url_status_code != 200:
        flash('Произошла ошибка при проверке', 'alert alert-danger')
        return redirect(url_for('id_sites', id=id))

    data_html = get_data_html(url_name)

    query = f'''INSERT INTO
            url_checks(url_id, status_code, h1, title, description, created_at)
            VALUES('{url_id}',
                    '{url_status_code}',
                    '{data_html["h1"]}',
                    '{data_html["title"]}',
                    '{data_html["description"]}',
                    '{url_date}')'''
    insert_to_db(query)
    flash('Страница успешно проверена', 'alert alert-success')
    return redirect(url_for('id_sites', id=id))
