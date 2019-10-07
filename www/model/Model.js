



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
    api.updateMessages(this);
    api.updateNetwork(this);
  }

  this.onTick = function() {
    api.updateMessages(this);
    api.updateNetwork(this);
  }

  this.updatePersonalInformation = function(personalInformation, observer) {
    this.personalInformation = personalInformation;
    persistance.storePersonalInformation(this.personalInformation);
    api.updatePersonalInformation(this.personalInformation, observer);
  }

  this.sendMessage = function(message, observer) {
    api.sendMessage(message, observer);
  }

  this.searchForContact = function(contactRequest, contactResultTarget) {
    api.searchForContact(contactRequest, contactResultTarget)
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
