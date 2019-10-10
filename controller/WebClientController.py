class WebClientController:


    def __init__(self, messageBoard, meshNetworkState, view, phoneBook):
        self.messageBoard = messageBoard;
        self.meshNetworkState = meshNetworkState;
        self.view = view;
        self.phoneBook = phoneBook

    def handleRequest(self, cl_file, addr, connection):

        self.view.handleRequest(cl_file)


        #Send Message Action
        if self.view.userSendsMessage():
            print("userSendsMessage");
            message = self.view.getMessage()
            self.messageBoard.lock()
            self.messageBoard.sendMessage(message)
            self.messageBoard.unlock()
            self.view.sendMessagesJSON(connection)

        elif self.view.userPollsMessages():
            print("userPollsMessages");
            self.view.sendMessagesJSON(connection)

        elif self.view.userAddsContact():
            print("userAddsContact");
            client = self.view.getContact();
            self.phoneBook.updateContact(client);
            self.view.sendNeigborsJSON(connection)

        elif self.view.userPollsNetwork():
            print("userPollsNetwork");
            self.view.sendNeigborsJSON(connection)
        elif self.view.browserAskForFavicon():
            print("browserAskForFavicon");
            self.view.sendFavicon(connection)
        elif self.view.userSearchForContacts():
            print("userSearchForContacts");
            cr = self.view.getContactRequest();
            if self.phoneBook.hasContact(cr):
                #Note there may be more than one match...
                contacts = self.phoneBook.getContacts(cr);
                self.view.sendContactsJSON(contacts, connection)
            else:
                self.view.sendContactsJSON([], connection)

            if self.view.onlyDoLocalSearch() == False:
                myMac = self.meshNetworkState.getMac()
                message = self.phoneBook.createContactRequestMessage(cr, myMac)
                self.messageBoard.lock()
                self.messageBoard.sendMessage(message)
                self.messageBoard.unlock()

        else:
            self.view.sendIndexPageHTML(connection)
