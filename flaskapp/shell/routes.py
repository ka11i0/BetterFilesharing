from flaskapp.shell.config import *

@app.route("/send_shell", methods=['GET', 'POST'])
def send_shell():
    return render_template(
        'shell/overview_shell.html',
        active_shells = getShells("active", "send"),
        inactive_shells = getShells("inactive", "send")
    )

@app.route("/recv_shell", methods=['GET', 'POST'])
def recv_shell():
    return render_template(
        'shell/overview_shell.html',
        active_shells = getShells("active", "recv"),
        inactive_shells = getShells("inactive", "recv")
    )

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
    # createform
    recvShellForm = CreateRecvShell()

    # create shell
    if request.method == "POST":
        print(recvShellForm.sender.data)
        print(recvShellForm.pattern.data)
        return redirect(url_for('receive_shell'))

    return render_template('shell/create_recv_shell.html', form=recvShellForm)

# update pattern select-field by selected sender
@app.route("/receive_shell/<sender>")
def update_recv_shell(sender):
    # conditions = get_conditions(sender) # activate when functions is available
    shells = Shell_recv.query.filter_by(client_id=sender).all()
    patternArray = []   # list of dicts

    # create objects of pattern and append to list of dicts
    for shell in shells:
        shell_path = os.path.join(app.config['SHELL_RECEIVED_FOLDER'], shell.path)
        with open(shell_path) as json_file:
            json_shell = json.load(json_file)   # read json-shell
        patObj = {}
        patObj['shell_id'] = shell.shell_id
        patObj['pattern'] = json_shell.get('pattern')
        patternArray.append(patObj)
    
    return jsonify({'patterns' : patternArray})
    # return jsonify({'patterns' : patternArray, 'conditions' : conditions})  # use when get_conditions() is available