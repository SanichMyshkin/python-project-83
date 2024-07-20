PORT ?= 8000

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

debug:
	flask --app page_analyzer/app --debug run

install:
	poetry install

lint:
	poetry run flake8 --exclude=.venv/


# создание шаблона базы данных
database: db-create schema-load

db-create:
	createdb page_analyzer

schema-load:
	psql page_analyzer < database.sql


# docker 
build:
	docker build -t page_analyzer .

run:
	docker run -it -p 8000:8000 page_analyzer
# docker run --platform=linux/amd64 --name page_analyzer_container -p 8000:8000 page_analyzer

docker:
	docker compose up

