import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # . . .
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Company id-number (Swedish "organisationsnummer")
    COMPANY_ID = "890821"
    COMPANY_NAME = "BOBOS HEMMAFIX AB"

    # CONTRACT configurations
    CONTRACT_FOLDER = "Contract/SentContracts/"
    CONTRACT_FILEEXT = ".json"

    CONTRACT_CONDITIONS = [()]

    # SHELL configurations
    SHELL_RECEIVED_FOLDER = "Shell/ReceivedShells"
    SHELL_SENT_FOLDER = ""

    # Shared files folder

    SHARED_FILES = "Filesharing/SharedFiles/"

    # SHELL configurations
    SHELL_FOLDER = "Shell/SentShells/"
    SHELL_FILEEXT = ".json"
