#!/usr/bin/python

import socket
from scapy.contrib.mqtt import MQTT
from hashlib import sha256
import time, argparse

HASHES = ["56939f07f300cd31e9c462f5893b1abb50bf5e79d100806e41ea47a3093a01db",
          "0e1609970222da6f2b895886911591a057c70717b201863b9600f0b7ec339de3",
          "15408d910a9c5955f17c9ba255f64f972f3f3252737b51a852f513cc4b82f96c",
          "e8ccb1a7054431eb8aaa48e3cbe7a76dde439e1fad47c0a762f4f26bbfa52b7c"]

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 1883           # MQTT-Standardport
PSIZE = 1460

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--Segment", action="store_true", help = "Segement packets into Ethernet MTU sizes")
args = parser.parse_args()

SEG = False
if args.Segment == True: SEG = True
info = "ON" if SEG else "OFF"

# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"MQTT-Receiver running on port {PORT}...")
    print(f"with segmenting {info}")

    conn, addr = server.accept()
    with conn:
        print(f"RECEIVING data from {addr}")
        print("...")
        content = b""
        packet_counter = 0
        start_time = -1.0
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if start_time < 0.0: start_time = time.perf_counter()
            content += data

            #if mqtt_packet.type == 3:
            #    tmp += mqtt_packet.topic
            #    tmp += mqtt_packet.value
            #    print("Reassembled: " + tmp.hex())
        end_recv = time.perf_counter()
        print("FINISHED receiving data")
        print("reassembling payload ...")
        length = len(content)
        idx = 0
        payload = b""
        while idx + PSIZE <= length and SEG:
            x = MQTT(content[idx:idx + PSIZE])
#            x.show()
            packet_counter += 1
            payload += x.msgid.to_bytes(2, 'big')
            payload += x.topic + x.value
            idx += PSIZE

        #print("Länge: " + str(len(content)))
        if len(content[idx:]) != 0:
            x = MQTT(content[idx:])
#            print("Rem Length: " + str(len(content[idx:])))
#            x.summary()
            packet_counter += 1
            payload += x.msgid.to_bytes(2, 'big')
            payload += x.topic+x.value
        
        end_time = time.perf_counter()
        print("FINISHED reassembling data\n")

        hsh = sha256(payload).hexdigest()
        hshCheck = "OK" if hsh in HASHES else "NOT OK"

        print("Hash            : " + hsh + " " + hshCheck)
        print("Payload length  : " + str(len(payload)))
        print("Packet Count    : " + str(packet_counter))
        print(f"Packet reception time  : {end_recv - start_time:.6f} sec")
        print(f"Reassembling time      : {end_time - end_recv:.6f} sec")
        print(f"Total                  : {end_time -start_time:.6f} sec")