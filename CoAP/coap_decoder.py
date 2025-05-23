#!/usr/bin/python

import socket
from scapy.contrib.coap import CoAP
from hashlib import sha256

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 5683           # MQTT-Standardport
PSIZE = 1472

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 10 * 1024 * 1024)
    server.settimeout(1.0)
    server.bind((HOST, PORT))
    print(f"CoAP-UDP-Server läuft auf Port {PORT}...")
    tmp = b""
    payload = b""
    i = 0
    while True:
        data, addr = server.recvfrom(4096)

#        coap = CoAP(data)  # 'data' stammt aus recvfrom
        i += 1
#        print(str(i))
        payload += data
        if i == 3151: break

    length = len(payload)
    idx = 0
    packet_counter = 0
    while idx + PSIZE <= length:
        x = CoAP(payload[idx:idx + PSIZE])
#        x.show()
        packet_counter += 1
        tmp += x.topic + x.value
        idx += PSIZE
    
    x = CoAP(payload[idx:])
#    x.show()
    packet_counter += 1
    tmp += x.topic + x.value

    print("Count: " + str(packet_counter))
    print(len(payload))
    
#        if coap.code == 2:
#            tmp += coap.token
#            tmp += coap.options[0][1]
#            tmp += coap.load
#            print("Reassembled: " + tmp.hex())
#        if coap.code == 1:
#            tmp += coap.token
#            for opt in coap.options:
#                tmp += opt[1]
#        else:
#            print("Falscher Type")
    hsh = sha256(tmp).hexdigest()
#        print(hsh)
    if hsh == "56939f07f300cd31e9c462f5893b1abb50bf5e79d100806e41ea47a3093a01db" or hsh == "0e1609970222da6f2b895886911591a057c70717b201863b9600f0b7ec339de3":
        print("Packet Nr: " + str(i) + " Hash OK")
        #break
    
