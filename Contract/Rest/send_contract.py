from flaskapp.models import Contract_sent, Client
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
        jsonbody['contract'] = readfile.read()

    contracthash = int.from_bytes(sha512(json.loads(jsonbody['contract'])).digest(), byteorder='big')
    jsonbody['signature'] = hex(pow(contracthash, app.config['RSA_KEY']['d'], app.config['RSA_KEY']['n']))

    response = requests.put('http://' + sendaddr + ':5000/v1/register_contract', json=json.loads(jsonbody))
    if response.status_code != 201 or response.status_code != 200:
        raise Exception(response.text)
