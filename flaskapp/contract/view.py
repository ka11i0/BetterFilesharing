from flaskapp.contract.config import *

# get list of contracts from given table with given status and return a list of those contracts
# Parameters: status, table
def listContracts(status, table):
    contract_list = []
    if (table=="sent"):
        contracts = db.session.query(Contract_sent, Client).join(Contract_sent).filter(Contract_sent.status == status).all()
        for i in contracts:
            contract_dict = {}
            contract_dict['id'] = i.Contract_sent.id
            contract_dict['status'] = i.Contract_sent.status
            contract_dict['sender_id'] = i.Contract_sent.client_id

            contract = readContract(i.Contract_sent.id,'sent')
            contract_info = contract['senderID']
            for d in contract_info:
                contract_dict['name'] = contract_info[d]
            contract_list.append(contract_dict)
    if (table=="received"):
        contracts = db.session.query(Contract_recv, Client).join(Contract_recv).filter(Contract_recv.status == status).all()
        for i in contracts:
            contract_dict = {}
            contract_dict['id'] = i.Contract_recv.id
            contract_dict['status'] = i.Contract_recv.status
            contract_dict['sender_id'] = i.Contract_recv.client_id
            
            contract = readContract(i.Contract_recv.id,'recv')
            contract_info = contract['senderID']
            for d in contract_info:
                contract_dict['name'] = contract_info[d]
            contract_list.append(contract_dict)
    
    return contract_list


# get contract status from given contract id and table
# Parameters: cid, table
def getContractStatus(cid, table):
    if table == 'recv':
        status = Contract_recv.query.filter_by(id=cid).first().status
    if table == 'sent':
        status = Contract_sent.query.filter_by(id=cid).first().status
    return status


# get json-contract from given contract id and table
# Parameters: cid, table
def readContract(cid, table):
    if(table=='recv'):
        filepath = Contract_recv.query.filter_by(id=cid).first().path
        with open(filepath) as json_file:
            contract = json.load(json_file)
    else:
        filepath = Contract_sent.query.filter_by(id=cid).first().path
        with open(filepath) as json_file:
            contract = json.load(json_file)
    return contract
