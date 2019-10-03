class WebClientController:


    def __init__(self, messageBoard, meshNetworkState, view):
        self.messageBoard = messageBoard;
        self.meshNetworkState = meshNetworkState;
        self.view = view;

    def handleRequest(self, cl_file, addr, connection):

        self.view.handleRequest(cl_file)


        #Send Message Action
        if self.view.userSendsMessage():
            message = self.view.getMessage()
            self.messageBoard.sendMessage(message)
            self.view.getMessagesJSON(connection)
        elif self.view.userPollsMessages():
            self.view.getMessagesJSON(connection)
        elif self.view.userPollsNetwork():
            self.view.getNeighborsHTML(connection)
        else:
            self.view.getIndexResponse(connection)
