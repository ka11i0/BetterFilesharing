from flask import Flask
from flaskapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)     #This allows for schema modifications without, db recreation.

from flaskapp import routes, models
from Contract.Rest import contract
