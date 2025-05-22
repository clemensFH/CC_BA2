#!/usr/bin/python

import socket
from scapy.contrib.mqtt import MQTT
from hashlib import sha256

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 1883           # MQTT-Standardport
PSIZE = 1460

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"MQTT-TCP-Server läuft auf Port {PORT}...")

    conn, addr = server.accept()
    with conn:
        print(f"Verbindung von {addr}")
        content = b""
        packet_counter = 0
        while True:
            data = conn.recv(1024)
            if not data:
                break
            content += data

            #if mqtt_packet.type == 3:
            #    tmp += mqtt_packet.topic
            #    tmp += mqtt_packet.value
            #    print("Reassembled: " + tmp.hex())
        length = len(content)
        idx = 0
        payload = b""
        while idx + PSIZE <= length:
            x = MQTT(content[idx:idx + PSIZE])
#            x.show()
            packet_counter += 1
            payload += x.topic + x.value
            idx += PSIZE

        print("Länge: " + str(len(content)))
        if len(content[idx:]) != 0:
            x = MQTT(content[idx:])
            print("Rem Length: " + str(len(content[idx:])))
            x.summary()
            packet_counter += 1
            payload += x.topic+x.value

        print("Hex: " + sha256(payload).hexdigest())
        print("Packet Count: " + str(packet_counter))