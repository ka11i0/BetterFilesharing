from flask import Flask
from flaskapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'abc'           # required for wtform
db = SQLAlchemy(app)
migrate = Migrate(app, db)     #This allows for schema modifications without, db recreation.

from flaskapp import routes, models
