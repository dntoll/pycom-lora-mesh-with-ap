import socket
import _thread

from WebClientView import WebClientView

class WebServer:


    def __init__(self, webClientView):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(1)
        _thread.start_new_thread(WebServer.handleAccept, (self.s, self))
        self.webClientView = webClientView
        print("started webserver");

    def handleAccept(s, this):
        htmlStart = """<!DOCTYPE html>
        <html>
            <head> <title>ESP8266 Pins</title> </head>
            <body>

                <h1>Message Log</h1>
                <a href="http://192.168.1.1">reload</a>
                """

        htmlEnd = """</body>
        </html>
        """

        while True:
            #print('Listen for incomming socket connections')
            cl, addr = s.accept()
            print('client connected from', addr)
            cl_file = cl.makefile()
            this.webClientView.handleRequest(cl_file, addr);

            messageBoardHTML = this.webClientView.getFormHTML()
            messageBoardHTML += this.webClientView.getMessagesHTML()
            messageBoardHTML += this.webClientView.getNeighborsHTML()
            response = htmlStart + messageBoardHTML + htmlEnd

            cl.send(response)
            cl.close()
