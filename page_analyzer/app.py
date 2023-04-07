from flask import Flask, render_template, \
    get_flashed_messages, flash, request, redirect, url_for
import os

from dotenv import load_dotenv
from page_analyzer.connected import connect_to_db, insert_to_db
from page_analyzer.checks_request import get_status
from datetime import datetime

from page_analyzer.validate import is_valid

app = Flask(__name__)
load_dotenv()

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
        flash(f"{errors['name']}")
        if errors.get('id'):
            return redirect(url_for('id_sites', id=errors['id']))
        else:
            return render_template("index.html",
                                   data=data,
                                   errors=errors)

    current_datetime = datetime.today()

    sql_query = f'''INSERT INTO urls(name, created_at)
                    VALUES('{data['url']}','{current_datetime}')'''
    max_query = 'SELECT MAX(id) FROM urls'
    insert_to_db(sql_query)
    max_id = connect_to_db(max_query)
    flash("Страница успешно добавлена", 'success')
    return redirect(url_for('id_sites', id=max_id[0][0]))


@app.route("/urls/<int:id>", methods=["POST", "GET"])
def id_sites(id):
    message = get_flashed_messages(with_categories=True)
    url_id = f'''SELECT * FROM urls WHERE id={id}'''
    data_of_url = connect_to_db(url_id)

    url_id_check = f'''SELECT * FROM url_checks WHERE url_id={id}
                       ORDER BY id DESC'''
    data_cheking = connect_to_db(url_id_check)

    return render_template("url_id.html",
                           message=message,
                           id=id,
                           data=data_of_url,
                           checks=data_cheking)


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    query_id = f'SELECT id, created_at FROM urls WHERE id={id}'

    url_id = connect_to_db(query_id)
    query_id = url_id[0][0]
    query_data = datetime.today()
    status_code = get_status(id)

    if status_code != 200:
        flash('Произошла ошибка при проверке')
        return redirect(url_for('id_sites', id=id))

    query = f'''INSERT INTO url_checks(url_id, status_code, created_at)
                VALUES('{query_id}','{status_code}','{query_data}')'''
    insert_to_db(query)

    return redirect(url_for('id_sites', id=id))
