#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#
from LoraMeshChatApplication import LoraMeshChatApplication
import pycom
import model
import view

pycom.wifi_on_boot(False)
pycom.heartbeat(False)

app = LoraMeshChatApplication()
print("init done");
while True:
    app.update()
