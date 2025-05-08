import scapy.contrib.coap as CoAP
from scapy.all import send, IP, UDP
from cbor2 import dumps
import socket

daten = {"name": "Clemens", "wert": 42, "aktiv": 2}
data = dumps(daten).hex()
print(data + " len: " + str(len(data)))

byte_data = bytes.fromhex(data)

packet = CoAP.CoAP(code=1, msg_id=56, token=byte_data[:15])
#packet.options = [('Uri-Path', byte_data[15:])]
packet.options = [('Uri-Path', byte_data[15:20]), ('Uri-Path', byte_data[20:])]

s = IP(dst="10.0.0.12") / UDP(dport=5683) / packet
print(s.summary())
print(s.token)
send(s)