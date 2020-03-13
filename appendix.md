#Appendix
This appendix contains a short summary/explanation for all the modules in the program, for further development.

### The modules are identified by their folders:
    Contract
    Filehandlermodule
    Filesharing
    flaskapp
    Shell
    migration (folder created by sqlalchemy, should not be modified)

## Contract module
ReceivedContracts and SentContracts folders contains sent/received 
json contracts.

#### In the Rest folder we find:
- condition.py   (used for sending requested conditions from client)
- contract.py    (checks incoming contracts with existing shell)
- get_conditions.py (used to fetch conditions from another client)
- send_contract.py (for sending contracts to client)


## Filehandlermodule
In the folder "filehandlermodules" we find code for read/write different types of files.

#### We also find other files:
- filecheckerthread.py (checks SharedFiles folder for new files, and compare those with all Shell contracts
,then automatically creates a contracts which is sent to the matching client in a Shell contract.)

- filehandler.py (uses filehandlermodules to read a certain type of file.)


## Filesharing module
ReceivedFiles and SharedFiles folders contains sent/received files.

We also find:
- receiver.py (opens socket to receive file)
- sender.py   (opens socket to send file)


## flaskapp module
In the submodule folders for, clients, contract, files, shell, you will find:
- config.py (contains all the relevant imports for that module)
- form.py   (contains code for creating, saving and editing client/contract/files, etc.)
- routes.py (this is where all the gui functionality is linked)
- view.py   (code for reading from the database for html listing, etc.)

In the shell folder you will also find edit.py which is essentially an extension to view.py and form.py.

In the "static" folder you will find all the CSS code.
In the "templates" folder you will find all the HTML code.

##### Other files
+ app.db is the database file.
+ config.sample.py is to be copied, edited and renamed to config.py, to set company name/id.
+ models.py is a config file for all the tables and their attributes.


##Shell module
Contains the shell json schema.