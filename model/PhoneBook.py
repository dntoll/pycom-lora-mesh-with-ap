
from model.Message import Message

class PhoneBook:
    def __init__(self):
        self.seenClients = {}

    def updateContact(self, newClientInfo):
        self.seenClients[str(newClientInfo.phoneNumber)] = newClientInfo
        print(self.seenClients)

    def hasContact(self, contactRequest):
        for phoneNumber, client in self.seenClients.items():
            if phoneNumber == contactRequest.phone or (contactRequest.phone == "" and client.name == contactRequest.name):
                return True
        return False

    def getContacts(self, contactRequest):
        ret = [];
        for phoneNumber, client in self.seenClients.items():
            if phoneNumber == contactRequest.phone or (contactRequest.phone == "" and client.name == contactRequest.name):
                ret.append(client.toDictionary())
        return ret

    def getContactRequestMessage(self, contactRequest, myMac):
        content = contactRequest.toString();

        return Message(content, Message.TYPE_BROADCAST, myMac, 0, 0, False, False)
