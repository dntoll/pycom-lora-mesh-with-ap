
function View(model) {
  const phoneID = "phoneID";
  const nameID = "nameID";
  const passfraseID = "passfraseID";
  const RSAPublicKeyID = "RSAPublicKeyID";

  this.onLoad = function() {
    document.getElementById(phoneID).value = model.personalInformation.phone;
    document.getElementById(nameID).value = model.personalInformation.name;
    document.getElementById(passfraseID).value = model.personalInformation.passfrase;
  }

  this.getPersonalInformation = function() {
    let phone= document.getElementById(phoneID).value;
    let name= document.getElementById(nameID).value;
    let passfrase= document.getElementById(passfraseID).value;

    return new PersonalInformation(phone, name, passfrase);
  }

  this.personalInformationWasUpdated = function() {
    let publickey = model.personalInformation.publicKey;
    var RSAPublicKeyElement= document.getElementById(RSAPublicKeyID);
    RSAPublicKeyElement.innerHTML = publickey

    //document.getElementById(passfraseID).value = "******************"
  }

  this.onNeighborsUpdate = function() {

  }

  this.onDownloadedMessages = function(messagesJSON) {


    var messagesDiv= document.getElementById("messages");


    messageBoardHTML = "<h2>Received Messages</h2>"
    messageBoardHTML += "<table>" + getMessageHeader()
    for (const message of received) {
      messageBoardHTML += "<tr>" +  getMessageHTML(message)  + " </tr>"
    }
    messageBoardHTML +=  "</table>"

    messageBoardHTML += "<h2>Send Que</h2>"
    messageBoardHTML += "<table>" + getMessageHeader()
    for (const message of toBeSent) {
      messageBoardHTML += "<tr>" +  getMessageHTML(message)  + " </tr>"
    }
    messageBoardHTML = messageBoardHTML + "</table>"

    messageBoardHTML += "<h2>Sent Messages</h2>"
    messageBoardHTML += "<table>" + getMessageHeader()

    for (const message of sent) {
      messageBoardHTML += "<tr>" +  getMessageHTML(message)  + " </tr>"
    }
    messageBoardHTML = messageBoardHTML + "</table>"



    messagesDiv.innerHTML = messageBoardHTML;
  }
}
