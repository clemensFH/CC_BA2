import socket
from scapy.contrib.mqtt import MQTT

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 1883           # MQTT-Standardport

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"MQTT-TCP-Server läuft auf Port {PORT}...")

    conn, addr = server.accept()
    with conn:
        print(f"Verbindung von {addr}")
        
        content = b""
        while True:
            data = conn.recv(808)
            if not data:
                break
            
            print(f"[{addr}] Empfangene Daten (hex): {data.hex()}")
            mqtt_packet = MQTT(data)
            mqtt_packet.show()
            print("Packet Type: " + str(mqtt_packet.type))
            
            tmp = b""
            if mqtt_packet == 3: # Publish
                tmp += mqtt_packet.topic
                tmp += mqtt_packet.value
                print("Reassembled: " + tmp.hex())

