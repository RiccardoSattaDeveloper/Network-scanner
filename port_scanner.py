from scapy.all import IP, TCP, sr1

class PortScanner:

    def __init__(self, ip: str, ports=None): 
        self.ip = ip
        self.ports = ports if ports else [22, 80, 443, 3389, 8080]

    def scan(self):
        open_ports = []

        for port in self.ports:
            pkt = IP(dst=self.ip)/TCP(dport=port, flags="S") 

            response = sr1(pkt, timeout=1, verbose=0)

            if response and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
                open_ports.append(port)

                sr1(IP(dst=self.ip)/TCP(dport=port, flags="R"), timeout=1, verbose=0)

        return open_ports
