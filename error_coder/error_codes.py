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

from PySide6.QtCore import QTimer
import threading
import keyboard
import queue

style_sheet = """
QMainWindow {
    background-color: #222831;
    padding: 20px; /* Add padding around the whole app */
}

QTextEdit, QPushButton {
    background-color: #393E46;
    color: #EEEEEE;
    font-size: 32px;
    border-radius: 10px; /* Round corners for buttons and text edits */
    padding: 10px; /* Add padding inside text edits and buttons for better text alignment */
}
QLabel {
    color: #EEEEEE; 
    font-size: 32px;
}
QPushButton {
    border: none; /* Remove border from buttons */
}

QPushButton:hover {
    background-color: #00ADB5;
    color: #EEEEEE;
}
"""

def is_valid_file(file_path: str) -> bool:
    """Check if the given file_path is a valid existing file."""
    return os.path.isfile(file_path)

def return_error_code_txt_file():
    dist_path = "C:\work\projects\Magnets\error_coder\error_codes.txt"
    if is_valid_file(dist_path):
        print("Vf6c7", dist_path)
        return dist_path
    elif is_valid_file("error_coder\\error_codes.txt"):
        print("YJsjm", "error_codes.txt")
        return "error_codes.txt"

class ErrorCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.codes_file = return_error_code_txt_file()
        self.existing_codes = self.load_existing_codes()
        self.setWindowTitle("Error Coder")
        self.initUI()
        self.existing_codes = self.load_existing_codes()
        self.action_queue = queue.Queue()
        self.initGlobalShortcutsListener()
        self.initTimer()

    def initGlobalShortcutsListener(self):
        def listenForGlobalShortcuts():
            keyboard.add_hotkey(
                'alt+shift+z', lambda: self.action_queue.put(lambda: self.generate_code(False)))
            keyboard.add_hotkey(
                'alt+shift+d', lambda: self.action_queue.put(lambda: self.generate_code(True)))
            keyboard.wait()

        threading.Thread(target=listenForGlobalShortcuts, daemon=True).start()

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkActionQueue)
        self.timer.start(100)  # Check every 100 milliseconds

    def checkActionQueue(self):
        while not self.action_queue.empty():
            action = self.action_queue.get()
            action()  # Execute the action
    
    def initUI(self):
        font_id = QFontDatabase.addApplicationFont("OpenSans.ttf")
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]
        else:
            font_family = self.font().family()  # Fallback to the default application font family
        font = QFont(font_family, 32)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(20, 20, 20, 20)

        self.display_label = QLabel("No code generated yet", self)
        self.display_label.setFont(font)
        self.display_label.setAlignment(Qt.AlignCenter)

        self.generate_btn = QPushButton("Generate Error Code", self)
        self.generate_btn.setFont(font)
        self.generate_btn.clicked.connect(lambda: self.generate_code(False))
        generate_btn_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_Z), self)
        generate_btn_shortcut.activated.connect(lambda: self.generate_code(False))

        self.generate_print_btn = QPushButton("Generate Print Statement", self)
        self.generate_print_btn.setFont(font)
        self.generate_print_btn.clicked.connect(lambda: self.generate_code(True))
        generate_print_btn_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_D), self)
        generate_print_btn_shortcut.activated.connect(lambda: self.generate_code(True))

        self.code_count_label = QLabel(f"Codes generated: {len(self.existing_codes)}", self)
        self.code_count_label.setFont(font)
        self.code_count_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.display_label)
        self.layout.addWidget(self.generate_btn)
        self.layout.addWidget(self.generate_print_btn)
        self.layout.addWidget(self.code_count_label)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.setFixedSize(600, 400)


    def load_existing_codes(self):

        if os.path.exists(self.codes_file):
            with open(self.codes_file, "r") as file:
                return set(line.strip() for line in file)
        return set()

    def save_code(self, code):
        with open(self.codes_file, "a") as file:
            file.write(f'"{code}",\n')

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
                self.code_count_label.setText(
                    f"Codes generated: {len(self.existing_codes)}")


if __name__ == "__main__":
    font_path = "C:\work\projects\TSHIRTER\SIDE_APP\local\error_coder\OpenSans.ttf"
    app = QApplication([])
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:  # Ensure the font was added successfully
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        app.setFont(QFont(font_family))
    app.setStyleSheet(style_sheet)
    window = ErrorCodeGenerator()
    window.show()
    app.exec()
