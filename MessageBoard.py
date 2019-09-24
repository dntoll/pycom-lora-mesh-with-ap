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

from Message import Message

class MessageBoard:
    def __init__(self):
        self.received = []
        self.toBeSent = []
        self.sent = []

    def sendMessage(self, message):
        self.toBeSent.append(message)

    def receiveMessage(self, message):
        #is this an ACK?
        if message.isACK:
            newSendList = []
            print("received acc on " + message.content)
            #remove all that are not this message
            for sent in self.toBeSent:
                if message.isAccForMessage(sent) == False:
                    newSendList.append(sent)
                else:
                    self.sent.append(sent)
            self.toBeSent = newSendList #remove from send list
        else:
            self.sendAcc(message)
            self.received.append(message)

    #remove acc
    def sendCompleted(self):
        newSendList = []

        for sent in self.toBeSent:
            if sent.isACK == False:
                newSendList.append(sent)
        self.toBeSent = newSendList

    def getReceivedMessages(self):
        return self.received

    def getMessagesToBeSent(self):
        return self.toBeSent

    def getMessagesSent(self):
        return self.sent

    def sendAcc(self, message):
        accMessage = Message(message.content, message.target, message.sender, 0, True, False);
        self.sendMessage(accMessage)
        print("sent acc on " + message.content)
