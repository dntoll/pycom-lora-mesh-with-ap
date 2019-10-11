# pycom-lora-mesh-with-ap

## vision
This project enables communication when there is no service, no internet, no power. Short messages are sent over a LoRa-Mesh network of cheap solar powered nodes that self-organise. Users connect to the closest node with their cellphone (WiFi-AP) and is able to send messages to users at other nodes. Messages are asynchronous.

## details
Dictionary

* System - The entire mesh
* User - A human using the system to send messages and find contacts
* Contact - Another user whom the first user has a relation established with.
  * phoneNumber, name and public key
* PhoneBook - The list of contacts in a client  (confusion with the phonebook class in the node... solve  this...)
* Client - The Webbrowser the user uses to communicate with the system, is connected to a Node
* Node - A Physical Node of the system
* Message - A Message sent in the System, can be different types.


User <-> Client <-http-> Node <-mesh-> Node 2 <-http-> Client 2 <-> User 2

 * Each Node can act as a WiFi Access Point (AP) and provides a web-interface to connected nodes on 192.168.1.1
 * Clients connect to a nearby Node
 * A JavaScript application runs in the Client browser and keeps personalized state.
 * The AP provides an API to discover other connected clients and search on phonenumber or names
 * The client encrypts messages which are delivered to the node on which

### Hardware

Each Node consists of:
 * pycom LoPy4 with
 * expansion board
 * LoRa antennae connected to the EU868
 * (Not tested) Solar panel with 5V converter, battery?

### installation
LoPy4 needs a firmware with pymesh enabled. This has been disabled in the newest releases.

Run pycom-fwtool, select developer mode and firmware 1.20.0.rc11 (developer)
Please note that the firmware is not a stable release.


## Use cases

## Administrator/Developer Use Cases

### decorate node information with name and location

### show network structure (Implemented)
In the interface
 * on routers show id and jumps (from mesh.routers())
 * show firmware and code version (perhaps md5(all code files)?)
 * Distribute all router IP-adresses and info about each router...
 * Distribute Node information to all nodes in mesh.

### show network structure (TODO)
 * Set masterkey and AP-access information in the interface
 * Set node name and attributes in interface (Eg. location, etc)
 * save information on the Network Node?

### Manage AP (TODO)
Swap between AP, WiFi-Client, Router mode with physical button on the nodes
  * start in router mode (no-wifi enabled) These nodes are for extending the network in locations without users
  * AP-WiFi
  * ATA-WiFi client but only if this is saved in AP settings

### Enter contact information (Implemented)
Starts when a User wants to connect to the network for the first time.
The contact information is needed to be discovered by other users, and to send messages.

Pre conditions:
 * User has connected her device to a network node AP or STA

Steps:
 * System presents option to input name, phoneNumber, name and passfrase
 * User provides name, phonenumber and passfrase
 * System presents that the information has been saved (TODO)

Post condition:
 * Users contact information is stored locally in the Client.

### discover user at other node with phone number (Implemented)
Starts when a User wants to find another user (add a Contact)

Pre condition:
 * The second user has added contact information

Steps:
 * System provides option to search on name or phoneNumber
 * User provides name or phoneNumber
 * System states search has started
 * Time passes
 * System provides search results as they come in from other nodes.
 * More than one result may appear with name, phoneNumber, Node-information, time and public key
 * User selects the user-result that indicates the requested user
 * System presents that the user has been added to Users PhoneBook

Post condition
 * Contact has been added to User PhoneBook

### send message to user at other node
Send to all?
 * Broadcast messages

### receive message directed to me





## tests

* range test (max range between nodes with different distance / obstacles )
* mesh-test (try to put one unreachable from first and send a message to it through the mesh
