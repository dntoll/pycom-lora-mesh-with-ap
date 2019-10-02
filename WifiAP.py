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

from network import WLAN

import machine
import ubinascii

class WifiAP:
    def __init__(self):

        self.ID = str(ubinascii.hexlify(machine.unique_id()))[2:-1]
        print("My ssid:")
        print(self.ID);
        '''
        self.wlan = WLAN(mode=WLAN.AP, ssid=self.ID, auth=(WLAN.WPA2, 'Own password'), channel=11, antenna=WLAN.INT_ANT)
        self.wlan.ifconfig(id=1, config=('192.168.1.1', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
        print("done configuring");
        '''
        wlan = WLAN()
        wlan.init(mode=WLAN.STA)
        nets = wlan.scan()
        for net in nets:
            if net.ssid == 'Minecraft':
                print('Network found!')
                wlan.connect(net.ssid, auth=(net.sec, 'GudmundsV4genIsTheBest'), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
                    print('WLAN connection succeeded!')
                    break
