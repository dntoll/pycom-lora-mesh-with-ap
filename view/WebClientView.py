from model.Message import Message
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

    def userSendsMessage(self):
        return self.httpget.has("message") and self.httpget.has("target") and self.httpget.has("time")

    def userPollsMessages(self):
        return self.httpget.has("messages")

    def userPollsNetwork(self):
        return self.httpget.has("network")

    def getMessage(self):
        mess = self.httpget.get("message")
        tar = self.httpget.get("target")
        time = self.httpget.get("time")
        return Message(mess, tar, self.meshNetworkState.me.rloc16, time, 0, False, False, False)

    def getIndexResponse(self, connection):
        #perhaps read and include all files from www/include?

        connection.send("""<!DOCTYPE html>
        <html>
            <head> <title>Pycom loramesh</title> </head>

            <script t language=\"JavaScript\" type=\"text/javascript\" >
                """)
        self.sendFile("www/jquery-3.4.1.min.js", connection)
        connection.send("</script><script t language=\"JavaScript\" type=\"text/javascript\" >")
        self.sendFile("www/cryptico.min.js", connection)
        self.sendFile("www/clientsideapp.js", connection)
        connection.send( "</script><style>")
        self.sendFile("www/style.css", connection)
        connection.send("</style> <body>");
        self.sendFile("www/body.html", connection)
        connection.send("</body></html>")
    def sendFile(self, filename, connection):
        f = open(filename, 'r')
        connection.send(f.read())
        f.close();

    def getNeighborsHTML(self, connection):
        ret = "<h2>Neighborhood</h2>"

        ret += "<table>"
        ret += "<tr>" + self._getTitlesHTML() + "</tr>"
        ret += "<tr>" + self._getCompleteNodeHTML(self.meshNetworkState.me.mac) + "</tr>"
        ret += "<tr>" + self._getTitlesHTML() + "</tr>"

        for mac in self.meshNetworkState.getAllNodesMacs():
            ret += "<tr>" + self._getCompleteNodeHTML(mac) + "</tr>"
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
        neighbors = self.meshNetworkState.getNeighbors()
        others = self.meshNetworkState.getOthers();
        routers = self.meshNetworkState.getRouters();


        ip = -1;
        name = "";
        mlEID = -1
        role = -1;
        rssi = -1;
        age = -1;
        id = -1;
        path_cost = -1;
        firmware = "not set"

        if self.meshNetworkState.me.mac == str(mac):
            ip = self.meshNetworkState.me.ip
            role = self.meshNetworkState.me.role
            ip = self.meshNetworkState.me.ip
            name = self.meshNetworkState.selfDecoration.name
            mlEID = self.meshNetworkState.selfDecoration.mlEID
            firmware = self.meshNetworkState.selfDecoration.firmware
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

        row += "<td><a onclick='document.getElementById(\"targetID\").value=\"" + str(mlEID) + "\"'>" + str(mlEID) + "</a></td>"
        row += "<td>" + self._translateRole(role) + "</td>"
        row += "<td>" + str(rssi) + "</td>"
        row += "<td>" + str(path_cost) + "</td>"
        row += "<td>" + str(age) + "</td>"
        row += "<td>" + str(id) + "</td>"
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
        return row


    def getMessagesJSON(self, connection):
        dict = {
            "Received" : self.messageBoard.getReceivedMessagesList(),
            "To be sent" : self.messageBoard.getMessagesToBeSentList(),
            "Sent" : self.messageBoard.getMessagesSentList()
        }
        ret = ujson.dumps(dict)
        connection.send(ret)
