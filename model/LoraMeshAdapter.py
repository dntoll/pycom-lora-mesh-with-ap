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

import pycom
import time
from pymesh_config import PymeshConfig
from pymesh import Pymesh

#from loramesh import Loramesh
#from network import LoRa
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


def receive_pack(rcv_ip, rcv_port, rcv_data):

    ''' callback triggered when a new packet arrived '''
    print('Incoming %d bytes from %s (port %d):' %
            (len(rcv_data), rcv_ip, rcv_port))
    print(rcv_data)

    try:
        if len(rcv_data) == 0:
            return

        strData = rcv_data.decode();
        message = Message.fromString(strData)
        messageBoard.lock();
        messageBoard.receiveMessage(message)
        messageBoard.unlock();
        print("Received message from " + str(message.getSender()) + " " + str(message.type))

    except Exception as e:
        print("something went wrong in receive_pack " + repr(e))
        #raise e


class LoraMeshAdapter:
    def __init__(self, messageBoard):
        self.messageBoard = messageBoard
        pymesh_config = PymeshConfig.read_config()
        print("pre Pymesh");
        self.pymesh = Pymesh(pymesh_config, receive_pack)
        print("post Pymesh");

        self.pack_num = 0

    def getMAC(self):
        return self.pymesh.mac();

    def isConnected(self):
        return self.pymesh.is_connected()

    def update(self):
        # check if topology changes, maybe RLOC IPv6 changed

        if not self.isConnected():
            print("still not connected")
        else:
            print("connected")

            self.messageBoard.lock();
            for key, message in self.messageBoard.getMessagesToBeSent().items():
                message.doSend();
                try:
                    theContent = message.toString();

                    self.pymesh.send_mess(message.target, theContent)
                    print('Sent message to ' + message.target + " : " + str(message.type)) #, repr(theContent)))
                except NoRecipientException as nre:
                    print("Could not send message to " + repr(message.target) + " since no ip was found...")
                except Exception as e:
                    print("something went wrong when sending message " + repr(e) + " " + str(len(message.toString())))
                    print('Tried to send message to ' + message.target);
                    #raise e
            self.messageBoard.sendCompleted() #remove accs etc..
            self.messageBoard.unlock();
