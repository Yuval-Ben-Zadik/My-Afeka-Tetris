from PySide6.QtWidgets import QWidget, QListWidget, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os


class ChoosePlayerWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Choose Player")
        self.setGeometry(525, 60, 450, 740)

        self.image_label = QLabel('', self)
        self.image_label.setGeometry(0, 0, 450, 740)
        image = QPixmap("Choose_Player_image.png")
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)

        self.player_list = QListWidget(self)
        self.player_list.setGeometry(120, 305, 200, 430)
        self.player_list.setSpacing(1)

        self.load_players_names()

        self.select_button = QPushButton("Select", self)
        self.select_button.setGeometry(150, 30, 150, 40)
        self.select_button.clicked.connect(self.select_player)

    def load_players_names(self):
        if os.path.exists("Players_Names.txt"):
            with open("Players_Names.txt", "r") as file:
                players = file.read().splitlines()
                self.player_list.addItems(players)

    def select_player(self):
        selected_player = self.player_list.currentItem()
        if selected_player:
            player_name = selected_player.text()
            self.main_window.set_player_name(player_name)
            self.close()