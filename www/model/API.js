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
      this.onNeighborsUpdate(data, observer);
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

this.searchForContact = function(contactRequest, contactResultTarget) {
  $.ajax({
    url:  "?contactName=" + contactRequest.name + "&contactPhone=" + contactRequest.phone,
    context: this,
     error: this.onError
  }).done(function( contactResoponseJSONString ) {
    let pyMatchedContacts = JSON.parse(contactResoponseJSONString);
    console.log("askForContact", pyMatchedContacts);

    let ret = [];
    for (const contact of pyMatchedContacts) {
      ret.push( new Contact(contact.name, contact.phoneNumber, contact.publicKeyString, contact.time ) )
    }
    contactResultTarget.setContactSearchResult(ret)


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
    let ret = [];
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
    return new NetworkNode(pyNeightbor.mac, pyNeightbor.ip, pyNeightbor.name, pyNeightbor.mlEID, pyNeightbor.role, pyNeightbor.rssi, pyNeightbor.age, pyNeightbor.id, pyNeightbor.path_cost, pyNeightbor.firmware)
  }
}
