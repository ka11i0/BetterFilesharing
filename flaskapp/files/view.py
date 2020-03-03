from flaskapp.files.config import *

class file_view():

    # getAllFiles() returns list file id and path from File-table
    def getAllFiles():
        return File.query.order_by(File.id).all()

    # getFileAccess(fid) takes file-id as parameter and returns list of all Client with access to the file
    def getFileAccess(fid):
        return db.session.query(Access, Client).join(Access).filter(Access.client_id==Client.id).filter(Access.file_id==fid).all()