from model.Message import Message
from model.Client import Client
from unquote import unquote
from view.HTTPGet import HTTPGet

import ujson

class WebClientView:


    def __init__(self, messageBoard, meshNetworkState):
        self.messageBoard = messageBoard;
        self.meshNetworkState = meshNetworkState;

    def handleRequest(self, cl_file):

        self.httpget = HTTPGet()

        while True:
            line = cl_file.readline()
            strline = line.decode();
            self.httpget.addLine(strline);
            if not line or strline == '\r\n':
                break
    def userAddsClient(self):
        return self.httpget.has("phoneNumber") and self.httpget.has("name") and self.httpget.has("time") and self.httpget.has("publickey")

    def userSendsMessage(self):
        return self.httpget.has("message") and self.httpget.has("target") and self.httpget.has("time")

    def userPollsMessages(self):
        return self.httpget.has("messages")

    def userPollsNetwork(self):
        return self.httpget.has("network")

    def browserAskForFavicon(self):
        return self.httpget.hasFavicon();

    def getClient(self):
        phoneNumber = self.httpget.get("phoneNumber")
        name = self.httpget.get("name")
        time = self.httpget.get("time")
        publicKeyString = self.httpget.get("publickey")
        return Client(phoneNumber, name, publicKeyString, time)

    def getMessage(self):
        mess = self.httpget.get("message")
        tar = self.httpget.get("target")
        time = self.httpget.get("time")
        return Message(mess, tar, self.meshNetworkState.getMac(), time, 0, False, False)

    def sendFavicon(self, connection):
        connection.send("poo")

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
        self.sendFile("www/model.js", connection)
        self.sendFile("www/view.js", connection)
        self.sendFile("www/controller.js", connection)
        connection.send( "</script><style>")
        self.sendFile("www/style.css", connection)
        connection.send("</style> <body>");
        self.sendFile("www/body.html", connection)
        connection.send("</body></html>")

    def sendFile(self, filename, connection):
        f = open(filename, 'r')
        connection.send(f.read())
        f.close();


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
            "me" : self.meshNetworkState.getMyNodFullInformation(),
            "others" : self.meshNetworkState.getOthersAsFullInformationList(),
        }
        ret = ujson.dumps(dict)
        connection.send(ret)
