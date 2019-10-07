function Message(sender, target, content, time, isACK, isSelfInformation, sendCount) {
  this.sender = sender;
  this.target = target;
  this.content = content;
  this.time = time;
  this.isACK = isACK;
  this.isSelfInformation = isSelfInformation;
  this.sendCount = sendCount;
}
