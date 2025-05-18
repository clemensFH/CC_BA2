import socket
from scapy.contrib.mqtt import MQTT
from hashlib import sha256

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 1883           # MQTT-Standardport

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
            print(f"[{addr}] Empfangene Daten (hex): {data.hex()}")
            
            """mqtt_packet = MQTT(data)
            mqtt_packet.show()
            print("Packet Type: " + str(mqtt_packet.type))
            
            tmp = b""
            if mqtt_packet == 3: # Publish
                tmp += mqtt_packet.topic
                tmp += mqtt_packet.value
                print("Reassembled: " + tmp.hex())"""
        x = MQTT(content)
        x.show()
        payload = x.topic + x.value
        print(sha256(payload).hexdigest())

