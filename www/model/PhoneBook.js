function PhoneBook() {
  this.contacts = [];

  this.addContact = function(contact) {
    //check if we have this contact before!
    this.contacts.push(contact)
  }

  this.removeContact = function(contact) {
    this.contacts = this.contacts.filter(function(value, index, arr) {
        return value.equals(contact) === false; //we keep the others
      }.bind(this));
  }
}
