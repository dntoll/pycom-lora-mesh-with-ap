function Contact(name, phoneNumber, publicKeyString, time, lastSeenMac ) {
  this.name = name;
  this.phoneNumber = phoneNumber;
  this.publicKeyString = publicKeyString;
  this.time = time;
  this.lastSeenMac = lastSeenMac

  this.equals = function(other) {
    return (this.name === other.name &&
      this.phoneNumber === other.phoneNumber &&
      this.publicKeyString === other.publicKeyString &&
      this.time === other.time &&
      this.lastSeenMac === other.lastSeenMac)
  }

  this.getUniqueID = function() {
    return sha1(this.name + this.phoneNumber + this.publicKeyString + this.time + this.lastSeenMac)
  }
}
