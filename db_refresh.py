from flaskapp import db
from flaskapp.models import Client
import os
import shutil
#This script refreshes the db and adds dummy client, conditions, and SharedFiles.

#Remove app.db and migrations folder
try:
    shutil.rmtree("migrations")
    print("Migrations folder removed")
except(FileNotFoundError):
    print("Migration folder not found")

try:
    os.remove("flaskapp/app.db")
    print("app.db removed")
except(FileNotFoundError):
    print("app.db not found")


#New db
os.system("set FLASK_APP=run.py")
os.system("flask db init")
os.system("flask db migrate")
os.system("flask db upgrade")


