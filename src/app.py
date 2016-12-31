import uuid

from flask import Flask
from flask import render_template

from src.common.database import Database
from src.models.users.views import user_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint

__author__ = 'glgs'

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = uuid.uuid4().hex


@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
