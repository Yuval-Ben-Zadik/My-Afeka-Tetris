from PySide6.QtWidgets import QWidget, QLabel, QSlider, QPushButton, QCheckBox, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
import os

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(525, 150, 450, 550)
        self.setWindowIcon(QIcon("settings_icon.png"))

        self.image_label = QLabel('', self)
        self.image_label.setGeometry(0, 0, 450, 550)
        image = QPixmap("Settings_background_image1.png")
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)

        self.volume_label = QLabel("Music Volume:", self)
        self.volume_label.setGeometry(60, 140, 180, 100)
        self.volume_label.setStyleSheet("font-size: 24px;")

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setGeometry(50, 200, 300, 50)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.load_volume_setting())

        self.mute_checkbox = QCheckBox("Mute Music", self)
        self.mute_checkbox.setGeometry(60, 248, 150, 30)
        if self.load_mute_setting():
            self.mute_checkbox.setChecked(True)

        self.grid_label = QLabel("Grid Size:", self)
        self.grid_label.setGeometry(60, 300, 180, 100)
        self.grid_label.setStyleSheet("font-size: 24px;")

        self.grid_combo = QComboBox(self)
        self.grid_combo.setGeometry(60, 370, 150, 30)
        self.grid_combo.addItems(["Small", "Large"])
        self.load_grid_size_setting()

        self.volume_percent_label = QLabel(f"{self.volume_slider.value()}%", self)
        self.volume_percent_label.setGeometry(245, 166, 100, 50)
        self.volume_percent_label.setStyleSheet("font-size: 24px;")
        self.volume_slider.valueChanged.connect(self.update_volume_label)

        self.save_button = QPushButton("Save", self)
        self.save_button.setGeometry(150, 500, 150, 40)
        self.save_button.clicked.connect(self.save_settings)
    
    
    def update_volume_label(self):
        value = self.volume_slider.value()
        self.volume_percent_label.setText(f"{value}%")

    def save_settings(self):
        volume = self.volume_slider.value()
        mute = self.mute_checkbox.isChecked()
        grid_size = self.grid_combo.currentText().lower()
        with open("settings.txt", "w") as f:
            f.write(f"volume={volume}\n")
            f.write(f"mute={mute}\n")
            f.write(f"grid_size={grid_size}\n")
        self.close()

    def load_volume_setting(self):
        if os.path.exists("settings.txt"):
            with open("settings.txt", "r") as f:
                for line in f:
                    if line.startswith("volume="):
                        return int(line.strip().split("=")[1])
        return 100
    
    def load_mute_setting(self):
        if os.path.exists("settings.txt"):
            with open("settings.txt", "r") as f:
                for line in f:
                    if line.startswith("mute="):
                        return line.strip().split("=")[1].lower() == "true"
        return False

    def load_grid_size_setting(self):        
        if os.path.exists("settings.txt"):
            with open("settings.txt", "r") as f:
                for line in f:
                    if line.startswith("grid_size="):
                        grid_size = line.strip().split("=")[1]
                        if grid_size.lower() == "small":
                            self.grid_combo.setCurrentText("Small")
                        else:
                            self.grid_combo.setCurrentText("Large")