from Contract.contracthandler import getHandler
from Filesharing.reciever import FileReciever
import requests
import json

filename = input("filename to fetch: ")
outputfile = input("filename to store as: ")

host = "127.0.0.1"
port = 8001
data = "{{ \"filename\":\"{0}\", \"host\": \"{1}\", \"port\":{2} }}".format(filename, host, port)
print(data)
response = requests.put("http://127.0.0.1:5000/v1/register_contract", data=data)

if response.status_code == 201: 
    fr = FileReciever(host, port)
    print("waiting for file")
    fr.start(outputfile, 'w')
else:
    print(response.text)
