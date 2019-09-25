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
from Message import Message

import ubinascii
import pycom
import time
import socket
import machine
import json


def receive_pack(tuple):
    sockets, messageBoard = tuple
    #print("receive_pack called")
    # listen for incomming packets
    for s in sockets:
        rcv_data, rcv_addr = s.recvfrom(128)
        if len(rcv_data) == 0:
            break
        rcv_ip = rcv_addr[0]
        rcv_port = rcv_addr[1]
    #    print('Incomming %d bytes from %s (port %d)'%(len(rcv_data), rcv_ip, rcv_port))
    #    print(rcv_data)

        strData = rcv_data.decode();
        try:
            message = Message.fromString(strData)
            print(message);
            messageBoard.receiveMessage(message)
        except Exception as e:
            print("something went wrong in receive_pack" + repr(e) +" Data: "+ repr(strData))
            pass


class LoraMeshAdapter:
    def __init__(self, messageBoard, meshNetworkState):
        self.messageBoard = messageBoard
        self.meshNetworkState = meshNetworkState;

        pycom.wifi_on_boot(False)
        pycom.heartbeat(False)
        self.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_125KHZ, sf=7)
        self.MAC = str(ubinascii.hexlify(self.lora.mac()))[2:-1]
        self.mesh = Loramesh(self.lora)
        sockets = []
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.myport = 1234
        self.s.bind(self.myport)
        sockets.append(self.s)
        self.mesh.mesh.rx_cb(receive_pack, (sockets, messageBoard))
        self.pack_num = 0

        self.meshNetworkState.setSelfInfo(self.mesh.ip(), self.MAC, self.mesh.state, self.mesh.rloc);


        #print("self.ip")
        #print(self.ip)

    def getIP(self):
        return self.mesh.ip();

    def getNeighbors(self):
        return self.mesh.neighbors_ip();

    def update(self):
        # check if topology changes, maybe RLOC IPv6 changed
        self.meshNetworkState.setSelfInfo(self.mesh.ip(), self.MAC, self.mesh.state, self.mesh.rloc);

        if not self.mesh.is_connected():
            self.mesh.led_state()
            print("%d: State %s, single %s"%(time.time(), self.mesh.cli('state'), self.mesh.cli('singleton')))
        else:
            self.meshNetworkState.setNeighbors(self.mesh.neighbors(), self.mesh.neighbors_ip(), self.mesh.mesh.routers(), self.mesh.mesh.ipaddr())

            self.mesh.led_state()
            #print("%d: State %s, single %s"%(time.time(), self.mesh.cli('state'), self.mesh.cli('singleton')))

            # update neighbors list
            neigbors = self.mesh.neighbors_ip()
            print("%d neighbors, IPv6 list: %s"%(len(neigbors), neigbors))

            # send PING and UDP packets to all neighbors
            for neighbor in neigbors:
                '''if self.mesh.ping(neighbor) > 0:
                    print('Ping OK from neighbor %s'%neighbor)
                    self.mesh.blink(10, .1)
                else:
                    print('Ping not received from neighbor %s'%neighbor)

                #print("sleep after ping")
                time.sleep(1)'''


                for message in self.messageBoard.getMessagesToBeSent():
                    message.doSend();
                    try:
                        theContent = message.toString();
                        self.s.sendto(theContent, (neighbor, self.myport))
                        print('Sent message to %s %s'%(neighbor, repr(theContent)))
                    except Exception as e:
                        print("something went wrong" + repr(e))
                        pass
                    #sleep between neighbors
                    #print("sleep between neigbors")
                    time.sleep(1)
                self.messageBoard.sendCompleted()
