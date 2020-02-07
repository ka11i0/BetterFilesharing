from flaskapp.contract.config import *

class clientForm(FlaskForm):
    client_id = TextField('Organisation number:', validators=[DataRequired()])
    name = TextField('Company name:', validators=[DataRequired()])
    ip_address = TextField('IP-address:', validators=[DataRequired()])

    def save(self, **kwargs):
        newclient = Client(
            id = kwargs.get('id'),
            name = kwargs.get('name'),
            ip_address = kwargs.get('ip_address')
        )

        db.session.add(newclient)
        db.session.commit()
        db.session.close()
    
    def update(self, **kwargs):
        db.session.autocommit = False
        try:
            db.session.query(Client).filter_by(id=kwargs.get('curr_id')).\
                update({
                    Client.id: kwargs.get('new_id'),
                    Client.name: kwargs.get('name'),
                    Client.ip_address: kwargs.get('ip_address')
                },synchronize_session=False)
            db.session.commit()
        except:
            raise
        finally:
            db.session.close
