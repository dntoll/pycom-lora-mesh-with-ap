function EncryptedMessage(contact, message, senderPersonalInfo) {
  var d = new Date();
  let time = d.getTime();
  let enMess = cryptico.encrypt(message, contact.publicKeyString, senderPersonalInfo.myRSAKey)

  let payload = {
    name : contact.name,
    key : contact.publicKeyString,
    content : enMess
  }

  jsonString = JSON.stringify(payload);

  this.sender = "setByServer";
  this.target = contact.lastSeenMac;
  this.content = jsonString;
  this.time = time;
  this.type = 0;
  this.sendCount = 0;
}
