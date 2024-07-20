# Page Analyzer

<p>
Analyze specified pages for SEO suitability
</p>

[![Actions Status](https://github.com/SanichMakakich/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/SanichMakakich/python-project-83/actions)
[![Flake8](https://github.com/SanichMakakich/python-project-83/actions/workflows/main.yml/badge.svg)](https://github.com/SanichMakakich/python-project-83/actions/workflows/main.yml)
<a href="https://codeclimate.com/github/SanichMakakich/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/4ad048f0ec810f00f164/maintainability" /></a>


## About

Page Analyzer is a full-featured application based on the Flask framework that analyzes specified pages for SEO suitability. 

Here the basic principles of building modern websites on the MVC architecture are used: working with routing, query handlers and templating, interaction with the database.

In this project the Bootstrap 5 framework along with Jinja2 template engine are used. The frontend is rendered on the backend. This means that the page is built by the Jinja2 backend, which returns prepared HTML. And this HTML is rendered by the server.

PostgreSQL is used as the object-relational database system with Psycopg library to work with PostgreSQL directly from Python.

[Demo](https://python-project-83-production-8bc8.up.railway.app/)

### Features

* [X] Validate, normalize and add new URL to the database;
* [X] Check the site for its availability;
* [X] Query the desired site, collect information about it and add it to the database;
* [X] Display all added URLs;
* [X] Display the specific entered URL on a separate page with obtained information;

---

## Installation

### Prerequisites

#### Poetry

The project uses the Poetry dependency manager. To install Poetry use its [official instruction](https://python-poetry.org/docs/#installation).

#### PostgreSQL

As database the PostgreSQL database system is being used. You need to install it first. You can download the ready-to-use package from [official website](https://www.postgresql.org/download/) or use Homebrew:
```shell
brew install postgresql
```

### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
git clone git@github.com:SanichMyshkin/python-project-83.git
cd python-project-83
```



---

## Usage without docker

Then you have to install all necessary dependencies:

```bash
make install
```

Create .env file in the root folder and add following variables:
```bash
DATABASE_URL = 'postgresql://{provider}://{user}:{password}@{host}:{port}/page_analyzer'
SECRET_KEY = '{your secret key}'
```
To create a database, run the command 
```bash
make datadase
```

Start the gunicorn Flask server by running:
```bash
make start
```
By default, the server will be available at http://0.0.0.0:8000. 

_It is also possible to start it local in development mode with debugger active using:_
```bash
make dev
```
_The dev server will be at http://127.0.0.1:8000_

-- 

## Using Docker

If you want to use the application using docker, then you need to create a .env.docker file with the following data
```bash
DATABASE_URL = 'postgres://{provider}://{user}:{password}@db:{port}/page_analyzer'
SECRET_KEY = '{your secret key}'
```

Once filled in, run the command 
```bash
make docker
```

By default, the server will be available at http://0.0.0.0:8000