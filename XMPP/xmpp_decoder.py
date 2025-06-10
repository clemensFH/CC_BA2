#!/usr/bin/python

import socket
from hashlib import sha256
import xml.etree.ElementTree as ET
import base64
import time, argparse


HASHES = ["56939f07f300cd31e9c462f5893b1abb50bf5e79d100806e41ea47a3093a01db",
          "0e1609970222da6f2b895886911591a057c70717b201863b9600f0b7ec339de3",
          "15408d910a9c5955f17c9ba255f64f972f3f3252737b51a852f513cc4b82f96c",
          "e8ccb1a7054431eb8aaa48e3cbe7a76dde439e1fad47c0a762f4f26bbfa52b7c"]

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 5222           # MQTT-Standardport
PSIZE = 1460

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--Segment", action="store_true", help = "Segement packets into Ethernet MTU sizes")
args = parser.parse_args()

# SEG
#   -> True: Packetgröße auf MTU limitieren
#   -> False: Beliebige Packetgröße (ein Packet mit vollständigem Payload)
SEG = False
if args.Segment == True: SEG = True
info = "ON" if SEG else "OFF"

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))   # Socket auf IP und Port setzen
    server.listen(5)            # Max Anzahl Verbindingen
    print(f"XMPP-Receiver running on port {PORT}...")
    print(f"with segmenting {info}")

    conn, addr = server.accept() # Auf Verbindung warten
    with conn:                   # Solange Verbindung besteht
        print(f"RECEIVING data from {addr}")
        print("...")
        
        content = b""
        start_time = -1.0
        while True:
            data = conn.recv(1024)   # Daten empfangen
            if not data:
                break
            if start_time < 0.0: start_time = time.perf_counter()
            content += data

        end_recv = time.perf_counter()
        print("FINISHED receiving data")
        print("reassembling payload ...")

        length = len(content)
        idx = 0
        payload = b""
        b64payload = ""
        packet_counter = 0

        while idx + PSIZE <= length and SEG:                    # Payload aufteilen
            xml_str = content[idx:idx+PSIZE].decode("utf-8")    # XML content auslesen

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

        xml_str = content[idx:].decode("utf-8")                 # restliche bytes
        #print(xml_str)
        try:
            root=ET.fromstring(xml_str)
            body=root.find("body")
            b64payload+=body.text
            packet_counter += 1
        except ET.ParseError:
            print("Fehler beim Parsen.")

        end_time = time.perf_counter()
        print("FINISHED reassembling data\n")

        payload = base64.b64decode(b64payload)
        hsh = sha256(payload).hexdigest()
        hshCheck = "OK" if hsh in HASHES else "NOT OK"

        print("Hash            : " + hsh + " " + hshCheck)
        print("Payload length  : " + str(len(b64payload)))
        print("Packet Counter  : " + str(packet_counter))
        print(f"Packet reception time  : {end_recv - start_time:.6f} sec")
        print(f"Reassembling time      : {end_time - end_recv:.6f} sec")
        print(f"Total                  : {end_time - start_time:.6f} sec")