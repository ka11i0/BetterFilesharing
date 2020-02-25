import threading, os, glob, ntpath, json, uuid, time
from flaskapp import db, app
from flaskapp.models import File, Shell_recv, Contract_sent
from Contract.Rest import send_contract
import sqlalchemy

BASE_PATH = os.path.abspath("/home/frappe/document/cpp")
CHECK_DELAY = 2 # Hur många sekunder mellan checks


def checkfiles():
    #time.sleep(CHECK_DELAY)
    url = os.path.join(BASE_PATH,"*","*")
    files = glob.iglob(os.path.join(BASE_PATH, "**", "*"), recursive=True) #hämtar alla paths på files
    newfiles = [] #innehåller alla filepaths som inte finns i databasen
    dbfiles = [r.path for r in File.query.all()] #hämtar alla paths i databasen
    for file in files:
        if file not in dbfiles: #kollar om filen inte finns i databasen
            newfiles.append(file)
    print(newfiles)
    print(dbfiles)
    for file in newfiles: #går igenom alla nya filer
        #hämtar alla shellcontracts vars pattern stämmer överens med pathen
        result = db.engine.execute("SELECT * FROM shell_recv WHERE \"{}\" LIKE shell_recv.pattern".format(file)).fetchall()
        try: #lägg till nya filen i databasen
            dbfile = File(path=file)
            db.session.add(dbfile)
            db.session.commit()
            print(dbfile.id)
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        if result: #om det finns ett shellcontract
            for r in result:
                send_contractShell(r[0], dbfile.path,dbfile.id) #skicka kontrakt utifrån skalkontraktet

    #checkThread = threading.Thread(target=checkfiles, args=())
    #checkThread.start()


def send_contractShell(shellid, filepath, fileid):
    shell = Shell_recv.query.filter_by(shell_id=shellid).first() #hämta skalkontrakt från databasen
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
