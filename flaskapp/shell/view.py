from flaskapp.shell.config import *

def getShells(status, table):
    shellList = []
    if(table == "send"):
        fetchedShell = Shell_send.query.filter(Shell_send.status==status).all()
    if(table == "recv"):
        fetchedShell = Shell_recv.query.filter(Shell_recv.status==status).all()

    for s in fetchedShell:
        temp_dict = {}
        temp_dict['shell_id'] = s.shell_id
        temp_dict['client_id'] = s.client_id
        if(s.client_id):
            client = Client.query.filter_by(id=s.client_id).all()
            for c in client:
                temp_dict['name'] = c.name
        if(s.pattern):
            temp_dict['pattern'] = s.pattern
        temp_dict['status'] = s.status
        shellList.append(temp_dict)
    
    return shellList
