from flaskapp import db
from flaskapp import models
import os
import shutil

# db_clear is for debugging, clears everything except clients and shells from db.

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


#New db
os.mkdir("Contract/ReceivedContracts")
print("ReceivedContracts folder created")
os.mkdir("Contract/SentContracts")
print("SentContracts folder created")
os.mkdir("Filesharing/SharedFiles")
print("SharedFiles folder created")
os.mkdir("Filesharing/ReceivedFiles")
print("ReceivedFiles folder created")

models.Contract_recv.query.delete()
models.Contract_sent.query.delete()
models.File.query.delete()
models.Access.query.delete()
db.session.commit()

