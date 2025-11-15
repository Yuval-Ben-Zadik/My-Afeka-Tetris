from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtGui import QPixmap
import os

class CreatePlayerWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Create Player")
        self.setGeometry(525, 150, 450, 550)

        self.image_label = QLabel('', self)
        self.image_label.setGeometry(0, 0, 450, 550)
        image = QPixmap("Create_Player_image.png")
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)

        self.main_window = main_window

        self.new_player_label = QLabel("Enter A New Player Name:", self)
        self.new_player_label.setGeometry(90, 280, 300, 30)
        self.new_player_label.setStyleSheet("font-size: 20px;")

        self.new_player_input = QLineEdit(self)
        self.new_player_input.setGeometry(80, 320, 300, 30)
        self.new_player_input.setStyleSheet("border-bottom: 2px solid white;")
        self.new_player_input.setMaxLength(20)

        self.create_button = QPushButton("Create", self)
        self.create_button.setGeometry(150, 500, 150, 40)
        self.create_button.clicked.connect(self.create_player)

    def create_player(self):
        player_name = self.new_player_input.text()
        if not player_name:
            QMessageBox.warning(self, "Missing Name", "Please enter a name or close the window to cancel.")
            return
        if os.path.exists("Players_Names.txt"):
            with open("Players_Names.txt", "r") as file:
                existing_names = file.read().splitlines()
            if player_name in existing_names:
                QMessageBox.warning(self, "Name Exists", "This name already exists. Please choose a different name.")
                return   
        with open("Players_Names.txt", "a") as file:
            file.write(player_name + "\n")
        self.main_window.set_player_name(player_name)
        self.close()