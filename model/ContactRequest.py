
import ubinascii
import json

class ContactRequest:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def toString(self):
        tuple = [self.name, self.phone]
        return ubinascii.b2a_base64(json.dumps(tuple))

    def fromString(strData):
        rawText = ubinascii.a2b_base64(strData)
        tuple = json.loads(rawText);
        name, phone = tuple
        return ContactRequest(name, phone)
