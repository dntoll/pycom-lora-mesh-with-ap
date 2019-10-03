


from NetworkNode import NetworkNode
from NetworkNodeDecoration import NetworkNodeDecoration

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

    def setSelfInfo(self, newIP, mac, role, rloc):
        self.me = NetworkNode(newIP, mac, role, rloc, 0, 0, 0, 0)
        self.selfDecoration.mlEID = newIP
        self.selfDecoration.mac = mac

    def getIP(self):
        return self.me.getIP()
    def isDirectedToMe(self, targetAddress):

        if targetAddress == self.me.rloc16:
            return True
        elif targetAddress == self.me.ip:
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
