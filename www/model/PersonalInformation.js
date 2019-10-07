function PersonalInformation(phone, name, passfrase) {
  const Bits = 128;
  var d = new Date();
  this.time = d.getTime();
  this.phone = phone;
  this.name = name;
  this.passfrase = passfrase;
  this.myRSAKey = cryptico.generateRSAKey(passfrase, Bits);
  this.publicKey = cryptico.publicKeyString(this.myRSAKey);
}
