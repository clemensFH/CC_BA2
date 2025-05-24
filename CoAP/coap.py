import scapy.contrib.coap as CoAP
from scapy.all import send, IP, UDP
from cbor2 import dumps
import socket
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256

content = readFromFile("data_10mb.json")    # bytes von CBOR speichern
print(type(content))
print(len(content))
print(sha256(content).hexdigest())

# token max => 15
# Max-Age => 4
# ETag => 8
"""GET_packet = CoAP.CoAP(code=1, msg_id=56, token=byte_data[:15])
GET_packet.options = [("ETag", byte_data[15:19]), ('Uri-Path', byte_data[19:24]), ('Max-Age', byte_data[24:])]

POST_packet = CoAP.CoAP(code=2, msg_id=99, token=byte_data[:15], paymark=b'\xFF')
POST_packet.options = [('Uri-Path', byte_data[15:20])]
POST_packet /= byte_data[20:]"""


# 0-1464
itertor = CBORIterator(content)
packet_counter = 0
while itertor.getRemainingLength() >= 1464:
    x = CoAP.CoAP(code=1, msg_id=12, token=itertor.getNextBytes(15))
    x.options = [("ETag", itertor.getNextBytes(4)), ("Uri-Path", itertor.getNextBytes(1445))]
    get = IP(dst="10.0.0.14") / UDP(dport=5683) / x
    send(get)
    packet_counter += 1

x = CoAP.CoAP(code=1, msg_id=12, token=itertor.getNextBytes(15))
x.options = [("ETag", itertor.getNextBytes(4)), ("Uri-Path", itertor.getRemainingBytes())]
get = IP(dst="10.0.0.14") / UDP(dport=5683) / x
send(get)
packet_counter += 1
print("Packets sent: " + str(packet_counter))
print("Size: " + str(len(content)))