import sys
from PyQt5.QtWidgets import QApplication
from gui import NetworkScannerGUI

class MainApp:
    @staticmethod
    def run():
        app = QApplication(sys.argv)
        window = NetworkScannerGUI()
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    MainApp.run()