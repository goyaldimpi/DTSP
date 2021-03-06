from flask import Flask
import os
from src.common.database import Database

import src.config as Config

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = os.environ.get("app_secret_key")


@app.before_first_request
def init_db():
    Database.initialize()


import src.route
import src.registered_components
