from flaskapp import app, db
from flaskapp.models import Contract_recv
from Contract.contracthandler import getHandler
from flask import request
from jsonschema import validate
import json
import os

from Filesharing.sender import FileSender

CONTRACT_BASE_PATH = os.path.abspath("./Contract/ReceivedContracts/")


with open(os.path.abspath("./Contract/contract.schema.json"), 'r') as schema_file:
#with open("contract.py", 'r') as schema_file:
    schema = schema_file.read()

@app.route( "/v1/register_contract", methods=["PUT"])
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
    clientID = json_body['senderID']['id']
    status = "pending"
    path = os.path.join(CONTRACT_BASE_PATH, contractID + ".json")
    with open(path, 'w') as f:
        json.dump(json_body, f, indent=4)
        #f.write(json.dumps(json_body))
    
    # Update database
    result = Contract_recv.query.filter_by(id=contractID).first()
    
    if not result:
        # If no result, contract is new, register in database
        contract = Contract_recv(id=contractID, path=path, status=status, client_id=clientID, file_id=None)
        db.session.add(contract)
        db.session.commit()
    else:
        # Contract already exists, if it has been handled(accepted or declined) then you can't change it, otherwise update the contract
        if result.status != "pending":
            return 'This contract have already been accepted', 400
        
        result.path = path
        result.status = status
        result.client_id = clientID
        result.file_id=None
        db.session.commit()
    
    return '', 201
