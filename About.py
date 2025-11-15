from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from PySide6.QtGui import QPixmap
import webbrowser

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("About Me")
        self.setGeometry(500, 100, 500, 700) 
        with open('stylesheet.css', 'r') as fp:
            self.setStyleSheet(fp.read())

        self.background_image_label = QLabel('', self)
        self.background_image_label.setGeometry(0, 0, 500, 700)
        image = QPixmap("Settings_background_image1.png")
        self.background_image_label.setPixmap(image)
        self.background_image_label.setScaledContents(True)

        self.image_label = QLabel('', self)
        self.image_label.setGeometry(40, 10, 430, 350)
        image = QPixmap('thanos_about.png')
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)
        self.image_label.setStyleSheet("border: 5px solid white;")

        self.name_label = QLabel("Yuval Ben Zadik", self)
        self.name_label.setGeometry(120, 380, 300, 30)
        self.name_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")

        self.email_label = QLabel("Email: yuval.ben.zadik@s.afeka.ac.il", self)
        self.email_label.setGeometry(110, 450, 300, 30)
        self.email_label.setStyleSheet("font-size: 15px; color: white;")

        self.linkedin_button = QPushButton('My LinkedIn', self)
        self.linkedin_button.clicked.connect(self.linkedin_method)
        self.linkedin_button.setGeometry(150, 540, 200, 30)


    
    def linkedin_method(self):
        webbrowser.open('https://www.linkedin.com/in/yuval-ben-zadik-95816929b')


