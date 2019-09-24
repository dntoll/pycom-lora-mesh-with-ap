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

import json

class Message:

    def __init__(self, content, target, sender, sendCount, isAck, hasBeenAcced):
        self.content = content
        self.target = target
        self.sender = sender
        self.sendCount = sendCount
        self.isACK = isAck
        self.hasBeenAcced = hasBeenAcced

    def getSender(self):
        return str(self.sender)

    def getContent(self):
        return self.content

    def doSend(self):
        self.sendCount = self.sendCount + 1

    def toString(self):
        tuple = [self.content, self.target, self.sender, self.sendCount, self.isACK, self.hasBeenAcced]
        return json.dumps(tuple)

    def fromString(strData):
        tuple = json.loads(strData);

        print(tuple)
        content, target, sender, sendCount, isACK, hasBeenAcced = tuple

        message = Message(content, target, sender, sendCount, isACK, hasBeenAcced)

        return message

    def isAccForMessage(self, ackMessage):
        return self.content == ackMessage.content and self.target == ackMessage.target
