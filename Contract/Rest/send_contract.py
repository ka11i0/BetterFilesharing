from flaskapp.models import Contract_sent, Client
from flaskapp import app
import requests
import json
from hashlib import sha512

def send_contract(contractid, clientid):
    client = Client.query.filter_by(id=clientid).first()
    sendaddr = client.ip_address
    contract = Contract_sent.query.filter_by(id=contractid).first()
    path = contract.path
    jsonbody = {}
    with open(path, 'r') as readfile:
        jsonbody['contract'] = json.load(readfile)
    print(json.dumps(jsonbody['contract']))
    contracthash = int.from_bytes(sha512(str.encode(json.dumps(jsonbody['contract']))).digest(), byteorder='big')
    jsonbody['signature'] = hex(pow(contracthash, int(app.config['RSA_KEY']['d'], 16), int(app.config['RSA_KEY']['n'], 16)))
    print(contracthash)

    response = requests.put('http://' + sendaddr + ':5000/v1/register_contract', json=json.dumps(jsonbody))
    if response.status_code != 201 and response.status_code != 200:
        raise Exception(response.text)
