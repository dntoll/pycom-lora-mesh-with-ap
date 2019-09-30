
#This encapsulates the information we can get through the interfaces of loramesh
class NetworkNode:
    def __init__(self, ip, mac, role, rloc16, rssi, age, id, path_cost):
        self.ip = ip
        self.mac = mac
        self.role = role
        self.rloc16 = rloc16
        self.rssi = rssi
        self.age = age
        self.id = id
        self.path_cost = path_cost

    def setIP(self, newIP):
        self.ip = newIP
    def getIP(self):
        return self.ip

import json
import ubinascii

#This encapsulates the information we want to sent to others
class NetworkNodeDecoration:
    def __init__(self, name, mac, mlEID, clientsConnectedAtMySite):
        self.name = name
        self.mlEID = mlEID
        self.mac = mac
        self.clientsConnectedAtMySite = clientsConnectedAtMySite

    def getIP(self):
        return self.mlEID

    def toString(self):
        tuple = [self.name, self.mac, self.mlEID, self.clientsConnectedAtMySite]
        return ubinascii.b2a_base64(json.dumps(tuple))

    def fromString(strData):

        rawText = ubinascii.a2b_base64(strData)
        tuple = json.loads(rawText);

        name, mac, mlEID, clientsConnectedAtMySite = tuple

        decoration = NetworkNodeDecoration(name, mac, mlEID, clientsConnectedAtMySite)

        return decoration


class MeshNetworkState:


    def __init__(self, selfDecoration):
        self.me = NetworkNode(0, 0, 0, 0, 0, 0, 0, 0)

        self.selfDecoration = selfDecoration;
        self.others = {}
        self.neighbors = {}
        self.routers = {}

    def getNeighbors(self):
        return self.neighbors
    def getRouters(self):
        return self.routers
    def getOthers(self):
        return self.others

    def setSelfInfo(self, newIP, mac, role, rloc):
        self.me = NetworkNode(newIP, mac, role, rloc, 0, 0, 0, 0)
        self.selfDecoration.mlEID = newIP
        self.selfDecoration.mac = mac

    def getIP(self):
        return self.me.getIP()
    def isDirectedToMe(self, targetAddress):

        if targetAddress == self.me.rloc16:
            return true
        elif targetAddress == self.me.ip:
            return true
        return False

    def updateOthersDecorations(self, otherDecorationMessage):
        info = NetworkNodeDecoration.fromString(otherDecorationMessage.content)

        self.others[info.mac] = info


    def setNeighbors(self, neigbors, neighbors_ip, routers, ipaddr):
        if neigbors is not None:
            for id, neigh in enumerate(neigbors):
                nn = NetworkNode(neighbors_ip[id], neigh.mac, neigh.role, neigh.rloc16, neigh.rssi, neigh.age, 0, 0)
                self.neighbors[neigh.mac] = nn

        if routers is not None:
            for r in routers:
                nn = NetworkNode(0, r.mac, 0, r.rloc16, 0, r.age, r.id, r.path_cost) #id=0, path_cost=0,
                self.routers[r.mac] = nn
        #print(neigbors); #[(mac=8121069065175678681, role=3, rloc16=7168, rssi=-26, age=30)]
        #print(neigbors_ips); #['fdde:ad00:beef:0:0:ff:fe00:1c00']
        #print(routers); #[(mac=0, rloc16=0, id=0, path_cost=0, age=0), (mac=8121069065175678681, rloc16=7168, id=7, path_cost=0, age=30), (mac=0, rloc16=21504, id=21, path_cost=0, age=122)]
        #print(ipaddr);
