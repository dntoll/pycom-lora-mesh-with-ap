# pycom-lora-mesh-with-ap

## vision
This project enables communication when there is no service, no internet, no power. Short messages are sent over a LoRa-Mesh network of cheap solar powered nodes that self-organise. Users connect to the closest node with their cellphone (Wifi-Ap) and is able to send messages to users at other nodes. Messages are assynchronous. 

## details
Hardware: lopy4 with expansion boards and antennae. Solar panel with 5V converter

### installation
lopy4 needs a firmware with pymesh enabled. This has been disabled in the newest releases.

Run pycom-fwtool, select developer mode and firmware 1.20.0.rc11 (developer)

## Use cases

### send message to user at other node

### receive message directed to me

### discover user at other node with phone number

### decorate node information with name and location

### show network structure

## tests
