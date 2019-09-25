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
    def __init__(self, meshState):
        self.received = []
        self.toBeSent = []
        self.sent = []
        self.meshState = meshState

    def sendMessage(self, message):
        self.toBeSent.append(message)

    def receiveMessage(self, message):
        #we only care about our own messages
        print(message.target)
        print(self.meshState.me.rloc16)
        if message.target == self.meshState.me.rloc16:
            if message.isACK:
                newSendList = []
                print("received acc on " + message.content)
                #remove all that are not this message
                for sent in self.toBeSent:
                    if message.isAccForMessage(sent) == False:
                        newSendList.append(sent)
                    else:
                        self.sent.append(sent)
                        print("acc was recognized as for my sent message")
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
        accMessage = Message(message.content, message.sender, message.target, 0, True, False);
        self.sendMessage(accMessage)
        print("sent acc on " + message.content)
