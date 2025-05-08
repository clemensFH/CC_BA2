import socket
from scapy.contrib.coap import CoAP

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 5683           # MQTT-Standardport

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    print(f"CoAP-UDP-Server läuft auf Port {PORT}...")

    while True:
        data, addr = server.recvfrom(4096)
        print(f"Empfangen von {addr}: {data.hex()} (Länge: {len(data)} Bytes)")

        coap = CoAP(data)  # 'data' stammt aus recvfrom
        coap.show()