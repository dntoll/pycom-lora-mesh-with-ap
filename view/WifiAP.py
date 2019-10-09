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
        self.wlan = WLAN()
        self.wlan.disconnect()
        self.wlan.init(mode=WLAN.STA, antenna=WLAN.INT_ANT)
        found = False
        try:
            nets = self.wlan.scan()
            for net in nets:
                if net.ssid == 'Minecraft':
                    found = True
                    print('Network found!')
                    self.wlan.connect(net.ssid, auth=(net.sec, 'GudmundsV4genIsTheBest'), timeout=5000)
                    while not self.wlan.isconnected():
                        machine.idle() # save power while waiting
                        print('WLAN connection succeeded!')
                        break
        except OSError as e:
            print(repr(e))
            print("Failed To Setup Wifi as STA")

        if found is False:
            try:
                self.wlan.deinit()
                self.wlan = WLAN(mode=WLAN.AP, ssid=self.ID, auth=(WLAN.WPA2, 'Own password'), channel=11, antenna=WLAN.INT_ANT)
                self.wlan.ifconfig(id=1, config=('192.168.1.1', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
                print("Did set up own AP at: " +self.ID );
            except OSError as e:
                print(repr(e))
                print("Failed To Setup Wifi As AP")

        print(self.wlan.ifconfig())
