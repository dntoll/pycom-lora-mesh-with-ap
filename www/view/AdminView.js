
function AdminView(model) {

  this.getMessage = function() {
    var targetElement= document.getElementById("targetID");
    var messageElement= document.getElementById("messageID");
    let content = messageElement.value;
    let target = targetElement.value;

    var d = new Date();
    let time = d.getTime();
    return new Message("setByServer", target, content, time, 0, 0)
  }

  this.updateView = function() {
    this.updateMessages();
    this.updateNeighbors();
  }

  this.updateNeighbors = function() {

    html = "";

    html += "<table>";
    html += this.getNetworkNodeHeader()
    html += "<tr>" + this.getNetworkNodeHTML(model.me)  + " </tr>"
    html += this.getNetworkNodeHeader()
    for (const node of model.others) {
      html += "<tr>" +  this.getNetworkNodeHTML(node)  + " </tr>"
    }
    html +=  "</table>"

    var networkDiv= document.getElementById("network");
    networkDiv.innerHTML = html;
  }

  this.updateMessages = function() {

    messageBoardHTML = "<h2>Received Messages</h2>"
    messageBoardHTML += "<table>" + this.getMessageHeader()
    for (const message of model.received) {
      messageBoardHTML += "<tr>" +  this.getMessageHTML(message)  + " </tr>"
    }
    messageBoardHTML +=  "</table>"

    messageBoardHTML += "<h2>Send Que</h2>"
    messageBoardHTML += "<table>" + this.getMessageHeader()
    for (const message of model.toBeSent) {
      messageBoardHTML += "<tr>" +  this.getMessageHTML(message)  + " </tr>"
    }
    messageBoardHTML = messageBoardHTML + "</table>"

    messageBoardHTML += "<h2>Sent Messages</h2>"
    messageBoardHTML += "<table>" + this.getMessageHeader()

    for (const message of model.sent) {
      messageBoardHTML += "<tr>" +  this.getMessageHTML(message)  + " </tr>"
    }
    messageBoardHTML = messageBoardHTML + "</table>"


    var messagesDiv= document.getElementById("messages");
    messagesDiv.innerHTML = messageBoardHTML;
  }

  

  this.getNetworkNodeHeader = function() {
    return `<tr>
              <th>name</th>
              <th>mac</th>
              <th>role</th>
              <th>mlEID</th>
              <th>ip</th>
              <th>id</th>
              <th>rssi</th>
              <th>age</th>
              <th>path_cost</th>
            </tr>`
  }

  this.getNetworkNodeHTML = function(node) {
    html = ""
    html += "<td>" + node.name + "</td>"
    html += "<td>" + node.mac + "</td>"
    html += "<td>" + node.role + "</td>"
    html += "<td>" + node.mlEID + "</td>"
    html += "<td>" + node.ip + "</td>"
    html += "<td>" + node.id + "</td>"
    html += "<td>" + node.rssi + "</td>"
    html += "<td>" + node.age + "</td>"
    html += "<td>" + node.path_cost + "</td>"

    return html
  }

  this.getMessageHeader = function() {
    return `<tr>
              <th>From</th>
              <th>To</th>
              <th>Content</th>
              <th>Time</th>
              <th>type</th>
              <th>sendCount</th>
            </tr>`
  }

  this.getMessageHTML = function(message) {
    html = ""
    html += "<td>" + message.sender + "</td>"
    html += "<td>" + message.target + "</td>"
    html += "<td>" + message.content + "</td>"
    html += "<td>" + message.time + "</td>"
    html += "<td>" + message.type + "</td>"
    html += "<td>" + message.sendCount + "</td>"

    return html
  }
}
