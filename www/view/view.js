
function View(model) {
  const phoneID = "phoneID";
  const nameID = "nameID";
  const passfraseID = "passfraseID";
  const RSAPublicKeyID = "RSAPublicKeyID";

  this.onLoad = function() {
    document.getElementById(phoneID).value = model.personalInformation.phone;
    document.getElementById(nameID).value = model.personalInformation.name;
    document.getElementById(passfraseID).value = model.personalInformation.passfrase;
    this.setContactList();
  }

  this.updateView = function() {
  }

  this.getPersonalInformation = function() {
    let phone= document.getElementById(phoneID).value;
    let name= document.getElementById(nameID).value;
    let passfrase= document.getElementById(passfraseID).value;

    return new PersonalInformation(phone, name, passfrase);
  }

  this.getContactRequest = function() {
    var cname= document.getElementById("contactName");
    var cphone= document.getElementById("contactPhone");
    let name = cname.value;
    let phone = cphone.value;

    return new ContactRequest(name, phone);
  }

  this.messageContact = function(contact) {
    var name= document.getElementById("sendMessageNameID");
    var phone= document.getElementById("sendMessagePhoneID");
    var publicKey= document.getElementById("sendMessagePublicKey");
    var mac = document.getElementById("sendMessageMacID");
    name.value = contact.name
    phone.value = contact.phoneNumber
    publicKey.value = contact.publicKeyString
    mac.value = contact.lastSeenMac

    this.contact = contact
  }

  this.getEncryptedMessage = function() {
    var message= document.getElementById("sendMessageMessage").value;
    return new EncryptedMessage(this.contact, message, model.personalInformation)
  }



  this.personalInformationWasUpdated = function() {
    let publickey = model.personalInformation.publicKey;
    var RSAPublicKeyElement= document.getElementById(RSAPublicKeyID);
    RSAPublicKeyElement.innerHTML = publickey

    //document.getElementById(passfraseID).value = "******************"
  }

  this.setContactSearchResult = function(searchResultContactArray) {
    this.searchResultContactArray = searchResultContactArray;
    html = "";

    html += "<table>";
    html += this.getContactHeader()
    for (const contact of searchResultContactArray) {
      html += "<tr>" +  this.getContactHTML(contact)  + "<td><button type=\"button\" onclick=\"c.addContactFromSearchResult(\'"+contact.phoneNumber+"\')\">Add to contacts</button></td> </tr>"
    }
    html +=  "</table>"

    var networkDiv= document.getElementById("contactSearchResult");
    networkDiv.innerHTML = html;
  }

  this.setContactList = function() {
    html = "";

    html += "<table>";
    html += this.getContactHeader()
    for (const index in model.phoneBook.contacts) {
      const contact = model.phoneBook.contacts[index]
      html += "<tr>" +  this.getContactHTML(contact)
      html += "<td><button type=\"button\" onclick=\"c.messageContact(\'"+index+"\')\">Message</button></td> "
      html += "<td><button type=\"button\" onclick=\"c.removeContactFromPhoneBook(\'"+index+"\')\">Remove</button></td> "
      html += "</tr>"
    }
    html +=  "</table>"

    var networkDiv= document.getElementById("phoneBookID");
    networkDiv.innerHTML = html;
  }

  this.getContactHeader = function() {
    return `<tr>
              <th>name</th>
              <th>phoneNumber</th>
              <th>publicKeyString</th>
              <th>time</th>
              <th>lastSeenMac</th>
            </tr>`
  }

  this.getContactHTML = function(contact) {
    html = ""
    html += "<td>" + contact.name + "</td>"
    html += "<td>" + contact.phoneNumber + "</td>"
    html += "<td>" + contact.publicKeyString + "</td>"


    var d = new Date();
    d.setTime(contact.time);
    var n = d.toLocaleTimeString();
    html += "<td>" + n + "</td>"
    html += "<td>" + contact.lastSeenMac + "</td>"

    return html
  }



}
