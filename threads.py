from logger_config import log_args_kwargs as print
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, QRunnable, Signal
from PySide6.QtWidgets import QMessageBox


threadpool = QThreadPool()


icon_loader_cache = {}


class IconLoaderSignals(QObject):
    finished = Signal(list)


class IconLoader(QRunnable):
    signals = IconLoaderSignals()

    def __init__(self, filenames):
        super().__init__()
        self.filenames = filenames

    def run(self):
        icons = []
        for filename in self.filenames:
            if filename in icon_loader_cache:
                icons.append(icon_loader_cache[filename])
            else:
                icon = QIcon(filename)
                icon_loader_cache[filename] = icon
                icons.append(icon)
        self.signals.finished.emit(icons)
