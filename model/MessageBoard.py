#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

__version__ = '1'

import _thread
from model.Message import Message
from model.ContactRequest import ContactRequest

class MessageBoard:
    def __init__(self, phoneBook):
        self.received = {}
        self.toBeSent = {}
        self.sent = {}

        self.phoneBook = phoneBook
        self.myLock = _thread.allocate_lock()

    def lock(self):
        self.myLock.acquire()

    def unlock(self):
        self.myLock.release()

    def sendMessage(self, message):
        messageHash = message.getUniqueID();

        self.toBeSent[messageHash] = message

    def setMessageState(self, meshState):
        self.meshState = meshState

    #Move this to the controller!
    def receiveMessage(self, message):

        messageHash = message.getUniqueID();
        #we only care about our own messages or broadcasts
        if self.meshState.isDirectedToMe(message.target):
            if message.isACK():
                self._receivedAccMessageForMe(message);
            elif message.isContactFound():
                self.phoneBook.contactsFound(message)
                self.received[messageHash] = message
            else:
                self._sendAcc(message)
                self.received[messageHash] = message
        elif message.isBroadCast():
            if message.isContactSearch():
                cr = ContactRequest.fromString(message.content)
                if self.phoneBook.hasContact(cr):
                    crm = self.phoneBook.createContactsFoundMessage(cr, message, self.meshState.getMac());
                    self.sendMessage(crm)

            elif message.isDecoration():
                self.meshState.updateOthersDecorations(message)
            else:
                self.received[messageHash] = message


    def _receivedAccMessageForMe(self, message):
        #messageHash = message.getUniqueID();
        newSendDictionary = {}
        for hash, sent in self.toBeSent.items():
            if message.isAccForMessage(sent) == False:
                newSendDictionary[hash] = sent #We "remove messages" being acced by adding all others to the new send list
            else:
                self.sent[hash] =sent

        self.toBeSent = newSendDictionary #remove from send list

    #remove acc
    def sendCompleted(self):
        newSendDictionary = {}

        for hash, sent in self.toBeSent.items():
            if sent.isACK == False and sent.isBroadCast() == False:
                newSendDictionary[hash] = sent #Messages that are not ACC and not broadcasts should be kept in the send list until an acc is received
            else:
                if sent.isDecoration():
                    pass #we just remove these
                else:
                    self.sent[hash] = sent #broadcasts are added here
        self.toBeSent = newSendDictionary

    def getReceivedMessages(self):
        return self.received

    def getMessagesToBeSent(self):
        return self.toBeSent

    def getMessagesSent(self):
        return self.sent

    def getReceivedMessagesList(self):
        ret = []
        for hash, message in self.received.items():
            ret.append(message.toDictionary())
        return ret

    def getMessagesToBeSentList(self):
        ret = []
        for hash, message in self.toBeSent.items():
            ret.append(message.toDictionary())
        return ret

    def getMessagesSentList(self):
        ret = []
        for hash, message in self.sent.items():
            ret.append(message.toDictionary())
        return ret

    def _sendAcc(self, message):
        #note sender and target swapped places here...
        accMessage = Message(message.content, message.sender, message.target, message.time, 0, Message.IS_ACK);
        self.sendMessage(accMessage)
