import socket
import _thread
from Message import Message
from WebClientView import WebClientView

class WebServer:


    def __init__(self, webClientView, messageBoard):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(1)
        _thread.start_new_thread(WebServer.handleAccept, (self.s, self))
        self.webClientView = webClientView
        self.messageBoard = messageBoard;
        print("started webserver");

    def handleAccept(s, this):
        htmlStart = """<!DOCTYPE html>
        <html>
            <head> <title>ESP8266 Pins</title> </head>
            <body>
                <form method="get">
                    <input type='text' name='message'>
                    <input type="submit" value="Submit">
                </form>
                <h1>Message Log</h1>
                """

        htmlEnd = """</body>
        </html>
        """

        while True:
            #print('Listen for incomming socket connections')
            cl, addr = s.accept()
            print('client connected from', addr)
            cl_file = cl.makefile()
            while True:
                line = cl_file.readline()
                strline = line.decode();
                if strline.startswith("GET /?message="):
                    messageEnd = strline.find(" HTTP/1.1")
                    messageContent = strline[14:messageEnd];
                    #print("Message was" + messageContent)
                    message = Message(messageContent, "world", addr, 0, False, False)
                    this.messageBoard.sendMessage(message);
                if not line or strline == '\r\n':
                    break

            messageBoardHTML = this.webClientView.getMessagesHTML();
            response = htmlStart + messageBoardHTML + htmlEnd

            cl.send(response)
            cl.close()
