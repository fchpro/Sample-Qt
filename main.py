print("launched ...")
from settings import settings
from logger_config import log_args_kwargs as print
from logger_config import clear_log_txt_file , debug_mode

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLabel
)

from global_signals import global_signals
from models.data_model import model
from paths import Paths
from utils.os_funcs import clear_temp_folder
from managers.notifications import notification_manager, NotificationType
from PySide6.QtCore import Qt, QTimer
from ui.notification import get_notification_for_type
import logging
import os
import sys

logging.getLogger('PIL').setLevel(logging.WARNING)

def load_style_qss():
    """load the qss file"""
    with open(Paths.style("style.qss")) as f:
        return f.read()


class MyMainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        clear_temp_folder()
        clear_log_txt_file()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Magnets Cutter")
        self.setGeometry(100, 100, 1000, 600)
        self.app_framework_qwidget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.app_framework_qwidget.setLayout(self.main_layout)
        self.sections_layout = QHBoxLayout()
        self.sections_layout.setSpacing(5)
        self.sections_layout.setContentsMargins(0, 0, 0, 0)
        notification_manager.notify.connect(self.handle_notification)
        global_signals.notify.connect(self.show_notification)
        self.setCentralWidget(self.app_framework_qwidget)
        model.reset()
        self.status = self.statusBar()


    def show_notification(self, noti_dict):
        print("C7wG8", noti_dict)
        noti_type = noti_dict.get("type",None)
        title = noti_dict.get("title",None)
        text = noti_dict.get("text",None)

        if not noti_type or noti_type not in ["error", "warning", "info"]:
            print("O6CUA", "noti_type not valid", noti_type)
            return
        
        if not title or not text:
            print("1q5dj", "title or text not valid", title, text)
            return

        print("DE9sQ", type , title , text)
        if noti_type == "error":
            notification_manager.error(title, text)
        elif noti_type == "warning":
            notification_manager.warning(title, text)
        elif noti_type == "info":
            notification_manager.info(title, text)

    def handle_notification(self, notification):
        cls = get_notification_for_type(notification.ntype)
        self._notification_widget = cls(self, notification.title, notification.text)
        self._notification_widget.complete.connect(notification_manager.unlock)
        self._notification_widget.show()
        
    def show_some_notification_messages(self):
        notification_manager.error("Test error", "Test error message")
        notification_manager.warning("Test warning", "Test warning message")
        notification_manager.info("Test info", "Test info message")

    def start_processing_things(self):
        self.threadpool.start(self.process_things)

    def update_progress(self, v):
        pass

    def process_things(self):
        my_tasks = self.list_of_things_to_process.pop()

        for thing in self.list_of_things_to_process:
            # do something
            self.progress.emit(0.5)

        self.list_of_things_to_process = []

    def update_completed_images(self):
        self.completed_images += 1

        progress = self.completed_images / self.total_images
        self.progress.setValue(progress)

def load_fonts():
    fontfiles = os.listdir(Paths.ui_fonts)
    for f in fontfiles:
        print("Loading font", f)
        path = Paths.font(f)
        QFontDatabase.addApplicationFont(path)

def load_stylesheet(app):
    styles = load_style_qss()
    app.setStyleSheet(styles)


def main():
    app = QApplication(sys.argv)
    load_fonts()
    load_stylesheet(app)
    window = MyMainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
