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
        #we only care about our own messages or broadcasts
        if self.meshState.isDirectedToMe(message.target):
            if message.isACK:
                self._receivedAccMessageForMe(message);
            else:
                self.sendAcc(message)
                self.received.append(message)
        elif message.isBroadCast():
            if message.isDecoration():
                self.meshState.updateOthersDecorations(message)
            else:
                self.received.append(message)

    def _receivedAccMessageForMe(self, message):
        newSendList = []
        for sent in self.toBeSent:
            if message.isAccForMessage(sent) == False:
                newSendList.append(sent) #We "remove messages" being acced by adding all others to the new send list
            else:
                self.sent.append(sent)
        self.toBeSent = newSendList #remove from send list

    #remove acc
    def sendCompleted(self):
        newSendList = []

        for sent in self.toBeSent:
            if sent.isACK == False and sent.isBroadCast() == False:
                newSendList.append(sent) #Messages that are not ACC and not broadcasts should be kept in the send list until an acc is received
            else:
                if sent.isDecoration():
                    pass #we just remove these
                else:
                    self.sent.append(sent) #broadcasts are added here
        self.toBeSent = newSendList

    def getReceivedMessages(self):
        return self.received

    def getMessagesToBeSent(self):
        return self.toBeSent

    def getMessagesSent(self):
        return self.sent

    def sendAcc(self, message):
        #note sender and target swapped places here...
        accMessage = Message(message.content, message.sender, message.target, 0, True, False, False);
        self.sendMessage(accMessage)
