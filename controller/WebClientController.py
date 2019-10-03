class WebClientController:


    def __init__(self, messageBoard, meshNetworkState, view):
        self.messageBoard = messageBoard;
        self.meshNetworkState = meshNetworkState;
        self.view = view;

    def handleRequest(self, cl_file, addr):

        self.view.handleRequest(cl_file)


        #Send Message Action
        if self.view.userSendsMessage():
            print("User Sends Message");
            message = self.view.getMessage()
            self.messageBoard.sendMessage(message)
            return "sent"
        elif self.view.userPollsMessages():
            print("User Polls Messages");
            return self.view.getMessagesHTML()
        elif self.view.userPollsNetwork():

            print("User Polls Netowk");
            return self.view.getNeighborsHTML()
        else:
            return self.view.getIndexResponse()
