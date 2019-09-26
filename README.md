# pycom-lora-mesh-with-ap

## vision
This project enables communication when there is no service, no internet, no power. Short messages are sent over a LoRa-Mesh network of cheap solar powered nodes that self-organise. Users connect to the closest node with their cellphone (Wifi-AP) and is able to send messages to users at other nodes. Messages are assynchronous.

## details
Hardware: lopy4 with expansion boards and antennae. Solar panel with 5V converter

### installation
lopy4 needs a firmware with pymesh enabled. This has been disabled in the newest releases.

Run pycom-fwtool, select developer mode and firmware 1.20.0.rc11 (developer)


## Todo:

In the interface
 * on routers show id and jumps (from mesh.routers())
 * show firmware and code version (perhaps md5(all code files)?)

Distribute all router ip-adresses and info about each router...
 * Set node name and attributes in interface (Eg. location, users etc)
 * Set masterkey and AP information in the intetface
 * save this?
 * Distribute this information to all nodes in mesh.

Send to all
 * Broadcast messages

## Use cases

### send message to user at other node

### receive message directed to me

### discover user at other node with phone number

### decorate node information with name and location

### show network structure

## tests

* range test (max range between nodes with different distance / obstacles )
* mesh-test (try to put one unreachable from first and send a message to it through the mesh
