import sys
import ipaddress
import psutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QTextEdit, QMessageBox
)
from network_scanner import NetworkScanner

def get_network_interfaces():
    interfaces = []
    for iface_name, addrs in psutil.net_if_addrs().items():
        if iface_name == "lo":
            continue
        interfaces.append(iface_name)
    return interfaces

class NetworkScannerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Scanner")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Seleziona l'interfaccia di rete:")
        layout.addWidget(self.label)

        self.interface_combo = QComboBox()
        self.interface_combo.addItems(get_network_interfaces())
        layout.addWidget(self.interface_combo)

        self.scan_button = QPushButton("Scansiona la rete")
        self.scan_button.clicked.connect(self.scan_network)
        layout.addWidget(self.scan_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def scan_network(self):
        interface = self.interface_combo.currentText()
        scanner = NetworkScanner(interface)
        local_ip = scanner.get_local_ip()

        try:
            network = ipaddress.IPv4Network(local_ip + "/24", strict=False)
            ip_range = str(network)
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nel calcolo della rete: {e}")
            return

        self.result_area.append(f"Scansione in corso su {ip_range} ({interface})...\n")
        devices = scanner.scan(ip_range)

        if isinstance(devices, str):
            self.result_area.append(devices)
        elif devices:
            for device in devices:
                self.result_area.append(f"IP: {device['ip']}  -  MAC: {device['mac']}")
        else:
            self.result_area.append("Nessun host trovato.")