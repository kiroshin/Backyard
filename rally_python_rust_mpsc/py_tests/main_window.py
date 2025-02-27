#  main_window.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2025.
import threading

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)
from rally_python_rust_mpsc import ready

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HELLO")
        self.setMinimumSize(300, 150)
        self.resize(300, 150)
        self.bootup()
        self.tick_sender = ready(lambda x: print("PYTHON: ", x, threading.current_thread()))
        self.other_sender = self.tick_sender
        print("=>", self.tick_sender)


    def bootup(self):
        widget = QWidget(self)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)

        btn1 = QPushButton("TEST ACTION1")
        btn1.clicked.connect(self.action1)
        layout.addWidget(btn1, 0, Qt.AlignmentFlag.AlignCenter)

        btn2 = QPushButton("TEST ACTION2")
        btn2.clicked.connect(self.action2)
        layout.addWidget(btn2, 0, Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(widget)

    def action1(self):
        print("Action 1 ...")
        self.tick_sender.send(123)

    def action2(self):
        print("Action 2 ...")
        self.other_sender.send(456)
