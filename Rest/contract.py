from Rest import app, BASE_URL
from Contract.contracthandler import getHandler
from flask import request
from jsonschema import validate
import json
import os

from Filesharing.sender import FileSender

CONTRACT_BASE_PATH = os.path.abspath("./Contract/RecievedContracts/")


with open(os.path.abspath("./Contract/contract.schema.json"), 'r') as schema_file:
#with open("contract.py", 'r') as schema_file:
    schema = schema_file.read()

@app.route(BASE_URL + "/register_contract", methods=["PUT"])
def put_contract():
    # Check if the request is of the correct type
    if not (request.content_type.startswith("application/json")):
        return "Supported media type is application/json", 415
    
    # Get the json body
    json_body = request.get_json()
    
    # Check if the json is correctly formatted
    try:
        validate(instance = json_body, schema = json.loads(schema))
    except Exception as e:
        return "Exception occured while parsing the json data :" + str(e), 400
    
    # Get the contractID from the json dict
    contractID = json_body['contractID']
    clientID = json_body['senderID']
    status = "pending"
    path = CONTRACT_BASE_PATH + "/" + contractID
    print(path)
    with open(path, 'w') as f:
        f.write(json.dumps(json_body))
    
    # Update database
    
    return '', 201
