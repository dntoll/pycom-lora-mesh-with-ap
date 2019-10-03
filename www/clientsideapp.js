

function storePersonalInformation(){
  var inputElements = ["phoneID", "nameID", "passfraseID"];

  for (const variable of inputElements) {
    var inputElement= document.getElementById(variable);
    localStorage.setItem(variable, inputElement.value);
  }

  let passfrase = localStorage.getItem("passfraseID");
  var Bits = 1024;

  var myRSAKey = cryptico.generateRSAKey(let, Bits);
};

function loadPersonalInformation() {
  var inputElements = ["phoneID", "nameID", "passfraseID"];

  for (const variable of inputElements) {
    var inputElement= document.getElementById(variable);
    inputElement.value = localStorage.getItem(variable);
  }
}



function onError(xhr, ajaxOptions, thrownError) {
		console.log("onError", xhr, ajaxOptions, thrownError);
}

function onDownloadedMessages(something) {
  var messagesDiv= document.getElementById("messages");
  messagesDiv.innerHTML = something
}

function onDownloadedNetwork(something) {
  var networkDiv= document.getElementById("network");
  networkDiv.innerHTML = something
}

function onUploadedMessages(something) {
  var messageElement= document.getElementById("messageID");
  messageElement.value = "";
}

function userSendsMessage() {
  var targetElement= document.getElementById("targetID");
  var messageElement= document.getElementById("messageID");

  let message = messageElement.value;
  let target = targetElement.value;

	$.ajax({
	  url:  "?message=" + message + "&target=" + target,
	  context: document.body,
	   error: onError
	}).done(updateMessages);
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



window.setInterval(function(){
  updateNetwork();
  updateMessages();
}, 5000);

window.onload = function() {
  loadPersonalInformation();
};

//Om ansluten: Ladda om sidan då och då eller iaf hämta ny information typ var 10 sekund

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
