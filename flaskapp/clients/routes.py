from flaskapp.clients.config import *

@app.route("/clients")
def clients():
    return render_template(
        'clients/view_clients.html',
        clientlist = getClientlist()
        )

@app.route("/add_client", methods=['GET', 'POST'])
def add_client():
    form = clientForm()
    
    if form.validate_on_submit():
        form.save(
            id = form.client_id.data,
            name = form.name.data,
            ip_address = form.ip_address.data,
            max_debt = form.max_debt.data,
            rsa_n = form.rsa_n.data,
            rsa_e=form.rsa_e.data
        )
        return redirect(url_for('clients'))

    return render_template('clients/add_client.html', form=form)

@app.route("/edit_client", methods=['GET','POST'])
def edit_client():
    form = clientForm()
    client = getClient(request.args.get('id'))

    if form.validate_on_submit():
        form.update(
            curr_id = request.args.get('id'),
            new_id = form.client_id.data,
            name = form.name.data,
            ip_address = form.ip_address.data,
            max_debt = form.max_debt.data,
            rsa_n = form.rsa_n.data,
            rsa_e = form.rsa_e.data
        )
        return redirect(url_for('clients'))

    return render_template('clients/add_client.html', form=form, client=client)