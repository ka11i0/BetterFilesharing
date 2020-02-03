from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import TextField, SelectMultipleField, SelectField, TextAreaField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired
from flaskapp import db, app
from flaskapp.models import *
from werkzeug import secure_filename
import os, json