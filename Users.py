from PySide6.QtWidgets import QWidget, QLabel, QListWidget, QAbstractItemView
from PySide6.QtGui import Qt, QPixmap
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ScoreHistoryWindow(QWidget):
    def __init__(self, player_name):
        super().__init__()

        self.player_name = player_name
        self.setWindowTitle(f"{self.player_name}'s Score History")
        self.setGeometry(525, 60, 450, 740)

        self.image_label = QLabel('', self)
        self.image_label.setGeometry(0, 0, 450, 740)
        image = QPixmap("Score_History_image.png")
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)

        self.title_label = QLabel(f"Player: {self.player_name}", self)
        self.title_label.setGeometry(10, 20, 450, 50)
        self.title_label.setStyleSheet("font-size: 20px; color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.score_list = QListWidget(self)
        self.score_list.setGeometry(25, 305, 40, 430)
        self.score_list.setSpacing(1)
        self.score_list.setFocusPolicy(Qt.NoFocus) # Disable focus on the list
        self.score_list.setSelectionMode(QAbstractItemView.NoSelection) # Disable selection. CHATGPT helps me with it

        self.load_scores()

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: white;")
        self.canvas.setParent(self)
        self.canvas.setGeometry(80, 325, 360, 350)

        self.plot_scores_graph()


    
    def load_scores(self):
        self.scores = []
        found = False
        if os.path.exists("all_scores.txt"):
            with open("all_scores.txt", 'r') as file:
                for line in file:
                    if line.startswith(f"{self.player_name}-"):
                        score = line.strip().split("-")[1]
                        self.scores.append(int(score))
                        self.score_list.addItem(score)
                        found = True
            if not found:
                self.title_label.setText(f"No scores found for {self.player_name}")


    def plot_scores_graph(self):
        if not self.scores:
            return
        
        x = list(range(1, len(self.scores) + 1))
        y = self.scores

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(x, y, marker='o', color='blue', label='Score')

        ax.set_facecolor('white')
        self.figure.set_facecolor('white')

        ax.set_title("Score(Game Num)")
        ax.set_xlabel("Game Number")
        ax.set_ylabel("Score")
        ax.legend()

        self.figure.tight_layout()
        self.canvas.draw()