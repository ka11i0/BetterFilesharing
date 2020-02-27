from flaskapp.shell.config import *

def getSetConditionsSend(shell_id):
    shell_file = readShell(shell_id)
    set_conditions = shell_file['conditions']
    return set_conditions    

def readShell(shell_id):
    filepath = Shell_send.query.filter_by(shell_id=shell_id).first().path
    with open(filepath) as json_file:
        shell_file = json.load(json_file)
    return shell_file

def checkSetConditions(selected, all_cond):
    cond_list = []
    i = 0
    for c in all_cond:
        cond_tuple = ()
        desc = Conditions.query.filter_by(name=c[1]).first().desc
        if (c[1] in selected.keys()):
            cond_tuple = (c, True, desc)
        else:
            cond_tuple = (c, False, desc)
        cond_list.append(cond_tuple)
    return cond_list

def updateFileConditions(shell_id, selected_conditions):
    cond_dict = {}
    for c in selected_conditions:
        desc = Conditions.query.filter_by(name=c).first().desc
        cond_dict[c] = desc

    shell_file = readShell(shell_id)
    shell_file['conditions'] = cond_dict
    filepath = Shell_send.query.filter_by(shell_id=shell_id).first().path
    with open(filepath, 'w') as outfile:
        json.dump(shell_file, outfile, indent=4)