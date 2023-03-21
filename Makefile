PORT ?= 8000

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app




# Комады сборки проекта
package:
	python3 -m pip install --user --force dist/*.whl

build:
	poetry build

install:
	poetry install

lint:
	poetry run flake8