function Controller(model, view, adminView) {
  this.onSavePersonalInformation = function() {

    let pi = view.getPersonalInformation();
    model.updatePersonalInformation(pi);
    view.personalInformationWasUpdated();
  }

  this.userSendsMessage = function() {
    let m = adminView.getMessage();
    model.sendMessage(m, adminView);
  }

  this.searchForContact = function() {
    let cr = view.getContactRequest();
    model.searchForContact(cr, view)
  }

  this.addContactFromSearchResult = function(phoneNumber) {
    for (const contact of view.searchResultContactArray) {
      if (phoneNumber == contact.phoneNumber) {
        model.addContact(contact);
      }
    }
    view.setContactList();
  }

  this.messageContact = function(phoneNumber) {
    for (const contact of model.phoneBook.contacts) {
      if (phoneNumber == contact.phoneNumber) {
        view.messageContact(contact);
      }
    }
  }

  this.sendMessageEncrypted = function() {
    let m = view.getEncryptedMessage()

    model.sendMessage(m, adminView);
  }
}

let m = new Model();
let vi = new View(m);
let av = new AdminView(m);
let c = new Controller(m, vi, av);

window.onload = function() {
  m.onLoad();
  vi.onLoad();

}

window.setInterval( function() {
                      m.onTick(vi);
                      vi.updateView();
                      av.updateView();
                    }, 11000);
