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
