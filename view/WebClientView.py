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
        ret = "<h2>Neighborhood</h2>"

        ret += "<table>"
        ret += "<tr>" + self._getTitlesHTML() + "</tr>"
        ret += "<tr>" + self._getCompleteNodeHTML(self.meshNetworkState.me.mac) + "</tr>"
        ret += "<tr>" + self._getTitlesHTML() + "</tr>"

        for mac in self.meshNetworkState.getAllNodesMacs():
            ret += "<tr><a onclick='document.getElementById(\"targetID\").value=\"" + str(mac) + "\"'>" + self._getCompleteNodeHTML(mac) + "</a></tr>"
        ret += "</table>"

        connection.send(ret)

    def _translateRole(self, role):
        if role == 0:
            return "Disabled"
        elif role == 1:
            return "Detached"
        elif role == 2:
            return "Child"
        elif role == 3:
            return "Router"
        else:
            return "Leader"

    def _getNodeDecorationHTML(self, networkNodeDecoration):
        html = "<dl>";
        html += "<dt>Name:</dt><dd>" + str(networkNodeDecoration.name) + "</dd>"
        html += "<dt>MAC</dt><dd>" + str(networkNodeDecoration.mac) + "</dd>"
        html += "<dt>mlEID</dt><dd>" + str(networkNodeDecoration.mlEID) + "</dd>"
        for client in networkNodeDecoration.clientsConnectedAtMySite:
            html += "<dt>Client</dt><dd>" + str(client) + "</dd>"
        html += "</dl>";
        return html;

    def _getCompleteNodeHTML(self, mac):

        #TODO: Divide into two method of which one is meshNetworkState and returns this complete information about a node...
        neighbors = self.meshNetworkState.getNeighbors()
        others = self.meshNetworkState.getOthers();
        routers = self.meshNetworkState.getRouters();


        ip = "no info"
        name = "no info"
        mlEID = "no info"
        role = "no info"
        rssi = "no info"
        age = "no info"
        id = "no info"
        path_cost = "no info"
        firmware = "not set"
        clients = []

        if self.meshNetworkState.me.mac == str(mac):
            ip = self.meshNetworkState.me.ip
            role = self.meshNetworkState.me.role
            ip = self.meshNetworkState.me.ip
            name = self.meshNetworkState.selfDecoration.name
            mlEID = self.meshNetworkState.selfDecoration.mlEID
            firmware = self.meshNetworkState.selfDecoration.firmware
            clients = self.meshNetworkState.selfDecoration.clientsConnectedAtMySite
        else:
            if mac in neighbors:
                node = neighbors[mac]
                ip = node.ip
                role = node.role
                rssi = node.rssi
                age = node.age
            if mac in others:
                node = others[mac]
                name = node.name
                mlEID = node.mlEID
                firmware = node.firmware
                clients = node.clientsConnectedAtMySite
            if mac in routers:
                node = routers[mac]
                age = node.age
                id = node.id
                path_cost = node.path_cost


        row = ""
        row += "<td>" + str(name) + "</td>"
        row += "<td>" + str(firmware) + "</td>"
        row += "<td>" + str(mac) + "</td>"
        row += "<td>" + str(ip) + "</td>"
        #row += "<td>" + str(mlEID) + "</td>"

        row += "<td>" + str(mlEID) + "</td>"
        row += "<td>" + self._translateRole(role) + "</td>"
        row += "<td>" + str(rssi) + "</td>"
        row += "<td>" + str(path_cost) + "</td>"
        row += "<td>" + str(age) + "</td>"
        row += "<td>" + str(id) + "</td>"

        html = "<dl>";
        for number, client in clients.items():
            html += "<dt>phoneNumber</dt><dd>" + str(client.phoneNumber) + "</dd>"
            html += "<dt>name</dt><dd>" + str(client.name) + "</dd>"
            html += "<dt>publicKeyString</dt><dd>" + str(client.publicKeyString) + "</dd>"
            html += "<dt>time</dt><dd>" + str(client.time) + "</dd>"
        html += "</dl>"
        row += "<td>" + html + "</td>"
        return row

    def _getTitlesHTML(self):
        row = ""
        row += "<th>Name</th>"
        row += "<th>Code Version</th>"
        row += "<th>Mac</th>"
        row += "<th>IP</th>"
        row += "<th>mlEID</th>"
        row += "<th>Role</th>"
        row += "<th>rssi</th>"
        row += "<th>path_cost</th>"
        row += "<th>age</th>"
        row += "<th>id</th>"
        row += "<th>clients</th>"
        return row
