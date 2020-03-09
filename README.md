# Better Filesharing
## Setup
Make sure you are using python 3.8 or later versions.
Install all the modules for the program with:
```
 pip install -r requirements.txt
```
To be able to make changes to the database (windows command):
```
 set FLASK_APP=run.py
```
Then set the database to its base state:
```
 python db_refresh.py
```
## Start
run the server with 
```
 python run.py
```
## Sending a contract
Firstly go to the flaskapp folder make a copy of
```
 config.sample.py
```
paste in the same folder and change the name to
```
 config.py
```
In the the newly made file change
```
 COMPANY_ID = ""
 COMPANY_NAME = ""
```
on row 14, 15 too whatever you would like.
In your browser go to either
```
 localhost:5000
 127.0.0.1:5000
```
Click Clients in the navbar then add a new client.
Get the company id, name, IP-address, rsa n key and rsa e 
key from the opposing party 
(Both parties in a contract exchange must have this setup).

If you click your company name in the right of the navbar,
 the rsa n and rsa e key will show. Otherwise the keys are stored in:
```
 BetterFilesharing/rsa_key.json
```
To send a contract tied to a file, add a file you want 
to send to the folder:
```
 BetterFilesharing/Filesharing/SharedFiles
```
Go to Files in the navbar and 'upload' the file 
(this step adds the filepath to the local database).
Let the reciver have access to the file.
Go to Contracts in the navbar, click Create contract, choose
reciver from the list of clients choose which file to share
and add under which conditions it will be shared.

When create contract is clicked a .json file will be made
 locally and sent to the reciver. This file is also hashed and 
 signed by the senders private key. The receiver the uses the 
 public key and validates the signature.
 
 The id of the contract is a UUID.
 
 Off note is that a filhandlermodule must have been made for the
 filetype that is to be sent. Otherwise python wont be able to 
 read the file and the program will chrash. 
 Se the appendix for how to add filehandlermodules.
 
 The contract is now shown for the sender on the Contracts page,
 under Sent contract and under Pending. And for the receiver 
 its located under the Contracts page, under received contracts 
 and under pending. 
 
 When the reciver views the received contract in pending there
  will be two buttons, accept and decline. 
  
  When decline is clicked the status in the local 
  database is changed to declined
  and an http put request with the decline status
  regarding the specific contract is sent to the sender.
  The contract can then be seen in the decline tab.
  
  When accept is clicked the local database changes the
  status to accepted and the same http put request is
  performed but with the accept status instead.
  The sender then sends the file, the contract touches on
  and places the file in
 ```
 BetterFilesharing/Filesharing/ReceivedFiles
```
The contract can then be seen in the accepted tab, in either
sent- or received-contract.

## Setting up a shell contract

The shell contract makes it so that contracts are automatically
setup for files that follow a specified pattern with their 
naming.
Firstly setup the client like in "Sending a contract".
Then go to Shell in the navbar and choose if you want to setup 
a shell for outgoing contracts or received contracts.
#### Outgoing files
Click create senders shell, choose the receiver, enter the
regex pattern for the filepattern you want to send.
 ```
 (AAA).*([.]log$) accepts filename "AAAwildcard.log" or
 "AAAwhatever.log"
```
Important detail is that here the shouldnt be a ^ in the 
beginning of the regex expression, but it should in the
reciver shell.

Then specify the conditions that will be tied to the files
that are to be sent with the specified naming pattern.

When the program is started an additional thread is created
with filecheckerthread.py, this thread scans the SharedFiles
folder for files not already added to the database. Whenever 
a file not already in the database is found its added and all 
the active sender shells are checked to see if the regex pattern
matches the filename. If there is a match a contract is 
generated from the conditions for the file and this contract 
is then sent to the specified receiver.

#### Incoming files

Go to Create receivers shell, choose from who the files 
are inbound, specify the type of files you want to accept
with a regex pattern and also under witch conditions they are
acceptable.The regex pattern should look something like this:
  ```
 ^(AAA).*([.]log$) accepts filename "AAAwildcard.log" or
 "AAAwhatever.log"
```
Now whenever the specified sender sends a contract 
it will be automatically accepted if it follows the shell contract
conditions. Otherwise it will be given the status pending.