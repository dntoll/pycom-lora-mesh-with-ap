
from model.Message import Message
from model.Contact import Contact
import ubinascii
import json

class PhoneBook:
    def __init__(self):
        self.seenClients = {}

    def updateContact(self, newClientInfo):
        self.seenClients[str(newClientInfo.phoneNumber)] = newClientInfo

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



    #TODO: Move to factory?
    def createContactRequestMessage(self, contactRequest, myMac):
        content = contactRequest.toString();
        return Message(content, Message.TYPE_BROADCAST, myMac, 0, 0, Message.IS_CONTACT_SEARCH)

    def createContactsFoundMessage(self, contactRequest, message, myMac):
        contactsToSend = self.getContacts(contactRequest)
        content = ubinascii.b2a_base64(json.dumps(contactsToSend))
        return Message(content, message.sender, myMac, 0,0, Message.IS_CONTACT_FOUND)

    def contactsFound(self, message):
        print("contacts found message!")
        rawText = ubinascii.a2b_base64(message.content)
        arr = json.loads(rawText);
        #print(arr)
        for contact in arr:
            print(contact)
            self.updateContact(Contact(contact["phoneNumber"], contact["name"], contact["publicKeyString"], contact["time"], contact["lastSeenMac"]))
