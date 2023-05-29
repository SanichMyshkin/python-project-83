from flask import Flask
from page_analyzer.routes import blue_app

import os
from dotenv import load_dotenv

app = Flask(__name__)
app.register_blueprint(blue_app)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

if __name__ == '__main__':
    app.run()
