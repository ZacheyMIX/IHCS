from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys
from PyQt6.QtWidgets import (
    QWidget,
)

class Spacer(QWidget):
    def __init__(self):
        super().__init__()

        # Create Widgets
        self.s1 = QWidget()
        self.s2 = QWidget()
        self.s2.setFixedHeight(20)
        self.s3 = QWidget()
        self.s4 = QWidget()
        self.s5 = QWidget()
