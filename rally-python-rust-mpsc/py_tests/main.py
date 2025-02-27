#  main.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2025.

import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
