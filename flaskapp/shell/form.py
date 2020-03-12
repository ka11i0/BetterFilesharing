from flaskapp.shell.config import *
from Contract.Rest.get_conditions import get_conditions
from flaskapp.shell.edit import *

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(html_tag='ul', prefix_label=False)
    option_widget = CheckboxInput()


class CreateRecvShell(FlaskForm):
    # defining input fields
    sender = SelectField('Sender', validators=[DataRequired()]) # list of senders from initiated shells
    pattern = TextField('Pattern', validators=[DataRequired()]) # filename pattern            
    payment_amount = IntegerField('Pay')                        # maximum pay amount for pay condition

    def __init__(self, *args, **kwargs):
        super(CreateRecvShell, self).__init__(*args, **kwargs)
        
        # populate sender with client id and name from client table
        senders = Client.query.all()
        self.sender.choices = [(sc.id, sc.name+' Org.nr.: {}'.format(sc.id)) for sc in senders]

        # get conditions from current client id
        self.conditions_list = checkSetConditionsReceive({}, get_conditions(senders[0].id), {'maximum': '0'}) if senders else []


    # save the shell to db and create a json-schema linked to the shell
    def save(self, **kwargs):
        client_id_data = kwargs.get('client_id')
        pattern_data = kwargs.get('pattern')
        conditions_data = kwargs.get('conditions')
        pay_amount = int(kwargs.get('pay_amount'))

        # get the latest shell id if exists, else set to 1
        new_shell_id = Shell_recv.query.order_by(Shell_recv.shell_id.desc()).first().shell_id + 1 if Shell_recv.query.order_by(Shell_recv.shell_id.desc()).first() else 1

        # shell save path
        shell_path = os.path.join(app.config['SHELL_RECEIVED_FOLDER'], str(new_shell_id)+".schema.json")

        # create new shell
        new_shell = Shell_recv(
            shell_id = new_shell_id,
            client_id = client_id_data,
            pattern = pattern_data,
            path = shell_path,
            status = 'active'
        )

        # open json-schema-template
        with open(os.path.join('Shell', 'shell.schema.json')) as json_schema:
            schema_template = json.load(json_schema)

        # container for all condtion keys
        conditionDict = {}

        # always insert maximum pay amount in Pay condition, default value is 0
        conditionDict['Pay'] = {"type": "integer", "maximum": pay_amount}
        
        # insert condition keys to conditionDict
        for key in conditions_data:
            if key.lower() == 'pay':
                continue
            else:
                conditionDict[key] = {"type": "string"}

        # insert data to json-schema
        schema_template['title'] = 'Shell#{}'.format(new_shell_id)
        schema_template['properties']['senderID']['properties']['id']['pattern'] = '^{}$'.format(client_id_data)
        schema_template['properties']['file']['properties']['name']['pattern'] = pattern_data
        schema_template['properties']['conditions']['properties'] = conditionDict
        schema_template['properties']['conditions']['required'] = ["Pay"]

        # save to db and create new json-schema, rollback if fails
        try:
            db.session.autocommit = False
            db.session.add(new_shell)
            db.session.commit()

            with open(shell_path, 'w') as new_shell_schema:
                json.dump(schema_template, new_shell_schema, indent=4)

        except:
            db.session.rollback()
            raise

        finally:
            db.session.close()
    

class create_shellForm(FlaskForm):
    # defining form fields
    receiver = SelectField('Company', validators=[DataRequired()])
    pattern = TextField('File Pattern', validators=[DataRequired()])
    conditions = MultiCheckboxField('Conditions', validators=[DataRequired()])
    pay = IntegerField('payment_amount')

    def getClientlist(self):
        clientlist = []
        for client in Client.query.all():
            clientlist.append((str(client.id), client.name+", Org.nr.: "+str(client.id)))
        return clientlist

    def getConditions(self):
        conditions = []
        for condition in Conditions.query.all():
            conditions.append((str(condition.id), condition.name))
        return conditions

    # save contract to db and as json-object and upload shared file to shared folder
    def save(self, **kwargs):
        new_shellID = Shell_send.query.order_by(Shell_send.shell_id.desc()).first()
        if new_shellID is None:
            new_shellID = 1
        else:
            new_shellID = new_shellID.shell_id + 1

        clientID = kwargs.get('receiver')
        condData = kwargs.get('conditions')
        pattern = kwargs.get('pattern')
        payment = kwargs.get('payment')

        cond_dict = {}

        for i in condData:
            cond_name = Conditions.query.filter_by(id=i).first().name
            if (cond_name == "Pay"):
                cond_desc = int(payment)
            else:
                cond_desc = Conditions.query.filter_by(id=i).first().desc

            cond_dict[cond_name] = cond_desc
        
        if "Pay" not in cond_dict.keys():
            cond_dict["Pay"] = 0

        #saves shell to database
        new_shell = Shell_send(
            shell_id = new_shellID,
            path = app.config['SHELL_FOLDER']+str(new_shellID)+app.config['SHELL_FILEEXT'],
            status = "active",
            client_id = clientID,
            pattern = kwargs.get('pattern')
        )
        #saves shell as json file
        json_contract = {
            'shellID': str(new_shellID),
            'senderID': {'id' : app.config['COMPANY_ID'], 'name' : app.config['COMPANY_NAME']},
            'receiverID': str(clientID),
            'file': {'name':"", "filter":"n/a"},
            'pattern': str(pattern),
            'conditions': cond_dict
        }

        try:
            db.session.autocommit = False
            db.session.add(new_shell)
            db.session.commit()
            with open(app.config['SHELL_FOLDER']+str(new_shellID)+app.config['SHELL_FILEEXT'], 'w') as outfile:
                json.dump(json_contract, outfile, indent=4)
            
        except:
            db.session.rollback()
            raise

        finally:
            db.session.close()

class conditionsForm(FlaskForm):
    condition = TextField('Name', validators=[DataRequired()])
    desc = TextAreaField('Desciption')

    def save(self, **kwargs):
        data = Conditions(
            name = kwargs.get('name'),
            desc = kwargs.get('desc')
        )
        db.session.add(data)
        db.session.commit()
        db.session.close()
