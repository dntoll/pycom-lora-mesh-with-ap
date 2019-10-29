from LoraMeshChatApplication import LoraMeshChatApplication
import pycom
import model
import view

pycom.wifi_on_boot(False)
pycom.heartbeat(False)
fakeIt = False
app = LoraMeshChatApplication(fakeIt)
print("init done");
while True:
    app.update()
