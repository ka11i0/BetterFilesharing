from datetime import datetime
from flaskapp import db


# Data is represented by a collection of classes, also called database models.
class Contract_sent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(8), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)

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

    def __repr__(self):
        return '<Client {}>'.format(self.id)


class Contract_recv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(8), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    def __repr__(self):
        return '<Contract_recv {}>'.format(self.id)