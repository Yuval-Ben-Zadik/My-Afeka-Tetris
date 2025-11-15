from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
import sys
import os
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from TalStuff import Themes
from Game import TetrisGameWindow
from Settings import SettingsWindow
from Create_Player import CreatePlayerWindow
from Choose_player import ChoosePlayerWindow
from Users import ScoreHistoryWindow
from Scores import HighScoresWindow
from About import AboutWindow
import pygame



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Defaults
        self.mute_music = False
        self.music_volume = 1
        self.grid_size = "small"
        self.player_name = ""

        # Window setup
        self.setWindowTitle("Yuval's Tetris Game")
        self.setGeometry(500, 130, 500, 650)
        self.setWindowIcon(QIcon("my_tetris_icon.png"))

        # background image
        # I created the background image using chatGPT
        self.image_label = QLabel('', self)
        self.image_label.setGeometry(0, 0, 500, 650)
        image = QPixmap("background_image.png")
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)

        # Buttons
        self.buttons()

        # windows
        self.settings_window = None
        self.create_player_window = None


    def play_clicked_sound(self):
        pygame.mixer.init()
        if self.mute_music:
            return
        clicked_sound = pygame.mixer.Sound("click_sound.mp3")
        clicked_sound.set_volume(self.music_volume)
        clicked_sound.play()

    
    def set_player_name(self, player_name):
        self.player_name = player_name
        self.player_name_label.setText(f"Player Now Playing: {player_name}")


    def buttons(self):
        self.player_name_label = QLabel(self)
        self.player_name_label.setGeometry(25, 20, 450, 50)
        self.player_name_label.setText("Player Now Playing:")
        self.player_name_label.setStyleSheet("font-size: 20px;")
        self.player_name_label.setAlignment(Qt.AlignCenter)


        self.start_game_button = QPushButton("Start Game", self)
        self.start_game_button.setGeometry(170, 210, 160, 40)
        self.start_game_button.clicked.connect(self.play_clicked_sound)  
        self.start_game_button.clicked.connect(self.launch_game)


        self.choose_player_button = QPushButton("Choose Player", self)
        self.choose_player_button.setGeometry(170, 265, 160, 40)
        self.choose_player_button.clicked.connect(self.play_clicked_sound)
        self.choose_player_button.clicked.connect(self.choose_player)


        self.create_player_button = QPushButton("Create Player", self)
        self.create_player_button.setGeometry(170, 320, 160, 40)
        self.create_player_button.clicked.connect(self.play_clicked_sound)
        self.create_player_button.clicked.connect(self.create_player)


        self.score_history_button = QPushButton("Score History", self)
        self.score_history_button.setGeometry(170, 375, 160, 40)
        self.score_history_button.clicked.connect(self.play_clicked_sound)
        self.score_history_button.clicked.connect(self.show_score_history)


        self.high_scores_button = QPushButton("High Scores", self)
        self.high_scores_button.setGeometry(170, 430, 160, 40)
        self.high_scores_button.clicked.connect(self.play_clicked_sound)
        self.high_scores_button.clicked.connect(self.show_high_scores)


        self.about_button = QPushButton("About", self)
        self.about_button.setGeometry(170, 485, 160, 40)
        self.about_button.clicked.connect(self.play_clicked_sound)
        self.about_button.clicked.connect(self.show_about)


        self.video_button = QPushButton("Intro Video", self)
        self.video_button.setGeometry(170, 540, 160, 40)
        self.video_button.clicked.connect(self.play_clicked_sound)
        self.video_button.clicked.connect(self.show_intro_video)


        self.settings_button = QPushButton("Settings", self)
        self.settings_button.setGeometry(170, 595, 160, 40)
        self.settings_button.clicked.connect(self.play_clicked_sound)
        self.settings_button.clicked.connect(self.open_settings)


    def launch_game(self):
        # first check if the user input is existing
        if not self.player_name_label.text() or self.player_name_label.text() == "Player Now Playing:":
            warning_msg = QMessageBox.warning(self, "Input Error", "Please enter a new player name or choose an existing one.")

        # if the user input is existing, launch the game
        else:
            top_left_point = self.geometry().topLeft()
            x = top_left_point.x() + 125
            y = top_left_point.y() + 35

            self.game_window = TetrisGameWindow(x, y, player_name=self.player_name)
            self.game_window.run()
            self.show()




    def open_settings(self):
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsWindow()
            self.settings_window.show()

    
    def create_player(self):
        if self.create_player_window is None or not self.create_player_window.isVisible():
            self.create_player_window = CreatePlayerWindow(self)
            self.create_player_window.show()

    
    def choose_player(self):
        self.choose_window = ChoosePlayerWindow(self)
        self.choose_window.show()

    
    def show_score_history(self):
        player_name = self.player_name
        if not player_name:
            QMessageBox.warning(self, "No Player Selected", "Please select or create a player first.")
            return
        self.score_window = ScoreHistoryWindow(player_name)
        self.score_window.show()


    def show_high_scores(self):
        self.high_scores_window = HighScoresWindow()
        self.high_scores_window.show()

    
    def show_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    
    def show_intro_video(self):
        video_path = "the_best.mp4"
        if os.path.exists(video_path):
            print("Playing video")
            os.startfile(video_path)
        else:
            print("Video file not found.")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    Themes.dark_theme(app)

    css_file_path = os.path.join(os.path.dirname(__file__), "stylesheet.css")
    with open(css_file_path, "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
