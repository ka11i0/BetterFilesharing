from flaskapp import app, db
from flaskapp.models import Contract_recv, Shell_recv
from Contract.contracthandler import getHandler
from flask import request, redirect, url_for
from jsonschema import validate, exceptions as jsonschemaExceptions
import json
import os

from Filesharing.sender import FileSender

from hashlib import sha512

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
    json_body_raw = request.get_json()
    json_body = json_body_raw['contract']
    # Check if the json is correctly formatted
    try:
        validate(instance = json_body, schema = json.loads(schema))
    except Exception as e:
        return "Exception occured while parsing the json data :" + str(e), 400
    
    # Get the contractID from
    #  the json dict
    contractID = json_body['contractID']
    clientID = json_body['senderID']['id']
    status = "pending"

    client = Client.query.filter_by(id = clientID).first()
    
    contracthash = int.from_bytes(sha512(json.loads(json_body)).digest(), byteorder='big')
    calculated_sig = hex(pow(contracthash, int(client.e), int(client.n)))
    
    if not (calculated_sig == json_body_raw['signature']):
        return "signatures does not match", 400

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


    # get all shells with current ClientID
    shell_paths = Shell_recv.query.filter_by(client_id=clientID).all()

    # Validate contract with all shell schemas of current ClientID and send accept reply if validation is OK.
    for sp in shell_paths:
        # open shell schema and validate
        with open(sp.path) as json_schema:
            shell_schema = json.load(json_schema)
        
        try:
            # validate contract with shell schema
            validate(instance=json_body, schema=shell_schema)

            # update contract status from pending to accepted and send accept message to ClientID
            return redirect(url_for('accept_or_decline', id=contractID, status='accepted'))
        
        # catch SchemaError and pass (let status = pending)
        except jsonschemaExceptions.ValidationError as e:
            pass
    
    
    return '', 201
