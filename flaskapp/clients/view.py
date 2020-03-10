from flaskapp.clients.config import *

def getClientlist():
    return db.session.query(Client).all()

def getClient(id):
    return db.session.query(Client).filter_by(id=id).first()

def readRSA():
    with open("rsa_key.json") as json_file:
        rsa_file = json.load(json_file)
    return rsa_file