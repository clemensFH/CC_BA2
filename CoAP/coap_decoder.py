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

    content = b""
    packet_counter = 0
    
    while True:
        data, addr = server.recvfrom(4096)
        #print(f"Empfangen von {addr}: {data.hex()} (Länge: {len(data)} Bytes)")

        coap = CoAP(data)  # 'data' stammt aus recvfrom
        #coap.show()
        packet_counter += 1
        print(str(packet_counter))

        if coap.code == 1:  # GET packet
            content += coap.token
            for opt in coap.options:
                content += opt[1]
        elif coap.code == 2:# POST packet
            content += coap.token
            content += coap.option[0][1] # custom options!!!
            content += coap.load
        else:
            print("Falscher Packettyp!")

        hsh = sha256(content).hexdigest()
        if hsh == "0877035e06eb8aee6ab41d118a3bb7a15ebf5c6adc346925143557c98b20efe8":
            print("Packet Nr: " + str(packet_counter) + " Hash OK: " + hsh)