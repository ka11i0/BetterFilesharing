import requests
from flask import Flask, render_template, redirect, request, url_for, session
from flaskapp import app
from flaskapp.contract.form import *
from flaskapp.contract.view import *
from flaskapp.clients.form import *
from flaskapp.clients.view import *
import threading
from Filesharing.sender import FileSender
from Filesharing.receiver import FileReceiver
import json

@app.route("/")
def index():
    session['user'] = app.config['COMPANY_NAME']
    return redirect(url_for('sent_contracts'))

@app.route("/sent_contracts")
def sent_contracts():
    return render_template(
        'overview_contracts.html',
        pendingContracts = listContracts('pending', 'sent'),
        acceptedContracts = listContracts('accepted','sent'),
        declinedContracts = listContracts('declined', 'sent')
    )

@app.route("/recv_contracts")
def recv_contracts():
    return render_template(
        'overview_contracts.html',
        pendingContracts = listContracts('pending', 'received'),
        acceptedContracts = listContracts('accepted', 'received'),
        declinedContracts = listContracts('declined', 'received')
    )

@app.route("/create_contract", methods=['GET', 'POST'])
def create_contract():
    # initiate form objects
    form = create_contractForm()
    condForm = conditionsForm()
    form.conditions.choices = form.getConditions()
    form.receiver.choices = form.getClientlist()

    # save contract data to database and and json-file
    if request.method == 'POST':
        if request.args.get('step') == 'select_file':
            form.uploadfile.choices = form.getFileList(form.receiver.data)
            form.receiver.choices = [(
                form.receiver.data,
                Client.query.filter(Client.id==form.receiver.data).first().name
                )]
            return render_template(
                'create_contract.html',
                contractForm = form,
                step = 'select_file',
                conditionForm=condForm
                )
        else:
            form.save(
                receiver = form.receiver.data,
                file_id = form.uploadfile.data,
                conditions = form.conditions.data
            )
    
    # save new condotion
    if condForm.validate_on_submit():
        condForm.save(
            name = condForm.condition.data,
            desc = condForm.desc.data
        )
        return redirect(url_for('create_contract'))

    return render_template('create_contract.html', contractForm=form)

@app.route("/view_contract")
def view_contract():
    contract = readContract(request.args.get('cid'), request.args.get('from'))
    return render_template(
        'view_contract.html',
        contract = contract,
        conditions = contract['conditions']
        )
        

@app.route('/reply/<int:id>/<string:status>')
def accept_or_decline(id, status): # When contract is accepted/declined
    contract = Contract_recv.query.get(id)
    sender = Client.query.get(contract.client_id)

    data = "{{ \"contract_id\":\"{0}\", \"status\": \"{1}\"}}".format(id, status)
    try:
        requests.put("http://" + sender.ip_address + ":5000/contract_clientreply", data=data)
    except(ConnectionError):
        print("ConnectionError")
        return redirect('/contracts')

    contract.status = status # Update app.db
    db.session.commit()
    
    with open(contract.path, 'r') as contractfile:
        contractjson = json.loads(contractfile.read())
        filename = contractjson["file"]["name"]
    
    recv = Filereceiver("0.0.0.0", 80)
    recvThread = threading.Thread(target=recv.start(), args=(os.path.abspath("ReceivedFiles") + filename,))
    recvThread.start()
    
    return redirect('/contracts')


@app.route("/contract_clientreply", methods=["PUT"])
def contractreply(): # Runs when client accepts/declines a contract
    client_reply = request.get_json(force=True)
    contract = Contract_sent.query.get(client_reply["contract_id"])
    contract.status = client_reply["status"]
    db.session.commit()
    
    if client_reply["status"] == "accepted":
        client = Client.query.get(contract.client_id)
        send = Filesender(client.ip_address, 80)
        filedb = File.query.get(contract.file_id)
        sendThread = threading.Thread(target=send.start(), args=(filedb.path,))
        sendThread.start()
    
    return '', 201
