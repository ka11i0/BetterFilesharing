from flaskapp import db, app
from flaskapp.models import Contract_sent, Contract_recv, Client

import json
#This script adds a dummy contract to test accept/decline contract



print("enter: 0 for reciver, enter: 1 for sender")
state = input()

#sender
if (state=="1"):
    json_contract = {
        'contractID': 111,
        'senderID': "1",
        'receiverID': "2",
        'file': {
            'name': "fuck u",
            'filter': 'n/a'
        },
        'conditions': ["1"]
    }
    with open(app.config['CONTRACT_FOLDER'] + str("111") + app.config['CONTRACT_FILEEXT'], 'w') as outfile:
        json.dump(json_contract, outfile, indent=4)

    u = Contract_sent(id=111, path="Contract/SentContracts/", status="new", client_id="2", file_id="1")
    db.session.add(u)
    db.session.commit()

#reciver
if (state=="0"):
    json_contract = {
        'contractID': 111,
        'senderID': "2",
        'receiverID': "1",
        'file': {
            'name': "fuck u",
            'filter': 'n/a'
        },
        'conditions': ["1"]
    }
    with open(app.config['CONTRACT_FOLDER'] + str("111") + app.config['CONTRACT_FILEEXT'], 'w') as outfile:
        json.dump(json_contract, outfile, indent=4)

    u = Contract_recv(id=111, path="Contract/SentContracts/", status="pending", client_id="1", file_id="1")
    db.session.add(u)
    db.session.commit()


