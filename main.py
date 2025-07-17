import sys
from core.app import BanglaOCRApp
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = BanglaOCRApp()
    window.show()
    sys.exit(app.exec_())
