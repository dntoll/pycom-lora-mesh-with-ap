



function Model() {
  let api = new API();
  let persistance = new LocalPersistance();

  this.toBeSent = [];
  this.sent = [];
  this.received = [];
  this.others = [];
  this.me = new NetworkNode();

  this.onLoad = function() {
    this.personalInformation = persistance.getStoredPersonalInformation();
    this.phoneBook = persistance.getStoredPhoneBook()
    api.updateMessages(this);
    api.updateNetwork(this);
  }

  this.onTick = function(updateObserver) {
    api.updateMessages(this);
    api.updateNetwork(this);
    api.updateSearchResult(updateObserver);
  }

  this.updatePersonalInformation = function(personalInformation, observer) {
    this.personalInformation = personalInformation;
    persistance.storePersonalInformation(this.personalInformation);
    api.updatePersonalInformation(this.personalInformation, observer);
  }

  this.addContact = function(contact) {
    this.phoneBook.addContact(contact)
    persistance.storePhoneBook(this.phoneBook)
  }

  this.removeContact = function(contact) {
    this.phoneBook.removeContact(contact)
    persistance.storePhoneBook(this.phoneBook)
  }

  this.sendMessage = function(message, observer) {
    api.sendMessage(message, observer);
  }

  this.searchForContact = function(contactRequest, contactResultTarget) {
    api.searchForContact(contactRequest, contactResultTarget, false)
  }

  this.updateMessages = function(toBeSent, sent, received) {
    this.toBeSent = toBeSent;
    this.sent = sent;
    this.received = received;
  }

  this.updateNeighbors = function(me, others) {
    this.me = me;
    this.others = others;
  }


}
