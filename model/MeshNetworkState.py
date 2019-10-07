

from model.Message import Message
from model.NetworkNode import NetworkNode
from model.NetworkNodeDecoration import NetworkNodeDecoration

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

    def getAllNodesMacs(self):
        allNodes = set(self.others.keys()) | set(self.routers.keys()) | set(self.neighbors.keys())

        #remove self
        if self.selfDecoration.mac in allNodes:
            allNodes.remove(self.selfDecoration.mac)

        #remove the 0 node added into routers?
        if 0 in allNodes:
            allNodes.remove(0)
        if "0" in allNodes:
            allNodes.remove("0")
        return allNodes

    def getMyNodFullInformation(self):
        return self.getNodeCompleteInfo(self.me.getMac())

    def getOthersAsFullInformationList(self):
        allNodes = self.getAllNodesMacs()
        ret = []
        for mac in allNodes:
            ret.append(self.getNodeCompleteInfo(mac))
        return ret

    def getNodeCompleteInfo(self, mac):

        ip = "no info"
        name = "no info"
        mlEID = "no info"
        role = "no info"
        rssi = "no info"
        age = "no info"
        id = "no info"
        path_cost = "no info"
        firmware = "not set"
        clients = []

        if self.me.mac == str(mac):
            ip = self.me.ip
            role = self.me.role
            name = self.selfDecoration.name
            mlEID = self.selfDecoration.mlEID
            firmware = self.selfDecoration.firmware
        else:
            if mac in self.neighbors:
                node = self.neighbors[mac]
                ip = node.ip
                role = node.role
                rssi = node.rssi
                age = node.age
            if mac in self.others:
                node = self.others[mac]
                name = node.name
                mlEID = node.mlEID
                firmware = node.firmware
            if mac in self.routers:
                node = self.routers[mac]
                age = node.age
                id = node.id
                path_cost = node.path_cost
        ret = {
            "mac" : mac,
            "ip" : ip,
            "name" : name,
            "mlEID" : mlEID,
            "role" : role,
            "rssi" : rssi,
            "age" : age,
            "id" : id,
            "path_cost" : path_cost,
            "firmware" : firmware,
        }
        return ret;

    def setSelfInfo(self, newIP, mac, role, rloc):
        self.me = NetworkNode(newIP, mac, role, rloc, 0, 0, 0, 0)
        self.selfDecoration.mlEID = newIP
        self.selfDecoration.mac = mac

    def getMac(self):
        return self.me.getMac()

    def getIPFromMac(self, mac):
        if mac == self.me.mac:
            return self.me.ip
        elif mac in self.neighbors:
            return self.neighbors[mac].rloc16
        elif mac in self.others:
            return self.others[mac].mlEID
        elif mac == Message.TYPE_BROADCAST:
            return Message.TYPE_BROADCAST
        else:
            raise Exception("this address has no receiver");

    def isDirectedToMe(self, targetAddress):
        if targetAddress == self.me.mac:
            return True
        return False

    def updateOthersDecorations(self, otherDecorationMessage):
        info = NetworkNodeDecoration.fromString(otherDecorationMessage.content)
        self.others[str(info.mac)] = info


    def setNeighbors(self, neigbors, neighbors_ip, routers, ipaddr):
        if neigbors is not None:
            for id, neigh in enumerate(neigbors):
                nn = NetworkNode(neighbors_ip[id], neigh.mac, neigh.role, neigh.rloc16, neigh.rssi, neigh.age, 0, 0)
                self.neighbors[str(neigh.mac)] = nn

        if routers is not None:
            for r in routers:
                nn = NetworkNode(0, r.mac, 0, r.rloc16, 0, r.age, r.id, r.path_cost) #id=0, path_cost=0,
                self.routers[str(r.mac)] = nn
        #print(neigbors); #[(mac=8121069065175678681, role=3, rloc16=7168, rssi=-26, age=30)]
        #print(neigbors_ips); #['fdde:ad00:beef:0:0:ff:fe00:1c00']
        #print(routers); #[(mac=0, rloc16=0, id=0, path_cost=0, age=0), (mac=8121069065175678681, rloc16=7168, id=7, path_cost=0, age=30), (mac=0, rloc16=21504, id=21, path_cost=0, age=122)]
        #print(ipaddr);
