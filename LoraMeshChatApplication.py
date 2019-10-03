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

import model
import view

from model.MessageBoard import MessageBoard
from model.Message import Message
from model.LoraMeshAdapter import LoraMeshAdapter
from model.MeshNetworkState import MeshNetworkState
from model.NetworkNodeDecoration import NetworkNodeDecoration


from controller.WebClientController import WebClientController
from view.WebClientView import WebClientView
from view.WifiAP import WifiAP
from view.WebServer import WebServer
from FirmwareHasher import FirmwareHasher

import time
import machine
import utime

class LoraMeshChatApplication:
    """ Class for chatting over Lora """

    def __init__(self):
        self.timeToSendSelfInfo = 10;
        self.ap = WifiAP()

        firmware = FirmwareHasher.calculate();
        print("Code firmware: " + str(firmware))

        self.decoration = NetworkNodeDecoration(self.ap.ID, -1, -1, firmware, [])
        self.meshState = MeshNetworkState(self.decoration)
        self.messageBoard = MessageBoard(self.meshState)
        self.mesh = LoraMeshAdapter(self.messageBoard, self.meshState)

        self.view = WebClientView(self.messageBoard, self.meshState)
        self.controller = WebClientController(self.messageBoard, self.meshState, self.view)

        self.www = WebServer(self.controller)


    def update(self):
        self.mesh.update();
        # random sleep time
        #print("sleeping update")
        time.sleep(10)

        self.timeToSendSelfInfo -= 10
        if self.timeToSendSelfInfo <= 0:
            self.timeToSendSelfInfo = 40;
            self.messageBoard.sendMessage( Message(self.decoration.toString(), Message.TYPE_BROADCAST, self.meshState.getIP(), utime.time(), 0, False, False, True))
