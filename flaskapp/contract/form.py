from flaskapp.contract.config import *
from Contract.Rest.send_contract import *
import uuid


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(html_tag='ul', prefix_label=False)
    option_widget = CheckboxInput()

class create_contractForm(FlaskForm):
    # # defining form fields
    receiver = SelectField('Company')
    conditions = MultiCheckboxField('Conditions', validators=[DataRequired()])
    # uploadfile = FileField('Share file', validators=[DataRequired()])
    uploadfile = SelectField('Share file')


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
    
    def getFileList(self, client_id):
        fileList = []
        for files in db.session.query(File, Access).join(Access).filter(File.id==Access.file_id).filter(Access.client_id==client_id).all():
            fileList.append((files.File.id, files.File.path))
        return fileList

    # save contract to db and as json-object and upload shared file to shared folder
    def save(self, **kwargs):
        new_contractID = uuid.uuid1().int>>65

        clientID = kwargs.get('receiver')
        print(clientID)
        condData = kwargs.get('conditions')

        cond_dict = {}

        for i in condData:
            cond_name = Conditions.query.filter_by(id=i).first().name
            cond_desc = Conditions.query.filter_by(id=i).first().desc
            cond_dict[cond_name] = cond_desc


        new_contract = Contract_sent(
            id = new_contractID,
            path = app.config['CONTRACT_FOLDER']+str(new_contractID)+app.config['CONTRACT_FILEEXT'],
            status = "pending",
            client_id = clientID,
            file_id = kwargs.get('file_id')
        )

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

        try:
            db.session.autocommit = False
            db.session.add(new_contract)
            db.session.commit()
            with open(app.config['CONTRACT_FOLDER']+str(new_contractID)+app.config['CONTRACT_FILEEXT'], 'w') as outfile:
                json.dump(json_contract, outfile, indent=4)
            
            send_contract(new_contractID, clientID)
            
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

