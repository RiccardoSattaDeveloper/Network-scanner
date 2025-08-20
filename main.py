import tkinter as tk
from gui import ScannerApp

class MainApp:
    @staticmethod
    def run():
        root = tk.Tk()
        app = ScannerApp(root)
        root.mainloop()

if __name__ == "__main__":
    MainApp.run()