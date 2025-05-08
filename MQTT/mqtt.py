from cbor2 import dumps
import socket
import scapy.contrib.mqtt as mqtt
from scapy.all import IP, TCP, RandShort, send, sr1, load_contrib


daten = {"name": "Clemens", "wert": 42, "aktiv": 2}
data = dumps(daten).hex()
print(data + " len: " + str(len(data)))

byte_data = bytes.fromhex(data)

p = mqtt.MQTT()/mqtt.MQTTConnect(clientId=byte_data[:5],
                                 willflag=1, usernameflag=1, passwordflag=1,
                                 willtopic=byte_data[:5], willmsg=byte_data[:5],
                                 username=byte_data[:5], password=byte_data[0:5],
                                 protoname='MQTT', cleansess=1, klive=60, protolevel=6)
a = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=1, topic=byte_data[:5], value=byte_data[5:10])

# TCP-Verbindung aufbauen
"""ip = IP(dst="10.0.0.12")
sport = RandShort()
tcp_syn = TCP(sport=sport, dport=1883, flags="S", seq=1000)
synack = sr1(ip / tcp_syn, timeout=2)"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("10.0.0.12", 1883))
    s.sendall(bytes(p))
    print("MQTT CONNECT gesendet")
    s.sendall(bytes(a))
    print("MQTT PUBLISH gesendet")

"""
if synack and synack.haslayer(TCP):
    seq = tcp_syn.seq + 1
    ack = synack.seq + 1
    tcp_ack = TCP(sport=sport, dport=1883, flags="A", seq=seq, ack=ack)
    send(ip / tcp_ack)

    tcp_push = TCP(sport=sport, dport=1883, flags="PA", seq=seq, ack=ack)
    send(ip / tcp_push / p)
    print(p.summary())

    # MQTT CONNECT senden
    tcp_push = TCP(sport=sport, dport=1883, flags="PA", seq=seq, ack=ack)
    send(ip / tcp_push / a)
    print(p.summary())"""