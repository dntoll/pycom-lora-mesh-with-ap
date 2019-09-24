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
        message = Message.fromString(strData)

        print(message);

        messageBoard.receiveMessage(message);


class MeshChat:
    def __init__(self, messageBoard):
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
        self.ip = self.mesh.ip()
        self.messageBoard = messageBoard
        #print("self.ip")
        #print(self.ip)


    def update(self):
        # check if topology changes, maybe RLOC IPv6 changed
        new_ip = self.mesh.ip()
        if self.ip != new_ip:
            print("IP changed from: %s to %s"%(self.ip, new_ip))
            self.ip = new_ip

        if not self.mesh.is_connected():
            self.mesh.led_state()
            print("%d: State %s, single %s"%(time.time(), self.mesh.cli('state'), self.mesh.cli('singleton')))
        else:
            #print('Neighbors found: %s'%self.mesh.neighbors())

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
