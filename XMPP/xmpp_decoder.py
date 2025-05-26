#!/usr/bin/python

import socket
from hashlib import sha256
import xml.etree.ElementTree as ET
import base64
import time

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 5222           # MQTT-Standardport
PSIZE = 1460
SEG = True

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))   # Socket auf IP und Port setzen
    server.listen(5)            # Max Anzahl Verbindingen
    print(f"MQTT-TCP-Server läuft auf Port {PORT}...")

    conn, addr = server.accept() # Auf Verbindung warten | conn -> client socket, addr -> client adress + port
    with conn:                  # Solange Verbindung besteht
        print(f"Verbindung von {addr}")
        
        content = b""
        start_time = -1.0
        while True:
            data = conn.recv(1024)   # empfange MAX bytes
            if not data:
                break
            if start_time < 0.0: start_time = time.perf_counter()
            content += data

        length = len(content)
        print("Content Len:" + str(length))
        idx = 0
        payload = b""
        b64payload = ""
        packet_counter = 0

        while idx + PSIZE <= length and SEG:
            xml_str = content[idx:idx+PSIZE].decode("utf-8")
#            print(xml_str)

            try:
            # XML in ElementTree-Objekt umwandeln
                root = ET.fromstring(xml_str)

            # Zugriff auf die Nachricht
                if root.tag == "message":
                    body = root.find("body")
                    if body is None:
                        print("Kein <body>-Element gefunden.")
                        continue
                    b64payload += body.text
                    packet_counter += 1
                    idx += PSIZE
                else:
                    print("Kein <message>-Stanza erhalten.")

            except ET.ParseError as e:
                 print("Fehler beim Parsen:", e)
                 continue

        xml_str = content[idx:].decode("utf-8")
        print(xml_str)
        try:
            root=ET.fromstring(xml_str)
            body=root.find("body")
            b64payload+=body.text
            packet_counter += 1
        except ET.ParseError:
            print("Fehler beim Parsen.")

        end_time = time.perf_counter()

        payload = base64.b64decode(b64payload)
        print("Packet Counter: " + str(packet_counter))
        print("Result Hash: " + sha256(payload).hexdigest())
        print(f"Duration: {end_time - start_time:.6f} sec")