from flaskapp.models import Client
import requests
import json

def get_conditions(clientid):
    client = Client.query.filter_by(id=clientid).first()
    sendaddr = client.ip_address
    # 192.168.43.169:5000/v1/conditions
    url = "http://{}:5000/v1/conditions".format(sendaddr) 
    response = requests.get(url)
    jsonbody = json.loads(response.text)
    return jsonbody
