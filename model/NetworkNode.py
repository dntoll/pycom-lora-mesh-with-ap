

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
