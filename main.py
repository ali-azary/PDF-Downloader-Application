from app import App
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec_())
