from flaskapp.shell.config import *
from sqlalchemy import update

# Fetches the already selected conditions for thiss shell id
def getSetConditionsSend(shell_id):
    shell_file = readShellSent(shell_id)
    set_conditions = shell_file['conditions']
    return set_conditions   

def getSetConditionsReceive(shell_id):
    shell_file = readShellReceive(shell_id)
    set_conditions = shell_file['properties']['conditions']['properties'].keys()
    return set_conditions

# Opens a json file depending on if it is sent or received
def readShellSent(shell_id):
    filepath = Shell_send.query.filter_by(shell_id=shell_id).first().path
    with open(filepath) as json_file:
        shell_file = json.load(json_file)
    return shell_file

def readShellReceive(shell_id):
    filepath = Shell_recv.query.filter_by(shell_id=shell_id).first().path
    with open(filepath) as json_file:
        shell_file = json.load(json_file)
    return shell_file


# Makes a list containing [(cond_id, cond_name), True/False, cond_desc]
def checkSetConditionsSend(selected, all_cond):
    cond_list = []
    for c in all_cond:
        cond_tuple = ()
        desc = Conditions.query.filter_by(name=c[1]).first().desc
        if (c[1] in selected.keys()):
            cond_tuple = (c, True, desc)
        else:
            cond_tuple = (c, False, desc)
        cond_list.append(cond_tuple)
    return cond_list

def checkSetConditionsReceive(selected, all_cond):
    cond_list = []
    i = 1
    for c in all_cond.keys():
        cond_tuple = ()
        value_tuple = (i, c)
        desc = all_cond[c]
        if (c in selected):
            cond_tuple = (value_tuple, True, desc)
        else:
            cond_tuple = (value_tuple, False, desc)
        cond_list.append(cond_tuple)
        i = i + 1
    return cond_list


#Updates the files with the newly selected conditions.
def updateFileConditionsSent(shell_id, selected_conditions):
    cond_dict = {}
    for c in selected_conditions:
        desc = Conditions.query.filter_by(name=c).first().desc
        cond_dict[c] = desc

    shell_file = readShellSent(shell_id)
    shell_file['conditions'] = cond_dict
    filepath = Shell_send.query.filter_by(shell_id=shell_id).first().path
    with open(filepath, 'w') as outfile:
        json.dump(shell_file, outfile, indent=4)

def updateFileConditionsReceive(shell_id, selected_conditions, all_cond):
    cond_dict = {}
    for c in selected_conditions:
        desc = all_cond[c]
        cond_dict[c] = desc

    shell_file = readShellReceive(shell_id)
    shell_file['properties']['conditions']['enum'] = [cond_dict]
    filepath = Shell_recv.query.filter_by(shell_id=shell_id).first().path
    with open(filepath, 'w') as outschema:
        json.dump(shell_file, outschema, indent=4)

def getClient(shell_id):
    return Shell_recv.query.filter_by(shell_id=shell_id).first().client_id

def getStatus(shell_id, table):
    if (table == 'recv'):
       status = Shell_recv.query.filter_by(shell_id=shell_id).first().status
    elif (table == 'sent'):
        status = Shell_send.query.filter_by(shell_id=shell_id).first().status
    return status

def getPattern(shell_id, table):
    if (table == 'recv'):
       pattern = Shell_recv.query.filter_by(shell_id=shell_id).first().pattern
    elif (table == 'sent'):
        pattern = Shell_send.query.filter_by(shell_id=shell_id).first().pattern
    return pattern

def updateStatus(shell_id, status, table):
    db.session.autocommit = False
    if (status == 'active'):
        status = 'inactive'
    else:
        status = 'active'
    
    if table == 'sent':
        try:
            db.session.query(Shell_send).filter_by(shell_id=shell_id).\
                update({
                    Shell_send.status: status,
                },synchronize_session=False)
            db.session.commit()
        except:
            raise
        finally:
            db.session.close

    else:
        try:
            db.session.query(Shell_recv).filter_by(shell_id=shell_id).\
                update({
                    Shell_recv.status: status,
                },synchronize_session=False)
            db.session.commit()
        except:
            raise
        finally:
            db.session.close

def removeShell(shell_id, table):
    if table == 'recv':
        Shell_recv.query.filter_by(shell_id=shell_id).delete()
    else:
        Shell_send.query.filter_by(shell_id=shell_id).delete()

    db.session.commit()
        