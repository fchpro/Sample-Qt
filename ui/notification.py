from logger_config import log_args_kwargs as print
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QLabel,
    QPushButton,
    QStyle,
    QStyleOption,
    QVBoxLayout,
    QWidget,
)

from managers.notifications import NotificationType
##from debugger import print, log_error, log_function_call, stop_script, save_current_pil_images

class NotificationBase(QWidget):
    complete = Signal()

    def __init__(self, parent, title, text):
        super().__init__(parent)
        self.setParent(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout()

        title_l = QLabel(title)
        title_l.setObjectName("NotificationTitle")

        text_l = QLabel(text)
        text_l.setObjectName("NotificationText")

        self.layout.addWidget(title_l)
        self.layout.addWidget(text_l)

        self.setLayout(self.layout)

        self.opacity = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity)

        self._animation_in = QPropertyAnimation(self.opacity, b"opacity")
        self._animation_in.setStartValue(0)
        self._animation_in.setEndValue(1)
        self._animation_in.setDuration(500)
        self._animation_in.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._animation_in.finished.connect(self.fade_in_complete)

        self._animation_out = QPropertyAnimation(self.opacity, b"opacity")
        self._animation_out.setStartValue(1)
        self._animation_out.setEndValue(0)
        self._animation_out.setDuration(500)
        self._animation_out.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._animation_out.finished.connect(self.fade_out_complete)

        self.setFixedWidth(300)

    def paintEvent(self, e):
        """We need a custom paint Event to paint the background here."""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    def center_on_parent(self):
        pw, ph = self.parent().rect().width(), self.parent().rect().height()
        self.move(pw / 2, ph / 2)

    def show(self):
        super().show()
        self.raise_()
        self.center_on_parent()
        self.fade_in()

    def fade_in(self):
        self._animation_in.start()

    def fade_in_complete(self):
        self._animation_in.stop()

    def fade_out(self):
        self._animation_in.stop()
        self._animation_out.start()

    def fade_out_complete(self):
        self._animation_out.stop()
        self.hide()
        self.complete.emit()


class NotificationError(NotificationBase):
    def __init__(self, parent, title, text):
        super().__init__(parent, title, text)
        self.setObjectName("NotificationError")

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Add a button to dismiss the error.
        self.close_btn = QPushButton("Dismiss")
        self.close_btn.clicked.connect(self.fade_out)
        self.layout.addWidget(self.close_btn)


class NotificationWarning(NotificationBase):
    def __init__(self, parent, title, text):
        super().__init__(parent, title, text)
        self.setObjectName("NotificationWarning")

    def fade_in_complete(self):
        super().fade_in_complete()
        QTimer.singleShot(200, self.fade_out)


class NotificationInfo(NotificationBase):
    def __init__(self, parent, title, text):
        super().__init__(parent, title, text)
        self.setObjectName("NotificationInfo")

    def fade_in_complete(self):
        super().fade_in_complete()
        QTimer.singleShot(200, self.fade_out)


def get_notification_for_type(ntype):
    lookup = {
        NotificationType.ERROR: NotificationError,
        NotificationType.WARNING: NotificationWarning,
        NotificationType.INFO: NotificationInfo,
    }
    return lookup[ntype]
