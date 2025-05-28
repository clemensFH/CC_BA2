import paho.mqtt.client as mqtt
import aiocoap
import slixmpp
from cbor2 import dumps
import util.cborctl as cborctl
import scapy.contrib.coap as coap
from scapy.all import IP, UDP, send
from hashlib import sha256

print("Read target content")

content = cborctl.readFromFile("data_500kb.json")
print(len(content))
print(sha256(content).hexdigest())

print("Content read successfull")

"""
daten = {"name": "Clemens", "wert": 42, "aktiv": 2}
data = dumps(daten).hex()
print(data + " len: " + str(len(data)))

crwaler = cborctl.CBORIterator(data)
print(crwaler.getNextByte())
print(crwaler.getRemainingBytes())
print(crwaler.getNextBytes(27))
print(crwaler.getRemainingBytes())
print(crwaler.getNextBytes(28))
print(crwaler.getRemainingBytes())
print(crwaler.ReachedEnd())

print("Test packet")
byte_data = bytes.fromhex(data)

packet = coap.CoAP(code=1, msg_id=56, token=byte_data[:15])
#packet.options = [('Uri-Path', byte_data[15:])]
packet.options = [('Uri-Path', byte_data[15:20]), ('Uri-Path', byte_data[20:])]

s = IP(dst="127.0.0.1") / UDP(dport=5683) / packet
print(s.summary())
print(s.token)
send(s)"""
