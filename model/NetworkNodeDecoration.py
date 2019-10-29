import json
import ubinascii

#This encapsulates the information we want to sent to others
class NetworkNodeDecoration:
    def __init__(self, name, mac, firmware):
        self.name = name
        self.mac = mac
        self.firmware = firmware


    def toString(self):
        tuple = [self.name, self.mac, self.firmware]
        return ubinascii.b2a_base64(json.dumps(tuple))

    def fromString(strData):

        rawText = ubinascii.a2b_base64(strData)
        tuple = json.loads(rawText);

        name, mac, firmware = tuple

        decoration = NetworkNodeDecoration(name, mac, firmware)

        return decoration
