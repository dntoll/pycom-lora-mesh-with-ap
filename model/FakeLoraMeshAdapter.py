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

from model.Message import Message
from model.NoRecipientException import NoRecipientException
import ubinascii
import binascii
import pycom
import time
import socket
import machine
import json
from builtins import int



class FakeLoraMeshAdapter:
    def __init__(self, messageBoard, meshNetworkState):
        self.messageBoard = messageBoard
        self.meshNetworkState = meshNetworkState;
        self.MAC = 'IFAKEITIFIWANT' #str(ubinascii.hexlify(self.lora.mac()))[2:-1]
        self.meshNetworkState.setSelfInfo("IFAKEITIFIWANT", self.MAC, 1, "IFAKEITIFIWANT");

    def getIP(self):
        return "IFAKEITIFIWANT";

    def getNeighbors(self):
        return [];

    def update(self):
        # check if topology changes, maybe RLOC IPv6 changed
        self.messageBoard.lock();
        for key, message in self.messageBoard.getMessagesToBeSent().items():
            message.doSend();
            try:
                theContent = message.toString();
                ipTarget = self.meshNetworkState.getIPFromMac(message.target)
                if ipTarget is self.MAC:
                    self.messageBoard.receiveMessage(message)
                else:
                    self.messageBoard.receiveMessage(Message(message.content, message.sender, message.target, message.time, 0, Message.IS_ACK))
                #self.s.sendto(theContent, (str(ipTarget), self.myport))
                print('Sent message to ' + message.target + " : " + ipTarget + " " + str(message.type)) #, repr(theContent)))
            except NoRecipientException as nre:
                print("Could not send message to " + repr(message.target) + " since no ip was found...")
            except Exception as e:
                print("something went wrong when sending message " + repr(e) + " " + str(len(message.toString())))
                ipTarget = self.meshNetworkState.getIPFromMac(message.target)
                print('Tried to send message to ' + message.target + " " + str(ipTarget));
                #raise e
        self.messageBoard.sendCompleted() #remove accs etc..
        self.messageBoard.unlock();
