from dotenv import load_dotenv
from flask import Flask, render_template, \
    flash, request, redirect, url_for
import os
import requests
from datetime import datetime
from page_analyzer.connected import get_id, get_all_db, \
    get_one_db, insert_to_db
from page_analyzer.checks_request import get_status, get_data_html
from page_analyzer.validate import is_valid, get_normalize_domain

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET'])
def index():
    data = []
    return render_template('index.html',
                           data=data)


@app.route('/urls', methods=["GET"])
def get_sites():
    query = '''SELECT
                   urls.id,
                   urls.name,
                   url_checks.created_at,
                   url_checks.status_code
                FROM urls LEFT JOIN
                      (
                         SELECT url_id, MAX(id) AS max_id
                         FROM url_checks GROUP BY url_id
                      )
                      AS max_checks
                      ON urls.id = max_checks.url_id
                   LEFT JOIN
                      url_checks
                      ON max_checks.max_id = url_checks.id
                      ORDER BY urls.id DESC'''

    responce = get_all_db(query)
    return render_template('urls.html',
                           data=responce)


@app.route('/urls', methods=["POST"])
def post_sites():
    data = request.form.to_dict()

    url = data['url']

    current_url = get_normalize_domain(url)

    id = get_id(current_url)

    errors = is_valid(data)

    if errors:
        flash(f"{errors['name']}", 'alert alert-danger')
        return render_template("index.html",
                               data=current_url), 422

    if id:
        flash('Страница уже существует', 'alert alert-info')
        return redirect(url_for('id_sites', id=id))

    sql_query = f'''INSERT INTO urls(name, created_at)
                    VALUES('{current_url}','{datetime.today()}')'''
    insert_to_db(sql_query)
    flash("Страница успешно добавлена", 'alert alert-success')

    query_id = f"SELECT id FROM urls WHERE name='{current_url}'"
    id = get_one_db(query_id)

    return redirect(url_for('id_sites', id=id[0]))


@app.route("/urls/<int:id>", methods=["POST", "GET"])
def id_sites(id):
    url_id = f'''SELECT * FROM urls WHERE id={id}'''
    data_of_url = get_all_db(url_id)

    if not data_of_url:
        return render_template('error.html')

    url_id_check = f'''SELECT * FROM url_checks WHERE url_id={id}
                       ORDER BY id DESC'''
    data_check = get_all_db(url_id_check)
    return render_template("url_id.html",
                           id=id,
                           data=data_of_url,
                           checks=data_check)


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    query_data = f'SELECT * FROM urls WHERE id={id}'

    data_url = get_all_db(query_data)
    url_id = data_url[0][0]
    url_name = data_url[0][1]
    url_date = datetime.today()
    url_status_code = get_status(id)
    if url_status_code != 200:
        flash('Произошла ошибка при проверке', 'alert alert-danger')
        return redirect(url_for('id_sites', id=id))
    else:
        data_html = get_data_html(url_name)

        query = f'''INSERT INTO
                url_checks(url_id, status_code, h1, title, description, created_at)
                VALUES('{url_id}',
                        200,
                        '{data_html["h1"]}',
                        '{data_html["title"]}',
                        '{data_html["description"]}',
                        '{url_date}')'''
        insert_to_db(query)
        flash('Страница успешно проверена', 'alert alert-success')
        return redirect(url_for('id_sites', id=id))
