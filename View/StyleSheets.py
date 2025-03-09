from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys
from PyQt6.QtWidgets import (
    QWidget,
)


class StyleSheet():
    def __init__(self):
        super().__init__()

        # Style for enabled tab button

    def enabledButtonStyle(self):
        return """
                QPushButton {
                    background-color: transparent;
                    color: black;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(100, 100, 255, 100);
                    border-radius: 10px;
                }
                QPushButton:pressed {
                    background-color: rgba(80, 80, 255, 100);
                    border-radius: 10px;
                }
            """

    # Style for disabled tab buttons
    def disabledButtonStyle(self):
        return """
                        QPushButton {
                            background-color: transparent;
                            color: grey;
                            font-size: 16px;
                        }
                    """

    # Style for regular buttons on the page
    def pageButtonStyle(self):
        return """
                QPushButton {
                    background-color: transparent;
                    border-style: outset;
                    border-width: 1px;
                    border-color: blue;
                    border-radius: 2px;
                    color: blue;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(100, 100, 255, 100); 
                }
                QPushButton:pressed {
                    background-color: rgba(80, 80, 255, 100);
                }
            """

    def browseButtonStyle(self):
        return """
                        QPushButton {
                            background-color: rgba(120, 120, 255, 255);
                            color: white;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: rgba(100, 100, 255, 255);
                        }
                        QPushButton:pressed {
                            background-color: rgba(80, 80, 255, 255);
                        }
                    """
