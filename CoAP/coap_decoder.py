#!/usr/bin/python

import socket
from scapy.contrib.coap import CoAP
from hashlib import sha256
import time, argparse, sys


HASHES = ["56939f07f300cd31e9c462f5893b1abb50bf5e79d100806e41ea47a3093a01db" , "0e1609970222da6f2b895886911591a057c70717b201863b9600f0b7ec339de3", "15408d910a9c5955f17c9ba255f64f972f3f3252737b51a852f513cc4b82f96c"]

# Server-Konfiguration
HOST = '0.0.0.0'      # Lauscht auf allen Interfaces
PORT = 5683           # MQTT-Standardport
PSIZE = 1472

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--Length", type=int, help = "Length of expected exfiltratino data (1, 5, 10 MB)")
args = parser.parse_args()

size = int(args.Length)
if size == 1:
    exceptedPackets = 629
elif size == 5:
    exceptedPackets = 3142
elif size == 10:
    exceptedPackets = 6284
else:
    print("Invalid exfiltration size!")
    sys.exit(1)



# TCP-Socket einrichten
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 20 * 1024 * 1024)
#    server.settimeout(2.0)
    server.bind((HOST, PORT))
    print(f"CoAP-Receiver running on port {PORT}")
    tmp = b""
    payload = b""
    i = 0
    start_time = 0.0
    while True:
        data, addr = server.recvfrom(4096)
        if i == 0:
            print(f"RECEIVING data from {addr}")
            print("...")
            start_time = time.perf_counter()
#        coap = CoAP(data)  # 'data' stammt aus recvfrom
        i += 1

#        print(str(i))
        payload += data
        if i == exceptedPackets: break
#        if i == 629: break # 631
#        if i == 3142: break # 3151
#        if i == 6284: break # 6301

    length = len(payload)
#    print("i: " + str(i) + " len: " + str(len(payload)))
    end_recv = time.perf_counter()
    print("FINISHED receiving data")
    print("reassembling payload ...")

    idx = 0
    packet_counter = 0
    while idx + PSIZE <= length:
        x = CoAP(payload[idx:idx + PSIZE])
 #       x.show()
        packet_counter += 1
        tmp += x.msg_id.to_bytes(2, 'big')
        tmp += x.token
#        if x.code == 1:
        for opt in x.options:
            tmp += opt[1]
        if x.code == 2:     # Bei Publish Packets
            tmp += x.load

        idx += PSIZE
    
    x = CoAP(payload[idx:])
#    x.show()
    packet_counter += 1
    tmp += x.msg_id.to_bytes(2, 'big')
    tmp += x.token
#    if x.code == 1:
    for opt in x.options:
        tmp += opt[1]
    if x.code == 2:     # Bei Publish Packets
        tmp += x.load

    end_time = time.perf_counter()
    print("FINISHED reassembling data\n")

    hsh = sha256(tmp).hexdigest()
    hshCheck = "OK" if hsh in HASHES else "NOT OK"

    print("Hash                   : " + hsh + " " + hshCheck)
    print("Payload length         : " + str(len(tmp)))
    print("Packet Count           : " + str(packet_counter))
    print(f"Packet reception time  : {end_recv - start_time:.6f} sec")
    print(f"Reassembling time      : {end_time - end_recv:.6f} sec")
    print(f"Total                  : {end_time - start_time:.6f} sec")
    
    """print(hsh)
    if hsh == "56939f07f300cd31e9c462f5893b1abb50bf5e79d100806e41ea47a3093a01db" or hsh == "0e1609970222da6f2b895886911591a057c70717b201863b9600f0b7ec339de3":
        print("Packet Nr: " + str(i) + " Hash OK")"""
               