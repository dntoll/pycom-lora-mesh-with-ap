function API() {
  this.updatePersonalInformation = function(personalInformation, observer) {
    $.ajax({
  	  url:  "?phoneNumber=" + personalInformation.phone +
            "&name=" + personalInformation.name +
            "&time="+ personalInformation.time +
            "&publickey="+ personalInformation.publicKey,
  	  context: this,
  	  error: this.onError
  	}).done(function( data ) {
      this.onNeighborsUpdate(data);
      observer.onNeighborsUpdate(data);
    }.bind(this));
  }

  this.updateMessages = function(observer) {
  	$.ajax({
  	  url:  "?messages=update",
  	  context: this,
  	  error: this.onError
  	}).done(function( data ) {
      this.onMessagesUpdate(data, observer);
    }.bind(this));
  }

  this.onError = function(xhr, ajaxOptions, thrownError) {
    console.log("API.onError". xhr, ajaxOptions, thrownError);
  }

  this.onMessagesUpdate = function(messagesJSON) {
    let obj = JSON.parse(messagesJSON);

    let toBeSent = this.parseMessageList(obj["To be sent"])
    let sent = this.parseMessageList(obj["Sent"])
    let received = this.parseMessageList(obj["Received"])

    observer.updateMessages(toBeSent, sent, received)
  }

  this.parseMessageList = function(pyMessageArray) {
    let ret = new MessageList();
    for (const message of messageArray) {
      ret.add(this.parseMessage(message));
    return ret;
  }
  this.parseMessage = function(pyMessage) {
    return new Message(pyMessage.sender, pyMessage.target, pyMessage.content, pyMessage.time, pyMessage.isACK, pyMessage.isSelfInformation, pyMessage.sendCount)
  }

  this.onNeighborsUpdate = function(response) {
    console.log(response);
  }
}


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

function Model() {
  let api = new API();
  let persistance = new LocalPersistance();

  this.onLoad = function() {
    this.personalInformation = persistance.getStoredPersonalInformation();
    api.updateMessages(this);
  }

  this.onTick = function() {
    api.updateMessages(this);
  }

  this.updatePersonalInformation = function(personalInformation, observer) {
    this.personalInformation = personalInformation;
    persistance.storePersonalInformation(this.personalInformation);
    api.updatePersonalInformation(this.personalInformation, observer);
  }

  this.updateMessages = function(toBeSent, sent, received) {
    this.toBeSent = toBeSent;
    this.sent = sent;
    this.received = received;
  }
}

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

function Message(sender, target, content, time, isACK, isSelfInformation, sendCount) {
  this.sender = sender;
  this.target = target;
  this.content = content;
  this.time = time;
  this.isACK = isACK;
  this.isSelfInformation = isSelfInformation;
  this.sendCount = sendCount;
}

function MessageList () {
  this.messages = [];
}
