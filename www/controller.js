function Controller(model, view) {
  this.onSavePersonalInformation = function() {

    let pi = view.getPersonalInformation();
    model.updatePersonalInformation(pi, view);
    view.personalInformationWasUpdated();
  }
}

let m = new Model();
let v = new View(m);
let c = new Controller(m, v);

window.onload = function() {
  m.onLoad();
  v.onLoad();

}

window.setInterval(function(){m.onTick();}, 11000);
