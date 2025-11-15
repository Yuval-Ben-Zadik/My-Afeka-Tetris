'''
TalStuff.py
Some useful tools for the students in my courses
By: Tal Alon
Version: 1.0
Date: 2025-04-19
'''

from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class Themes:
    '''
    How to use Themes (for PySide6):

    1. Import the Themes class from this module (from TalStuff import Themes).
    2. After creating your QApplication instance, call the desired theme method:
        - For light theme: Themes.light_theme(app)
        - For dark theme: Themes.dark_theme(app)
    '''
    @staticmethod
    def light_theme(app):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f0f0f0"))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor("#e0e0e0"))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.Highlight, QColor("#3399ff"))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)

    @staticmethod
    def dark_theme(app):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2e2e2e"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#121212"))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#3c3c3c"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor("#3399ff"))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)