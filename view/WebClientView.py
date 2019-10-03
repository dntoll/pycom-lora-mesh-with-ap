from model.Message import Message
from unquote import unquote
from view.HTTPGet import HTTPGet

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
        return self.httpget.has("message") and self.httpget.has("target")

    def userPollsMessages(self):
        return self.httpget.has("messages")

    def userPollsNetwork(self):
        return self.httpget.has("network")

    def getMessage(self):
        mess = self.httpget.get("message")
        tar = self.httpget.get("target")
        return Message(mess, tar, self.meshNetworkState.me.rloc16, 0, False, False, False)

    def getIndexResponse(self):
        #perhaps read and include all files from www/include?
        f = open("www/cryptico.min.js", 'r')
        javascriptContents = f.read()
        f.close();

        f = open("www/clientsideapp.js", 'r')
        javascriptContents += "\n" + f.read()
        f.close();

        f = open("www/jquery-3.4.1.min.js", 'r')
        jQuery = "\n" + f.read()
        f.close();

        f = open("www/style.css", 'r')
        cssStyleContents = f.read()
        f.close();

        f = open("www/body.html", 'r')
        htmlBodyTop = f.read()
        f.close();



        html = """<!DOCTYPE html>
        <html>
            <head> <title>Pycom loramesh</title> </head>

            <script t language=\"JavaScript\" type=\"text/javascript\" >
                """ + jQuery + """
            </script>
            
            <script t language=\"JavaScript\" type=\"text/javascript\" >
                """ + javascriptContents + """
            </script>

            <style>
                """ + cssStyleContents + """
            </style>

            <body>
                """ + htmlBodyTop + """
            </body>
        </html>
        """
        return html

    def getNeighborsHTML(self):
        ret = "<h2>Neighborhood</h2>"

        ret += "<table>"
        ret += "<tr>" + self._getTitlesHTML() + "</tr>"
        ret += "<tr>" + self._getCompleteNodeHTML(self.meshNetworkState.me.mac) + "</tr>"
        ret += "<tr>" + self._getTitlesHTML() + "</tr>"

        for mac in self.meshNetworkState.getAllNodesMacs():
            ret += "<tr>" + self._getCompleteNodeHTML(mac) + "</tr>"
        ret += "</table>"

        return ret;

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

        row += "<td><a onclick='document.getElementById(\"idtarget\").value=\"" + str(mlEID) + "\"'>" + str(mlEID) + "</a></td>"
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


    def getMessagesHTML(self):
        messageBoardHTML = "<h2>Received Messages</h2>"
        messageBoardHTML += "<table>"
        for message in self.messageBoard.getReceivedMessages():
            messageBoardHTML += "<tr>" + self._getMessageHTML(message) + " </tr>"
        messageBoardHTML +=  "</table>"

        messageBoardHTML += "<h2>Send Que</h2>"
        messageBoardHTML += "<table>"
        for message in self.messageBoard.getMessagesToBeSent():
            messageBoardHTML += "<tr>" + self._getMessageHTML(message) + " </tr>"
        messageBoardHTML = messageBoardHTML + "</table>"

        messageBoardHTML += "<h2>Sent Messages</h2>"
        messageBoardHTML += "<table>"
        for message in self.messageBoard.getMessagesSent():
            messageBoardHTML += "<tr>" + self._getMessageHTML(message) + " </tr>"
        messageBoardHTML = messageBoardHTML + "</table>"

        return messageBoardHTML;

    def _getMessageHTML(self, message):
        messageHTML = ""
        messageHTML += "<td>From: " + str(message.getSender()) + "</td>"
        messageHTML += "<td>To: " + str(message.getTarget()) + "</td>"
        messageHTML += "<td>Content: " + str(message.getContent()) + "</td>"
        return messageHTML
