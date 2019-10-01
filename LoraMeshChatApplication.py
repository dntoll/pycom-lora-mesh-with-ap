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

from WifiAP import WifiAP
from WebServer import WebServer
from LoraMeshAdapter import LoraMeshAdapter
from MeshNetworkState import MeshNetworkState
from NetworkNodeDecoration import NetworkNodeDecoration
from MessageBoard import MessageBoard
from WebClientView import WebClientView
from FirmwareHasher import FirmwareHasher
from Message import Message
import time
import machine

class LoraMeshChatApplication:
    """ Class for chatting over Lora """

    def __init__(self):
        self.timeToSendSelfInfo = 10;
        self.ap = WifiAP()

        firmware = FirmwareHasher.calculate();
        print("Code firmware: " + str(firmware))

        self.decoration = NetworkNodeDecoration(self.ap.ID, -1, -1, firmware, {})
        self.meshState = MeshNetworkState(self.decoration)
        self.messageBoard = MessageBoard(self.meshState)


        self.mesh = LoraMeshAdapter(self.messageBoard, self.meshState)
        self.view = WebClientView(self.messageBoard, self.meshState)


        self.www = WebServer(self.view)


    def update(self):
        self.mesh.update();
        # random sleep time
        #print("sleeping update")
        time.sleep(10)

        self.timeToSendSelfInfo -= 10
        if self.timeToSendSelfInfo <= 0:
            self.timeToSendSelfInfo = 40;
            self.messageBoard.sendMessage(Message(self.decoration.toString(), Message.TYPE_BROADCAST, self.meshState.getIP(), 0, False, False, True))

        #time.sleep(5)
        #self.www.handleAccept();
