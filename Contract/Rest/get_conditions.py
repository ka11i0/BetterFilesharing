from flaskapp.models import Client
import requests
import json

def get_condition(clientid):
    client = Client.query.filter_by(id=clientid).first()
    sendaddr = client.ip_address
    response = requests.get('http://' + sendaddr + ':5000/v1/conditions')
    jsonbody = json.loads(response.text)
    return jsonbody
