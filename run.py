from flaskapp import app

# General info:
# You want to know how to run this? "python runthis.py" is to be written in the terminal.

# To be able to make necessary changes to the database "set FLASK_APP=runthis.py"(windows command).
#   This is needed for flask commands to know where the application lives.

# "flask db migrate" creates a migration-script and identifies changes made
# "flask db upgrade" commits those changes to app.db
# "flask db downgrade" undoes the last migration

if __name__ == "__main__":
    app.run(debug=True)