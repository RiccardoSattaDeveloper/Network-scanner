import threading
from scapy.all import ARP, Ether, srp, conf

class NetworkScanner:
    def __init__(self, ip_range=None, interface=None):
        if interface:
            conf.iface = interface
        self.interface = conf.iface
        self.ip_range = ip_range
        self.results = []

    def scan_network(self, callback=None):
        if not self.ip_range:
            self.ip_range = self.get_local_network_range()
        try:
            packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ip_range)
            ans, _ = srp(packet, timeout=2, retry=2, verbose=0, iface=self.interface)

            self.results = []
            for i, snd in enumerate(ans, 1):
                ip = snd[1].psrc
                mac = snd[1].hwsrc
                self.results.append((ip, mac))
                if callback:
                    callback(f"[{i}] IP: {ip}  MAC: {mac}")

        except Exception as e:
            if callback:
                callback(f"Errore durante la scansione: {e}")

    def get_local_network_range(self):
        import socket, struct, fcntl, os

        ip = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = fcntl.ioctl(
                s.fileno(),
                0x8915,
                struct.pack('256s', self.interface[:15].encode('utf-8'))
            )[20:24]
            ip = socket.inet_ntoa(ip)
        except:
            ip = "192.168.1.0"

        net = ".".join(ip.split(".")[:3]) + ".0/24"
        return net

    def start_scan_thread(self, callback=None):
        thread = threading.Thread(target=self.scan_network, args=(callback,))
        thread.daemon = True
        thread.start()