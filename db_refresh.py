from flaskapp import db
from flaskapp.models import Client, Conditions
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
os.system("flask db ")
add_pay_x = Conditions(
    id = 0,
    name = "Pay",
    desc = "x"
)
db.session.add(add_pay_x)
db.session.commit()
db.session.close()
