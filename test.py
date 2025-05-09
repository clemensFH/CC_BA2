import paho.mqtt.client as mqtt
import aiocoap
import slixmpp
from cbor2 import dumps
import util.cborctl as cborctl
import scapy.contrib.coap as coap
from scapy.all import IP, UDP, send

print("Read target content")

content = cborctl.readFromFile("target_1mb.txt", "output.cbor")

print(content)

print("Content read successfull")

daten = {"name": "Clemens", "wert": 42, "aktiv": 2}
data = dumps(daten).hex()
print(data + " len: " + str(len(data)))

crwaler = cborctl.cborIterator(data)
print(crwaler.getNextSign())
print(crwaler.getRemainingSigns())
print(crwaler.getNextSigns(27))
print(crwaler.getRemainingSigns())
print(crwaler.getNextSigns(28))
print(crwaler.getRemainingSigns())
print(crwaler.ReachedEnd())

print("Test packet")
byte_data = bytes.fromhex(data)

packet = coap.CoAP(code=1, msg_id=56, token=byte_data[:15])
#packet.options = [('Uri-Path', byte_data[15:])]
packet.options = [('Uri-Path', byte_data[15:20]), ('Uri-Path', byte_data[20:])]

s = IP(dst="127.0.0.1") / UDP(dport=5683) / packet
print(s.summary())
print(s.token)
send(s)
