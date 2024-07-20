from flask import render_template, \
    flash, request, redirect, url_for, Blueprint

from page_analyzer.db import get_connection
from page_analyzer.checks_request import get_data_html
from page_analyzer.validate import is_valid, get_normalize_domain
from page_analyzer.models import get_all_url, get_data_of_id, check_id, \
    get_data_of_name, add_url, get_status_and_name, add_checked

blue_app = Blueprint('blue_app', __name__)


@blue_app.route('/', methods=["GET"])
def index():
    data = []
    return render_template('index.html',
                           data=data), 200


@blue_app.route('/urls', methods=["GET"])
def get_sites():
    with get_connection() as conn:
        responce = get_all_url(conn.cursor())
        return render_template('urls.html',
                               data=responce)


@blue_app.route('/urls', methods=["POST"])
def post_sites():
    data = request.form.to_dict()
    url = data['url']
    current_url = get_normalize_domain(url)
    id = get_data_of_name(current_url)
    errors = is_valid(data)

    if errors:
        flash(f"{errors['name']}", 'alert alert-danger')
        return render_template("index.html",
                               data=current_url), 422
    if id:
        flash('Страница уже существует', 'alert alert-info')
        return redirect(url_for('blue_app.id_sites', id=id))

    add_url(current_url)
    flash("Страница успешно добавлена", 'alert alert-success')
    id = get_data_of_name(current_url)
    return redirect(url_for('blue_app.id_sites', id=id))


@blue_app.route("/urls/<int:id>", methods=["POST", "GET"])
def id_sites(id):
    data_of_id = get_data_of_id(id)

    if not data_of_id:
        return render_template('error.html'), 200

    id_checked = check_id(id)
    return render_template("url_id.html",
                           id=id,
                           data=data_of_id,
                           checks=id_checked)


@blue_app.post('/urls/<int:id>/checks')
def url_checks(id):
    url_name, url_status_code = get_status_and_name(id)

    if url_status_code != 200:
        flash('Произошла ошибка при проверке', 'alert alert-danger')
        return redirect(url_for('blue_app.id_sites', id=id, code=422))

    data_html = get_data_html(url_name)

    add_checked(id, url_status_code, data_html)
    flash('Страница успешно проверена', 'alert alert-success')

    return redirect(url_for('blue_app.id_sites', id=id))
