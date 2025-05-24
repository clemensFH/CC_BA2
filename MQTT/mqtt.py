from cbor2 import dumps, loads
import socket
import scapy.contrib.mqtt as mqtt
from scapy.all import IP, TCP, RandShort, send, sr1, load_contrib
import time
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256


content = readFromFile("data_10mb.json")    # bytes von CBOR speichern
print(type(content))
print(len(content))
print(sha256(content).hexdigest())
#print(loads(content))
crwaler =  CBORIterator(content)


"""p = mqtt.MQTT()/mqtt.MQTTConnect(clientId=byte_data[:5],
                                 willflag=1, usernameflag=1, passwordflag=1,
                                 willtopic=byte_data[5:10], willmsg=byte_data[10:15],
                                 username=byte_data[15:20], password=byte_data[20:25],
                                 protoname='MQTT', cleansess=1, klive=60, protolevel=6)
a = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=1, topic=byte_data[0:14], value=byte_data[14:])

test = mqtt.MQTT()/mqtt.MQTTConnect(clientId=crwaler.getNextBytes(5),
                                 willflag=1, usernameflag=1, passwordflag=1,
                                 willtopic=crwaler.getNextBytes(5), willmsg=crwaler.getNextBytes(5),
                                 username=crwaler.getNextBytes(5), password=crwaler.getNextBytes(5),
                                 protoname='MQTT', cleansess=1, klive=60, protolevel=6)
test = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=1, topic=content[:14], value=content[14:1507])"""


# Socket TCP-Verbindung aufbauen
# Publish -> 1453 Böcke
packet_counter = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("10.0.0.14", 1883))  # Verbinden

    while crwaler.getRemainingLength() >= 1453:
        packet = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=5, topic=crwaler.getNextBytes(14), value=crwaler.getNextBytes(1439))
        s.send(bytes(packet))
        packet_counter += 1
        #print(len(packet))
    
    packet = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=5, topic=crwaler.getNextBytes(14), value=crwaler.getRemainingBytes())
    s.send(bytes(packet))
    packet_counter += 1
    print(len(packet))
    print("Packets sent: " + str(packet_counter))
