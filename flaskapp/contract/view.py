from flaskapp.contract.config import *

def listContracts(status, table):
    if (table=="sent"):
        contracts = db.session.query(Contract_sent, Client).join(Contract_sent).filter(Contract_sent.status == status).all()
        return contracts
    if (table=="received"):
        contracts = db.session.query(Contract_recv, Client).join(Contract_recv).filter(Contract_recv.status == status).all()
        contract_list = []
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

def getContract(cid):
    contract = db.session.query(Contract)

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

# def getConditions(cond):
#     conditionlist = []
#     for i in cond:
#         conditionlist.append(Conditions.query.filter_by(id=i).first().name)
#     return conditionlist
