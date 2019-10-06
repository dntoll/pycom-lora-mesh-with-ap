

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

  this.sendMessage = function(message, observer) {
  	$.ajax({
  	  url:  "?message=" + message.content + "&target=" + message.target + "&time="+ message.time,
  	  context: this,
  	  error: this.onError
  	}).done(function( data ) {
      this.onMessagesUpdate(data, observer);
    }.bind(this));
  }

  this.updateNetwork = function(observer) {
  	$.ajax({
  	  url:  "?network=update",
  	  context: this,
  	   error: this.onError
  	}).done(function( data ) {
      this.onNeighborsUpdate(data, observer);
    }.bind(this));
  }

  this.onError = function(xhr, ajaxOptions, thrownError) {
    console.log("API.onError". xhr, ajaxOptions, thrownError);
  }

  this.onMessagesUpdate = function(messagesJSON, observer) {
    let obj = JSON.parse(messagesJSON);

    let toBeSent = this.parseMessageList(obj["To be sent"])
    let sent = this.parseMessageList(obj["Sent"])
    let received = this.parseMessageList(obj["Received"])

    observer.updateMessages(toBeSent, sent, received)
  }

  this.parseMessageList = function(pyMessageArray) {
    let ret = new MessageList();
    for (const message of pyMessageArray) {
      ret.push(this.parseMessage(message));
    }
    return ret;
  }

  this.parseMessage = function(pyMessage) {
    return new Message(pyMessage.sender, pyMessage.target, pyMessage.content, pyMessage.time, pyMessage.isACK, pyMessage.isSelfInformation, pyMessage.sendCount)
  }

  this.onNeighborsUpdate = function(neighborsJSON, observer) {
    let obj = JSON.parse(neighborsJSON);

    let me = this.parseNetworkNode(obj["me"])
    let others = this.parseNetworkNodeList(obj["others"])

    observer.updateNeighbors(me, others);
  }

  this.parseNetworkNodeList = function(pyArray) {
    let ret = new Array();
    for (const message of pyArray) {
      ret.push(this.parseNetworkNode(message));
    }
    return ret;

  }

  this.parseNetworkNode = function(pyNeightbor) {
    return new NetworkNode(pyNeightbor.mac, pyNeightbor.ip, pyNeightbor.name, pyNeightbor.mlEID, pyNeightbor.role, pyNeightbor.rssi, pyNeightbor.age, pyNeightbor.id, pyNeightbor.path_cost, pyNeightbor.firmware, pyNeightbor.clients)
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

  this.toBeSent = new MessageList();
  this.sent = new MessageList();
  this.received = new MessageList();
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

  this.push = function(message) {
    this.messages.push(message)
  }
}

function NetworkNode(mac, ip, name, mlEID, role, rssi, age, id, path_cost, firmware, clients) {
  this.mac = mac;
  this.ip = ip;
  this.name = name;
  this.mlEID = mlEID;
  this.role = role;
  this.rssi = rssi;
  this.age = age;
  this.id =  id;
  this.path_cost = path_cost;
  this.firmware = firmware;
  this.clients =clients;
}
