from flaskapp.contract.config import *

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(html_tag='ul', prefix_label=False)
    option_widget = CheckboxInput()

class create_contractForm(FlaskForm):
    # defining form fields
    receiver = SelectField('Company')
    conditions = MultiCheckboxField('Conditions', validators=[DataRequired()])
    uploadfile = FileField('Share file', validators=[DataRequired()])

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
        new_contractID = Contract_sent.query.order_by(Contract_sent.id.desc()).first()
        new_fileID = File.query.order_by(File.id.desc()).first()

        if new_contractID is None:
            new_contractID = 1
        else:
            new_contractID = new_contractID.id + 1
        
        if new_fileID is None:
            new_fileID = 1
        else:
            new_fileID = new_fileID.id + 1

        sendFile = kwargs.get('file')
        filename = secure_filename(sendFile.filename)
        clientID = kwargs.get('receiver')
        condData = kwargs.get('conditions')
        
        new_contract = Contract_sent(
            id = new_contractID,
            path = app.config['CONTRACT_FOLDER']+str(new_contractID)+app.config['CONTRACT_FILEEXT'],
            status = "pending",
            client_id = clientID,
            file_id = new_fileID
        )

        new_fileinfo = File(
            id = new_fileID,
            path = app.config['SHARED_FILES']+"{}".format(kwargs.get('file'))
        )

        json_contract = {
            'contractID': new_contractID,
            'senderID': app.config['COMPANY_ID'],
            'receiverID': clientID,
            'file': {
                'name': filename,
                'filter': 'n/a'
            },
            'conditions': condData
        }

        try:
            db.session.autocommit = False
            db.session.add(new_contract)
            db.session.add(new_fileinfo)
            db.session.commit()
            with open(app.config['CONTRACT_FOLDER']+str(new_contractID)+app.config['CONTRACT_FILEEXT'], 'w') as outfile:
                json.dump(json_contract, outfile, indent=4)
            
            sendFile.save(os.path.join(
                'Filesharing/SharedFiles/', filename
            ))
            
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

