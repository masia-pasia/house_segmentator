import sys
import traceback

from PIL import Image as im
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QPalette, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, \
    QColorDialog, QFileDialog, QFrame, QRadioButton

import main


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.segment = 0

        # Ustawienia okna
        self.setWindowTitle("House segmenter app")
        self.setGeometry(100, 100, 400, 300)

        # Ustawienie ikonki aplikacji
        app.setWindowIcon(QIcon("dom.jpg"))

        # Tworzenie całego layoutu
        layout = QVBoxLayout()

        # Towrzenie title layoutu
        title_layout = QVBoxLayout()
        title_frame = QFrame()
        title_frame.setStyleSheet("background-color: gray;")
        title_frame_layout = QVBoxLayout()

        title_label = QLabel(
            "<font color='yellow'><b><font size='+10' face='Georgia' >House Segmenter</font></b></font>")
        title_label.setStyleSheet(
            "font-family: verdana; font-size: 15px; color: #404040; font-style: normal; font-weight: bold; "
            "font-variant: small-caps; text-align: left; letter-spacing: 3px; line-height: 20px; "
            "text-shadow: 2px 6px 6px rgba(29, 40, 185, 1);")

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
        pixmap2 = QPixmap("brak_domu.jpg").scaled(512, 512)
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
        button_select_image.setStyleSheet("QPushButton { background-color: #404040; color: white; }")
        button_select_image.clicked.connect(self.select_image)

        # Radioboxy
        hbox = QHBoxLayout()
        # Tworzenie etykiety
        label = QLabel('Wybierz kolorowany element:')
        label.setStyleSheet("color: white;")
        # Tworzenie trzech radioboxów
        self.radio1 = QRadioButton('okna')
        self.radio2 = QRadioButton('dach')
        self.radio3 = QRadioButton('okna i dach')
        # Ustawianie kolorów buttonów
        self.radio1.setStyleSheet("color: white;")
        self.radio2.setStyleSheet("color: white;")
        self.radio3.setStyleSheet("color: white;")
        # Łączenie przycisków z funkcjami
        self.radio1.toggled.connect(self.radio_connect)
        self.radio2.toggled.connect(self.radio_connect)
        self.radio3.toggled.connect(self.radio_connect)
        self.radio3.toggled.connect(self.radio_connect)
        # Dodawanie etykiety i radioboxów do układu poziomego
        hbox.addWidget(label)
        hbox.addWidget(self.radio1)
        hbox.addWidget(self.radio2)
        hbox.addWidget(self.radio3)

        # Tworzenie slidera
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Współczynnik alfa:")
        slider_label.setStyleSheet("color: white;")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.slider)

        # Pole z aktualnie wybranym kolorem wybieraka 1
        self.color_preview_label = QLabel()
        self.color_preview_label.setFixedWidth(50)
        self.color_preview_label.setFixedHeight(20)
        self.update_color_preview(QColor("white"), self.slider.value())

        # Tworzenie kolorowego wybieraka 1
        color_picker_layout = QHBoxLayout()
        color_picker = QPushButton("Wybierz kolor okien")
        color_picker.setStyleSheet("QPushButton { background-color: #404040; color: white; }")
        color_picker.clicked.connect(self.choose_color)
        color_picker_layout.addWidget(color_picker)
        color_picker_layout.addWidget(self.color_preview_label)

        # Pole z aktualnie wybranym kolorem wybieraka 2
        self.color_preview_label2 = QLabel()
        self.color_preview_label2.setFixedWidth(50)
        self.color_preview_label2.setFixedHeight(20)
        self.update_color_preview2(QColor("white"), self.slider.value())

        # Tworzenie kolorowego wybieraka 2
        color_picker_layout2 = QHBoxLayout()
        color_picker2 = QPushButton("Wybierz kolor dachu")
        color_picker2.setStyleSheet("QPushButton { background-color: #404040; color: white; }")
        color_picker2.clicked.connect(self.choose_color2)
        color_picker_layout2.addWidget(color_picker2)
        color_picker_layout2.addWidget(self.color_preview_label2)

        # Tworzenie przycisku "Wygeneruj obraz"
        button_submit = QPushButton("Wygeneruj obraz")
        button_submit.setStyleSheet("QPushButton { background-color: #46ab66; color: white; }")

        # Tworzenie drugiej kolumny przycisków
        button1 = QPushButton("Zapisz obraz")
        button1.setStyleSheet("QPushButton { background-color: #404040; color: white; }")
        button1.clicked.connect(self.save_image)

        # Dodawanie przycisku wyboru obrazu
        title_layout.addWidget(QLabel(" "))
        title_layout.addWidget(button_select_image)
        title_layout.addWidget(QLabel("\n\n\n"))

        # Dodawanie widżetów do odpowiednich layoutów
        left_column_layout.addWidget(self.image_label1, alignment=Qt.AlignTop)
        left_column_layout.addLayout(hbox)
        left_column_layout.addLayout(slider_layout)
        left_column_layout.addLayout(color_picker_layout)
        left_column_layout.addLayout(color_picker_layout2)
        left_column_layout.addWidget(button_submit)

        middle_column_layout.addWidget(QLabel("\n\n\n\n\n\n\n\n\n\n"))
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

        # Połączenie zdarzenia generowania obrazu z funkcją
        button_submit.clicked.connect(self.generate_image)

        # defaultowy obraz do wizualizacji
        self.file_path = './dom.jpg'

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

    def choose_color2(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.update_color_preview2(color, self.slider.value())

    def update_color_preview(self, color, alpha):
        rgba_color = QColor(color.red(), color.green(), color.blue(), alpha)
        style_sheet = f"background-color: {rgba_color.name()}"
        self.color_preview_label.setStyleSheet(style_sheet)

    def update_color_preview2(self, color, alpha):
        rgba_color = QColor(color.red(), color.green(), color.blue(), alpha)
        style_sheet = f"background-color: {rgba_color.name()}"
        self.color_preview_label2.setStyleSheet(style_sheet)

    def generate_image(self):
        alpha = self.slider.value() / 100.0
        color = self.color_preview_label.palette().color(QPalette.Background)
        color_array = [color.red(), color.green(), color.blue()]
        color2 = self.color_preview_label2.palette().color(QPalette.Background)
        color_array2 = [color2.red(), color2.green(), color2.blue()]
        print(self.file_path, alpha, color_array, color_array2, self.segment)

        try:
            result_image = main.add_mask(self.file_path, alpha, color_array, color_array2, self.segment)
            # Konwersje
            pil_image = im.fromarray(result_image)
            qimage = ImageQt(pil_image)
            pixmap = QPixmap.fromImage(qimage)
        except Exception as e:
            print("Wystąpił błąd")
            print(traceback.format_exc())

        self.image_label2.setPixmap(pixmap.scaled(512, 512, Qt.KeepAspectRatio))

    def radio_connect(self):
        if self.radio1.isChecked():
            self.segment = 0
        elif self.radio2.isChecked():
            self.segment = 1
        elif self.radio3.isChecked():
            self.segment = 2
        else:
            print('Błąd wyboru radioboxa')

    def save_image(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("png")
        file_dialog.setNameFilter("Obrazy (*.png)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            file_path = selected_files[0]
            print("Zapisano plik:", file_path)

            pixmap = self.image_label2.pixmap()
            pixmap.save(file_path, "PNG")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setStyleSheet("background-color: #343434;")
    window.show()
    sys.exit(app.exec_())
