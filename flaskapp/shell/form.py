from flaskapp.contract.config import *
from Contract.Rest import send_contract

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(html_tag='ul', prefix_label=False)
    option_widget = CheckboxInput()

class create_shellForm(FlaskForm):
    # # defining form fields
    receiver = SelectField('Company')
    pattern = TextField('File Pattern')
    conditions = MultiCheckboxField('Conditions', validators=[DataRequired()])

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
        new_shellID = Shell_send.query.order_by(Shell_send.shell_id.desc()).first()
        if new_shellID is None:
            new_shellID = 1
        else:
            new_shellID = new_shellID.shell_id + 1

        clientID = kwargs.get('receiver')
        condData = kwargs.get('conditions')
        pattern = kwargs.get('pattern')

        cond_dict = {}

        for i in condData:
            cond_name = Conditions.query.filter_by(id=i).first().name
            cond_desc = Conditions.query.filter_by(id=i).first().desc
            cond_dict[cond_name] = cond_desc

        #saves shell to database
        new_shell = Shell_send(
            shell_id = new_shellID,
            path = app.config['SHELL_FOLDER']+str(new_shellID)+app.config['SHELL_FILEEXT'],
            status = "inactive",
            client_id = clientID,
            pattern = kwargs.get('pattern')
        )
        #saves shell as json file
        json_contract = {
            'shellID': str(new_shellID),
            'senderID': {'id' : app.config['COMPANY_ID'], 'name' : app.config['COMPANY_NAME']},
            'receiverID': str(clientID),
            'pattern': str(pattern),
            'conditions': cond_dict
        }

        try:
            db.session.autocommit = False
            db.session.add(new_shell)
            db.session.commit()
            with open(app.config['SHELL_FOLDER']+str(new_shellID)+app.config['SHELL_FILEEXT'], 'w') as outfile:
                json.dump(json_contract, outfile, indent=4)
            
            #send_contract(new_contractID, clientID)
            
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