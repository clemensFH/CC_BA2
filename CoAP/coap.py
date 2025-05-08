import scapy.contrib.coap as CoAP
from scapy.all import send, IP, UDP
from cbor2 import dumps
import socket

daten = {"name": "Clemens", "wert": 42, "aktiv": 2}
data = dumps(daten).hex()
print(data + " len: " + str(len(data)))

byte_data = bytes.fromhex(data)

# token max => 15
# Max-Age => 4
# ETag => 8
GET_packet = CoAP.CoAP(code=1, msg_id=56, token=byte_data[:15])
GET_packet.options = [('Uri-Path', byte_data[15:20]), ('Max-Age', byte_data[20:24]), ("ETag", byte_data[14:22])]


POST_packet = CoAP.CoAP(code=2, msg_id=99, token=byte_data[:15], paymark=byte_data[15:16])
POST_packet.options = [('Uri-Path', byte_data[15:20])]
POST_packet.paymark = b'\xFF'
POST_packet /= byte_data[24:]

s = IP(dst="10.0.0.12") / UDP(dport=5683) / POST_packet
print(s.summary())
print(s.token)
send(s)