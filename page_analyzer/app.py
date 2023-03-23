from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=['POST'])
def index():
    return render_template('index.html')
