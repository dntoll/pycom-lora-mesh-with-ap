from Message import Message

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

                #print("Message was" + messageContent)
                message = Message(allThemParts.get("message"), allThemParts.get("target"), self.meshNetworkState.getIP(), 0, False, False)
                self.messageBoard.sendMessage(message);
            if not line or strline == '\r\n':
                break

    def getNeighborsHTML(self):
        ret = "<h2>Neighborhood</h2>"
        nodeHTML = self._getNodeHTML(self.meshNetworkState.me)
        ret += "<p>Me: " + nodeHTML + "</p>"
        ret += "<table>"
        #print(self.meshNetworkState.getNeighbors());
        for neigh in self.meshNetworkState.getNeighbors():
            nodeHTML = self._getNodeHTML(neigh)
            ret += "<tr><td><a onclick='document.getElementById(\"idtarget\").value=\"" + neigh.getIP() + "\"'>" + nodeHTML + "</a></td></tr>"
        ret += "</table>"

        ret += "<table>"
        #print(self.meshNetworkState.getNeighbors());
        for neigh in self.meshNetworkState.getRouters():
            nodeHTML = self._getNodeHTML(neigh)
            ret += "<tr><td><a onclick='document.getElementById(\"idtarget\").value=\"" + neigh.getIP() + "\"'>" + nodeHTML + "</a></td></tr>"
        ret += "</table>"
        return ret;

    def _getNodeHTML(self, node):
        html = "<dl>";
        html += "<dt>IP</dt><dd>" + str(node.ip) + "</dd>"
        html += "<dt>MAC</dt><dd>" + str(node.mac) + "</dd>"
        html += "<dt>rloc16</dt><dd>" + str(node.rloc16) + "</dd>"
        html += "<dt>rssi</dt><dd>" + str(node.rssi) + "</dd>"
        html += "<dt>age</dt><dd>" + str(node.age) + "</dd>"
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
        messageHTML += "<td>" + message.getSender() + "</td>"
        messageHTML += "<td>" + message.getContent() + "</td>"
        messageHTML += "<td>" + message.toString() + "</td>"

        return messageHTML
