from flask import Flask, render_template, redirect, request
from flaskapp import app, db
from flaskapp.contract.contract_form import create_contractForm
from flaskapp.models import Contract_recv, Contract_sent



@app.route("/create_contract", methods=['GET', 'POST'])
def create_contract():
    con_form = create_contractForm()
    
    return render_template('create_contract.html', con_form=con_form)

@app.route("/")
@app.route("/view_contract")
def view_contract():
    cid= 1
    send_id = "123123"
    receive_id = "222222"
    filename = "File1"
    cond = "Open when naked only."
    return render_template('view_contract.html', cid=cid, send_id=send_id, receive_id=receive_id, filename=filename, cond=cond)


@app.route('/accept/<int:id>')
def accept_contract(id):
    print("hej1")
   # contract = Contract_recv.query.get_or_404(id)
    return redirect('/view_contract')


@app.route('/decline/<int:id>')
def decline_contract(id):
    print(id)
   # contract = Contract_recv.query.get_or_404(id)
    return redirect('/view_contract')


@app.route("/contract_clientreply", methods=["PUT"])
def contractreply(): # Runs when client accepts/declines a contract
    client_reply = request.get_json(force=True)
    contract = Contract_sent.query.get(client_reply["contract_id"])
    contract.status = client_reply["status"]
    db.session.commit()
    return '', 201

