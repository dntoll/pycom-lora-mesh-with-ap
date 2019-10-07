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
import uhashlib

class Message:
    #https://openthread.io/guides/thread-primer/ipv6-addressing#multicast
    TYPE_BROADCAST = "ff03::1";
    IS_ACK = 1
    IS_DECORATION = 2
    IS_CONTACT_SEARCH = 3
    IS_OPEN_MESSAGE = 4
    IS_ENCRYPTED_MESSAGE = 5
    IS_CONTACT_FOUND = 6


    def __init__(self, content, target, sender, time, sendCount, type):
        self.content = content
        self.target = target
        self.sender = sender
        self.time = time

        #Meta information
        self.sendCount = sendCount
        self.type = type

    def getUniqueID(self):
        hasher = uhashlib.md5(str(self.content) + str(self.target) + str(self.sender) + str(self.time))
        return ubinascii.hexlify(hasher.digest()).decode()

    def getSender(self):
        return self.sender
    def getTarget(self):
        return self.target

    def getContent(self):
        return self.content

    def isBroadCast(self):
        return self.target == Message.TYPE_BROADCAST

    def isDecoration(self):
        return self.type == Message.IS_DECORATION

    def isACK(self):
        return self.type == Message.IS_ACK

    def isContactSearch(self):
        return self.type == Message.IS_CONTACT_SEARCH

    def isContactFound(self):
        return self.type == Message.IS_CONTACT_FOUND


    def doSend(self):
        self.sendCount = self.sendCount + 1

    def toString(self):
        tuple = [self.content, self.target, self.sender, self.time, self.sendCount, self.type]
        return ubinascii.b2a_base64(json.dumps(tuple))

    def toDictionary(self):
        dict = {
            "content" : self.content,
            "target" : self.target,
            "sender" : self.sender,
            "sendCount" : self.sendCount,
            "type" : self.type,
            "time" : self.time
        }
        return dict

    def fromString(strData):

        rawText = ubinascii.a2b_base64(strData)
        tuple = json.loads(rawText);
        content, target, sender, time, sendCount, type = tuple
        message = Message(content, target, sender, time, sendCount, type)

        return message

    def isAccForMessage(self, message):
        return self.content == message.content and self.sender == message.target and self.time == message.time
