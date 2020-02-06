from flask import Flask, render_template, redirect, request
from flaskapp import app
from flaskapp.contract.contract_form import create_contractForm

@app.route("/create_contract", methods=['GET', 'POST'])
def create_contract():
    con_form = create_contractForm()
    
    return render_template('create_contract.html', con_form=con_form)

@app.route("/view_contract")
def view_contract():
    cid= 1
    send_id = "123123"
    receive_id = "222222"
    filename = "File1"
    cond = "Open when naked only."
    return render_template('view_contract.html', cid=cid, send_id=send_id, receive_id=receive_id, filename=filename, cond=cond)
