from datetime import datetime
from flaskapp import db


# Data is represented by a collection of classes, also called database models.
class Contract_sent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(8), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), index=True, nullable=False)

    def __repr__(self):  # Tells how to print objects of this class, (good for debugging)
        return '<Contract_sent {}>'.format(self.id)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    path = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<File {}>'.format(self.id)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    ip_address = db.Column(db.String(128), nullable=False)
    debt = db.Column(db.Integer, nullable=True) # curr_curr
    max_debt = db.Column(db.Integer, nullable=True) # cut_curr
    rsa_n = db.Column(db.String(256), nullable=True) # part of rsa public key
    rsa_e = db.Column(db.String(256), nullable=True) # part of rsa public key

    def __repr__(self):
        return '<Client {}>'.format(self.id)


class Contract_recv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(8), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), index=True, nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), index=True, nullable=True)

    def __repr__(self):
        return '<Contract_recv {}>'.format(self.id)


class Access(db.Model):
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True, nullable=False)

    def __repr__(self):
        return '<Access {}>'.format(self.file_id)

class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Access {}>'.format(self.id)
        

class Shell_send(db.Model):
    shell_id = db.Column(db.Integer, primary_key=True) # shell id
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True, nullable=False) # id of contract recv
    pattern = db.Column(db.String(256), nullable=True) # Ftype
    path = db.Column(db.String(256), nullable=True) # path to shell contract
    status = db.Column(db.String(8), nullable=False) # active OR inactive

    def __repr__(self):
        return '<Shell_send {}>'.format(self.shell_id)


class Shell_recv(db.Model):
    shell_id = db.Column(db.Integer, primary_key=True)  # shell id
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True, nullable=False)
    pattern = db.Column(db.String(256), nullable=True) # Ftype
    path = db.Column(db.String(256), nullable=True)  # path to shell contract
    status = db.Column(db.String(8), nullable=False) # active OR inactive

    def __repr__(self):
        return '<Shell_recv {}>'.format(self.shell_id)
