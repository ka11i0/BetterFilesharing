import requests
from flask import Flask, render_template, redirect, request, url_for, session
from flaskapp import app
from flaskapp.shell.form import *

@app.route("/view_shell", methods=['GET', 'POST'])
def view_shell():
    return "bobo"

@app.route("/create_send_shell", methods=['GET', 'POST'])
def create_send_shell():
    #initialize forms
    step = "select_client"
    form = create_shellForm()
    form.receiver.choices = form.getClientlist()
    form.conditions.choices = form.getConditions()

    condForm=conditionsForm()


    if (request.method == "POST"):
        #if a new condition is added save it to the db
        if condForm.validate_on_submit():
            condForm.save(
                name = condForm.condition.data,
                desc = condForm.desc.data
            )
        #step where user selects client from drop-down menu.
        getClient = request.args.get('client_id') if request.args.get('client_id') else form.receiver.data
        if (request.args.get('step') == 'select_pattern'):
            form.receiver.choices = [(
            form.receiver.data,
            Client.query.filter(Client.id==getClient).first().name
            )]
            step = "select_pattern"
            form.conditions.choices = form.getConditions()
            return render_template('shell/create_send_shell.html', shellForm=form, conditionForm=condForm, selectStep=step, client_id=getClient)

        #step where user sends shell, and is then saved to db
        if (request.args.get('step') == 'save_shell'):
            form.save(
                receiver = getClient,
                pattern = form.pattern.data,
                conditions = form.conditions.data
            )

    return render_template('shell/create_send_shell.html', shellForm=form, conditionForm=condForm, selectStep=step)

@app.route("/receive_shell", methods=['GET', 'POST'])
def receive_shell():
    return "hihi :)"