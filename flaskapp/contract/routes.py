from flaskapp.contract.config import *

##  INDEX PAGE - REDIRECTS TO SENT CONTRACTS OVERVIEW PAGE ##
@app.route("/")
def index():
    session['user'] = app.config['COMPANY_NAME']
    return redirect(url_for('sent_contracts'))


## OVERVIEW OF SENT CONTRACTS PAGE ##
@app.route("/sent_contracts")
def sent_contracts():
    return render_template(
        'contract/overview_contracts.html',
        pendingContracts = listContracts('pending', 'sent'),
        acceptedContracts = listContracts('accepted','sent'),
        declinedContracts = listContracts('declined', 'sent')
    )


## OVERVIEW OF RECEIVED CONTRACTS PAGE ##
@app.route("/recv_contracts")
def recv_contracts():
    return render_template(
        'contract/overview_contracts.html',
        pendingContracts = listContracts('pending', 'received'),
        acceptedContracts = listContracts('accepted', 'received'),
        declinedContracts = listContracts('declined', 'received')
    )


## CREATE CONTRACT PAGE ##
@app.route("/create_contract", methods=['GET', 'POST'])
def create_contract():
    form = create_contractForm()        # initiate create_contractForm()
    condForm = conditionsForm()         # initiate conditionsForm()

    # populate receiver and condition choices
    form.conditions.choices = form.getConditions()
    form.receiver.choices = form.getClientlist()

    # save contract data to database and and json-file
    if request.method == 'POST':

        # validate condition data on submit and call conditionsForm.save()
        if condForm.validate_on_submit():
            condForm.save(
                name = condForm.condition.data,
                desc = condForm.desc.data
            )

        getClient = request.args.get('client_id') if request.args.get('client_id') else form.receiver.data

        # step two in create contract
        if request.args.get('step') == 'select_file':
            # populate uploadfile choices with files available to selected receiver
            form.uploadfile.choices = form.getFileList(getClient)
            form.receiver.choices = [(
                form.receiver.data,
                Client.query.filter(Client.id==getClient).first().name
                )]

            # update choices when new condition has been added
            form.conditions.choices = form.getConditions()

            return render_template(
                'contract/create_contract.html',
                contractForm = form,
                step = 'select_file',
                conditionForm=condForm,
                client_id = getClient
                )

        else:
            # save contract with payment value = 0 if payment amount is None
            if (type(form.pay.data) != type(0)):
                form.save(
                    receiver=getClient,
                    file_id=form.uploadfile.data,
                    conditions=form.conditions.data,
                    payment=0
                )

            # save contract
            else:
                form.save(
                    receiver = getClient,
                    file_id = form.uploadfile.data,
                    conditions = form.conditions.data,
                    payment = form.pay.data
                )

    return render_template('contract/create_contract.html', contractForm=form)


## VIEW CONTRACT PAGE ##
@app.route("/view_contract")
def view_contract():
    contract = readContract(request.args.get('cid'), request.args.get('from'))
    return render_template(
        'contract/view_contract.html',
        contract = contract,
        conditions = contract['conditions'],
        table = request.args.get('from'),
        status = getContractStatus(request.args.get('cid'), request.args.get('from'))
        )
        

## CONTRACT REPLY FUNCTION ON RECEIVER SIDE##
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
    
    recv = FileReceiver("0.0.0.0", 80)
    recvThread = threading.Thread(target=recv.start, args=(os.path.join(os.path.abspath("Filesharing/ReceivedFiles"), filename), ))
    recvThread.start()
    
    return redirect('/recv_contracts')


## CONTRACT REPLY FUNCTION ON SENDER SIDE ##
@app.route("/contract_clientreply", methods=["PUT"])
def contractreply(): # Runs when client accepts/declines a contract
    client_reply = request.get_json(force=True)
    contract = Contract_sent.query.get(client_reply["contract_id"])
    contract.status = client_reply["status"]
    
    if client_reply["status"] == "accepted":
        with open(contract.path) as json_file: # For debt
            cont_json = json.load(json_file)
        client = Client.query.get(contract.client_id)
        try:
            client.debt += int(cont_json['conditions']['Pay']) # Add cost to debt
        except(KeyError):
            print("KeyError")

        send = FileSender(client.ip_address, 80)
        filedb = File.query.get(contract.file_id)
        sendThread = threading.Thread(target=send.start, args=(filedb.path,))
        sendThread.start()

    db.session.commit()
    
    return '', 201
