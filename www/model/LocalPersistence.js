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
       ret.contacts = JSON.parse(x);
       return ret
    }
  }

  this.storePhoneBook = function(phoneBook) {

    localStorage.setItem(phoneBookIndex, JSON.stringify(phoneBook.contacts));
  }
}
