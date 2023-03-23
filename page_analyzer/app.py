from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    hello = 'Hello, Im gay!'
    return f"{hello}"
