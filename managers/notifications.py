from logger_config import log_args_kwargs as print
from PySide6.QtCore import QObject, Signal, QTimer, QAbstractListModel, Qt
from enum import Enum
from collections import namedtuple

class NotificationType(Enum):
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'

notification = namedtuple('notification', 'ntype title text')



class NotificationManager(QAbstractListModel):
    """This manager holds a simple queue so notifications don't override
    previous notifications. It implements a QAbstractListModel api so it
    can be used to drive list views directly.
    """

    notify = Signal(notification)

    def __init__(self):
        super().__init__()
        # When notified, items are moved from the queue to the history.
        self._history = []
        self._queue = []
        self.is_locked = False

        # We use a timer to clear out the queue.
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.send_notification)
        self.timer.start()

    def error(self, title, text):
        print("FA5xW", title, text)
        self.add_notification(NotificationType.ERROR, title, text)

    def warning(self, title, text):
        self.add_notification(NotificationType.WARNING, title, text)

    def info(self, title, text):
        self.add_notification(NotificationType.INFO, title, text)

    def add_notification(self, ntype, title, text):
        n = notification(ntype, title, text)
        self._queue.append(n)
        self.send_notification()

    def send_notification(self):
        if self.is_locked:
            return
        if not self._queue:
            return
        self.lock()
        n = self._queue.pop(0)
        self.layoutAboutToBeChanged.emit()
        self._history.insert(0, n) # Add into the visible queue.
        self.layoutChanged.emit()
        self.notify.emit(n)

    def lock(self):
        self.is_locked = True

    def unlock(self):
        self.is_locked = False
        self.send_notification()

    # QAbstractListModel API.
    def data(self, index, role):
        # self._history[idx] returns the noficiation object, meaning we can show icons etc. depending on type.
        # alternatively we could create a custom delegate to draw whatever we want.
        if role == Qt.ItemDataRole.DisplayRole:
            idx = index.row()
            notification = self._history[idx]
            return f"{notification.title}: {notification.text}"
        if role == Qt.ItemDataRole.DecorationRole:
            idx = index.row()
            notification = self._history[idx]

    def colCount(self, index):
        return 1

    def rowCount(self, index):
        return len(self._history)

    def clear(self):
        self.layoutAboutToBeChanged.emit()
        self._history.clear()
        self.layoutChanged.emit()


notification_manager = NotificationManager()

