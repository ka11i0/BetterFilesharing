from flask import Flask
from flaskapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy.engine import Engine
from sqlalchemy import event

import re
import sqlite3

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'abc'           # required for wtform
db = SQLAlchemy(app)
migrate = Migrate(app, db)     #This allows for schema modifications without, db recreation.

def regexp(expr, item):
    try:
        reg = re.compile(expr)
        return reg.search(item) is not None
    except Exception as e:
        print(str(e))
        pass

#db.engine.connect().create_function("REGEXP", 2, regexp)

@event.listens_for(Engine, 'connect')
def sqlite_engine_connect(dbapi_connection, connection_record):
    if not isinstance(dbapi_connection, sqlite3.Connection):
        return
    dbapi_connection.create_function("REGEXP", 2, regexp)
    sqlite3.enable_callback_tracebacks(True)

from flaskapp import models
from flaskapp.files import routes
from flaskapp.clients import routes
from flaskapp.contract import routes
from Contract.Rest import contract
from flaskapp.shell import routes
from Contract.Rest import conditions
