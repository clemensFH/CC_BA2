import socket
from hashlib import sha256
import xml.etree.ElementTree as ET

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 5222          # MQTT-Standardport

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))   # Socket auf IP und Port setzen
    server.listen(5)            # Max Anzahl Verbindingen
    print(f"MQTT-TCP-Server läuft auf Port {PORT}...")

    conn, addr = server.accept() # Auf Verbindung warten | conn -> client socket, addr -> client adress + port
    with conn:                  # Solange Verbindung besteht
        print(f"Verbindung von {addr}")
        
        content = b""
        while True:
            data = conn.recv(1024)   # empfange MAX bytes
            if not data:
                break
            content += data
            #print(f"[{addr}] Empfangene Daten (hex): {data.hex()}")
        
        xml_str = content.decode("utf-8")

        try:
            # XML in ElementTree-Objekt umwandeln
            root = ET.fromstring(xml_str)

            # Zugriff auf die Nachricht
            if root.tag == "message":
                body = root.find("body")
                if body is not None:
                    print("Inhalt der Nachricht:", body.text)
                else:
                    print("Kein <body>-Element gefunden.")
                head = root.find("head")
                print("Inhalt Head: " + head.text)
            else:
                print("Kein <message>-Stanza erhalten.")

        except ET.ParseError as e:
            print("Fehler beim Parsen:", e)
        
        res = bytes.fromhex(body.text)
        print("Result Hash: " + sha256(res).hexdigest())