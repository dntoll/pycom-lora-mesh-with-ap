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

        #perhaps read and include all files from www/include?
        f = open("www/cryptico.min.js", 'r')
        javascriptContents = f.read()
        f.close();

        f = open("www/clientsideapp.js", 'r')
        javascriptContents += "\n" + f.read()
        f.close();

        f = open("www/style.css", 'r')
        cssStyleContents = f.read()
        f.close();

        f = open("www/body.html", 'r')
        htmlBodyTop = f.read()
        f.close();



        htmlStart = """<!DOCTYPE html>
        <html>
            <head> <title>Pycom loramesh</title> </head>
            <script type=\"text/javascript\">
                """ + javascriptContents + """
            </script>
            <style>
                """ + cssStyleContents + """
            </style>

            <body>
                """ + htmlBodyTop + """
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
            response = "";
            try:
                messageBoardHTML = this.webClientView.getFormHTML()
                messageBoardHTML += this.webClientView.getMessagesHTML()
                messageBoardHTML += this.webClientView.getNeighborsHTML()
                response = htmlStart + messageBoardHTML + htmlEnd
                cl.send(response)
                cl.close()
            except Exception as e:
                response = htmlStart + repr(e) + htmlEnd
                cl.send(response)
                cl.close()
                print("something went wrong when sending message " + repr(e))
                raise e
