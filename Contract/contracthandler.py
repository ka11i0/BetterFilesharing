class ContractHandler:
    def __init__(self):
        self.contractqueue = []
    
    def popcontract(self, index):
        if not self.contractqueue:
            raise ContractQueueEmpty("The contract queue is empty")
        if (index >= len(self.contractqueue)):
            raise IndexError()
        return self.contractqueue.pop(index)
    
    def addcontract(self, contract):
        self.contractqueue.append(contract)
        print(self.contractqueue)
    
    def getallcontracts(self):
        return self.contractqueue[:]
    
    def getnumberofcontracts(self):
        return len(self.contractqueue)

contracthandler = ContractHandler()
def getHandler():
    return contracthandler

class ContractQueueEmpty(Exception):
    pass
