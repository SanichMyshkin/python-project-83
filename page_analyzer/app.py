from flask import Flask, render_template, \
    flash, request, redirect, url_for

import os
from dotenv import load_dotenv

from page_analyzer.checks_request import get_data_html
from page_analyzer.validate import is_valid, get_normalize_domain
from page_analyzer.routes import get_all_url, get_url_id, check_id,\
    url_id, add_url, get_status_and_name, add_all

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")


@app.route('/', methods=['GET'])
def index():
    data = []
    return render_template('index.html',
                           data=data), 200


@app.route('/urls', methods=["GET"])
def get_sites():
    responce = get_all_url()
    return render_template('urls.html',
                           data=responce)


@app.route('/urls', methods=["POST"])
def post_sites():
    data = request.form.to_dict()
    url = data['url']
    current_url = get_normalize_domain(url)
    id = url_id(current_url)
    errors = is_valid(data)

    if errors:
        flash(f"{errors['name']}", 'alert alert-danger')
        return render_template("index.html",
                               data=current_url), 422
    if id:
        flash('Страница уже существует', 'alert alert-info')
        return redirect(url_for('id_sites', id=id))

    add_url(current_url)
    flash("Страница успешно добавлена", 'alert alert-success')
    return redirect(url_for('id_sites', id=id))


@app.route("/urls/<int:id>", methods=["POST", "GET"])
def id_sites(id):
    data_of_id = get_url_id(id)

    if not data_of_id:
        return render_template('error.html'), 200

    id_checked = check_id(id)
    return render_template("url_id.html",
                           id=id,
                           data=data_of_id,
                           checks=id_checked)


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    url_name, url_status_code = get_status_and_name(id)

    if url_status_code != 200:
        flash('Произошла ошибка при проверке', 'alert alert-danger')
        return redirect(url_for('id_sites', id=id, code=422))

    data_html = get_data_html(url_name)

    add_all(id, url_status_code, data_html)
    flash('Страница успешно проверена', 'alert alert-success')

    return redirect(url_for('id_sites', id=id))


if __name__ == '__main__':
    app()
