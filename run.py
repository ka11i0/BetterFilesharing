from flaskapp import app
from Filehandlermodule.filecheckerthread import checkfiles
import threading
# General info:
# You want to know how to run this? "python run.py" is to be written in the terminal.

# To be able to make necessary changes to the database "set FLASK_APP=run.py"(windows command).
#   This is needed for flask commands to know where the application lives.

# If you made changes to the schema and want to keep database data:
# "flask db migrate" creates a migration-script and identifies changes made
# "flask db upgrade" commits those changes to app.db
# "flask db downgrade" undoes the last migration
# install modules: pip install -r requirements.txt


if __name__ == "__main__":
    checkthread = threading.Thread(target=checkfiles, args=())
    checkthread.daemon = True #CTRL + C now terminates this thread aswell, if removed CTRL + C will only terminate main
    checkthread.start()
    app.run(debug=True, host="0.0.0.0")
