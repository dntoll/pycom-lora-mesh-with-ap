function Controller(model, view) {
  this.onSavePersonalInformation = function() {

    let pi = view.getPersonalInformation();
    model.updatePersonalInformation(pi, view);
    view.personalInformationWasUpdated();
  /*  for (const variable of inputElements) {
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
    }).done(onUploadedClient);*/
  }
}

let m = new Model();
let v = new View(m);
let c = new Controller(m, v);

window.onload = function() {
  m.onLoad();
  v.onLoad();
  window.setInterval(function(){
    m.onTick();
  }, 10000);
};
