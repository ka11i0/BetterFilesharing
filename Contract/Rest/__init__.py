from Contract.Rest.contract import put_contract
from flaskapp.models import Contract_sent, Client
import requests
import json

def send_contract(contractid, clientid):
    client = Client.query.filter_by(id=clientid).first()
    sendaddr = client.ip_address
    contract = Contract_sent.query.filter_by(id=contractid).first()
    path = contract.path
    with open(path, 'r') as readfile:
        jsonbody = readfile.read()
    response = requests.put('http://' + sendaddr + ':5000/v1/register_contract', json=json.loads(jsonbody))
    if response.status_code != 201:
        raise Exception(response.text)

def get_request(clientid):
    client = Client.query.filter_by(id=clientid).first()
    sendaddr = client.ip_address
    response = requests.get('http://' + sendaddr + ':5000/v1/conditions')
    jsonbody = json.loads(response.text)
    return jsonbody


