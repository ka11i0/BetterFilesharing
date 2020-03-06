from flaskapp.clients.config import *

## CLIENT LIST PAGE ##
@app.route("/clients")
def clients():
    return render_template(
        'clients/view_clients.html',
        clientlist = getClientlist()
        )

## ADD CLIENT PAGE ##
@app.route("/add_client", methods=['GET', 'POST'])
def add_client():
    form = clientForm()     # initiate clientForm
    
    # validate form data on submit and call form save function in form.py
    if form.validate_on_submit():
        form.save(
            client_id = form.client_id.data,
            name = form.name.data,
            ip_address = form.ip_address.data,
            max_debt = form.max_debt.data,
            rsa_n = form.rsa_n.data,
            rsa_e=form.rsa_e.data
        )
        return redirect(url_for('clients'))

    return render_template('clients/add_client.html', form=form)


## EDIT CLIENT PAGE ##
@app.route("/edit_client", methods=['GET','POST'])
def edit_client():
    form = clientForm()                         # inititate clientForm
    client = getClient(request.args.get('id'))  # get Client data to show/edit

    # validate form data on submit and call form update function in form.py
    if form.validate_on_submit():
        form.update(
            client_id = form.client_id.data,
            name = form.name.data,
            ip_address = form.ip_address.data,
            max_debt = form.max_debt.data,
            rsa_n = form.rsa_n.data,
            rsa_e = form.rsa_e.data
        )
        return redirect(url_for('clients'))

    return render_template('clients/add_client.html', form=form, client=client)


## SEND INVOICE FUNCTION ##
@app.route("/send_invoice", methods=['GET'])
def send_invoice():
    client = getClient(request.args.get('id'))
    client.debt = 0
    db.session.commit()
    return redirect(url_for('clients'))