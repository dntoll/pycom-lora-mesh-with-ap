function PhoneBook() {
  this.contacts = [];

  this.addContact = function(contact) {
    //check if we have this contact before!
    this.contacts.push(contact)
  }
}
