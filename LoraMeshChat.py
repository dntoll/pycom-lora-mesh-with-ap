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
from MeshChat import MeshChat
from MessageBoard import MessageBoard
from WebClientView import WebClientView
import time
import machine

class LoraMeshChat:
    """ Class for chatting over Lora """

    def __init__(self):
        self.messageBoard = MessageBoard()

        self.view = WebClientView(self.messageBoard)
        self.mesh = MeshChat(self.messageBoard)
        self.ap = WifiAP()
        self.www = WebServer(self.view, self.messageBoard)


    def update(self):
        self.mesh.update();
        # random sleep time
        #print("sleeping update")
        time.sleep(2)
        #time.sleep(5)
        #self.www.handleAccept();
