from Contract.contracthandler import getHandler
from Filesharing.sender import FileSender
import json

def startserver():
    contracthandler = getHandler()
    
    while True:
        print("No new contracts")
        while contracthandler.getnumberofcontracts() < 1:
            pass
        
        print("A new Contract have arrived")
        input("Press enter to view contract")
        
        contract = contracthandler.popcontract(-1)
        
        print(json.dumps(contract))
        
        answer = input("Do you accept these conditions: ")
        if answer == "no":
            continue
        
        fs = FileSender(contract['host'], contract['port'])
        fs.sendfile(contract['filename'])
        print("done")
