from flaskapp.contract.config import *

def getClientlist():
    return db.session.query(Client).all()

def getClient(id):
    return db.session.query(Client).filter_by(id=id).first()