import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # . . .
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Company id-number (Swedish "organisationsnummer")
    COMPANY_ID = "32052"
    COMPANY_NAME = "Anton"

    # CONTRACT configurations
    CONTRACT_FOLDER = "Contract/SentContracts/"
    CONTRACT_FILEEXT = ".json"

    CONTRACT_CONDITIONS = [()]

    # Shared files folder

    SHARED_FILES = "Filesharing/SharedFiles/"

