from model.Message import Message
from model.Contact import Contact
from model.ContactRequest import ContactRequest

from unquote import unquote
from view.HTTPGet import HTTPGet

import ujson
import os

class WebClientView:


    def __init__(self, messageBoard, meshNetworkState, meshAdapter):
        self.messageBoard = messageBoard;
        self.meshNetworkState = meshNetworkState;
        self.meshAdapter = meshAdapter;

    def handleRequest(self, cl_file):

        self.httpget = HTTPGet()

        while True:
            line = cl_file.readline()
            strline = line.decode();
            self.httpget.addLine(strline);
            if not line or strline == '\r\n':
                break
    def userAddsContact(self):
        return self.httpget.has("phoneNumber") and self.httpget.has("name") and self.httpget.has("time") and self.httpget.has("publickey")

    def userSendsMessage(self):
        return self.httpget.has("message") and self.httpget.has("target") and self.httpget.has("time")

    def userPollsMessages(self):
        return self.httpget.has("messages")

    def userPollsNetwork(self):
        return self.httpget.has("network")

    def browserAskForFavicon(self):
        return self.httpget.hasFavicon();

    def userSearchForContacts(self):
        return self.httpget.has("contactPhone") and self.httpget.has("contactName") and self.httpget.has("local")

    def onlyDoLocalSearch(self):
        return self.httpget.get("local") == "true"

    def getContactRequest(self):
        phone = self.httpget.get("contactPhone")
        name = self.httpget.get("contactName")
        return ContactRequest(name, phone);

    def getContact(self):
        phoneNumber = self.httpget.get("phoneNumber")
        name = self.httpget.get("name")
        time = self.httpget.get("time")
        publicKeyString = self.httpget.get("publickey")
        mac = self.meshAdapter.getMAC()
        return Contact(phoneNumber, name, publicKeyString, time, mac)

    def getMessage(self):
        mess = self.httpget.get("message")
        tar = self.httpget.get("target")
        time = self.httpget.get("time")
        return Message(mess, tar, self.meshAdapter.getMAC(), time, 0, Message.IS_OPEN_MESSAGE)

    def sendFavicon(self, connection):
        connection.send("poo")

    def noLocalContact(self, connection):
        connection.send("noLocalContact");

    def sendContactsJSON(self, contacts, connection):
        ret = ujson.dumps(contacts)
        connection.send(ret)



    def sendIndexPageHTML(self, connection):
        #perhaps read and include all files from www/include?

        connection.send("""<!DOCTYPE html>
        <html>
            <head> <title>Pycom loramesh</title> </head>

            <script t language=\"JavaScript\" type=\"text/javascript\" >
                """)
        self.sendFile("www/jquery-3.4.1.min.js", connection)
        connection.send("</script><script t language=\"JavaScript\" type=\"text/javascript\" >")
        self.sendFile("www/cryptico.min.js", connection)

        self.sendFiles("www/model", connection)
        self.sendFiles("www/view", connection)
        self.sendFiles("www/controller", connection)

        connection.send( "</script><style>")
        self.sendFile("www/style.css", connection)
        connection.send("</style> <body>");
        self.sendFile("www/body.html", connection)
        connection.send("</body></html>")

    def sendFile(self, filename, connection):
        f = open(filename, 'r')
        connection.send(f.read())
        f.close();

    def sendFiles(self, path, connection):

        files = os.listdir(path)
        for file in files:
            if file.endswith('.js'):
                print(file)
                self.sendFile(path + "/"+ file, connection)

    def sendMessagesJSON(self, connection):
        dict = {
            "Received" : self.messageBoard.getReceivedMessagesList(),
            "To be sent" : self.messageBoard.getMessagesToBeSentList(),
            "Sent" : self.messageBoard.getMessagesSentList()
        }
        ret = ujson.dumps(dict)
        connection.send(ret)

    def sendNeigborsJSON(self, connection):
        dict = {
            "me" : self.meshNetworkState.getMe(),
            "others" : self.meshNetworkState.getOthers(),
        }
        ret = ujson.dumps(dict)
        connection.send(ret)
