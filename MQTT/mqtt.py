from cbor2 import dumps
import scapy.contrib.mqtt as mqtt
from scapy.all import IP, TCP, RandShort, send, sr1, load_contrib


daten = {"name": "Clemens", "wert": 42, "aktiv": 2}
data = dumps(daten).hex()
print(data + " len: " + str(len(data)))

byte_data = bytes.fromhex(data)

p = mqtt.MQTT()/mqtt.MQTTConnect(clientIdlen=len(byte_data[:5]), clientId=byte_data[:5], protoname='MQTT', protolevel=5)
a = mqtt.MQTT(QOS=1)/mqtt.MQTTPublish(msgid=1, topic=byte_data[:5], value=byte_data[5:10])

# TCP-Verbindung aufbauen
ip = IP(dst="127.0.0.1")
sport = RandShort()
tcp_syn = TCP(sport=sport, dport=1883, flags="S", seq=1000)
synack = sr1(ip / tcp_syn, timeout=2)

""" """
if synack and synack.haslayer(TCP):
    seq = tcp_syn.seq + 1
    ack = synack.seq + 1
    tcp_ack = TCP(sport=sport, dport=1883, flags="A", seq=seq, ack=ack)
    send(ip / tcp_ack)

    # MQTT CONNECT senden
    tcp_push = TCP(sport=sport, dport=1883, flags="PA", seq=seq, ack=ack)
    send(ip / tcp_push / a)
    print(p.summary())

#s = IP(dst="10.0.0.11") / TCP(dport=1883) / a
#print(s.summary())
#send(s)