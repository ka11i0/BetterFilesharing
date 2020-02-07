from flaskapp.models import *
from flaskapp import db

get = Contract_recv.query.all()
print(get)