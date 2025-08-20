import tkinter as tk
from tkinter import ttk, messagebox
from network_scanner import NetworkScanner

class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LAN Scanner")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        ttk.Label(root, text="Range IP (lascia vuoto per rete locale):").pack(pady=5)
        self.ip_entry = ttk.Entry(root, width=30)
        self.ip_entry.pack(pady=5)

        ttk.Label(root, text="Interfaccia di rete:").pack(pady=5)
        self.iface_combobox = ttk.Combobox(root, values=self.get_interfaces(), state="readonly")
        self.iface_combobox.pack(pady=5)
        if self.iface_combobox['values']:
            self.iface_combobox.current(0)

        self.scan_button = ttk.Button(root, text="Avvia scansione", command=self.start_scan)
        self.scan_button.pack(pady=10)

        self.text = tk.Text(root, height=15, width=60)
        self.text.pack(pady=5)
        self.text.config(state=tk.DISABLED)

    def get_interfaces(self):
        from scapy.all import get_if_list
        return get_if_list()

    def log(self, message):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)

    def start_scan(self):
        ip_range = self.ip_entry.get().strip() or None
        iface = self.iface_combobox.get() or None
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.config(state=tk.DISABLED)

        self.log(f"Scansione della rete locale in corso su {iface}...")

        self.scanner = NetworkScanner(ip_range=ip_range, interface=iface)
        self.scanner.start_scan_thread(callback=self.log)