from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    Hello = 'Hello, Im gay!'
    return f"{Hello}"
