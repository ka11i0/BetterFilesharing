from Rest import app, BASE_URL
from Contract.contracthandler import getHandler
from flask import request
import json

from Filesharing.sender import FileSender

@app.route(BASE_URL + "/register_contract", methods=["PUT"])
def put_contract():
    contracthandler = getHandler()
    contracthandler.addcontract(request.get_json(force=True))
    return '', 201
