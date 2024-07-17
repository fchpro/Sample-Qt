from logger_config import log_args_kwargs as print
import os
import random
import string
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QGuiApplication

import os
import random
import string
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QFont, QFontDatabase, QGuiApplication, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QShortcut, QKeySequence


def is_valid_file(file_path: str) -> bool:
    """Check if the given file_path is a valid existing file."""
    return os.path.isfile(file_path)


def return_error_code_txt_file():
    if is_valid_file("error_codes.txt"):
        return "error_codes.txt"
    elif is_valid_file("dist/error_codes.txt"):
        return "dist/error_codes.txt"


class ErrorCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.codes_file = "error_codes.txt"
        self.existing_codes = self.load_existing_codes()
        self.setWindowTitle("Error Coder")
        self.initUI()
        self.existing_codes = self.load_existing_codes()

    def initUI(self):
        # Load and set custom font
        font_id = QFontDatabase.addApplicationFont("OpenSans.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 32)

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f"background-color: #{'7AA2E3'};")
        self.layout = QVBoxLayout()

        # Padding around the layout
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.display_label = QLabel("No code generated yet", self)
        self.display_label.setFont(font)
        self.display_label.setStyleSheet("color: #FFFFFF;")
        self.display_label.setAlignment(Qt.AlignCenter)

        self.generate_btn = QPushButton("Generate Error Code", self)
        self.generate_btn.setFont(font)
        self.generate_btn.setStyleSheet(
            f"background-color: #{'6AD4DD'}; color: #FFFFFF;")
        self.generate_btn.clicked.connect(self.generate_code)

        self.code_count_label = QLabel(
            f"Codes generated: {len(self.existing_codes)}", self)
        self.code_count_label.setFont(font)
        self.code_count_label.setStyleSheet("color: #FFFFFF;")
        self.code_count_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.display_label)
        self.layout.addWidget(self.generate_btn)
        self.layout.addWidget(self.code_count_label)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Adjust window size
        self.setFixedSize(600, 400)

    def initUI(self):
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.display_label = QLabel("No code generated yet", self)

        self.generate_btn = QPushButton("Generate Error Code", self)
        self.generate_btn.setStyleSheet("QPushButton { border-radius: 12px; }")
        self.generate_btn.clicked.connect(lambda: self.generate_code(False))
        generate_btn_shortcut = QShortcut(
            QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_S), self)
        generate_btn_shortcut.activated.connect(
            lambda: self.generate_code(False))

        self.generate_print_btn = QPushButton("Generate Print Statement", self)
        self.generate_print_btn.setStyleSheet(
            "QPushButton { border-radius: 12px; }")
        self.generate_print_btn.clicked.connect(
            lambda: self.generate_code(True))
        generate_print_btn_shortcut = QShortcut(
            QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_D), self)
        generate_print_btn_shortcut.activated.connect(
            lambda: self.generate_code(True))

        self.layout.addWidget(self.display_label)
        self.layout.addWidget(self.generate_btn)
        self.layout.addWidget(self.generate_print_btn)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def load_existing_codes(self):
        if os.path.exists(self.codes_file):
            with open(self.codes_file, "r") as file:
                return set(line.strip() for line in file)
        return set()

    def save_code(self, code):
        with open(self.codes_file, "a") as file:
            file.write(f'"{code}",\n')

    def generate_code(self):
        unique_code = False
        while not unique_code:
            code = ''.join(random.choices(
                string.ascii_letters + string.digits, k=5))
            if code not in self.existing_codes:
                unique_code = True
                self.existing_codes.add(code)
                self.save_code(code)
                formatted_code = f'"{code}",'
                self.display_label.setText(formatted_code)
                QGuiApplication.clipboard().setText(formatted_code)
                self.code_count_label.setText(
                    f"Codes generated: {len(self.existing_codes)}")

    def generate_code(self, print_statement):
        unique_code = False
        while not unique_code:
            code = ''.join(random.choices(
                string.ascii_letters + string.digits, k=5))
            if code not in self.existing_codes:
                unique_code = True
                self.existing_codes.add(code)
                self.save_code(code)
                if print_statement:
                    formatted_code = f'print("{code}", )'
                    self.display_label.setText(formatted_code)
                    QGuiApplication.clipboard().setText(formatted_code)
                else:
                    formatted_code = f'"{code}",'
                    self.display_label.setText(formatted_code)
                    QGuiApplication.clipboard().setText(formatted_code)


if __name__ == "__main__":
    app = QApplication([])
    window = ErrorCodeGenerator()
    window.show()
    app.exec()
