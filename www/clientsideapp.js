/*function Model() {
  function Message(sender, target, content, time, isACK, isSelfInformation, sendCount) {

  }

  function PersonalInformation(name, phone, passfrase) {
    var Bits = 128;
    this.name = name;
    this.phone = phone;
    this.myRSAKey = cryptico.generateRSAKey(passfrase, Bits);
  }


  this.myPersonalInformation = new PersonalInformation();

  function API() {
    this.getMessages() {
      $.ajax({
    	  url:  "?messages=update",
    	  context: document.body,
    	   error: onError
    	}).done(onDownloadedMessages);
    }
  }
}

function HTMLView(model) {
  this.model = model;
}
*/


//var inputElements = ["phoneID", "nameID", "passfraseID"];
//var myRSAKey = "";

/*function storePersonalInformation() {
  for (const variable of inputElements) {
    var inputElement= document.getElementById(variable);
    localStorage.setItem(variable, inputElement.value);
  }

  //Generate new RSAKey
  let passfrase = localStorage.getItem("passfraseID");
  var Bits = 128;

  myRSAKey = cryptico.generateRSAKey(passfrase, Bits);
  setRSAKeyHTML(myRSAKey);
  localStorage.setItem(myRSAKey, "RSAKey");

  var d = new Date();
  let time = d.getTime();
  let phoneNumber= document.getElementById("phoneID").value;
  let name       = document.getElementById("nameID").value;
  let publickey = cryptico.publicKeyString(myRSAKey);

  $.ajax({
	  url:  "?phoneNumber=" + phoneNumber + "&name=" + name + "&time="+ time + "&publickey="+ publickey,
	  context: document.body,
	   error: onError
	}).done(onUploadedClient);
};

function loadPersonalInformation() {
  for (const variable of inputElements) {
    var inputElement= document.getElementById(variable);
    inputElement.value = localStorage.getItem(variable);
  }

  myRSAKey = localStorage.getItem("RSAKey");
  setRSAKeyHTML(myRSAKey);
}

function setRSAKeyHTML(myRSAKey) {
  let publickey = cryptico.publicKeyString(myRSAKey);
  var RSAPublicKeyElement= document.getElementById("RSAPublicKeyID");
  RSAPublicKeyElement.innerHTML = publickey

}


//AJAX COMPLETED EVENT LISTENERS
function onError(xhr, ajaxOptions, thrownError) {
		console.log("onError", xhr, ajaxOptions, thrownError);
}

function onDownloadedMessages(something) {
  var messagesDiv= document.getElementById("messages");


  var obj = JSON.parse(something);

  console.log(obj["To be sent"])
  let toBeSent = obj["To be sent"];
  let sent = obj["Sent"];
  let received = obj["Received"];

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

function getMessageHeader() {
  return "<tr><th>From</th><th>To</th><th>Content</th><th>Time</th><th>isACK</th><th>isSelfInformation</th><th>sendCount</th></tr>"
}

function getMessageHTML(message) {
  messageHTML = ""
  messageHTML += "<td>" + message.sender + "</td>"
  messageHTML += "<td>" + message.target + "</td>"
  messageHTML += "<td>" + message.content + "</td>"
  messageHTML += "<td>" + message.time + "</td>"
  messageHTML += "<td>" + message.isACK + "</td>"
  messageHTML += "<td>" + message.isSelfInformation + "</td>"
  messageHTML += "<td>" + message.sendCount + "</td>"

  return messageHTML
}*/



/*function onUploadedMessages(something) {
  var messageElement= document.getElementById("messageID");
  messageElement.value = "";
  onDownloadedMessages(something)
}

function onUploadedClient(something) {

}

//API Calls
function userSendsMessage() {
  var targetElement= document.getElementById("targetID");
  var messageElement= document.getElementById("messageID");


  let message = messageElement.value;
  let target = targetElement.value;

  var d = new Date();
  let time = d.getTime();
	$.ajax({
	  url:  "?message=" + message + "&target=" + target + "&time="+ time,
	  context: document.body,
	   error: onError
	}).done(onUploadedMessages);
}

function updateMessages() {
	$.ajax({
	  url:  "?messages=update",
	  context: document.body,
	   error: onError
	}).done(onDownloadedMessages);
}

function updateNetwork() {
	$.ajax({
	  url:  "?network=update",
	  context: document.body,
	   error: onError
	}).done(onDownloadedNetwork);
}


//INITIATE APPLICATION
window.setInterval(function(){
  updateMessages();
}, 5000);
*/
window.setInterval(function(){
  updateNetwork();
}, 10000);

window.onload = function() {
  //loadPersonalInformation();
  updateNetwork();
  //updateMessages();
};

//interface för din egen session men som lagras på klienten
//användarnamn som är sökbart, ex telefonnummer och namn
//generera privat nyckel
//detta sparas i local storage så att det finns kvar nästa gång

//meddelanden laddas ner och finns kvar

//meddelanden kan skapas lokalt

//sök efter användare
// The passphrase used to repeatably generate this RSA key.
//alert("http://wwwtyro.github.io/cryptico/");
/*
var PassPhrase1 = "The Moon is a Harsh Mistress.";
var PassPhrase2 = "There Ain't No Such Thing As A Free Lunch.";
// The length of the RSA key, in bits.
var PlainText = "Matt, I need you to help me with my Starcraft strategy.";

var MattsRSAkey = cryptico.generateRSAKey(PassPhrase1, Bits);
var SamsRSAkey = cryptico.generateRSAKey(PassPhrase2, Bits);

var MattsPublicKeyString = cryptico.publicKeyString(MattsRSAkey);


var EncryptionResult = cryptico.encrypt(PlainText, MattsPublicKeyString);

var DecryptionResult = cryptico.decrypt(EncryptionResult.cipher, MattsRSAkey);


//Signing by Sams key!
var EncryptionResult = cryptico.encrypt(PlainText, MattsPublicKeyString, SamsRSAkey);*/
//Not working
//var PublicKeyID = cryptico.publicKeyID(EncryptionResult.publickey);
