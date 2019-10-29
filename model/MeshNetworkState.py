

from model.Message import Message

from model.NetworkNodeDecoration import NetworkNodeDecoration
from model.NoRecipientException import NoRecipientException

class MeshNetworkState:


    def __init__(self, selfDecoration):
        self.selfDecoration = selfDecoration;
        self.others = {}

    def updateOthersDecorations(self, otherDecorationMessage):
        info = NetworkNodeDecoration.fromString(otherDecorationMessage.content)
        self.others[str(info.mac)] = info

    def getOthers(self):
        return self.others

    def getMe(self):
        return self.selfDecoration;

    def getAllNodesMacs(self):
        return self.others.keys();
