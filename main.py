# main.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from ui.main_window import HRPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HRPanel()
    window.showFullScreen()
    sys.exit(app.exec())