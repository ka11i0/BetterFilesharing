from Rest import app
import threading
import server

if __name__=='__main__':
    server = threading.Thread(target=server.startserver)
    server.start()
    app.run(debug=True)

def runRest():
    app.run(debug=True)
