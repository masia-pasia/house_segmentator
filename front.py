import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QColor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QComboBox, \
    QColorDialog, QFileDialog, QFrame
import main
import numpy as np
from PIL import Image as im
from PIL.ImageQt import ImageQt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Ustawienia okna
        self.setWindowTitle("House segmenter app")
        self.setGeometry(100, 100, 400, 300)

        # Tworzenie całego layoutu
        layout = QVBoxLayout()

        # Towrzenie title layoutu
        title_layout = QVBoxLayout()
        title_frame = QFrame()
        title_frame.setStyleSheet("background-color: white;")
        title_frame_layout = QVBoxLayout()

        title_label = QLabel("<font color='navy'><b><font size='+10' face='Georgia'>House Segmenter</font></b></font>")

        title_frame_layout.addWidget(title_label, alignment=Qt.AlignHCenter)
        title_frame.setLayout(title_frame_layout)
        title_layout.addWidget(title_frame)

        # Tworzenie layoutów
        main_layout = QHBoxLayout()
        left_column_layout = QVBoxLayout()
        middle_column_layout = QVBoxLayout()
        right_column_layout = QVBoxLayout()

        # Tworzenie widżetów
        self.image_label1 = QLabel()
        self.image_label2 = QLabel()
        image_label3 = QLabel()

        # Wczytywanie obrazów
        pixmap1 = QPixmap("dom.jpg").scaled(512, 512)
        pixmap2 = QPixmap("dom.jpg").scaled(512, 512)
        pixmap3 = QPixmap("strzalka.png").scaledToHeight(150, Qt.SmoothTransformation)

        # Wyświetlanie obrazów
        self.image_label1.setPixmap(pixmap1)
        self.image_label2.setPixmap(pixmap2)
        image_label3.setPixmap(pixmap3)

        # Dodanie ramki do obrazów
        self.image_label1.setStyleSheet("border: 2px solid black;")
        self.image_label2.setStyleSheet("border: 2px solid black;")

        # Tworzenie przycisku "Wybierz obraz"
        button_select_image = QPushButton("Wybierz obraz")
        button_select_image.setStyleSheet("QPushButton { background-color: navy; color: white; }")
        button_select_image.clicked.connect(self.select_image)

        # Tworzenie slidera
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Współczynnik alfa:")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.slider)

        # Pole z aktualnie wybranym kolorem
        self.color_preview_label = QLabel()
        self.color_preview_label.setFixedWidth(50)
        self.color_preview_label.setFixedHeight(20)
        self.update_color_preview(QColor("white"), self.slider.value())

        # Tworzenie kolorowego wybieraka
        color_picker_layout = QHBoxLayout()
        color_picker = QPushButton("Wybierz kolor")
        color_picker.clicked.connect(self.choose_color)
        color_picker_layout.addWidget(color_picker)
        color_picker_layout.addWidget(self.color_preview_label)

        # Tworzenie przycisku "Wygeneruj obraz"
        button_submit = QPushButton("Wygeneruj obraz")
        button_submit.setStyleSheet("QPushButton { background-color: #46ab66; color: white; }")

        # Tworzenie drugiej kolumny przycisków
        button1 = QPushButton("Zapisz obraz")

        # Dodawanie przycisku wyboru obrazu
        title_layout.addWidget(QLabel(" "))
        title_layout.addWidget(button_select_image)
        title_layout.addWidget(QLabel("\n\n\n"))

        # Dodawanie widżetów do odpowiednich layoutów
        left_column_layout.addWidget(self.image_label1, alignment=Qt.AlignTop)
        left_column_layout.addLayout(slider_layout)
        left_column_layout.addLayout(color_picker_layout)
        left_column_layout.addWidget(button_submit)

        middle_column_layout.addWidget(QLabel("\n\n\n\n\n\n\n\n"))
        middle_column_layout.addWidget(image_label3)
        middle_column_layout.addStretch()

        right_column_layout.addWidget(self.image_label2, alignment=Qt.AlignTop)
        right_column_layout.addWidget(button1, alignment=Qt.AlignTop)

        main_layout.addLayout(left_column_layout)
        main_layout.addLayout(middle_column_layout)
        main_layout.addLayout(right_column_layout)

        layout.addLayout(title_layout)
        layout.addLayout(main_layout)

        # Ustawienie layoutu głównego dla okna
        self.setLayout(layout)

        # Połączenie zdarzenia zmiany wartości slidera z aktualizacją podglądu koloru
        self.slider.valueChanged.connect(lambda value: self.update_color_preview(QColor("white"), value))

        # Połączenie zdarzenia generowania obrazu z funkcją
        button_submit.clicked.connect(self.generate_image)

        self.file_path = ''

    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setNameFilter("Obrazy (*.jpg *.png)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.file_path = selected_files[0]
            print("Wybrano plik:", self.file_path)

        if self.file_path:
            pixmap = QPixmap(self.file_path).scaled(512, 512)
            self.image_label1.setPixmap(pixmap)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.update_color_preview(color, self.slider.value())

    def update_color_preview(self, color, alpha):
        rgba_color = QColor(color.red(), color.green(), color.blue(), alpha)
        style_sheet = f"background-color: {rgba_color.name()}"
        self.color_preview_label.setStyleSheet(style_sheet)

    def generate_image(self):
        alpha = self.slider.value() / 100.0
        color = self.color_preview_label.palette().color(QPalette.Background)
        color_array = [color.red(), color.green(), color.blue()]
        segment = 1
        print(self.file_path, alpha, color_array, segment)

        try:
            result_image = main.add_mask(self.file_path, alpha, color_array, color_array, segment)
            pil_image = im.fromarray(result_image)
            qimage = ImageQt(pil_image)
            pixmap = QPixmap.fromImage(qimage)
        except Exception as e:
            print("Wystąpił błąd")
            print(traceback.format_exc())

        self.image_label2.setPixmap(pixmap.scaled(512, 512, Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
