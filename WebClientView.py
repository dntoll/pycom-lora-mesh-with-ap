from Message import Message
from unquote import unquote


class WebClientView:


    def __init__(self, messageBoard, meshNetworkState):
        self.messageBoard = messageBoard;
        self.meshNetworkState = meshNetworkState;


    def handleRequest(self, cl_file, addr):
        while True:
            line = cl_file.readline()
            strline = line.decode();
            if strline.startswith("GET /?"):
                messageEnd = strline.find(" HTTP/1.1")
                allGetStuff = strline[6:messageEnd]; #skip GET /?
                parts = allGetStuff.split("&")

                allThemParts = {}
                for getVariable in parts:
                    firstAndSecond = getVariable.split("=");
                    name = firstAndSecond[0]
                    value = firstAndSecond[1]
                    allThemParts.update( {name : value } )

                print(allThemParts)

                mess = unquote(allThemParts.get("message"))
                tar = unquote(allThemParts.get("target"))
                message = Message(mess.decode(), tar.decode(), self.meshNetworkState.me.rloc16, 0, False, False, False)
                self.messageBoard.sendMessage(message)
            if not line or strline == '\r\n':
                break

    def getNeighborsHTML(self):
        ret = "<h2>Neighborhood</h2>"

        ret += "<table>"
        ret += "<tr>" + self._getTitlesHTML() + "</tr>"
        ret += "<tr>" + self._getCompleteNodeHTML(self.meshNetworkState.me.mac) + "</tr>"

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

        if self.meshNetworkState.me.mac == str(mac):
            ip = self.meshNetworkState.me.ip
            role = self.meshNetworkState.me.role
            ip = self.meshNetworkState.me.ip
            name = self.meshNetworkState.selfDecoration.name
            mlEID = self.meshNetworkState.selfDecoration.mlEID
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
            if mac in routers:
                node = routers[mac]
                age = node.age
                id = node.id
                path_cost = node.path_cost


        row = ""
        row += "<td>" + str(name) + "</td>"
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
        row += "<th>Mac</th>"
        row += "<th>IP</th>"
        row += "<th>mlEID</th>"
        row += "<th>Role</th>"
        row += "<th>rssi</th>"
        row += "<th>path_cost</th>"
        row += "<th>age</th>"
        row += "<th>id</th>"
        return row

    def _getNodeHTML(self, node):
        html = "<dl>";
        html += "<dt>IP</dt><dd>" + str(node.ip) + "</dd>"
        html += "<dt>MAC</dt><dd>" + str(node.mac) + "</dd>"
        html += "<dt>role</dt><dd>" + self._translateRole(node.role) + "</dd>"
        html += "<dt>rloc16</dt><dd>" + str(node.rloc16) + "</dd>"
        html += "<dt>rssi</dt><dd>" + str(node.rssi) + "</dd>"
        html += "<dt>age</dt><dd>" + str(node.age) + "</dd>"
        html += "<dt>id</dt><dd>" + str(node.id) + "</dd>"
        html += "<dt>path_cost</dt><dd>" + str(node.path_cost) + "</dd>"
        html += "</dl>";
        return html;

    def getFormHTML(self):
        return """<form method="get">
            Message:<input type='text' name='message'><br/>
            Target :<input type='text' name='target' id='idtarget'>
            <input type="submit" value="Submit">
        </form>"""

    def getMessagesHTML(self):

        messageBoardHTML = "<h2>Received Messages</h2>"
        messageBoardHTML += "<table>"
        for message in self.messageBoard.getReceivedMessages():
            messageBoardHTML += "<tr>" + self._getMessageHTML(message) + " </tr>"
        messageBoardHTML +=  "</table>"


        messageBoardHTML += "<h2>To be sent Messages</h2>"
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
