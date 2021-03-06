from flaskapp import db
from flaskapp.models import Client, Conditions
import os
import shutil
#This script refreshes the db and adds dummy client, conditions, SharedFiles and ReceivedFiles.

#Remove app.db and migrations folder
#
try:
    shutil.rmtree("migrations")
    print("Migrations folder removed")
except(FileNotFoundError):
    print("Migration folder not found")

try:
    shutil.rmtree("Contract/ReceivedContracts")
    print("ReceivedContracts folder removed")
except(FileNotFoundError):
    print("ReceivedContracts folder not found")

try:
    shutil.rmtree("Contract/SentContracts")
    print("SentContracts folder removed")
except(FileNotFoundError):
    print("SentContracts folder not found")

try:
    shutil.rmtree("Filesharing/SharedFiles")
    print("SharedFiles folder removed")
except(FileNotFoundError):
    print("SharedFiles folder not found")

try:
    shutil.rmtree("Filesharing/ReceivedFiles")
    print("ReceivedFiles folder removed")
except(FileNotFoundError):
    print("ReceivedFiles folder not found")

try:
    shutil.rmtree("Shell/SentShells")
    print("SentShells folder removed")
except(FileNotFoundError):
    print("SentShells folder not found")

try:
    shutil.rmtree("Shell/ReceivedShells")
    print("ReceivedShells folder removed")
except(FileNotFoundError):
    print("ReceivedShells folder not found")

try:
    os.remove("flaskapp/app.db")
    print("app.db removed")
except(FileNotFoundError):
    print("app.db not found")


#New db
os.mkdir("Contract/ReceivedContracts")
print("ReceivedContracts folder created")
os.mkdir("Contract/SentContracts")
print("SentContracts folder created")
os.mkdir("Filesharing/SharedFiles")
print("SharedFiles folder created")
os.mkdir("Filesharing/ReceivedFiles")
print("ReceivedFiles folder created")
os.mkdir("Shell/ReceivedShells")
print("ReceivedShells folder created")
os.mkdir("Shell/SentShells")
print("SentShells folder created")


os.system("set FLASK_APP=run.py")
os.system("flask db init")
os.system("flask db migrate")
os.system("flask db upgrade")
os.system("flask db ")
add_pay_x = Conditions(#we always want the pay condition in the db
    id = 0,
    name = "Pay",
    desc = "x"
)
db.session.add(add_pay_x)
db.session.commit()
db.session.close()
print("Database refresh completed")
