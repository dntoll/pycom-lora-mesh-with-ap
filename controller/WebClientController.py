class WebClientController:


    def __init__(self, messageBoard, meshNetworkState, view):
        self.messageBoard = messageBoard;
        self.meshNetworkState = meshNetworkState;
        self.view = view;

    def handleRequest(self, cl_file, addr):

        self.view.handleRequest(cl_file)


        #Send Message Action
        if self.view.userSendsMessage():
            message = self.view.getMessage()
            self.messageBoard.sendMessage(message)
            return self.view.getMessagesJSON()
        elif self.view.userPollsMessages():
            return self.view.getMessagesJSON()
        elif self.view.userPollsNetwork():
            return self.view.getNeighborsHTML()
        else:
            return self.view.getIndexResponse()
