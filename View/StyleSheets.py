from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys

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
                    border-radius: 10px
                }
                QPushButton:hover {
                    background-color: rgba(100, 100, 255, 100);
                    border-radius: 10px;
                }
                QPushButton:pressed {
                    background-color: rgba(60, 60, 255, 100);
                    border-radius: 10px;
                }
            """

    def selectedButtonStyle(self):
        return """
                        QPushButton {
                            background-color: rgba(100, 100, 255, 100);
                            color: black;
                            font-size: 16px;
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
                            border-radius: 10px;
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
                    color: rgba(30, 30, 30, 255)
                }
                QPushButton:pressed {
                    background-color: rgba(0, 0, 255, 155);
                    color: white
                }
            """

    def disabledPageButtonStyle(self):
        return """
                QPushButton {
                    background-color: transparent;
                    border-style: outset;
                    border-width: 1px;
                    border-color: grey;
                    border-radius: 2px;
                    color: grey;
                    font-size: 16px;
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

    def progressBarStyle(self):
        return """
    QProgressBar {
        background-color: #E8E8E8;
        color: #333;
        border: 1px solid #999;
        border-radius: 5px;
    }
    
    QProgressBar::chunk {
        background-color: #007BFF;
    }
"""
