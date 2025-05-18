from cbor2 import dumps, loads
import socket
import scapy.contrib.mqtt as mqtt
from scapy.all import IP, TCP, RandShort, send, sr1, load_contrib
import time
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256


daten = {"name": "Clemens", "wert": 42, "aktiv": 2}
data = dumps(daten).hex()
#print(data + " len: " + str(len(data)))

content = readFromFile("data_1mb.json")    # bytes von CBOR speichern
print(type(content))
print(len(content))
print(sha256(content).hexdigest())
#print(loads(content))
crwaler =  CBORIterator(content)

byte_data = bytes.fromhex(data)

p = mqtt.MQTT()/mqtt.MQTTConnect(clientId=byte_data[:5],
                                 willflag=1, usernameflag=1, passwordflag=1,
                                 willtopic=byte_data[5:10], willmsg=byte_data[10:15],
                                 username=byte_data[15:20], password=byte_data[20:25],
                                 protoname='MQTT', cleansess=1, klive=60, protolevel=6)
a = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=1, topic=byte_data[0:14], value=byte_data[14:])

"""test = mqtt.MQTT()/mqtt.MQTTConnect(clientId=crwaler.getNextBytes(5),
                                 willflag=1, usernameflag=1, passwordflag=1,
                                 willtopic=crwaler.getNextBytes(5), willmsg=crwaler.getNextBytes(5),
                                 username=crwaler.getNextBytes(5), password=crwaler.getNextBytes(5),
                                 protoname='MQTT', cleansess=1, klive=60, protolevel=6)"""
test = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=1, topic=content[:14], value=content[14:])

#print(test.password)

# Socket TCP-Verbindung aufbauen

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("10.0.0.12", 1883))  # Verbinden
    s.send(bytes(test))
    #s.send(bytes(p)) #send ?
    #print("MQTT CONNECT gesendet")
    #s.send(bytes(a))
    #time.sleep(3)
    #print("MQTT PUBLISH gesendet")
    #s.send(bytes(a))
    #time.sleep(3)
    #print("MQTT PUBLISH gesendet")
    #s.send(bytes(a))
    #time.sleep(3)
    #print("MQTT PUBLISH gesendet")
