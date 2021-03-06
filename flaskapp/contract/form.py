from flaskapp.contract.config import *
from Contract.Rest.send_contract import *
import uuid

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(html_tag='ul', prefix_label=False)
    option_widget = CheckboxInput()


class create_contractForm(FlaskForm):
    # defining form fields
    receiver = SelectField('Company', validators=[DataRequired()])
    conditions = MultiCheckboxField('Conditions', validators=[DataRequired()])
    uploadfile = SelectField('Share file')
    pay = IntegerField('payment_amount')

    # get all Clients from db and return a list of tuple with client_id and client_name
    def getClientlist(self):
        clientlist = []
        for client in Client.query.all():
            clientlist.append((str(client.id), client.name+", Org.nr.: "+str(client.id)))
        return clientlist

    # get all Conditions from db and return a list of tuples with condition_id and condition name
    def getConditions(self):
        conditions = []
        for condition in Conditions.query.all():
            conditions.append((str(condition.id), condition.name))
        return conditions
    
    # get all Files avalable to specific client and return a list of tuples with file_id and file_path
    # Parameters: client_id
    def getFileList(self, client_id):
        fileList = []
        for files in db.session.query(File, Access).join(Access).filter(File.id==Access.file_id).filter(Access.client_id==client_id).all():
            fileList.append((files.File.id, files.File.path))
        return fileList

    # save contract data to db and to json-object and upload shared file to shared folder
    # Parameters: receiver, conditions, payment
    def save(self, **kwargs):
        new_contractID = uuid.uuid1().int>>65       # random generated UUID as contract id
        clientID = kwargs.get('receiver')           # contract receiver id
        condData = kwargs.get('conditions')         # contract conditions
        payment = kwargs.get('payment')             # contract payment amount
        cond_dict = {}                              # dict of KV pair of contract conditions as keys and conditions descriptions as value

        # insert contract conditions and descriptions to cond_dict
        for i in condData:
            cond_name = Conditions.query.filter_by(id=i).first().name
            if (cond_name == "Pay"):
                cond_desc = int(payment)
            else:
                cond_desc = Conditions.query.filter_by(id=i).first().desc
            cond_dict[cond_name] = cond_desc

        if "Pay" not in cond_dict.keys():
            cond_dict["Pay"] = 0

        # create new contract db input
        new_contract = Contract_sent(
            id = new_contractID,
            path = app.config['CONTRACT_FOLDER']+str(new_contractID)+app.config['CONTRACT_FILEEXT'],
            status = "pending",
            client_id = clientID,
            file_id = kwargs.get('file_id')
        )

        # create new json contract
        json_contract = {
            'contractID': str(new_contractID),
            'senderID': {'id' : app.config['COMPANY_ID'], 'name' : app.config['COMPANY_NAME']},
            'receiverID': str(clientID),
            'file': {
                'name': File.query.filter_by(id=kwargs.get('file_id')).first().path.split('/')[-1],
                'filter': 'n/a'
            },
            'conditions': cond_dict
        }

        # save contract to db and json-file and send the contract to receiver
        try:
            #save contract to db and json-file
            db.session.autocommit = False
            db.session.add(new_contract)
            with open(app.config['CONTRACT_FOLDER']+str(new_contractID)+app.config['CONTRACT_FILEEXT'], 'w') as outfile:
                json.dump(json_contract, outfile, indent=4)
                
            # send contract to receiver
            db.session.commit()

            send_contract(new_contractID, clientID)
            
        except:
            db.session.rollback()
            raise

        finally:
            db.session.close()


class conditionsForm(FlaskForm):
    condition = TextField('Name', validators=[DataRequired()])
    desc = TextAreaField('Desciption')

    # save condition to db
    # Parameters: name, desc
    def save(self, **kwargs):
        data = Conditions(
            name = kwargs.get('name'),
            desc = kwargs.get('desc')
        )
        db.session.add(data)
        db.session.commit()
        db.session.close()