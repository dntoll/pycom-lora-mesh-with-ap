import socket
import _thread

class WebServer:


    def __init__(self, webClientController):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(1)
        _thread.start_new_thread(WebServer.handleAccept, (self.s, self))
        self.webClientController = webClientController
        print("started webserver");

    def handleAccept(s, this):
        while True:
            #Simple web-server that closes the socket directly
            try:
                #print('Listen for incomming socket connections')
                cl, addr = s.accept()
                print('client connected from', addr)
                cl_file = cl.makefile()
                response = this.webClientController.handleRequest(cl_file, addr, cl);

                cl.close()
            except Exception as e:
                try:
                    response =  repr(e)
                    cl.send(response)
                    cl.close()
                    raise e
                except Exception as e:
                    print("something went wrong when sending message " + repr(e))
                    raise e
