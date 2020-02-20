from flaskapp.shell.config import *

@app.route("/view_shell", methods=['GET', 'POST'])
def view_shell():
    return "bobo"

@app.route("/send_shell", methods=['GET', 'POST'])
def send_shell():
    return "suger"

@app.route("/receive_shell", methods=['GET', 'POST'])
def receive_shell():
    # createform
    recvShellForm = CreateRecvShell()

    # create shell
    if request.method=="POST":
        print(recvShellForm.sender.data)
        print(recvShellForm.pattern.data)
        return redirect(url_for('receive_shell'))

    return render_template('shell/create_recv_shell.html', form=recvShellForm)

# update pattern select field by selected sender
@app.route("/receive_shell/<sender>")
def update_recv_shell(sender):
    # conditions = get_conditions(sender) # activate when functions is available
    patterns = Shell_recv.query.filter_by(client_id=sender).all()
    patternArray = []   # list of dicts

    # create objects of pattern and append to list of dicts
    for pat in patterns:
        patObj = {}
        patObj['shell_id'] = pat.shell_id
        patObj['path'] = pat.path
        patternArray.append(patObj)
    
    return jsonify({'patterns' : patternArray})
    # return jsonify({'patterns' : patternArray, 'conditions' : conditions})  # use when get_conditions() is available