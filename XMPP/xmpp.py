import slixmpp
import asyncio
import logging
import socket
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256
import base64
logging.basicConfig(level=logging.DEBUG)

def getMessage(data: bytes):
    encoded = base64.b64encode(data).decode()
    message = """
    <message
        from='juliet@example.com/balcony'
        id='ktx72v49'
        to='romeo@example.net'
        type='chat'
        xml:lang='en'>
        <body>""" + encoded + """</body>
    </message>
    """
    return message


content = readFromFile("data_10mb.json")    # bytes von CBOR speichern
print(type(content))
print(len(content))
print(sha256(content).hexdigest())

crwaler = CBORIterator(content)

# hex     : 632 - Blöcke
# base 64 : 948 - Blöcke

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("10.0.0.14", 5222))
    packet_counter = 0

    while crwaler.getRemainingLength() >= 948: # nicht genau
        packet = getMessage(crwaler.getNextBytes(948))
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