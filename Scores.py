from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel,QHeaderView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os


class HighScoresWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("High Scores")
        self.setGeometry(525, 60, 450, 740)

        self.image_label = QLabel('', self)
        self.image_label.setGeometry(0, 0, 450, 740)
        image = QPixmap("High_Scores_image.png")
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)

        self.high_scores_table = QTableWidget(self)
        self.high_scores_table.setColumnCount(2)
        self.high_scores_table.setHorizontalHeaderLabels(["Player", "Score"])
        self.high_scores_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.high_scores_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.high_scores_table.setSelectionMode(QTableWidget.NoSelection)
        self.high_scores_table.setGeometry(50, 330, 340, 380)

        self.load_high_scores()


    def load_high_scores(self):
        scores = []

        if os.path.exists("all_scores.txt"):
            with open("all_scores.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if "-" in line:
                        name, score_str = line.split("-")
                        if score_str.isdigit():
                            score = int(score_str)
                            scores.append([name, score])
        
        for i in range(len(scores)):
            for j in range(i + 1, len(scores)):
                if scores[j][1] > scores[i][1]:
                    temp = scores[i]
                    scores[i] = scores[j]
                    scores[j] = temp


        if len(scores) > 10:
            scores = scores[:10]

        self.high_scores_table.setRowCount(len(scores))

        for row in range(len(scores)):
            name_item = QTableWidgetItem(scores[row][0])
            score_item = QTableWidgetItem(str(scores[row][1]))
            name_item.setTextAlignment(Qt.AlignCenter)
            score_item.setTextAlignment(Qt.AlignCenter)

            self.high_scores_table.setItem(row, 0, name_item)
            self.high_scores_table.setItem(row, 1, score_item)