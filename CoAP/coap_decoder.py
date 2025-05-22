#!/usr/bin/python

import socket
from scapy.contrib.coap import CoAP
from hashlib import sha256

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 5683           # MQTT-Standardport

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    print(f"CoAP-UDP-Server läuft auf Port {PORT}...")
    tmp = b""
    i = 0
    while True:
        data, addr = server.recvfrom(4096)

        coap = CoAP(data)  # 'data' stammt aus recvfrom
        i += 1
        print(str(i))

#        if coap.code == 2:
#            tmp += coap.token
#            tmp += coap.options[0][1]
#            tmp += coap.load
#            print("Reassembled: " + tmp.hex())
        if coap.code == 1:
            tmp += coap.token
            for opt in coap.options:
                tmp += opt[1]
        else:
            print("Falscher Type")
        hsh = sha256(tmp).hexdigest()
        print(hsh)
        if hsh == "56939f07f300cd31e9c462f5893b1abb50bf5e79d100806e41ea47a3093a01db":
            print("Packet Nr: " + str(i) + " Hash OK")
            break