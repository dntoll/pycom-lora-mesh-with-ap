
class NetworkNode:
    def __init__(self, ip, mac, role, rloc16, rssi, age):
        self.ip = ip
        self.mac = mac
        self.role = role
        self.rloc16 = rloc16
        self.rssi = rssi
        self.age = age

    def setIP(self, newIP):
        self.ip = newIP
    def getIP(self):
        return self.ip

class MeshNetworkState:


    def __init__(self):
        self.me = NetworkNode(0, 0, 0, 0, 0, 0)
        self.neighbors = []
        self.routers = []

    def getNeighbors(self):
        return self.neighbors
    def getRouters(self):
        return self.routers

    def setSelfInfo(self, newIP, mac, role, rloc):
        self.me = NetworkNode(newIP, mac, role, rloc, 0, 0)

    def getIP(self):
        return self.me.getIP()

    def setNeighbors(self, neigbors, neighbors_ip, routers, ipaddr):
        self.neighbors = []
        self.routers = []

        if neigbors is not None:
            for id, neigh in enumerate(neigbors):
                nn = NetworkNode(neighbors_ip[id], neigh.mac, neigh.role, neigh.rloc16, neigh.rssi, neigh.age)
                self.neighbors.append(nn)

        if routers is not None:
            for r in routers:
                nn = NetworkNode(0, r.mac, "?", r.rloc16, "?", r.age) #id=0, path_cost=0,
                self.routers.append(nn)
        #print(neigbors); #[(mac=8121069065175678681, role=3, rloc16=7168, rssi=-26, age=30)]
        #print(neigbors_ips); #['fdde:ad00:beef:0:0:ff:fe00:1c00']
        #print(routers); #[(mac=0, rloc16=0, id=0, path_cost=0, age=0), (mac=8121069065175678681, rloc16=7168, id=7, path_cost=0, age=30), (mac=0, rloc16=21504, id=21, path_cost=0, age=122)]
        #print(ipaddr);
