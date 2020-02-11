from flaskapp.contract.config import *
from Contract.Rest import send_contract

class fileForm():
    def getClientlist():
        clientlist = []
        for client in Client.query.all():
            clientlist.append((str(client.id), client.name+", Org.nr.: "+str(client.id)))
        return clientlist

    def getFilelist():
        filelist = []
        for f in File.query.all():
            filelist.append((str(f.id), f.path))
        return filelist


class addFileForm(FlaskForm):
    # defining form fields
    access_by = SelectField('Access by:', validators=[DataRequired()])
    uploadfile = FileField('Upload file:', validators=[DataRequired()])

    # save file-info to db and upload shared file to shared folder
    def save(self, **kwargs):
        # get next file-id, if not found, set to one
        new_fileID = File.query.order_by(File.id.desc()).first()
        if new_fileID is None:
            new_fileID = 1
        else:
            new_fileID = new_fileID.id + 1

        # get file from Form-data
        sendFile = kwargs.get('file')
        filename = secure_filename(sendFile.filename)

        # db-posts
        new_fileinfo = File(
            id = new_fileID,
            path = app.config['SHARED_FILES']+"{}".format(filename)
        )

        new_access = Access(
            file_id = new_fileID,
            client_id = kwargs.get('client_id')
        )

        try:
            # save file-info to Files-table
            db.session.autocommit = False
            db.session.add(new_fileinfo)
            db.session.add(new_access)
            db.session.commit()

            # upload file to shared file folder
            sendFile.save(os.path.join(
                app.config['SHARED_FILES'], filename
            ))

        except:
            db.session.rollback()
            raise

        finally:
            db.session.close()

class accessForm(FlaskForm):
    # define form fields
    access_by = SelectField('Access by:', validators=[DataRequired()])
    access_file = SelectField('File:', validators=[DataRequired()])

    def save(self, **kwargs):
        new_access = Access(
            file_id = kwargs.get('access_file'),
            client_id = kwargs.get('access_by')
        )

        try:
            # add new access
            db.session.autocommit = False
            db.session.add(new_access)
            db.session.commit()
        
        except:
            db.session.rollback()
            raise

        finally:
            db.session.close()