from flaskapp import db
from flaskapp.models import Client
import os
import shutil
#This script refreshes the db and adds dummy client, conditions, and files.

#Remove app.db and migrations folder
shutil.rmtree("migrations")
print("Migrations folder removed")
os.remove("flaskapp/app.db")
print("app.db removed")

#New db
os.system("set FLASK_APP=run.py")
os.system("flask db init")
os.system("flask db migrate")
os.system("flask db upgrade")
print("New db created, dummy table rows to be added")

#Adding clients
file = open("db_refresh.txt", 'r')
for line in file:
    u = Client(name=line, ip_address="0.0.0.0")
    db.session.add(u)
    db.session.commit()

print(Client.query.all())

#more to be added

