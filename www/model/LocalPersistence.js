function LocalPersistance() {
  let keyIndex = "LocalPersistance.storedPersonalInformation.2";

  this.getStoredPersonalInformation = function() {
    let x = localStorage.getItem(keyIndex)

    if ( x === null)
      return new PersonalInformation("+4670...", "Not set", "Secret passfrase");
    else {
      return  JSON.parse(x);
    }
  }

  this.storePersonalInformation = function(pi) {
    localStorage.setItem(keyIndex, JSON.stringify(pi));
  }
}
