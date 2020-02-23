from flaskapp.shell.config import *
# from Contract.Rest.get_conditions import get_conditions

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(html_tag='ul', prefix_label=False)
    option_widget = CheckboxInput()

class CreateRecvShell(FlaskForm):
    # defining input fields
    sender = SelectField('Sender', validators=[DataRequired()])                              # list of senders from initiated shells
    pattern = SelectField('Pattern', choices=[], validators=[DataRequired()])                # file pattern for this shell
    conditions = MultiCheckboxField('Conditions', choices=[], validators=[DataRequired])     # condition from senders db (implemented later)

    def __init__(self, *args, **kwargs):
        super(CreateRecvShell, self).__init__(*args, **kwargs)
        # populate sender with client id and name if exists in Shell_recv table with status "inactive"
        senders = db.session.query(Client).outerjoin(Shell_recv).filter_by(status='inactive').all()
        self.sender.choices = [(sc.id, sc.name) for sc in senders]
        
        # populate pattern with patterns from selected sender
        shells = db.session.query(Shell_recv).filter_by(client_id=senders[0].id).all()
        for shell in shells:
            shell_path = os.path.join(app.config['SHELL_FOLDER'], shell.path)
            with open(shell_path) as json_file:
                json_shell = json.load(json_file)   # read json-shell

            # append tuple (shell_id, pattern) to pattern choices
            self.pattern.choices.append((shell.shell_id, json_shell.get('pattern')))