function Controller(model, view) {
  this.onSavePersonalInformation = function() {

    let pi = view.getPersonalInformation();
    model.updatePersonalInformation(pi, view);
    view.personalInformationWasUpdated();
  }

  this.userSendsMessage = function() {
    let m = view.getMessage();
    model.sendMessage(m, view);
  }

  this.searchForContact = function() {
    let cr = view.getContactRequest();
    model.searchForContact(cr, view)
  }
}

let m = new Model();
let v = new View(m);
let c = new Controller(m, v);

window.onload = function() {
  m.onLoad();
  v.onLoad();

}

window.setInterval( function() {
                      m.onTick(v);
                      v.updateView();
                    }, 11000);
