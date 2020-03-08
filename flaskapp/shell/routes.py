from flaskapp.shell.config import *
from Contract.Rest.get_conditions import get_conditions
from flask import Request

@app.route("/send_shell", methods=['GET', 'POST'])
def send_shell():
    #fetches data for all sent shells
    if request.args.get('shell_id'):
        removeShell(request.args.get('shell_id'), 'send')
    return render_template(
        'shell/overview_shell.html',
        active_shells = getShells("active", "send"),
        inactive_shells = getShells("inactive", "send")
    )

@app.route("/recv_shell", methods=['GET', 'POST'])
def recv_shell():
    if request.args.get('shell_id'):
        removeShell(request.args.get('shell_id'), 'recv')
    #fetches data for all received shells
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
                receiver=getClient,
                pattern=form.pattern.data,
                conditions=form.conditions.data,
                payment=form.pay.data
            )

    return render_template('shell/create_send_shell.html', shellForm=form, conditionForm=condForm, selectStep=step)

@app.route("/receive_shell", methods=['GET', 'POST'])
def receive_shell():
    # createform
    recvShellForm = CreateRecvShell()

    # create shell
    if request.method == "POST":
        client_id = recvShellForm.sender.data
        pattern = recvShellForm.pattern.data
        conditions = request.form.getlist('conditions')
        pay_amount = recvShellForm.payment_amount.data

        # save data to db and json-schema
        recvShellForm.save(client_id=client_id, pattern=pattern, conditions=conditions, pay_amount=pay_amount)
        
        return redirect(url_for('receive_shell'))

    return render_template('shell/create_recv_shell.html', form=recvShellForm)

# update pattern select-field by selected sender
@app.route("/receive_shell/<sender>")
def update_recv_shell(sender):
    conditionDict = get_conditions(sender) # activate when functions is available
    # conditionArray = [(key, conditionDict[key]) for key in conditionDict]
    conditionArray = checkSetConditionsReceive({}, get_conditions(sender))
    return jsonify({'conditions' : conditionArray})  # use when get_conditions() is available

@app.route("/edit_shell", methods=['GET', 'POST'])
def edit_shell():
    form = create_shellForm()
    pay_amount = 0

    shell_id = request.args.get('shell_id')
    #Updates conditions for the specified shell depending if it is a sent or received shell.
    if request.method == "POST":
        if request.args.get('update') == "cond" and request.args.get('table') == 'sent':
            selected_conditions = request.form.getlist('conditions')
            if "Pay" in selected_conditions:
                pay_amount = form.pay.data
            updateFileConditionsSent(shell_id, selected_conditions, pay_amount)
        
        elif request.args.get('update') == "cond" and  request.args.get('table') == 'recv':
            selected_conditions = request.form.getlist('conditions')
            if "Pay" in selected_conditions:
                pay_amount = form.pay.data
            client_id = getClient(shell_id)
            conditions = get_conditions(client_id)
            updateFileConditionsReceive(shell_id, selected_conditions, conditions, pay_amount)
        
        if request.args.get('status'):
            updateStatus(shell_id, request.args.get('status'), request.args.get('table'))


    #Fetches the shells already selected conditions and fetches all of the origins conditions and saves it into a list.
    if(request.args.get('table') == 'recv'):
        client_id = getClient(shell_id)
        conditions = get_conditions(client_id)
        curr_cond = getSetConditionsReceive(shell_id)
        pay_value = fetchPay(shell_id, 'recv')
        conditions_list = checkSetConditionsReceive(curr_cond, conditions,pay_value)
        status = getStatus(shell_id, 'recv')
        pattern = getPattern(shell_id, 'recv')
        
    elif(request.args.get('table')=='sent'):
        form.conditions.choices = form.getConditions()
        curr_cond = getSetConditionsSend(shell_id)
        pay_value = fetchPay(shell_id, 'sent')
        conditions_list = checkSetConditionsSend(curr_cond, form.conditions.choices, pay_value)
        status =  getStatus(shell_id, 'sent')
        pattern = getPattern(shell_id, 'sent')
        

    return render_template(
        'shell/edit_shell.html',
        conditions_list = conditions_list,
        shell_id = shell_id,
        table = request.args.get('table'),
        status = status,
        pattern = pattern,
        form = form
    )
