import threading, os, glob, ntpath, json, uuid, time
from flaskapp import db, app
from flaskapp.models import File, Shell_send, Contract_sent
from Contract.Rest import send_contract
import sqlalchemy

BASE_PATH = app.config['SHARED_FILES']
CHECK_DELAY = 10 # Hur många sekunder mellan checks


def checkfiles():
    time.sleep(CHECK_DELAY)
    files = glob.iglob(os.path.join(BASE_PATH, "**", "*.*"), recursive=True) #hämtar alla paths på files
    newfiles = [] #innehåller alla filepaths som inte finns i databasen
    dbfiles = [r.path for r in File.query.all()] #hämtar alla paths i databasen
    for file in files:
        if file not in dbfiles: #kollar om filen inte finns i databasen
            newfiles.append(file)
    for file in newfiles: #går igenom alla nya filer
        #hämtar alla shellcontracts vars pattern stämmer överens med pathen
        result = db.engine.execute("SELECT * FROM shell_send WHERE \"{}\" REGEXP shell_send.pattern AND shell_send.status=\"active\"".format(
            file.translate(str.maketrans({"\\":r"\\"})))).fetchall()
        try: #lägg till nya filen i databasen
            dbfile = File(path=file)
            db.session.add(dbfile)
            db.session.commit()
            dbfileid = dbfile.id
            dbfilepath = dbfile.path
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        if result: #om det finns ett shellcontract
            for r in result:
                send_contractShell(r[0], dbfilepath, dbfileid) #skicka kontrakt utifrån skalkontraktet

    checkThread = threading.Thread(target=checkfiles, args=())
    checkThread.start()


def send_contractShell(shellid, filepath, fileid):
    shell = Shell_send.query.filter_by(shell_id=shellid).first() #hämta skalkontrakt från databasen
    path = shell.path
    with open(path,'r') as readfile:
        contract = json.loads(readfile.read()) #läs in skalkontrakt
    contract["contractID"] = str(uuid.uuid1().int>>65)
    contract["file"]["name"] = ntpath.basename(filepath)
    #skapa nytt contract
    newcontract = Contract_sent(
        id=contract["contractID"],
        path=app.config["CONTRACT_FOLDER"]+str(contract["contractID"])+app.config["CONTRACT_FILEEXT"],
        status="pending",
        client_id=contract["receiverID"],
        file_id=fileid
    )
    try: #uppdatera databasen med nytt kontrakt
        db.session.add(newcontract)
        db.session.commit()
        #skriv ner kontraktet
        with open(app.config["CONTRACT_FOLDER"]+str(contract["contractID"])+app.config["CONTRACT_FILEEXT"], "w") as outfile:
            json.dump(contract, outfile, indent=4)

        send_contract(contract["contractID"], contract["receiverID"]) #skicka kontraktet
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
