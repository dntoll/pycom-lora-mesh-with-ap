function LocalPersistance() {
  let personalInformationIndex = "LocalPersistance.storedPersonalInformation";
  let phoneBookIndex = "LocalPersistance.storedPhoneBook2";

  this.getStoredPersonalInformation = function() {
    let x = localStorage.getItem(personalInformationIndex)

    if ( x === null)
      return new PersonalInformation("+4670...", "Not set", "Secret passfrase");
    else {
      return  JSON.parse(x);
    }
  }

  this.storePersonalInformation = function(pi) {
    localStorage.setItem(personalInformationIndex, JSON.stringify(pi));
  }

  this.getStoredPhoneBook = function() {
    let x = localStorage.getItem(phoneBookIndex)

    let ret = new PhoneBook();
    if ( x === null)
      return ret;
    else {
        let jsonObjects = JSON.parse(x);
        for (index in jsonObjects) {
          let contact = jsonObjects[index];
          ret.addContact(new Contact(contact.name, contact.phoneNumber, contact.publicKeyString, contact.time, contact.lastSeenMac))
        }
        return ret
    }
  }

  this.storePhoneBook = function(phoneBook) {

    localStorage.setItem(phoneBookIndex, JSON.stringify(phoneBook.contacts));
  }
}
