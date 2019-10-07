


class Contact:
    def __init__(self, phoneNumber, name, publicKeyString, time, lastSeenMac):
        self.phoneNumber = phoneNumber
        self.name = name
        self.publicKeyString = publicKeyString
        self.time = time
        self.lastSeenMac = lastSeenMac;

    def toDictionary(self):
        return {
            "phoneNumber": self.phoneNumber,
            "name": self.name,
            "publicKeyString": self.publicKeyString,
            "time": self.time,
            "lastSeenMac": self.lastSeenMac,
        }
