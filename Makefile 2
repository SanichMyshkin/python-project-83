PORT ?= 8000

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

debug:
	flask --app page_analyzer/app --debug run



# Комады сборки проекта
pu:
	git add .
	git commit -m "fix"
	git push

package-install:
	python3 -m pip install --user --force dist/*.whl

build:
	poetry build

install:
	poetry install

lint:
	poetry run flake8

push: build package-install install