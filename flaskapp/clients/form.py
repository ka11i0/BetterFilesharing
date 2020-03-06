from flaskapp.clients.config import *

class clientForm(FlaskForm):
    # create form fields
    client_id = TextField('Organisation number:', validators=[DataRequired()])
    name = TextField('Company name:', validators=[DataRequired()])
    ip_address = TextField('IP-address:', validators=[DataRequired()])
    max_debt = StringField('Maximum debt:', validators=[DataRequired()])
    rsa_n = StringField('Rsa n key:', validators=[DataRequired()])
    rsa_e = StringField('Rsa e key:', validators=[DataRequired()])

    # save form data to Client table in db
    # parameters: client_id, name, ip_address, max_debt, rsa_n, rsa_e
    def save(self, **kwargs):
        newclient = Client(
            id = kwargs.get('client_id'),
            name = kwargs.get('name'),
            ip_address = kwargs.get('ip_address'),
            debt = 0,
            max_debt = kwargs.get('max_debt'),
            rsa_n = kwargs.get('rsa_n'),
            rsa_e=kwargs.get('rsa_e')
        )

        db.session.add(newclient)
        db.session.commit()
        db.session.close()
    
    # update form data to Client table in db
    # parameters: client_id, name, ip_address, max_debt, rsa_n, rsa_e
    def update(self, **kwargs):
        db.session.autocommit = False
        try:
            db.session.query(Client).filter_by(id=kwargs.get('client_id')).\
                update({
                    Client.id: kwargs.get('client_id'),
                    Client.name: kwargs.get('name'),
                    Client.ip_address: kwargs.get('ip_address'),
                    Client.max_debt: kwargs.get('max_debt'),
                    Client.rsa_n: kwargs.get('rsa_n'),
                    Client.rsa_e: kwargs.get('rsa_e')
                },synchronize_session=False)
            db.session.commit()
        except:
            raise
        finally:
            db.session.close
