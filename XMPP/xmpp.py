import slixmpp
import asyncio
import logging
import socket
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256
import base64
logging.basicConfig(level=logging.DEBUG)

SEG = True

def getMessage(data: bytes):
    encoded = base64.b64encode(data).decode()
    message = """
    <message
        to='example.com'>
        <body>""" + encoded + """</body>
    </message>
    """
    #print(message)
    return message


content = readFromFile("data_10mb.json")    # bytes von CBOR speichern
print(type(content))
print(len(content))
print(sha256(content).hexdigest())

test = """
    <message
        to='example.com'>
        <body></body>
    </message>
    """
b = test.encode("utf-8") # len 81 "Overhead"
print(len(b))

crwaler = CBORIterator(content)

#a = getMessage(crwaler.getNextBytes(0)).encode("UTF-8")
#b = getMessage(crwaler.getNextBytes(948)).encode("UTF-8")

#print("Len a " + str(len(a)))
#print("Len b: " + str(len(b)))

# hex     : 632 - Blöcke
# base 64 : 948 - Blöcke

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("10.0.0.14", 5222))
    packet_counter = 0

    while crwaler.getRemainingLength() >= 1032 and SEG: # nicht genau
        packet = getMessage(crwaler.getNextBytes(1032))
        output = packet.encode("utf-8")
        #print(len(output))
        s.send(output)
        packet_counter += 1
    
    packet = getMessage(crwaler.getRemainingBytes())
    print(packet)
    output = packet.encode("utf-8")
    print(len(output))
    s.send(output)
    packet_counter += 1
    print("Packets sent: " + str(packet_counter))