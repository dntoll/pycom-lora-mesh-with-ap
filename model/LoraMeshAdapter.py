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

from loramesh import Loramesh
from network import LoRa
from model.Message import Message

import ubinascii
import binascii
import pycom
import time
import socket
import machine
import json
from builtins import int


def receive_pack(tuple):
    try:
        #print("receive_pack:" + repr(tuple))
        sockets, messageBoard = tuple
        #print("receive_pack called")
        # listen for incomming packets
        for s in sockets:
            rcv_data, rcv_addr = s.recvfrom(4096)
            if len(rcv_data) == 0:
                break
            rcv_ip = rcv_addr[0]
            rcv_port = rcv_addr[1]

            strData = rcv_data.decode();
            message = Message.fromString(strData)
            messageBoard.receiveMessage(message)
            print("Received message from " + str(message.getSender()) + " " + str(message.type))

    except Exception as e:
        print("something went wrong in receive_pack " + repr(tuple))
        raise e


class NoRecipientException(Exception):
    pass

class LoraMeshAdapter:
    def __init__(self, messageBoard, meshNetworkState):
        self.messageBoard = messageBoard
        self.meshNetworkState = meshNetworkState;


        self.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=7)
        mac = self.lora.mac();
        self.MAC = str(int.from_bytes(mac, 'big')) #str(ubinascii.hexlify(self.lora.mac()))[2:-1]
        #print("MAC" + str(self.MAC));
        print("pre loramesh")
        self.mesh = Loramesh(self.lora)
        print("Lora mesh complete")
        sockets = []
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.myport = 1234
        self.s.bind(self.myport)
        sockets.append(self.s)
        self.mesh.mesh.rx_cb(receive_pack, (sockets, messageBoard))
        self.pack_num = 0

        self.meshNetworkState.setSelfInfo(self.mesh.ip(), self.MAC, self.mesh.state, self.mesh.rloc);

    def getIP(self):
        return self.mesh.ip();

    def getNeighbors(self):
        return self.mesh.neighbors_ip();

    def update(self):
        # check if topology changes, maybe RLOC IPv6 changed
        self.meshNetworkState.setSelfInfo(self.mesh.ip(), self.MAC, self.mesh.state, self.mesh.rloc);

        self.mesh.led_state()
        if not self.mesh.is_connected():
            print("%d: State %s, single %s"%(time.time(), self.mesh.cli('state'), self.mesh.cli('singleton')))
        else:
            #Update mesh information
            self.meshNetworkState.setNeighbors(self.mesh.neighbors(), self.mesh.neighbors_ip(), self.mesh.mesh.routers(), self.mesh.mesh.ipaddr())
            neigbors = self.mesh.neighbors_ip()
            print("%d neighbors, IPv6 list: %s"%(len(neigbors), neigbors))

            for key, message in self.messageBoard.getMessagesToBeSent().items():
                message.doSend();
                try:
                    theContent = message.toString();
                    ipTarget = self.meshNetworkState.getIPFromMac(message.target)
                    self.s.sendto(theContent, (str(ipTarget), self.myport))
                    print('Sent message to ' + message.target + " : " + ipTarget + " " + str(message.type)) #, repr(theContent)))
                except NoRecipientException as nre:
                    print("Could not send message to " + repr(message.target) + " since no ip was found...")
                except Exception as e:
                    print("something went wrong when sending message " + repr(e))
                    raise e
            self.messageBoard.sendCompleted() #remove accs etc..
