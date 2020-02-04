from flaskapp.contract.config import *

def listContracts(status):
    contracts = db.session.query(Contract_sent, Client).join(Contract_sent).filter(Contract_sent.status == status).all()
    return contracts

def getContract(cid):
    contract = db.session.query(Contract)

def readContract(cid):
    filepath = Contract_sent.query.filter_by(id=cid).first().path
    with open(filepath) as json_file:
        contract = json.load(json_file)
        return contract

def getConditions(cond):
    conditionlist = []
    for i in cond:
        conditionlist.append(Conditions.query.filter_by(id=i).first().name)
    return conditionlist
