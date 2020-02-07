import requests
from flask import Flask, render_template, redirect, request, url_for, session
from flaskapp import app
from flaskapp.contract.form import *
from flaskapp.contract.view import *
from flaskapp.clients.form import *
from flaskapp.clients.view import *

@app.route("/")
def index():
    session['user'] = app.config['COMPANY_NAME']
    return redirect(url_for('sent_contracts'))

@app.route("/sent_contracts")
def sent_contracts():
    return render_template(
        'new_contracts.html',
        pendingContracts = listContracts('pending', 'sent'),
        acceptedContracts = listContracts('accepted','sent'),
        declinedContracts = listContracts('declined', 'sent')
    )

@app.route("/recv_contracts")
def recv_contracts():
    return render_template(
        'new_contracts.html',
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
    if form.validate_on_submit():
        form.save(
            receiver = form.receiver.data,
            file = form.uploadfile.data,
            conditions = form.conditions.data
        )

        return redirect(url_for('sent_contracts'))
    
    # save new condotion
    if condForm.validate_on_submit():
        condForm.save(
            name = condForm.condition.data,
            desc = condForm.desc.data
        )
        return redirect(url_for('create_contract'))

    return render_template('create_contract.html', contractForm=form, conditionForm=condForm)

@app.route("/view_contract")
def view_contract():
    contract = readContract(request.args.get('cid'))
    condition = getConditions(contract['conditions'])
    return render_template(
        'view_contract.html',
        contract = contract,
        conditions = condition
        )

@app.route("/clients")
def clients():
    return render_template(
        'view_clients.html',
        clientlist = getClientlist()
        )

@app.route("/add_client", methods=['GET', 'POST'])
def add_client():
    form = clientForm()
    
    if form.validate_on_submit():
        form.save(
            id = form.client_id.data,
            name = form.name.data,
            ip_address = form.ip_address.data
        )
        return redirect(url_for('clients'))

    return render_template('add_client.html', form=form)

@app.route("/edit_client", methods=['GET','POST'])
def edit_client():
    form = clientForm()
    client = getClient(request.args.get('id'))

    if form.validate_on_submit():
        form.update(
            curr_id = request.args.get('id'),
            new_id = form.client_id.data,
            name = form.name.data,
            ip_address = form.ip_address.data
        )
        return redirect(url_for('clients'))

    return render_template('add_client.html', form=form, client=client)


@app.route('/reply/<int:id>/<string:status>')
def accept_or_decline(id, status): # When contract is accepted/declined
    print(id)
    print(status)
    contract = Contract_recv.query.get(id)
    sender = Client.query.get(contract.client_id)

    print(sender.ip_address)

    data = "{{ \"contract_id\":\"{0}\", \"status\": \"{1}\"}}".format(id, status)
    try:
        requests.put("http://" + sender.ip_address + ":5000/contract_clientreply", data=data)
    except(ConnectionError):
        print("ConnectionError")
        return redirect('/contracts')

    contract.status = status # Update app.db
    db.session.commit()

    return redirect('/contracts')


@app.route("/contract_clientreply", methods=["PUT"])
def contractreply(): # Runs when client accepts/declines a contract
    client_reply = request.get_json(force=True)
    contract = Contract_sent.query.get(client_reply["contract_id"])
    contract.status = client_reply["status"]
    db.session.commit()
    return '', 201

