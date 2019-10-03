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
import ubinascii

class Message:
    #https://openthread.io/guides/thread-primer/ipv6-addressing#multicast
    TYPE_BROADCAST = "ff03::1";

    def __init__(self, content, target, sender, sendCount, isAck, hasBeenAcced, isDecoration):
        self.content = content
        self.target = target
        self.sender = sender
        self.sendCount = sendCount
        self.isACK = isAck
        self.hasBeenAcced = hasBeenAcced
        self.isSelfInformation = isDecoration

    def getSender(self):
        return self.sender
    def getTarget(self):
        return self.target

    def getContent(self):
        return self.content

    def isBroadCast(self):
        return self.target == Message.TYPE_BROADCAST

    def isDecoration(self):
        return self.isSelfInformation

    def doSend(self):
        self.sendCount = self.sendCount + 1

    def toString(self):
        tuple = [self.content, self.target, self.sender, self.sendCount, self.isACK, self.hasBeenAcced, self.isSelfInformation]
        return ubinascii.b2a_base64(json.dumps(tuple))

    def fromString(strData):

        rawText = ubinascii.a2b_base64(strData)
        tuple = json.loads(rawText);
        content, target, sender, sendCount, isACK, hasBeenAcced, isSelfInformation = tuple
        message = Message(content, target, sender, sendCount, isACK, hasBeenAcced, isSelfInformation)

        return message

    def isAccForMessage(self, message):
        return self.content == message.content and self.sender == message.target
