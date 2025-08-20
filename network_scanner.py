from scapy.all import ARP, Ether, srp, conf
import socket

class NetworkScanner:
    def __init__(self, interface):
        self.interface = interface
        conf.iface = interface

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def scan(self, ip_range):
        try:
            arp_request = ARP(pdst=ip_range)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered = srp(arp_request_broadcast, timeout=2, verbose=0)[0]

            devices = []
            for sent, received in answered:
                devices.append({
                    "ip": received.psrc,
                    "mac": received.hwsrc
                })
            return devices
        except Exception as e:
            return f"Errore durante la scansione: {e}"